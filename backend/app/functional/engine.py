"""Source-bound fictional decisions. Never feeds the clinical/semantic registry."""
from collections import defaultdict
from decimal import Decimal, localcontext

from app.functional.models import Decision, Candidate, FunctionalPlan, PlanCheck, AllocationCheck, StageRow, StageMovement
from app.interactive.analysis import Analysis, ANGULAR, VERTICAL, TRANSLATION
from app.interactive.models import AnalyticalFinding, ModuleSection
from app.interactive.module_reports import validate_details

TITLES = {
    'macro': {'SAGITTAL': 'Sagittal proposals', 'TRANSVERSE': 'Transverse proposals', 'VERTICAL': 'Vertical proposals', 'ADDITIONAL': 'Additional considerations'},
    'micro': {'ATTACHMENT_OPTIONS': 'Tooth-wise attachment options', 'ATTACHMENT_SCOPE': 'Attachment assumptions and limits'},
    'nano': {'PHASES': 'Ordered phases and movements', 'STAGE_CHECKS': 'Stage consistency checks', 'ANCHORAGE': 'Illustrative anchorage review', 'SEQUENCE_SCOPE': 'Sequencing assumptions and limits'},
}
CONCEPT_LABELS = {'RECTANGULAR': 'Rectangular', 'VERTICAL_RECTANGULAR': 'Vertical rectangular',
    'HORIZONTAL_RECTANGULAR': 'Horizontal rectangular', 'OVAL': 'Ellipsoid / oval',
    'OPTIMIZED_STYLE': 'Optimized-style category (geometry unspecified)', 'NO_ATTACHMENT': 'No attachment in this fictional scenario'}


def exact_sum(values):
    numbers = [Decimal(v) for v in values]
    with localcontext() as ctx:
        ctx.prec = max(28, sum(len(v.as_tuple().digits) + abs(v.as_tuple().exponent) for v in numbers) + 4)
        return str(sum(numbers, Decimal(0)))


