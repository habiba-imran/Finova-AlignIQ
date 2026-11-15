"""Reusable source-driven review policies, independent of any example identifier.

These policies select engineering review topics and optional fictional categories.
They never execute or authorize any predicate in the clinical registry.
"""
from collections import Counter, defaultdict
from decimal import Decimal, localcontext

from app.functional.engine import Engine, CONCEPT_LABELS
from app.functional.models import AttachmentOption, Candidate, FunctionalContext, MovementTarget, ReviewOutline
from app.interactive.analysis import ANGULAR, TRANSLATION, VERTICAL


def make_context(parsed, submission):
    options = submission.planning_options
    details = submission.review_details
    bound = bool(options.targets or options.attachment_options or options.phases or options.support_constraints
        or options.illustration != 'NONE' or any(details.model_dump().values()))
    if options.source_sha256 is not None and options.source_sha256 != parsed.raw_sha256 or bound and options.source_sha256 != parsed.raw_sha256:
        raise ValueError('FUNCTIONAL_CONTEXT_SOURCE_MISMATCH')
    if (submission.module != 'macro' and (options.targets or options.illustration != 'NONE')
        or submission.module != 'micro' and options.attachment_options
        or submission.module != 'nano' and (options.phases or options.support_constraints)):
        raise ValueError('FUNCTIONAL_CONTEXT_MODULE_MISMATCH')
    supplied = {o.concept:o for o in options.attachment_options}
    if len(supplied) != len(options.attachment_options):
        raise ValueError('FUNCTIONAL_CONTEXT_INVALID')
    movements={m.id:m for m in parsed.measurements}
    for target in options.targets:
        if target.measurement_ref not in movements or movements[target.measurement_ref].recognized_label not in (*ANGULAR,*TRANSLATION,*VERTICAL):
            raise ValueError('FUNCTIONAL_CONTEXT_INVALID')
    catalog = ({c:AttachmentOption(concept=c) for c in CONCEPT_LABELS} if options.catalog_policy == 'CONCEPTS_WITH_SUPPLIED_SPECS' else {})
    catalog.update(supplied)
    return FunctionalContext(origin='INPUT_DRIVEN_POLICY_REVIEW',module=submission.module,
        source_sha256=parsed.raw_sha256,notation='FDI' if parsed.source.context.notation in {'UNKNOWN','FDI'} else 'UNVERIFIED',
        objectives=options.objectives,targets=options.targets,
        attachment_options=list(catalog.values()) if submission.module == 'micro' else [],
        phases=options.phases,stage_value_basis=options.stage_value_basis,support_constraints=options.support_constraints)


