"""Audit IDs retained. No numerical policy or path to enable clinical predicates."""

from app.review.models import RuleDefinition
import json
from pathlib import Path

CATALOG = {r['rule_id']: r for r in json.loads(Path(__file__).with_name('catalog.json').read_text(encoding='utf-8'))['rules']}

_GATES = (
    ("Non-empty structured input", ("lexical_structure",)),
    ("Reliable source identity", ("source_application", "source_version")),
    ("Tooth numbering convention", ("notation", "dentition", "arch")),
    ("Tooth ID validity", ("tooth_identifier", "notation", "dentition")),
    ("Arch association", ("arch",)),
    ("Duplicate tooth records", ("duplicate_scope",)),
    ("Canonical movement label mapping", ("axis",)),
    ("Numeric, unit and precision integrity", ("numeric_value", "unit")),
    ("Directional meaning verified", ("sign", "direction")),
    ("Missing versus zero", ("numeric_value",)),
    ("Reference basis: crown/root/cusp", ("reference_basis",)),
    ("Total versus stage mode", ("scope", "stage_index", "stage_kind")),
    ("Plan/comparison mode", ("plan_mode",)),
    ("Absent/unmovable teeth", ("verified_external_tooth_status",)),
    ("Stage ordering and identifiers", ("verified_stage_dataset",)),
    ("Schema version and original evidence", ("source_provenance",)),
    ("Conflict and unsupported input handling", ("field_semantic_eligibility",)),
    ("Recognized tooth types only", ("verified_tooth_group_map",)),
)
_DESCRIPTIONS = (
    "Movement inventory per tooth", "Co-programmed movement axes", "Rotation by tooth group",
    "Extrusion by tooth group", "Intrusion by tooth group", "Source inclination/angulation inventory",
    "Buccolingual displacement inventory", "Mesiodistal displacement inventory", "Molar mesial/distal movement",
    "Co-programmed rotation and vertical axes", "Co-programmed angular and translational axes",
    "Movement distribution summary", "Equivalent opposite-side comparison", "Requested context inventory",
    "All supported, observed axes are zero", "Historical plan difference",
)
_CLINICAL = (
    "Canine/premolar rotation review", "Rotation magnitude band by tooth type", "Anterior extrusion review",
    "Posterior extrusion review", "Lower incisor intrusion review", "Other intrusion review",
    "Incisor inclination/root-control review", "Mesiodistal angulation review", "Posterior transverse movement review",
    "Maxillary molar distalization review", "Molar mesialization review", "Movement combination review",
    "Staged versus total concern", "Context-sensitive assessment withheld", "Attachment strategy review", "Whole-case complexity",
)
_STAGING = (
    "Per-stage movement ceilings", "Cumulative/incremental consistency", "Observed configured constraint exceedance",
    "Sequential distalization pattern", "Movement overlap interaction", "Geometry interference", "IPR timing and quantity",
    "Anchorage/root balancing",
)
_ATTACHMENTS = (
    "Attachment presence audit", "Attachment-to-movement review", "Conflicting attachment preferences",
    "Attachment stage scheduling", "Exact attachment placement withheld", "Universal attachment superiority blocked",
)
_SAFETY = (
    "No suitability diagnosis", "Periodontal condition unavailable", "Root/bone assessment unavailable",
    "Occlusal contacts unavailable", "No unseen IPR planning", "No extraction/surgery recommendations",
    "No predicted probability/duration", "No attachment prescriptions", "No collision-free staging claim",
    "Draft and clinician inspection", "Context-dependent exclusions", "Privacy/data minimization",
)
_OUTPUT = (
    "Only structured template facts", "Measurement exactness", "Finding-to-source traceability",
    "Deduplication and explicit conflicts", "Localized uncertainty", "Draft-only review status",
)
_PROTECTIONS = (
    "Expected coverage remains unknown", "Unknown format/version abstention", "Single-capture identity isolation",
    "Raw Unicode evidence preservation", "Verified mirrored sign convention only", "External tooth status required",
    "Stage states required", "No unproven composition", "Field-scoped abstention", "Untrusted text cannot alter claims",
    "Immutable signed amendments", "Requested purpose separate from measurements", "Rule-dependent eligibility",
    "Incident and rollback workflow",
)

