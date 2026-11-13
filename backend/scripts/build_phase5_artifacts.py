"""Reproducible documentation/examples from audited definitions; synthetic assets only.

This does not approve clinical policies or generate independent test expectations.
The hand-authored test oracles live in tests/fixtures/phase5_rule_cases.json.
"""
from collections import Counter
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'backend'))
sys.path.insert(0,str(ROOT/'backend/tests'))
from app.review.registry import RULES, CATALOG, execution_order
from app.review.clinical import REQUIREMENTS, preparation
from app.review.context import ToothContext, TestRuleContext, input_digest
from app.review.service import review_table
from app.reports.service import generate_report
from app.domain.models import SourceContext, RawTMTSubmission
from test_review import synthetic_review, observed

def table(rows):
    return '\n'.join('| '+' | '.join(str(c).replace('|',' / ').replace('\n',' ') for c in row)+' |' for row in rows)+'\n'

def joined(items): return ', '.join(items) or 'None'

BEHAVIOR={
    'G01':'Reject unsupported/invalid structure or global provenance failure before movement evaluation.',
    'G06':'Keep duplicate positions unresolved; the semantic field gate excludes ambiguous source associations.',
    'G08':'Require parsed/exact-zero numeric state and a recognized lexical unit; no coercion or rounding.',
    'G10':'Distinguish numeric zero from missing/invalid source cells; never fill missing data.',
    'G14':'Require independently supplied movement permission; nonzero/forbidden contradictions block only that field.',
    'G15':'Actual stage records only: detect duplicate IDs/indices, order and unresolved stage-zero kind. Gaps or absent stage zero do not imply missing data. Total-only capture without stages is NOT_APPLICABLE.',
    'G16':'Validate raw digest, versions and exact cell/header/tooth source spans; quarantine affected positions.',
    'G17':'Evaluate semantic readiness per position and retain field-specific missing prerequisites.',
    'G18':'Require independently supplied recognized permanent tooth-group evidence; no inferred FDI/Universal grouping.',
    'D01':'List authorized nonzero programmed values without risk, threshold or achieved-movement claims.',
    'D02':'Co-programmed nonzero axes only in an identical tooth/source/mode/basis/TOTAL/frame context; never temporal concurrency.',
    'D03':'Describe nonzero rotation only with explicit recognized tooth-group evidence.',
    'D04':'Describe nonzero extrusion only with explicit tooth group and canonical EXTRUSION direction.',
    'D05':'Describe nonzero intrusion only with explicit tooth group and canonical INTRUSION direction.',
    'D06':'Describe verified inclination/angulation values without inferring torque/root movement.',
    'D07':'Describe verified buccolingual displacement without inferring expansion safety or bone housing.',
    'D08':'Describe verified mesiodistal displacement without inferring bodily/root movement.',
    'D09':'Describe mesial/distal molar movement only with independently supplied MOLAR group and verified direction.',
    'D10':'Use corrected TOTAL co-programming logic, deduplicated with D02; no temporal overlap inference.',
    'D11':'Use corrected TOTAL angular/translational co-programming logic; no bodily/root-control conclusion.',
    'D12':'Count observed nonzero positions, axes, teeth and arches within compatible context; not case difficulty.',
    'D13':'Compare two explicit paired magnitudes only after independent mirror/equivalence proof and identical source/mode/basis/scope/frame/unit. Preserve both exact values; no subtraction or pathologic-asymmetry inference.',
    'D14':'Requested clinical assessments yield missing-context records; no unsolicited clinical inventory.',
    'D15':'Describe explicit zeros only for supported observed axes with no unresolved sibling; unlisted axes remain unknown.',
    'D16':'Withhold historical-plan calculation: no trusted same-case/plan binding, common baseline geometry or validated comparison operations.',
    'R14':'Withhold requested suitability/context-sensitive conclusions when necessary examination/context is absent.',
    'A05':'Globally withhold exact placement. Geometry-based placement evaluation is not implemented.',
    'A06':'Block universal attachment-superiority wording; no attachment choice is recommended.',
    'H10':'Always mark DRAFT; authenticated clinician sign-off and review invalidation workflow are not implemented.',
    'H12':'Current synthetic confirmation, no-persistence design and separate cloud gates only; no PHI detector, full privacy compliance or de-identification claim.',
    'L01':'Accept only closed templates bound to structured facts; reject injected or unsupported wording.',
    'L02':'Compare exact observation snapshots, Decimal precision, original identifiers and source evidence; reject mutations.',
    'L03':'Retain source spans, field evidence, input references and all triggering rule versions.',
    'L04':'Merge identical propositions while retaining triggering IDs; quarantine contradictions instead of choosing one.',
    'L05':'Preserve localized uncertainty and suppress unsupported facts without converting abstention to a negative.',
    'L06':'DRAFT output label only; no authenticated signature or final clinical approval.',
    'N01':'Require independently supplied expected coverage; report exact missing axis/position pairs, never zero-fill.',
    'N02':'Require a released vendor semantic version; TEST_ONLY and unknown vendor claims cannot satisfy this vendor-release guard.',
    'N03':'One capture per submission, no cross-capture combination. Patient/plan identity cannot be independently established.',
    'N04':'Preserve logical Unicode input, validate hash/spans. Browser newline canonicalization is allowed; not byte-original clipboard preservation.',
    'N05':'Require explicit paired identifiers, directions and independently asserted equivalence; do not infer mirrored signs.',
    'N06':'Require explicit independently supplied tooth status; cannot infer status from absence or magnitude.',
    'N07':'Require actual staged data when staged semantics apply; no stage-count/stage-kind inference from totals.',
    'N08':'Require compatible coordinate semantics and withhold on missing dependent fields. No geometric/transform composition implemented.',
    'N09':'Keep uncertainty field-local; independent authorized fields can retain descriptive observations.',
    'N10':'Treat all pasted content as literal untrusted text; it cannot set authority, policy, evidence or output templates.',
    'N11':'Deferred: authenticated reviewer identity, immutable versioned amendments and invalidation workflow unavailable.',
    'N12':'Withhold requested clinical purpose/endpoint assessment absent verified objectives; magnitude is not treatment intent.',
    'N13':'Apply common semantic eligibility plus rule-specific allowed domain/mode/scope and additional input checks.',
    'N14':'Deferred: incident triage, escalation and approved rollback workflow unavailable.',
}