class GeneralizedEngine(Engine):
    comparison_review_only = True

    def __init__(self, parsed, submission, context):
        self.options = submission.planning_options
        super().__init__(parsed,submission.model_copy(update={'planning_context':context}))

    def usable(self,m):
        return m.recognized_label in (*ANGULAR,*TRANSLATION,*VERTICAL) and super().usable(m)

    def run(self):
        sections,findings,plan=super().run()
        titles={}
        if self.submission.module=='macro':
            titles={'SAGITTAL':'Sagittal review','TRANSVERSE':'Transverse review','VERTICAL':'Vertical review'}
        elif self.submission.module=='nano':
            supplied=bool(self.submission.review_details.stages or self.submission.review_details.allocations)
            titles={'PHASES':'Ordered phases and movements' if plan.stages else 'Supplied stage review' if supplied else 'Movement patterns and review outline'}
        return [s.model_copy(update={'title':titles.get(s.section_id,s.title)}) for s in sections],findings,plan

    def ranked(self, family):
        cells = self.analysis.numeric(family)
        positive = [m for m in cells if m.magnitude_decimal > 0]
        if not positive:
            return cells,[],None
        ordered = sorted((m.magnitude_decimal for m in positive),reverse=True)
        boundary = ordered[(len(ordered)-1)//2]
        return cells,[m for m in positive if m.magnitude_decimal >= boundary],boundary

    def ranked_review(self, section, family):
        cells, selected, boundary = self.ranked(family)
        policy = f'DEMO-PLAN-INPUT-{section}-v1'
        label = family.replace('_',' ')
        unknown = [m for m in self.parsed.measurements if m.recognized_label == family and m not in cells]
        if not cells:
            self.add(section,policy,'INSUFFICIENT_INFORMATION',unknown,
                f'{label.capitalize()} has no comparable recorded values.',
                f'Request the missing {label} values and units before assessing this movement pattern.')
            return
        if not selected:
            self.add(section,policy,'NOT_APPLICABLE',cells,
                f'All {len(cells)} comparable {label} entries are explicitly zero.',
                'No nonzero pattern triggers this review policy. Unknown fields remain separate.')
            return
        maximum = max(m.magnitude_decimal for m in selected)
        winners = [m for m in selected if m.magnitude_decimal == maximum]
        companion_families = VERTICAL if family in VERTICAL else ANGULAR if family not in ANGULAR else (*TRANSLATION,*VERTICAL)
        companions = [m for m in self.parsed.measurements if m.tooth_ref in {s.tooth_ref for s in selected}
            and m.recognized_label in companion_families and m.recognized_label != family and self.usable(m) and m.magnitude_decimal > 0]
        labels = Counter(m.raw_direction or 'unlabelled' for m in selected)
        evidence = list({m.id:m for m in [*cells,*unknown,*companions]}.values())
        unit = 'deg' if family in ANGULAR else 'mm'
        rationale = (f'{self.analysis.tokens(selected)} are in the upper half of nonzero {label} magnitudes '
            f'(boundary {boundary} {unit}; ties retained). Largest recorded: {self.observation(winners)}. '
            'Selected source labels: '+', '.join(f'{k}: {v}' for k,v in sorted(labels.items()))+'.')
        if companions:
            rationale += f' Coupled nonzero components occur at {self.analysis.tokens(companions).lower()}.'
        d = self.add(section,policy,'REVIEW_REQUEST',evidence,rationale,
            f'Technician review: confirm the intended {label} distribution for these teeth'+
            (' alongside the coupled components' if companions else '')+' before changing programmed values.',
            alternative='Retain the recorded values, or '+('review the coupled components separately' if companions else f'check the {label} source conventions')+' against an explicit planning objective.',
            missing=[f'{len(unknown)} unavailable {label} position(s)'] if unknown else [])
        self.findings[-1].selected_refs = list(dict.fromkeys(m.id for m in selected))
        return d

    def macro(self):
        for section,families in [('SAGITTAL',TRANSLATION[:1]),('TRANSVERSE',TRANSLATION[1:]),('VERTICAL',VERTICAL),('ADDITIONAL',ANGULAR)]:
            present = [f for f in families if any(m.recognized_label == f for m in self.parsed.measurements)]
            for family in present or families[:1]:
                self.ranked_review(section,family)
        targets = list(self.context.targets)
        if self.options.illustration == 'HALF_MAGNITUDE':
            m = self.movements.get(self.options.illustration_measurement_ref)
            if self.options.illustration_measurement_ref is not None and not m:
                raise ValueError('FUNCTIONAL_CONTEXT_INVALID')
            if not m or not self.usable(m):
                self.add('ADDITIONAL','DEMO-PLAN-INPUT-TARGET-v1','INSUFFICIENT_INFORMATION',[m] if m else [],
                    'No comparable source field is selected for the fictional calculation.',
                    'No replacement example is generated.',missing=['An unambiguous source measurement with a unit'])
            elif self.options.policy_mode == 'SYNTHETIC_REVIEW':
                with localcontext() as ctx:
                    ctx.prec = max(28,len(m.signed_decimal.as_tuple().digits)+4)
                    amount = format(m.signed_decimal / Decimal(2),'f')
                if len(amount)<=24:
                    targets.append(MovementTarget(measurement_ref=m.id,amount=amount,unit=m.unit,source_direction=m.raw_direction))
                else:
                    self.add('ADDITIONAL','DEMO-PLAN-INPUT-TARGET-v1','INSUFFICIENT_INFORMATION',[m],
                        'The exact fictional calculation exceeds the supported replacement-value length.',
                        'No value is rounded or substituted; the original source remains unchanged.')
        if len({t.measurement_ref for t in targets}) != len(targets):
            raise ValueError('FUNCTIONAL_CONTEXT_INVALID')
        if targets:
            for target in targets:
                m = self.movements[target.measurement_ref]
                section = 'SAGITTAL' if m.recognized_label == 'mesiodistal' else 'TRANSVERSE' if m.recognized_label == 'buccolingual' else 'VERTICAL' if m.recognized_label in VERTICAL else 'ADDITIONAL'
                goal = 'REDISTRIBUTE_TRANSLATIONS' if m.recognized_label in TRANSLATION else 'VERTICAL_REVIEW' if m.recognized_label in VERTICAL else 'ANGULAR_CONTROL'
                missing=[]
                if goal not in self.options.objectives: missing.append('A matching explicit planning objective')
                if self.options.source_convention != 'SOURCE_LABELS_AS_RECORDED': missing.append('The source-label convention for this example')
                if self.parsed.source.context.plan_mode == 'COMPARISON': missing.append('A compatible total-movement source, rather than comparison values')
                if not self.usable(m): missing.append('An unambiguous comparable source value and unit')
                if self.options.policy_mode != 'SYNTHETIC_REVIEW': missing.append('Synthetic illustration mode')
                if self.usable(m) and Decimal(target.amount)==m.signed_decimal: missing.append('A distinct replacement value; the supplied value is unchanged')
                eligible=not missing
                method = 'Transparent fictional example: divide this source scalar by 2; preserve its source label.' if self.options.illustration == 'HALF_MAGNITUDE' and target not in self.context.targets else 'The replacement value is explicitly supplied by the user.'
                self.add(section,'DEMO-PLAN-INPUT-TARGET-v1','ILLUSTRATIVE_PROPOSAL' if eligible else 'INSUFFICIENT_INFORMATION',[m],
                    (self.observation([m])+'.' if self.usable(m) else 'The selected source value is unavailable or not comparable for this policy.')+' '+method,
                    f'Illustrative modification example: replace {self.analysis.value(m)} with {target.amount} {target.unit}'+(f' ({target.source_direction}-labelled).' if target.source_direction else '.') if eligible else 'No replacement is proposed with the current context.',
                    alternative='Retain the source value pending independent review.',
                    missing=missing,
                    context_refs=['planning_context/targets','planning_options'],changes=[target] if eligible else [])
                if eligible and target not in self.context.targets:
                    self.context.targets.append(target)
        self.add('ADDITIONAL','DEMO-PLAN-INPUT-SCOPE-v1','INSUFFICIENT_INFORMATION',[],
            'Relative ranks identify review topics, not clinical severity or safe movement limits.',
            'Numerical replacements require explicit objectives and source conventions. Clinical IPR, extraction, surgery, auxiliaries and anchorage prescriptions remain unevaluated.')

    def micro(self):
        catalog = {o.concept:o for o in self.context.attachment_options}
        for tooth in self.parsed.teeth:
            angular = self.own(tooth.id,ANGULAR)
            known = {m.recognized_label:m for m in angular if self.usable(m)}
            own = [m for m in self.parsed.measurements if m.tooth_ref == tooth.id]
            primary = alternative = None
            missing = []
            outcome = 'INSUFFICIENT_INFORMATION'
            rule = 'INCOMPLETE'
            profile = 'Incomplete angular profile'
            evidence = angular
            if len(angular) != 3 or len(known) != 3:
                missing = ['Complete unambiguous rotation, angulation and inclination values in degrees']
            else:
                nonzero = [f for f in ANGULAR if known[f].magnitude_decimal > 0]
                if nonzero:
                    maximum = max(known[f].magnitude_decimal for f in nonzero)
                    dominant = [f for f in nonzero if known[f].magnitude_decimal == maximum]
                    profile = ('Combined angular profile; ' if len(nonzero)>1 else 'Single angular component; ')+(', '.join(dominant)+' has the largest absolute angular magnitude within this tooth' if len(dominant)==1 else 'equal largest angular magnitudes at '+', '.join(dominant))
                    if len(dominant)>1:
                        primary,alternative,rule = 'VERTICAL_RECTANGULAR','RECTANGULAR','TIED-ANGULAR'
                    else:
                        primary,alternative,rule = {'rotation':('OVAL','VERTICAL_RECTANGULAR','ROTATION'),
                            'angulation':('HORIZONTAL_RECTANGULAR','VERTICAL_RECTANGULAR','ANGULATION'),
                            'inclination':('OPTIMIZED_STYLE','RECTANGULAR','INCLINATION')}[dominant[0]]
                elif (len(own)==7 and {m.recognized_label for m in own} == {*ANGULAR,*TRANSLATION,'vertical','relative_vertical'} and all(self.usable(m) for m in own)):
                    evidence = own
                    if all(m.magnitude_decimal==0 for m in own):
                        primary,rule,profile='NO_ATTACHMENT','ZERO','Complete seven-field explicit-zero profile'
                    elif any(m.magnitude_decimal>0 for m in own if m.recognized_label in VERTICAL):
                        primary,alternative,rule,profile='RECTANGULAR','OVAL','VERTICAL','Zero-angular/nonzero-vertical profile'
                    else:
                        outcome,rule,profile='NO_CANDIDATE','TRANSLATION-ONLY','Complete translation-only profile; no applicable shape policy'
                else:
                    profile='Explicit-zero angular profile; other required movement fields are incomplete'
                    required={*ANGULAR,*TRANSLATION,'vertical','relative_vertical'}
                    available={m.recognized_label for m in own if self.usable(m)}
                    missing=['Unavailable fields: '+', '.join(sorted(required-available))]
            if self.options.policy_mode == 'EVIDENCE_REVIEW' and primary:
                primary=alternative=None
                missing=['Synthetic illustration mode or an independently validated clinical selection policy']
            if self.parsed.source.context.plan_mode == 'COMPARISON' and primary:
                primary=alternative=None
                missing=['Compatible total-movement source; comparison zeros do not establish zero programmed movement']
            if primary and primary not in catalog:
                missing.append('Supplied catalog concept: '+primary); primary=None
            if alternative not in catalog:
                alternative=None
            positive = [m for m in evidence if self.usable(m) and m.magnitude_decimal>0]
            rationale = f'Tooth {tooth.token}: {profile}. '+(self.observation(positive)+'.' if positive else '')
            proposal = 'Illustrative catalog category: '+CONCEPT_LABELS[primary]+'.' if primary else 'No supported category is selected.'
            if primary:
                option=catalog[primary]
                if option.geometry:
                    g=option.geometry; proposal+=f' Supplied dimensions: {g.width_mm} × {g.height_mm} × {g.depth_mm} mm.'
                if option.orientation: proposal+=f' Supplied orientation: {option.orientation.lower()}.'
                if option.surface: proposal+=f' Supplied surface: {option.surface.lower()}.'
                if option.placement:
                    p=option.placement; proposal+=f' Supplied local position: ({p.x_mm}, {p.y_mm}, {p.z_mm}) mm; frame {p.frame}.'
                outcome='NO_ATTACHMENT' if primary=='NO_ATTACHMENT' else 'CANDIDATE'
            d=self.add('ATTACHMENT_OPTIONS',f'DEMO-ATT-INPUT-{rule}-v1',
                'ILLUSTRATIVE_PROPOSAL' if primary else 'NOT_APPLICABLE' if outcome=='NO_CANDIDATE' else 'INSUFFICIENT_INFORMATION',
                evidence,rationale,proposal,alternative=CONCEPT_LABELS.get(alternative),missing=missing,
                context_refs=['planning_context/attachment_options','planning_options'],attachment_primary=primary,attachment_alternative=alternative)
            self.plan.attachment_rows.append(Candidate(tooth_ref=tooth.id,decision_id=d.decision_id,
                movement_refs=[m.id for m in positive] or [m.id for m in evidence],primary=primary,alternative=alternative,outcome=outcome,missing_fields=missing))
        self.add('ATTACHMENT_SCOPE','DEMO-ATT-INPUT-SCOPE-v1','INSUFFICIENT_INFORMATION',[],
            'Catalog categories follow documented component-presence and within-tooth angular-dominance toy policies, independent of dataset rank.',
            'Dimensions and placement remain unspecified unless supplied. Optimized-style is a category only; clinical suitability and actual attachment need are not established.')

    def nano(self):
        if self.submission.review_details.stages or self.submission.review_details.allocations:
            if self.parsed.source.context.plan_mode == 'COMPARISON':
                self.check('COMPARISON_NOT_STAGE_TOTAL','CONFLICT','A comparison table cannot supply the total-movement basis for stage calculations or support strategies.')
                self.add('PHASES','DEMO-STAGE-DATA-v1','CONFLICT',[],
                    'The source declares comparison values rather than compatible movement totals.',
                    'Stage calculations are withheld; supply a compatible total table and stage records.')
                self.finish_nano()
                return
            return super().nano()
        self.analysis.distribution('PHASES')
        for f in self.analysis.findings:
            if f.kind=='TOKEN_GROUP':
                self.add('PHASES','DEMO-STAGE-INPUT-GROUPS-v1','REVIEW_REQUEST',
                    [self.movements[r] for r in f.source_refs],f.text,'Review movement combinations within this token group.')
        coupled=defaultdict(list)
        for tooth in self.parsed.teeth:
            values=[m for m in self.parsed.measurements if m.tooth_ref==tooth.id and self.usable(m) and m.magnitude_decimal>0]
            if len(values)>1:
                coupled[self.analysis.token_group(tooth),tuple(sorted(m.recognized_label for m in values))].extend(values)
        for (group,components),values in sorted(coupled.items()):
            self.add('PHASES','DEMO-STAGE-INPUT-COUPLING-v1','REVIEW_REQUEST',values,
                f'{group}: {self.analysis.tokens(values)} combine '+', '.join(f.replace('_',' ') for f in components)+'.',
                'Sequencing review priority: check coordination of these components before assigning stage amounts; totals do not establish simultaneous delivery.')
        for families,title in [(TRANSLATION,'Translation coupling review'),(ANGULAR,'Angular component review'),(VERTICAL,'Vertical relationship review')]:
            evidence=[]; selected_evidence=[]; parts=[]
            if families != ANGULAR:
                start=len(self.analysis.findings)
                self.analysis.concentration('PHASES',families)
                for f in self.analysis.findings[start:]:
                    if f.kind!='CONCENTRATION': continue
                    evidence.extend(self.movements[ref] for ref in f.source_refs)
                    selected_evidence.extend(self.movements[ref] for ref in f.selected_refs)
                    parts.append(f.text)
            for family in families:
                if families != ANGULAR: continue
                cells,selected,boundary=self.ranked(family)
                if selected:
                    evidence.extend(cells)
                    selected_evidence.extend(selected)
                    labels=Counter(m.raw_direction or 'unlabelled' for m in selected)
                    parts.append(f'{family.replace("_"," ")}: {self.analysis.tokens(selected)}; upper-half boundary {boundary} deg (ties retained); source labels '+', '.join(f'{k}: {v}' for k,v in sorted(labels.items())))
            if not evidence: continue
            evidence=list({m.id:m for m in evidence}.values())
            selected_evidence=list({m.id:m for m in selected_evidence}.values())
            d=self.add('PHASES','DEMO-STAGE-INPUT-OUTLINE-v1','REVIEW_REQUEST',evidence,
                title+' — '+' '.join(part if part.endswith('.') else part+'.' for part in parts),
                'Review the recorded components and confirm coordination where they overlap before assigning any actual stages.',
                alternative='Inspect these movement families separately; use explicit stage records for allocation checks.')
            self.findings[-1].selected_refs=[m.id for m in selected_evidence]
            self.plan.review_outline.append(ReviewOutline(outline_id=f'R{len(self.plan.review_outline)+1}',title=title,
                purpose='Inspection topic only; no treatment stage, count, duration or allocation is generated.',
                tooth_refs=list(dict.fromkeys(m.tooth_ref for m in selected_evidence)),measurement_refs=[m.id for m in selected_evidence],decision_id=d.decision_id))
        if not any(d.dimension=='PHASES' for d in self.plan.decisions):
            self.add('PHASES','DEMO-STAGE-INPUT-EMPTY-v1','INSUFFICIENT_INFORMATION',[],
                'No comparable movement combination is available.','Request the missing values and units before a sequencing review.')
        self.check('STAGE_DATA_NOT_SUPPLIED','UNAVAILABLE','Review outline only. Supply stage-bound amounts and compatible conventions for allocation checks.')
        self.finish_nano()

    def support(self,phase_map):
        if self.options.policy_mode == 'EVIDENCE_REVIEW':
            self.check('SUPPORT_ILLUSTRATION_DISABLED','UNAVAILABLE','Evidence-only mode retains allocation checks and withholds fictional support strategies.')
            return
        super().support(phase_map)


def generalized_review(parsed,submission):
    context=make_context(parsed,submission)
    engine=GeneralizedEngine(parsed,submission,context)
    sections,findings,plan=engine.run()
    return sections,findings,plan,context