_CONTROL_INPUTS = {
    'D14': ('requested_assessments','verified_clinical_context'),
    'A05': ('output_attachment_placement_claims',), 'A06': ('output_attachment_superiority_claims',),
    'H01': ('requested_suitability_assessment','clinical_examination'),
    'H02': ('requested_periodontal_assessment','periodontal_records'),
    'H03': ('requested_root_bone_assessment','root_bone_records'),
    'H04': ('requested_occlusion_assessment','occlusal_records'),
    'H05': ('requested_ipr_assessment','contact_enamel_and_ipr_plan'),
    'H06': ('requested_extraction_surgery_assessment','clinical_diagnosis'),
    'H07': ('requested_prognosis','validated_patient_specific_outcomes'),
    'H08': ('requested_attachment_assessment','actual_attachment_plan'),
    'H09': ('requested_collision_assessment','validated_staged_geometry'),
    'H10': ('report_review_status',), 'H11': ('requested_intervention_assessment','verified_clinical_exclusions'),
    'H12': ('synthetic_data_confirmed','separate_server_cloud_authorization'),
    'L01': ('structured_findings','closed_output_templates'), 'L02': ('exact_observation_snapshot',),
    'L03': ('finding_input_refs','source_evidence_refs'), 'L04': ('finding_propositions','conflict_keys'),
    'L05': ('field_scoped_verification_states',), 'L06': ('report_review_status',),
    'N01': ('verified_expected_axis_coverage',), 'N02': ('released_source_version',),
    'N03': ('single_capture_boundary',), 'N04': ('raw_text','raw_sha256','source_spans'),
    'N05': ('verified_pair_map_and_mirror_operations',), 'N06': ('verified_external_tooth_status',),
    'N07': ('verified_stage_dataset',), 'N08': ('verified_coordinate_frame_and_operations',),
    'N09': ('field_verification_states',), 'N10': ('trusted_structured_context','untrusted_literal_text'),
    'N12': ('verified_treatment_objectives','clinical_endpoint'), 'N13': ('rule_specific_eligibility_contract',),
}


