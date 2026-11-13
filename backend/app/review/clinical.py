"""Clinical prerequisite preparation; there is no production activation path."""

from decimal import Decimal
from typing import Literal
from pydantic import Field

from app.review.context import AdditionalInputRequirements
from app.review.models import ObservedMeasurement
from app.semantics.models import EvidenceContract

# Explicit rule-specific needs derived from corrected v2, not default thresholds.
REQUIREMENTS = {
    'R01': ('verified_tooth_group','verified_rotation','source_specific_review_policy','approved_exceptions_and_intent'),
    'R02': ('verified_tooth_group','verified_rotation','approved_movement_size_bands'),
    'R03': ('verified_anterior_group','verified_extrusion','approved_extrusion_policy'),
    'R04': ('verified_posterior_group','verified_extrusion','approved_device_specific_policy'),
    'R05': ('verified_lower_incisor_identity','verified_intrusion','approved_intrusion_policy'),
    'R06': ('verified_tooth_group','verified_intrusion','root_support_and_occlusal_objectives','approved_intrusion_policy'),
    'R07': ('verified_incisor_identity','verified_inclination','root_position_and_geometry','approved_root_control_review_policy'),
    'R08': ('verified_angulation','verified_tooth_group','approved_angulation_review_policy'),
    'R09': ('verified_posterior_group','verified_buccolingual_movement','bone_and_root_assessment','approved_transverse_review_policy'),
    'R10': ('verified_upper_molar_identity','verified_distal_direction','staged_anchorage_context','approved_distalization_policy'),
    'R11': ('verified_molar_identity','verified_mesial_direction','extraction_space_and_root_context','approved_mesialization_policy'),
    'R12': ('verified_combination_axes','verified_directions_and_groups','approved_validated_interaction_matrix'),
    'R13': ('actual_stage_dataset','verified_device_version_profile','approved_stage_policy'),
    'R14': ('requested_assessment_context',),
    'R15': ('verified_movement_group','actual_attachment_plan','approved_open_ended_review_policy'),
    'R16': ('full_clinical_examination','occlusion_and_skeletal_periodontal_context','treatment_objectives','approved_full_case_rubric'),
    'T01': ('actual_per_stage_values','verified_device_profile','orthodontist_approved_stage_limits'),
    'T02': ('actual_stage_dataset','verified_baseline_geometry','verified_coordinate_transforms','approved_composition_operations_and_tolerance'),
    'T03': ('actual_per_stage_values','verified_configured_constraint','configuration_history','approved_stage_policy'),
    'T04': ('actual_stage_dataset','verified_intended_distalization_sequence','approved_anchorage_protocol'),
    'T05': ('actual_stage_overlap','device_specific_validated_interaction_matrix','approved_interaction_policy'),
    'T06': ('validated_3d_geometry','verified_alignment_and_staged_paths','validated_contact_engine'),
    'T07': ('approved_ipr_plan','enamel_and_interproximal_contacts','stage_timing','clinical_review'),
    'T08': ('staged_force_and_anchorage_strategy','crown_root_coordinates','approved_protocol'),
    'A01': ('actual_attachment_tooth_surface_stage_map','verified_tooth_and_stage_identity','intentional_removal_metadata'),
    'A02': ('actual_attachment_tooth_surface_stage_map','verified_stage_and_movements','approved_attachment_indications'),
    'A03': ('two_approved_attachment_proposals','approved_conflict_resolution_policy'),
    'A04': ('actual_attachment_start_end_stages','verified_plan_mode_and_stage_conventions','approved_timing_policy'),
    'A05': ('validated_crown_surface_and_attachment_geometry','clinical_geometry_validation'),
    'A06': ('case_specific_comparative_evidence','approved_qualified_wording'),
}


class ClinicalPreparation(EvidenceContract):
    rule_id: str
    classification: Literal['POLICY_REQUIRED','EXTRA_CONTEXT_REQUIRED','NOT_TMT_EVALUABLE','UNSUPPORTED_INTERACTION','WITHHOLDING_ONLY']
    required_fields: tuple[str, ...]
    unapproved_parameters: tuple[str, ...]
    additional_inputs: AdditionalInputRequirements
    production_enabled: Literal[False] = False
    approval_status: Literal['NOT APPROVED'] = 'NOT APPROVED'
    policy_id: None = None
    clinical_approver: None = None


def preparation(rid: str) -> ClinicalPreparation:
    if rid not in REQUIREMENTS: raise ValueError('NOT_A_CLINICAL_CANDIDATE')
    withholding=rid in {'R14','A05','A06'}
    extra=rid in {'R06','R07','R09','R10','R11','R15'}
    impossible=rid.startswith('T') or rid in {'R13','R16','A01','A02','A03','A04'}
    classification='WITHHOLDING_ONLY' if withholding else 'UNSUPPORTED_INTERACTION' if rid=='R12' else 'NOT_TMT_EVALUABLE' if impossible else 'EXTRA_CONTEXT_REQUIRED' if extra else 'POLICY_REQUIRED'
    inputs=AdditionalInputRequirements(
        stage_sequence=rid.startswith('T') or rid in {'R10','R13','R15','A01','A02','A04'},
        attachment_tooth_surface_stage_map=rid.startswith('A') or rid=='R15',
        initial_final_crown_root_geometry=rid in {'R07','R09','T02','T06','T08','A05'},
        coordinate_frame_and_validated_operations=rid in {'T02','T06','T08'},
        interproximal_contact_and_enamel_assessment=rid=='T07',approved_ipr_plan=rid=='T07',
        verified_occlusal_examination=rid in {'R06','R16'},periodontal_and_root_assessment=rid in {'R06','R07','R09','R16','T08'},
        patient_objectives_and_exclusions=rid.startswith('R'),device_profile_and_config_history=rid.startswith('T'))
    parameters=() if withholding else ('exact_applicability_and_exclusions','approved_output_and_severity','independent_validation_protocol')
    if rid in {'R01','R03','R04','R05','R06','R08','R09','R10','R11','T01','T03'}: parameters+=('comparator','source_specific_boundary_and_unit')
    if rid=='R02': parameters+=('movement_size_category_boundaries',)
    if rid in {'R12','T05'}: parameters+=('validated_interaction_matrix',)
    if rid=='T02': parameters+=('composition_operation','numeric_tolerance',)
    return ClinicalPreparation(rule_id=rid,classification=classification,required_fields=REQUIREMENTS[rid],unapproved_parameters=parameters,additional_inputs=inputs)