def behavior(r):
    rid=r.rule_id
    if rid in BEHAVIOR: return BEHAVIOR[rid]
    if rid in REQUIREMENTS:
        return 'Non-executable clinical preparation only: '+joined(preparation(rid).required_fields)+'. Production always DISABLED; no approved numerical or categorical policy.'
    if rid.startswith('G'): return 'Use existing exact lexical/field-semantic states for '+joined(r.required_fields)+'; unavailable fields abstain without vendor inference.'
    if rid.startswith('H'): return 'On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim.'
    raise ValueError(rid)

def status(r):
    return f'{r.execution} / {r.implementation_kind}'

def sources(r):
    return f'[{r.source_title}]({Path(r.source_locator.split(":")[0]).name}) (line {r.source_locator.split(":")[-1]}); '+joined(r.evidence_ids)

def blocker(r):
    if r.execution=='DISABLED': return 'No approved source-specific clinical policy or released clinical validation; '+joined(r.required_fields)+'.'
    if r.execution=='DEFERRED': return r.reason+': '+joined(r.required_fields)+'.'
    if r.implementation_kind=='PARTIAL_SYSTEM_CONTROL': return behavior(r)+' Full system workflow remains outside this phase.'
    if r.rule_id in {'G14','G15','G18','D03','D04','D05','D09','D13','N01','N05','N06','N07'}:
        return 'Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.'
    return 'No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).'