def _build_registry() -> tuple[RuleDefinition, ...]:
    rules = []
    for i, (name, fields) in enumerate(_GATES, 1):
        rid = f"G{i:02}"
        rules.append(RuleDefinition(rule_id=rid, name=name, category="TECHNICAL", disposition="REVISE" if i == 14 else "READY",
                                    execution="DEFERRED" if i in {14, 15, 18} else "ACTIVE", required_fields=fields,
                                    reason="CONSUMES_EXISTING_PARSER_AND_SEMANTIC_GATES" if i not in {14, 15, 18} else "VERIFIED_EXTERNAL_DATA_CONTRACT_REQUIRED"))
    for i, name in enumerate(_DESCRIPTIONS, 1):
        deferred = i in {3, 4, 5, 9, 13, 16}
        fields = ("verified_tooth_group_map",) if i in {3, 4, 5, 9} else ("verified_pair_map_and_mirror_operations",) if i == 13 else ("verified_baseline_geometry_and_operations",) if i == 16 else ("authorized_semantic_measurement",)
        rules.append(RuleDefinition(rule_id=f"D{i:02}", name=name, category="DESCRIPTIVE",
                                    disposition="REVISE" if i in {2, 10, 11, 16} else "READY",
                                    execution="DEFERRED" if deferred else "ACTIVE", required_fields=() if i == 14 else fields,
                                    dependencies=() if deferred or i in {1, 14} else ("D01",),
                                    allowed_evidence=("AUTHORIZED_VENDOR", "TEST_ONLY"), allowed_modes=("ALIGN_FINAL", "DOCTOR_FINAL", "TEST_PLAN_MODE"),
                                    allowed_scopes=("TOTAL",) if i in {2, 10, 11} else ("TOTAL", "CUMULATIVE", "INCREMENTAL", "STAGE_SPECIFIC"),
                                    reason="AUDIT_CORRECTED_DESCRIPTIVE_ONLY" if not deferred else "ADDITIONAL_VERIFIED_MAP_OR_GEOMETRY_REQUIRED"))
    for i, name in enumerate(_CLINICAL, 1):
        rules.append(RuleDefinition(rule_id=f"R{i:02}", name=name, category="SAFETY" if i == 14 else "CLINICAL",
                                    disposition="READY" if i == 14 else "MORE DATA" if i in {13, 16} else "VALIDATE",
                                    execution="ACTIVE" if i == 14 else "DISABLED",
                                    required_fields=("orthodontist_approved_policy", "policy_specific_verified_context") if i != 14 else ("requested_assessment_context",),
                                    reason="SUFFICIENCY_ABSTENTION_ONLY" if i == 14 else "NO_APPROVED_CLINICAL_POLICY"))
    for prefix, names, category in (("T", _STAGING, "STAGING"), ("A", _ATTACHMENTS, "ATTACHMENT")):
        for i, name in enumerate(names, 1):
            guard = prefix == "A" and i in {5, 6}
            rules.append(RuleDefinition(rule_id=f"{prefix}{i:02}", name=name, category="SAFETY" if guard else category,
                                        disposition="READY" if prefix == "A" and i == 6 else "MORE DATA",
                                        execution="ACTIVE" if guard else "DISABLED", required_fields=() if guard else ("approved_policy_and_verified_extra_data",),
                                        reason="GLOBAL_WITHHOLDING_GUARD_ONLY" if guard else "NO_POLICY_OR_EXTRA_DATA_MODULE"))
    for prefix, names, category in (("H", _SAFETY, "SAFETY"), ("L", _OUTPUT, "OUTPUT"), ("N", _PROTECTIONS, "PROTECTION")):
        for i, name in enumerate(names, 1):
            deferred = prefix == "N" and i in {11, 14}
            rules.append(RuleDefinition(rule_id=f"{prefix}{i:02}", name=name, category=category,
                                        disposition="ADDITIONAL" if prefix == "N" else "READY",
                                        execution="DEFERRED" if deferred else "ACTIVE",
                                        reason="FUTURE_AUTHORIZED_WORKFLOW_REQUIRED" if deferred else "PHASE2A_INVARIANT_ONLY"))
    return tuple(sorted(rules, key=lambda r: r.rule_id))