class Engine:
    def __init__(self, parsed, submission):
        self.parsed, self.submission, self.context = parsed, submission, submission.planning_context
        self.analysis = Analysis(parsed)
        self.teeth = {t.id: t for t in parsed.teeth}
        self.movements = {m.id: m for m in parsed.measurements}
        self.plan = FunctionalPlan(source_sha256=parsed.raw_sha256)
        self.findings = []
        c = self.context
        if c.source_sha256 != parsed.raw_sha256:
            raise ValueError('FUNCTIONAL_CONTEXT_SOURCE_MISMATCH')
        if c.module != submission.module:
            raise ValueError('FUNCTIONAL_CONTEXT_MODULE_MISMATCH')
        if (parsed.source.context.plan_mode == 'COMPARISON' and not getattr(self,'comparison_review_only',False) or
            c.notation == 'FDI' and parsed.source.context.notation not in {'UNKNOWN','FDI'}):
            raise ValueError('FUNCTIONAL_CONTEXT_INVALID')
        if len(set(c.objectives)) != len(c.objectives) or len({o.concept for o in c.attachment_options}) != len(c.attachment_options):
            raise ValueError('FUNCTIONAL_CONTEXT_INVALID')
        if (submission.module != 'macro' and c.targets or submission.module != 'micro' and c.attachment_options
            or submission.module != 'nano' and (c.phases or c.support_constraints)):
            raise ValueError('FUNCTIONAL_CONTEXT_INVALID')
        if len({t.measurement_ref for t in c.targets}) != len(c.targets):
            raise ValueError('FUNCTIONAL_CONTEXT_INVALID')
        for target in c.targets:
            m = self.movements.get(target.measurement_ref)
            if not m or m.unit != target.unit or m.raw_direction != target.source_direction:
                raise ValueError('FUNCTIONAL_CONTEXT_INVALID')

    def names(self, refs):
        return ', '.join(sorted({self.teeth[r].token for r in refs}))

    def own(self, tooth_ref, families):
        return [m for m in self.parsed.measurements if m.tooth_ref == tooth_ref and m.recognized_label in families]

    def usable(self, m):
        return self.analysis.usable(m, 'deg' if m.recognized_label in ANGULAR else 'mm')

    def observation(self, measurements):
        return '; '.join(f'Tooth {self.teeth[m.tooth_ref].token}: {self.analysis.value(m)} {m.recognized_label.replace("_", " ")}' for m in measurements)

    def add(self, section, policy, status, measurements, rationale, proposal, *, alternative=None, missing=(), context_refs=(), changes=(), attachment_primary=None, attachment_alternative=None):
        refs = list(dict.fromkeys(m.id for m in measurements))
        teeth = list(dict.fromkeys(m.tooth_ref for m in measurements))
        d = Decision(decision_id=f'D{len(self.plan.decisions)+1:04d}', finding_id=f'F{len(self.findings)+1:04d}', policy_id=policy, dimension=section,
            status=status, tooth_refs=teeth, measurement_refs=refs, context_refs=list(context_refs), rationale=rationale,
            proposal=proposal, alternative=alternative, missing_fields=list(missing), proposed_changes=list(changes),
            attachment_primary=attachment_primary,attachment_alternative=attachment_alternative)
        self.plan.decisions.append(d)
        text = ' '.join(x.strip() for x in [rationale, proposal, 'Alternative: '+alternative if alternative else '',
            'Information needed: '+ '; '.join(missing)+'.' if missing else ''] if x)
        self.findings.append(AnalyticalFinding(finding_id=f'F{len(self.findings)+1:04d}', section_id=section,
            kind=status, text=text, source_refs=refs, selected_refs=refs, demo_rule=policy, origin='SIMULATED_DEMO'))
        return d

    def macro(self):
        definitions = [('SAGITTAL', TRANSLATION[:1], 'REDISTRIBUTE_TRANSLATIONS'),
            ('TRANSVERSE', TRANSLATION[1:], 'REDISTRIBUTE_TRANSLATIONS'),
            ('VERTICAL', VERTICAL, 'VERTICAL_REVIEW'), ('ADDITIONAL', ANGULAR, 'ANGULAR_CONTROL')]
        for section, families, objective in definitions:
            policy = {'SAGITTAL':'DEMO-PLAN-SAGITTAL-v1','TRANSVERSE':'DEMO-PLAN-TRANSVERSE-v1',
                'VERTICAL':'DEMO-PLAN-VERTICAL-v1','ADDITIONAL':'DEMO-PLAN-ANGULAR-v1'}[section]
            targets = [t for t in self.context.targets if self.movements[t.measurement_ref].recognized_label in families]
            relevant = [m for m in self.parsed.measurements if m.recognized_label in families]
            if objective not in self.context.objectives or not targets:
                self.add(section, policy, 'INSUFFICIENT_INFORMATION', relevant,
                    'A total movement table does not define a modification objective or replacement values.',
                    'No movement change is proposed for this dimension.', missing=['Explicit fictional objective and source-bound replacement targets'], context_refs=['planning_context/objectives'])
                continue
            eligible, evidence, missing = [], [], []
            for target in targets:
                m = self.movements[target.measurement_ref]
                companions = self.own(m.tooth_ref, VERTICAL if section == 'VERTICAL' else ANGULAR)
                companions = [v for v in companions if v.id != m.id and self.usable(v) and v.magnitude_decimal > 0]
                if not self.usable(m):
                    missing.append(f'Unambiguous source value/unit for tooth {self.teeth[m.tooth_ref].token}')
                elif m.magnitude_decimal > 0 and companions and Decimal(target.amount) != m.signed_decimal:
                    eligible.append(target)
                    evidence.extend([m, *companions])
            if not eligible:
                self.add(section, policy, 'INSUFFICIENT_INFORMATION' if missing else 'NOT_APPLICABLE', relevant,
                    'The combined nonzero movement profile and distinct supplied target required by this toy policy are not established.',
                    'No change is selected.', missing=missing, context_refs=['planning_context/targets'])
                continue
            source = [self.movements[t.measurement_ref] for t in eligible]
            replacements = '; '.join(f'Tooth {self.teeth[m.tooth_ref].token}: change {m.recognized_label.replace("_", " ")} from {self.analysis.value(m)} to {t.amount} {t.unit}'+(f' ({t.source_direction}-labelled)' if t.source_direction else '') for m,t in zip(source,eligible))
            self.add(section, policy, 'ILLUSTRATIVE_PROPOSAL', list({m.id:m for m in evidence}.values()),
                'The supplied objective and targets coincide with coupled nonzero components. Coupled evidence: '+self.observation([m for m in {m.id:m for m in evidence}.values() if m.id not in {v.id for v in source}])+'.',
                'Illustrative technician request — '+replacements+'. Targets come from the fictional scenario; they are not calculated clinical limits.',
                alternative='Retain the source values and request a separate review of the coupled components.' + (' Keep absolute and relative vertical fields separate.' if section == 'VERTICAL' else ''),
                missing=missing, context_refs=['planning_context/objectives','planning_context/targets'], changes=eligible)
        self.add('ADDITIONAL','DEMO-PLAN-CONTEXT-v1','INSUFFICIENT_INFORMATION',[],
            'No validated clinical policy or patient-specific assessment is supplied.',
            'IPR, extraction, surgery, auxiliaries and clinical anchorage modifications remain unevaluated.',
            missing=['Independent clinical assessment, appropriate source records and an approved policy'])

    def micro(self):
        catalog = {o.concept:o for o in self.context.attachment_options}
        for tooth in self.parsed.teeth:
            angular = self.own(tooth.id, ANGULAR)
            known = {m.recognized_label:m for m in angular if self.usable(m)}
            measurements = angular
            primary = alternative = None
            missing = []
            policy = 'DEMO-ATT-INCOMPLETE-v1'
            if len(known) != 3 or len(angular) != 3:
                missing = ['Complete unambiguous rotation, angulation and inclination values in degrees']
            else:
                rotation, angulation, inclination = [known[f].magnitude_decimal > 0 for f in ANGULAR]
                if rotation and angulation:
                    primary, alternative, policy = 'VERTICAL_RECTANGULAR','HORIZONTAL_RECTANGULAR','DEMO-ATT-COMBINED-v1'
                elif rotation:
                    primary, alternative, policy = 'OVAL','RECTANGULAR','DEMO-ATT-ROTATION-v1'
                elif angulation:
                    primary, alternative, policy = 'HORIZONTAL_RECTANGULAR','VERTICAL_RECTANGULAR','DEMO-ATT-ANGULATION-v1'
                elif inclination:
                    primary, alternative, policy = 'OPTIMIZED_STYLE','RECTANGULAR','DEMO-ATT-INCLINATION-v1'
                else:
                    own = [m for m in self.parsed.measurements if m.tooth_ref == tooth.id]
                    required = set((*ANGULAR, 'vertical','relative_vertical',*TRANSLATION))
                    if len(own) == 7 and {m.recognized_label for m in own} == required and all(self.usable(m) for m in own):
                        measurements = own
                        if all(m.magnitude_decimal == 0 for m in own):
                            primary, policy = 'NO_ATTACHMENT','DEMO-ATT-ZERO-v1'
                        elif any(m.magnitude_decimal > 0 for m in own if m.recognized_label in VERTICAL):
                            primary, alternative, policy = 'RECTANGULAR','OVAL','DEMO-ATT-VERTICAL-v1'
                        else:
                            missing = ['A toy policy for this translation-only profile']
                    else:
                        missing = ['Complete seven-field profile before a zero-profile or vertical-only decision']
            selected = [m for m in measurements if self.usable(m) and m.magnitude_decimal > 0]
            if primary and primary not in catalog:
                missing.append(f'Supplied catalog option: {primary}')
                primary = None
            if alternative not in catalog:
                alternative = None
            geometry_missing = []
            if primary and primary != 'NO_ATTACHMENT':
                option = catalog[primary]
                geometry_missing = [label for label in ('geometry','orientation','surface','placement') if getattr(option,label) is None]
            observed = self.observation(selected) if selected else 'All seven source fields are explicitly zero' if primary == 'NO_ATTACHMENT' else 'Required movement evidence is incomplete or unsupported'
            outcome = 'NO_ATTACHMENT' if primary == 'NO_ATTACHMENT' else 'CANDIDATE' if primary else 'INSUFFICIENT_INFORMATION'
            rationale = f'Tooth {tooth.token} — {observed}. '
            explanation = {'DEMO-ATT-COMBINED-v1':'The combined rotation/angulation profile matches the toy catalog rule.',
                'DEMO-ATT-ROTATION-v1':'Nonzero rotation matches the toy oval rule.',
                'DEMO-ATT-ANGULATION-v1':'Nonzero angulation matches the toy horizontal-rectangle rule.',
                'DEMO-ATT-INCLINATION-v1':'Nonzero inclination matches the toy optimized-style category rule.',
                'DEMO-ATT-VERTICAL-v1':'The zero-angular/nonzero-vertical profile matches the toy rectangular rule.',
                'DEMO-ATT-ZERO-v1':'The complete explicit-zero profile matches the fictional no-attachment rule.'}.get(policy,'The profile has no complete applicable toy rule.')
            rationale += explanation
            proposal = ('Illustrative candidate: '+CONCEPT_LABELS[primary]+'.' if primary else 'No candidate can be selected from the supplied evidence and catalog.')
            if primary:
                option = catalog[primary]
                if option.geometry:
                    g = option.geometry
                    proposal += f' Fictional supplied dimensions: {g.width_mm} × {g.height_mm} × {g.depth_mm} mm.'
                if option.orientation:
                    proposal += f' Supplied orientation: {option.orientation.lower()}.'
                if option.surface:
                    proposal += f' Supplied surface: {option.surface.lower()}.'
                if option.placement:
                    p = option.placement
                    proposal += f' Supplied fictional local position: ({p.x_mm}, {p.y_mm}, {p.z_mm}) mm; frame {p.frame}.'
            d = self.add('ATTACHMENT_OPTIONS', policy, 'ILLUSTRATIVE_PROPOSAL' if primary else 'INSUFFICIENT_INFORMATION',
                measurements, rationale, proposal, alternative=CONCEPT_LABELS.get(alternative),
                missing=missing+geometry_missing, context_refs=['planning_context/attachment_options'],attachment_primary=primary,attachment_alternative=alternative)
            self.plan.attachment_rows.append(Candidate(tooth_ref=tooth.id,decision_id=d.decision_id,
                movement_refs=[m.id for m in selected] or [m.id for m in measurements],primary=primary,alternative=alternative,
                outcome=outcome,missing_fields=missing+geometry_missing))
        self.add('ATTACHMENT_SCOPE','DEMO-ATT-SCOPE-v1','INSUFFICIENT_INFORMATION',[],
            'These independent toy mappings use component presence, not dataset rank or tooth order.',
            'Catalog geometry and placement are explicitly supplied fictional examples. No clinical suitability or proprietary optimized-attachment specification is established.')

    def check(self, code, status, message, refs=()):
        self.plan.checks.append(PlanCheck(code=code,status=status,message=message,source_refs=list(refs)))

    def nano(self):
        details = self.submission.review_details
        try:
            validate_details(self.parsed,self.submission)
        except ValueError as error:
            self.check(str(error),'CONFLICT','Supplied stage/reference metadata conflict. All stage calculations and support proposals are withheld.')
            self.add('PHASES','DEMO-STAGE-DATA-v1','CONFLICT',[], 'Stage records cannot be bound reliably.',
                'No stage-based plan is produced; correct the supplied metadata.')
            self.finish_nano()
            return
        if not details.stages:
            self.add('PHASES','DEMO-STAGE-DATA-v1','INSUFFICIENT_INFORMATION',[],
                'Only total movements are available.', 'No stages are invented or obtained by dividing total movements.',
                missing=['Explicit ordered stages and stage-bound movement amounts'])
            # Reuse the movement-only analyzer; no second clustering/ranking policy.
            _, descriptive = self.analysis.run('nano')
            for finding in descriptive:
                if finding.kind in {'TOKEN_GROUP','CONCENTRATION','MULTI_COMPONENT','INCOMPLETE_COMPARISON','SHARED_PROFILE'}:
                    self.add('PHASES','DEMO-STAGE-MOVEMENT-ONLY-v1','INSUFFICIENT_INFORMATION',
                        [self.movements[ref] for ref in finding.source_refs],finding.text,'')
            self.finish_nano()
            return
        phase_map = {}
        phase_ids = set()
        stage_ids = {s.stage_id for s in details.stages}
        phase_conflict = False
        for phase in self.context.phases:
            if phase.phase_id in phase_ids or len(set(phase.stage_ids)) != len(phase.stage_ids):
                phase_conflict = True
            phase_ids.add(phase.phase_id)
            for stage in phase.stage_ids:
                if stage not in stage_ids or stage in phase_map:
                    phase_conflict = True
                phase_map[stage] = phase.phase_id
        if phase_conflict:
            self.check('PHASE_METADATA_CONFLICT','CONFLICT','Duplicate, overlapping or unknown phase/stage identifiers; all stage calculations are withheld.')
            self.add('PHASES','DEMO-STAGE-DATA-v1','CONFLICT',[], 'Phase metadata conflict.', 'Correct phase membership before reviewing a stage plan.')
            self.finish_nano()
            return
        if set(phase_map) != stage_ids:
            self.check('PHASE_ASSIGNMENT_MISSING','UNAVAILABLE','Some stages have no supplied phase; their phase remains unknown.')
        if self.context.stage_value_basis != 'INCREMENTS_MATCH_SOURCE_LABELS':
            self.check('STAGE_BASIS_UNSPECIFIED','UNAVAILABLE','Stage-to-total comparisons and group sums require an explicit increment/source-label convention.')
        by_stage, by_movement = defaultdict(list), defaultdict(list)
        for row in details.allocations:
            by_stage[row.stage_id].append(row)
            by_movement[row.measurement_ref].append(row)
            if row.amount is None or row.unit is None:
                self.check('STAGE_AMOUNT_MISSING','UNAVAILABLE',f'A supplied amount/unit is missing in stage {row.stage_id}; it remains unknown.',[row.measurement_ref])
        for stage in sorted(details.stages,key=lambda s:s.order):
            rows = by_stage[stage.stage_id]
            movements = [StageMovement(tooth_ref=row.tooth_ref,measurement_ref=row.measurement_ref,amount=row.amount,
                unit=row.unit,source_direction=self.movements[row.measurement_ref].raw_direction if self.context.stage_value_basis == 'INCREMENTS_MATCH_SOURCE_LABELS' else None) for row in rows]
            self.plan.stages.append(StageRow(stage_id=stage.stage_id,order=stage.order,phase_id=phase_map.get(stage.stage_id),duration_days=stage.duration_days,movements=movements))
            if not rows:
                self.check('STAGE_ASSIGNMENT_MISSING','UNAVAILABLE',f'Stage {stage.stage_id} has no supplied movement assignments.')
                d = self.add('PHASES','DEMO-STAGE-GROUP-v1','INSUFFICIENT_INFORMATION',[],f'Stage {stage.stage_id}, supplied order {stage.order}.','Movement assignments are missing.')
                self.plan.stages[-1].decision_ids.append(d.decision_id)
            groups = defaultdict(list)
            for row in rows:
                m = self.movements[row.measurement_ref]
                group = self.analysis.token_group(self.teeth[row.tooth_ref]) if self.context.notation == 'FDI' else 'Unassigned tokens'
                groups[group,m.recognized_label,row.unit,m.raw_direction].append(row)
            for (group,family,unit,direction), assignments in groups.items():
                values = '; '.join(f'Tooth {self.teeth[row.tooth_ref].token}: {row.amount if row.amount is not None else "unknown"} {row.unit or "(unit unknown)"}' for row in assignments)
                complete = all(row.amount is not None and row.unit is not None for row in assignments)
                total = exact_sum([row.amount for row in assignments]) if complete and self.context.stage_value_basis == 'INCREMENTS_MATCH_SOURCE_LABELS' else None
                d = self.add('PHASES','DEMO-STAGE-GROUP-v1','ILLUSTRATIVE_PROPOSAL' if complete else 'INSUFFICIENT_INFORMATION',
                    [self.movements[row.measurement_ref] for row in assignments],
                    f'Phase {phase_map.get(stage.stage_id,"unknown")}, stage {stage.stage_id} (supplied order {stage.order}); {group}; {(family or "unrecognized field").replace("_"," ")}.',
                    'Supplied stage movements: '+values+(f'; source label {direction}.' if direction and self.context.stage_value_basis == 'INCREMENTS_MATCH_SOURCE_LABELS' else '.')+
                    (f' Stage-group sum: {total} {unit}.' if total is not None else ' Group sum unavailable without complete amounts and a declared convention.')+
                    (f' Supplied duration: {stage.duration_days} days.' if stage.duration_days is not None else ''),
                    context_refs=[f'review_details/stages/{details.stages.index(stage)}','review_details/allocations','planning_context/phases'])
                self.plan.stages[-1].decision_ids.append(d.decision_id)
        for m in self.parsed.measurements:
            rows = by_movement[m.id]
            if not rows and self.usable(m) and m.magnitude_decimal > 0:
                self.check('MOVEMENT_ASSIGNMENT_MISSING','UNAVAILABLE',f'Tooth {self.teeth[m.tooth_ref].token}, {m.recognized_label}: no stage assignment supplied.',[m.id])
            if not rows:
                continue
            complete = all(row.amount is not None and row.unit is not None for row in rows)
            total = exact_sum([row.amount for row in rows]) if complete and self.context.stage_value_basis == 'INCREMENTS_MATCH_SOURCE_LABELS' else None
            status = 'NOT_COMPARABLE' if self.context.stage_value_basis != 'INCREMENTS_MATCH_SOURCE_LABELS' else 'UNAVAILABLE' if total is None or not self.usable(m) else 'MATCH' if Decimal(total) == m.signed_decimal else 'MISMATCH'
            self.plan.allocation_checks.append(AllocationCheck(measurement_ref=m.id,source_total=str(m.signed_decimal) if self.usable(m) else None,allocated_total=total,unit=m.unit,status=status))
            if status != 'MATCH':
                self.check('ALLOCATION_'+status,'CONFLICT' if status == 'MISMATCH' else 'UNAVAILABLE',f'Tooth {self.teeth[m.tooth_ref].token}, {m.recognized_label}: stage sum {total or "unknown"}; source total {m.signed_decimal if self.usable(m) else "unknown"}.',[m.id])
        if not self.plan.checks:
            self.check('STAGE_DATA_CONSISTENT','PASS','Stage IDs, order, references, phase membership and supplied allocation totals agree with the declared source convention.')
        self.support(phase_map)
        self.finish_nano()

    def support(self, phase_map):
        for i, constraint in enumerate(self.context.support_constraints):
            refs = constraint.support_tooth_refs+constraint.active_tooth_refs
            valid = (constraint.phase_id in set(phase_map.values()) and len(set(constraint.support_tooth_refs)) == len(constraint.support_tooth_refs)
                and len(set(constraint.active_tooth_refs)) == len(constraint.active_tooth_refs) and all(ref in self.teeth for ref in refs)
                and not set(constraint.support_tooth_refs)&set(constraint.active_tooth_refs))
            phase_rows = [m for stage in self.plan.stages if stage.phase_id == constraint.phase_id for m in stage.movements]
            active = {m.tooth_ref for m in phase_rows if m.amount is not None and Decimal(m.amount) != 0}
            if (not valid or not set(constraint.active_tooth_refs) <= active or active & set(constraint.support_tooth_refs)
                or any(c.status != 'PASS' for c in self.plan.checks)):
                self.check('SUPPORT_CONSTRAINT_CONFLICT','CONFLICT','A supplied support constraint is inconsistent or lacks complete stage evidence.')
                self.add('ANCHORAGE','DEMO-STAGE-SUPPORT-v1','CONFLICT',[],
                    'The supplied support constraint conflicts with identities, assigned movement or incomplete stage checks.',
                    'Anchorage consideration withheld.',missing=['Consistent phase, support/active roles and complete stage evidence'],context_refs=[f'planning_context/support_constraints/{i}'])
            else:
                source = [self.movements[m.measurement_ref] for m in phase_rows]
                self.add('ANCHORAGE','DEMO-STAGE-SUPPORT-v1','ILLUSTRATIVE_PROPOSAL',source,
                    f'Phase {constraint.phase_id}: scenario-supplied support teeth {self.names(constraint.support_tooth_refs)}; active teeth {self.names(constraint.active_tooth_refs)}.',
                    'Illustrative support strategy: track the supplied support group while reviewing the assigned active movements. Stationary support is a fictional assumption, not a finding inferred from missing assignments. No force or clinical anchorage prescription is calculated.',
                    alternative='Review a different explicitly supplied support grouping before accepting this fictional sequence.',context_refs=[f'planning_context/support_constraints/{i}'])

    def finish_nano(self):
        counts = {s:sum(c.status==s for c in self.plan.checks) for s in ('PASS','CONFLICT','UNAVAILABLE')}
        self.add('STAGE_CHECKS','DEMO-STAGE-CHECKS-v1','CONFLICT' if counts['CONFLICT'] else 'INSUFFICIENT_INFORMATION' if counts['UNAVAILABLE'] else 'ILLUSTRATIVE_PROPOSAL',[],
            f"Stage checks: {counts['PASS']} passed; {counts['CONFLICT']} conflicting; {counts['UNAVAILABLE']} unavailable.",
            ' '.join(c.message for c in self.plan.checks) or 'Stage-level checks require supplied stage data.',context_refs=['review_details','planning_context'])
        if not any(f.section_id == 'ANCHORAGE' for f in self.findings):
            self.add('ANCHORAGE','DEMO-STAGE-SUPPORT-v1','INSUFFICIENT_INFORMATION',[],
                'No supported phase-specific anchorage constraint is available.', 'No anchorage strategy is inferred from total TMT values.',missing=['Explicit fictional phase, support group, active group and stationary-support assumption'])
        self.add('SEQUENCE_SCOPE','DEMO-STAGE-SCOPE-v1','INSUFFICIENT_INFORMATION',[],
            'Stages and amounts come only from supplied fictional records, never by dividing source totals.',
            'Stage grouping and arithmetic do not establish biological timing, forces, clinical staging limits or a validated treatment schedule.')

    def run(self):
        if self.submission.module != 'nano':
            validate_details(self.parsed,self.submission)
            if any(self.submission.review_details.model_dump().values()):
                raise ValueError('FUNCTIONAL_CONTEXT_INVALID')
        getattr(self,self.submission.module)()
        sections = []
        for key,title in TITLES[self.submission.module].items():
            own = [f for f in self.findings if f.section_id == key]
            sections.append(ModuleSection(section_id=key,title=title,status='SIMULATED_DEMO',text='\n\n'.join(f.text for f in own),
                source_refs=list(dict.fromkeys(ref for f in own for ref in f.source_refs))))
        return sections,self.findings,self.plan


def functional_review(parsed,submission):
    if submission.planning_context.origin != 'EXPLICIT_SYNTHETIC_SCENARIO':
        raise ValueError('FUNCTIONAL_CONTEXT_INVALID')
    return Engine(parsed,submission).run()