def write_docs():
    inventory=['# Complete Phase 5 rule inventory','',
        '96 IDs, version 2.0.0. The audit and corrected v2 govern. The standalone original 82-rule research file is unavailable; only the corrected document’s original-proposal trace paragraphs are available. They are historical trace, never active policies. Source hashes and exact extracted text are recorded in `backend/app/review/catalog.json`.','',
        'ACTIVE means an engineering handler can run, including a required-data check or withholding control. It never means clinically approved. All 27 clinical predicates remain DISABLED. Three controls are DEFERRED. Additional group/pair/stage/status evidence currently has only a bound, private TEST_ONLY path; there is no production clinical-data intake.','',
        'Field-level missing evidence is not a negative result. Legacy `evaluated` remains true only for OBSERVED records; NOT_APPLICABLE has `predicate_result=false`, while withheld/disabled/suppressed has null. A mixed ledger status reports the limiting state; inspect linked findings for unaffected positive descriptions.','']
    for r in RULES:
        c=CATALOG[r.rule_id]
        inventory += [f'## {r.rule_id} v{r.version} — {c["source_title"]}','',
            f'1. **ID/version:** {r.rule_id} / {r.version}.',
            f'2. **Purpose (corrected):** {r.purpose}',
            f'3. **Source/evidence:** {sources(r)}. Audit assessment: {c["audit_assessment"]}',
            f'4. **Audit disposition:** {r.disposition}.',
            f'5. **Required fields:** {joined(r.required_fields)}.',
            f'6. **TMT-only feasibility (governing classification):** {r.tmt_dependence}. Even “Yes” requires independently released semantics; lexical detection is insufficient.',
            f'7. **Applicability/exclusions:** {r.applicability} {behavior(r)} Exclude: {joined(r.exclusions)}.',
            f'8. **Dependencies/conflicts:** {joined(r.dependencies)} / {joined(r.conflicting_rules)}. Priority {r.priority}. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.',
            f'9. **Deterministic behavior:** {behavior(r)}',
            f'10. **Implementation:** {status(r)}; handler identity `{r.predicate_id}` is a registry locator, not clinical approval.',
            f'11. **Clinical review:** {r.approval_status}. {joined(r.clinical_review_requirements)}. No clinical approver, policy or threshold is populated.',
            f'12. **Blocker/deferral:** {blocker(r)}','']
    (ROOT/'docs/RULE_ENGINE_PHASE5_INVENTORY.md').write_text('\n'.join(inventory),encoding='utf-8')

    approval=['# Clinical rule approval register','',
        'Every proposed clinical predicate below is **NOT APPROVED**. No orthodontist approval, cutoff, validation result or consensus is fabricated. R14/A05/A06 operate only as withholding/output guards; this does not approve their proposed clinical/geometry predicates. Runtime guards have approval_status=NOT APPLICABLE.','',
        'Evidence IDs refer to section J of [corrected v2](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md). Audit access limits remain binding: S02 is historical; S06/S07 partially verified; S08/S16 abstract-level; S09 metadata/full-text limited. Literature relevance and model predictability are not patient-specific safety limits. Phase 5 has not independently revalidated all 21 sources. No numerical limits are imported.','',
        'The input checklist is an executable structural-readiness aid only. It never returns a clinical predicate result. TEST_ONLY comparator demonstrations use explicit caller-supplied illustrative Decimal parameters, perform only GT/GE comparisons and do not implement the full anatomical applicability of a clinical rule. No comparator is called by the production engine.','']
    for r in RULES:
        if r.rule_id not in REQUIREMENTS: continue
        p=preparation(r.rule_id)
        approval += [f'## {r.rule_id} — {r.source_title}','',
            f'- **Proposed purpose:** {r.purpose}',f'- **Supporting references:** {sources(r)}.',
            f'- **Evidence limits:** {CATALOG[r.rule_id]["audit_assessment"]} No released case-based trigger validation is available; source-specific context and applicability remain necessary.',
            f'- **Required measurements/context:** {joined(p.required_fields)}. Additional input contract: `{json.dumps(p.additional_inputs.model_dump(),sort_keys=True)}`.',
            f'- **Applicability/exclusions:** {behavior(r)} Exclude unverified source/version/numbering/direction/unit, comparison-as-absolute data, incompatible basis/scope/frame and absent dependent examination information.',
            f'- **Unapproved policy parameters:** {joined(p.unapproved_parameters)}. Values deliberately absent.',
            '- **False-positive/false-negative consequences:** An unsupported flag could misdirect review, anchorage, attachment or staging decisions; an omitted flag could falsely reassure a reviewer. Neither rate is measured. Clinical reviewers must define rule-specific harms and adjudication criteria before activation.',
            f'- **Orthodontist review questions:** For {r.source_title.lower()}, which exact source/version/dentition/mode/basis/scope, clinical intent and exclusions apply? Which of {joined(p.required_fields)} must be independently supplied? Is a trigger justified at all? Approve the exact comparator/category/interaction, severity and qualified wording; do not infer approval from cited literature.',
            '- **Approval:** NOT APPROVED; approver=null; approved policy=null; production clinical predicate disabled.',
            '- **Before activation:** Authentic de-identified vendor captures and independent dual-review expected semantics; code-controlled vendor release; independently verified additional inputs bound to case/plan/stage; versioned signed orthodontist policy defining trigger/applicability/exclusions/wording; preregistered multi-reader shadow evaluation with adjudicated critical misses and over-flags; formal release, audit, invalidation and rollback process. Production activation is not implemented in this phase.','']
    (ROOT/'docs/CLINICAL_RULE_APPROVAL_REGISTER.md').write_text('\n'.join(approval),encoding='utf-8')

    feasibility=['# Rule feasibility: TMT and additional inputs','',
        'An ordinary total TMT establishes neither achieved movement nor patient suitability. A readable scalar is lexical evidence only. All vendor semantics remain unverified. “Yes” below is the corrected specification’s feasibility classification, never an assertion that public pasted input is currently authorized.','',
        '| Family / subset | Engineering capability now | Additional evidence required |',
        '| --- | --- | --- |',
        '| G / D movement inventory | Structure, provenance, exact scalar and field eligibility checks | Released numbering/dentition/axes/units/signs/directions/version/mode/basis/scope/frame |',
        '| G14/G18, D03–05/D09, N06 | Typed group/status guards, TEST_ONLY demonstrations | Independently verified tooth-group and tooth-status map; no inference from numeric tooth IDs |',
        '| D13 / N05 | Exact paired-magnitude comparison, no subtraction | Verified pair/mirror-direction proof and equivalent plan/basis/scope/frame/unit |',
        '| G15 / N07 | Actual stage sequence validation | Stage ID/index/kind/arch dataset with source/version and baseline semantics |',
        '| D16 / T02 / N08 | Withhold arithmetic/composition | Same-case/plan binding, initial geometry, common coordinate frames and validated composition/comparison operations |',
        '| R01–12 / R15 | Rule-specific prerequisites; limited illustrative comparator plumbing | Tooth groups, anatomy/direction, objectives/exclusions and orthodontist-approved rule-specific policy; several need root/bone/stage/attachment context |',
        '| R13 / T01–05/T08 | Disabled prerequisite designs | Actual staged values, source device profile/config history, intended sequence and validated interaction/anchorage protocol |',
        '| R16 | Disabled | Examination, skeletal/occlusal/periodontal context, objectives and validated full-case rubric |',
        '| T06 | Disabled | Validated 3D geometry, staged paths and contact/interference engine |',
        '| T07 | Disabled | Approved IPR plan, enamel/contact assessment and stage timing |',
        '| A01–04 | Disabled | Actual tooth/surface/stage attachment map, proposals, indications, removals and timing policy |',
        '| R14 / A05–06 / H / L | Withholding and closed-output guards | Clinical/geometry conclusions remain unavailable; sign-off and privacy workflows only partial |',
        '| N11 / N14 | Deferred | Authenticated immutable amendments, invalidation and incident/rollback workflows |','',
        '## Complete 96-rule feasibility matrix','']
    feasibility.append(table([('Rule','Corrected TMT class','Required fields','Implementation'),('---','---','---','---')]+[(r.rule_id,r.tmt_dependence,joined(r.required_fields),status(r)) for r in RULES]))
    feasibility += ['', 'The public API has no extra clinical-data contract or TEST_ONLY evidence authorization fields. AdditionalInputRequirements is a future integration checklist; TestRuleContext is private illustrative library evidence only. N01 expected coverage remains null in the legacy summary; explicit TEST_ONLY expected coverage is recorded in N01 findings, never synthesized into missing values.']
    (ROOT/'docs/RULE_FEASIBILITY_MATRIX.md').write_text('\n'.join(feasibility),encoding='utf-8')

    matrix=table([('Rule v2.0.0','Audited purpose','Disposition','Execution','Implementation kind'),('---','---','---','---','---')]+[(r.rule_id,r.source_title,r.disposition,r.execution,r.implementation_kind) for r in RULES])
    (ROOT/'examples/phase5-rule-matrix.md').write_text(matrix,encoding='utf-8')