def _complete(rule: RuleDefinition) -> RuleDefinition:
    from app.review.clinical import REQUIREMENTS
    rid=rule.rule_id; data=rule.model_dump(); source=CATALOG[rid]
    if rid in _CONTROL_INPUTS: data['required_fields']=_CONTROL_INPUTS[rid]
    priority=10 if rid in {'G01','G16','N04'} else 20 if rid.startswith('G') else 30 if rid in {'D14','R14'} else 40 if rid.startswith('D') else 50 if rid.startswith(('R','T')) else 70 if rid.startswith('A') else 80 if rid.startswith(('H','N')) else 90
    if rid in {'N01','N02','N03','N05','N06','N07','N08','N09','N13'}: priority=25
    if rid=='N12': priority=30
    guarded=rid in {'G14','G15','G18','D03','D04','D05','D09','D13'}
    clinical=(rid.startswith('R') and rid!='R14') or rid.startswith('T') or rid in {'A01','A02','A03','A04'}
    if guarded: data.update(execution='ACTIVE',reason='VERIFIED_ADDITIONAL_INPUT_OR_LOCALIZED_ABSTENTION')
    if clinical: data['required_fields']=('orthodontist_approved_policy',)+REQUIREMENTS[rid]
    if rid=='D13': data['required_fields']=('authorized_semantic_measurement','verified_pair_map_and_mirror_operations')
    if rid in {'D03','D04','D05','D09'}: data['required_fields']=('authorized_semantic_measurement','verified_tooth_group_map')
    if rid=='D16': data['required_fields']=('verified_case_plan_identity','verified_baseline_geometry_and_operations','verified_coordinate_frame','approved_comparison_operation')
    if rid=='G15': data['required_fields']=('verified_stage_dataset',)
    if rid=='G18': data['required_fields']=('verified_tooth_group_map',)
    if rid=='G14': data['required_fields']=('verified_external_tooth_status',)
    if rid=='N11': data['required_fields']=('authenticated_reviewer_identity','immutable_versioned_review_events','approval_invalidation_workflow')
    if rid=='N14': data['required_fields']=('incident_severity_policy','approved_escalation_workflow','reviewed_rollback_release_process')
    dependencies=data['dependencies']
    if rid.startswith('D') and rid not in {'D01','D14','D16'}: dependencies=('D01',)
    if rid=='D01': dependencies=('G01','G16','G17')
    if rid=='R13': dependencies=('T01',)
    if rid in {'D03','D04','D05','D09'}: dependencies+=('G18',)
    if rid=='D13': dependencies+=('N05',)
    kind='DEFERRED' if data['execution']=='DEFERRED' else 'REQUIRED_DATA_GUARD' if clinical or guarded or rid=='N12' else 'EXECUTABLE'
    if rid.startswith('L') or rid in {'A05','A06','N10'}: kind='OUTPUT_GUARD'
    if rid in {'H10','H12','L06','N03','N04'}: kind='PARTIAL_SYSTEM_CONTROL'
    data.update(priority=priority,purpose=source['audit_required'],source_title=source['source_title'],
                source_locator=f"docs/FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md:{source['source_line']}",
                evidence_ids=tuple(source['evidence_ids']),audit_required=source['audit_required'],
                disposition=source['disposition'],tmt_dependence=source['tmt_dependence'],
                applicability='Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain.',
                exclusions=('Unverified or ambiguous dependent fields','Cross-basis/mode/frame operations without verified mapping','No inference of achieved movement'),
                dependencies=dependencies,conflicting_rules=('T01',) if rid=='R13' else ('R13',) if rid=='T01' else (),
                predicate_id=rid.lower()+'_v2',implementation_kind=kind,
                approval_status='NOT APPROVED' if clinical else 'NOT APPLICABLE',
                clinical_review_requirements=('Exact policy and exclusions','Orthodontist approval','Independent multi-reader case evaluation','Controlled release and rollback') if clinical else ())
    return RuleDefinition.model_validate(data)


RULES = tuple(_complete(rule) for rule in _build_registry())


def execution_order(rules: tuple[RuleDefinition, ...] = RULES) -> tuple[RuleDefinition, ...]:
    """Stable topological order; malformed registries never execute opportunistically."""
    remaining = {r.rule_id: r for r in rules}
    if len(remaining) != len(rules) or any(d not in remaining for r in rules for d in r.dependencies):
        raise ValueError("INVALID_RULE_DEPENDENCIES")
    ordered = []
    done = set()
    while remaining:
        ready = sorted((rid for rid, rule in remaining.items() if set(rule.dependencies) <= done),key=lambda rid:(remaining[rid].priority,rid))
        if not ready:
            raise ValueError("CYCLIC_RULE_DEPENDENCIES")
        # Recompute after each node so newly unblocked earlier-priority gates run first.
        rid=ready[0]
        ordered.append(remaining.pop(rid))
        done.add(rid)
    return tuple(ordered)


RULE_BY_ID = {r.rule_id: r for r in RULES}