# Structural preconditions only. No tooth-number lookup, vendor sign mapping or cutoff.
MOVEMENT_REQUIREMENTS = {
    'R01': (('ROTATION',), ('CANINE','PREMOLAR'), ()),
    'R02': (('ROTATION',), ('INCISOR','CANINE','PREMOLAR','MOLAR'), ()),
    'R03': (('EXTRUSION','VERTICAL'), ('INCISOR','CANINE'), ('EXTRUSION',)),
    'R04': (('EXTRUSION','VERTICAL'), ('PREMOLAR','MOLAR'), ('EXTRUSION',)),
    'R05': (('INTRUSION','VERTICAL'), ('INCISOR',), ('INTRUSION',)),
    'R06': (('INTRUSION','VERTICAL'), ('INCISOR','CANINE','PREMOLAR','MOLAR'), ('INTRUSION',)),
    'R07': (('INCLINATION',), ('INCISOR',), ()),
    'R08': (('ANGULATION',), ('INCISOR','CANINE','PREMOLAR','MOLAR'), ()),
    'R09': (('BUCCOLINGUAL',), ('PREMOLAR','MOLAR'), ()),
    'R10': (('MESIODISTAL',), ('MOLAR',), ('DISTAL',)),
    'R11': (('MESIODISTAL',), ('MOLAR',), ('MESIAL',)),
}


class CandidateInputReadiness(EvidenceContract):
    """Evidence checklist, never a clinical predicate, recommendation or Finding."""
    rule_id: str
    measurement_id: str
    structural_fields_satisfied: bool
    missing_required_fields: tuple[str, ...]
    predicate_result: None = None
    production_enabled: Literal[False] = False
    approval_status: Literal['NOT APPROVED'] = 'NOT APPROVED'


def inspect_candidate_inputs(rid: str, observation: ObservedMeasurement) -> CandidateInputReadiness:
    if rid not in MOVEMENT_REQUIREMENTS: raise ValueError('NO_TMT_MOVEMENT_PRECONDITIONS')
    v={c.name:c.canonical_value for c in observation.components}
    axes,groups,directions=MOVEMENT_REQUIREMENTS[rid]
    structural=[]
    if v.get('axis') not in axes: structural.append('rule_specific_movement_axis')
    if observation.tooth_group not in groups or not observation.additional_evidence_refs:
        structural.append('independently_verified_tooth_group')
    if directions and v.get('direction') not in directions: structural.append('rule_specific_direction')
    if observation.magnitude.is_zero(): structural.append('nonzero_programmed_movement')
    # No anatomical arch identity is inferred from an opaque or vendor identifier.
    if rid in {'R05','R10'}: structural.append('independently_verified_lower_or_upper_arch_identity')
    missing=tuple(sorted(set(structural+list(REQUIREMENTS[rid])+['orthodontist_approved_policy'])))
    return CandidateInputReadiness(rule_id=rid,measurement_id=observation.measurement_id,
        structural_fields_satisfied=not structural,missing_required_fields=missing)


class IllustrativePolicy(EvidenceContract):
    """Not an approved policy; cannot be accepted by HTTP or the production engine."""
    domain: Literal['TEST_ONLY']
    axis: str
    unit: str
    comparator: Literal['GT','GE']
    illustrative_boundary: Decimal = Field(ge=0)


class IllustrativeResult(EvidenceContract):
    domain: Literal['TEST_ONLY'] = 'TEST_ONLY'
    rule_id: str
    predicate_result: bool | None
    reason: str
    production_enabled: Literal[False] = False
    clinical_approval: Literal['NOT APPROVED'] = 'NOT APPROVED'


def simulate_test_only(rid: str, observation: ObservedMeasurement, policy: IllustrativePolicy) -> IllustrativeResult:
    """Exercise comparator plumbing only, not a complete clinical predicate or Finding."""
    if rid not in {'R01','R03','R04','R05','R06','R08','R09','R10','R11'}:
        raise ValueError('NO_DEFINED_ILLUSTRATIVE_COMPARATOR')
    if observation.verification!='TEST_ONLY': raise ValueError('TEST_ONLY_OBSERVATION_REQUIRED')
    v={c.name:c.canonical_value for c in observation.components}
    if v.get('axis')!=policy.axis or v.get('unit')!=policy.unit:
        return IllustrativeResult(rule_id=rid,predicate_result=None,reason='ILLUSTRATIVE_INPUT_REQUIREMENTS_NOT_MET')
    triggered=observation.magnitude>policy.illustrative_boundary if policy.comparator=='GT' else observation.magnitude>=policy.illustrative_boundary
    return IllustrativeResult(rule_id=rid,predicate_result=triggered,reason='COMPARATOR_PLUMBING_ONLY_NOT_CLINICAL_VALIDATION')