def write_examples():
    raw='# SYNTHETIC TEST_ONLY — illustrative evidence, no patient or vendor\nTooth\tRotation (deg)\tExtrusion (mm)\n13\t−1.2300 M\t0.00 E\n'
    s=RawTMTSubmission(raw_text=raw,synthetic_data_confirmed=True,context=SourceContext(source_version='TEST_ONLY-1'))
    with TemporaryDirectory(prefix='finova-phase5-synthetic-') as temp:
        _,checked=synthetic_review(Path(temp),raw=raw,overrides={'measurement-1':{'axis':'ROTATION'}})
        extra=TestRuleContext(input_digest=input_digest(s),teeth=(ToothContext(canonical_tooth_id='TEST_TOOTH_tooth-1',group='CANINE',status='PRESENT',movement_permitted=True,evidence_ref='TEST_ONLY:independent-group-oracle'),))
        r=review_table(s,checked=checked,test_only=True,test_context=extra)
        finding=observed(r,'D03')[0]
        report=generate_report(s,checked=checked,test_only=True,test_context=extra,mode='TEMPLATES')
        (ROOT/'examples/phase5-synthetic-finding.json').write_text(finding.model_dump_json(indent=2)+'\n',encoding='utf-8')
        (ROOT/'examples/phase5-synthetic-draft-report.json').write_text(report.model_dump_json(indent=2)+'\n',encoding='utf-8')
        (ROOT/'examples/phase5-synthetic-draft-report.txt').write_text('SYNTHETIC TEST_ONLY EXAMPLE — NO VENDOR OR CLINICAL VALIDATION\n\n'+report.export_text+'\n',encoding='utf-8')
    # Public unverified API response fixture; contains no authorized synthetic semantics.
    parse=json.loads((ROOT/'frontend/src/test/fixtures/synthetic-parse-result.json').read_text(encoding='utf-8'))
    result=review_table(RawTMTSubmission(raw_text=parse['raw_text'],synthetic_data_confirmed=True))
    (ROOT/'frontend/src/test/fixtures/synthetic-phase5-review.json').write_text(result.model_dump_json(indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    write_docs(); write_examples()
    print('96-rule inventory, approval register, feasibility matrix and synthetic examples written; no clinical activation.')
