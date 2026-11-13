# Rule feasibility: TMT and additional inputs

An ordinary total TMT establishes neither achieved movement nor patient suitability. A readable scalar is lexical evidence only. All vendor semantics remain unverified. “Yes” below is the corrected specification’s feasibility classification, never an assertion that public pasted input is currently authorized.

| Family / subset | Engineering capability now | Additional evidence required |
| --- | --- | --- |
| G / D movement inventory | Structure, provenance, exact scalar and field eligibility checks | Released numbering/dentition/axes/units/signs/directions/version/mode/basis/scope/frame |
| G14/G18, D03–05/D09, N06 | Typed group/status guards, TEST_ONLY demonstrations | Independently verified tooth-group and tooth-status map; no inference from numeric tooth IDs |
| D13 / N05 | Exact paired-magnitude comparison, no subtraction | Verified pair/mirror-direction proof and equivalent plan/basis/scope/frame/unit |
| G15 / N07 | Actual stage sequence validation | Stage ID/index/kind/arch dataset with source/version and baseline semantics |
| D16 / T02 / N08 | Withhold arithmetic/composition | Same-case/plan binding, initial geometry, common coordinate frames and validated composition/comparison operations |
| R01–12 / R15 | Rule-specific prerequisites; limited illustrative comparator plumbing | Tooth groups, anatomy/direction, objectives/exclusions and orthodontist-approved rule-specific policy; several need root/bone/stage/attachment context |
| R13 / T01–05/T08 | Disabled prerequisite designs | Actual staged values, source device profile/config history, intended sequence and validated interaction/anchorage protocol |
| R16 | Disabled | Examination, skeletal/occlusal/periodontal context, objectives and validated full-case rubric |
| T06 | Disabled | Validated 3D geometry, staged paths and contact/interference engine |
| T07 | Disabled | Approved IPR plan, enamel/contact assessment and stage timing |
| A01–04 | Disabled | Actual tooth/surface/stage attachment map, proposals, indications, removals and timing policy |
| R14 / A05–06 / H / L | Withholding and closed-output guards | Clinical/geometry conclusions remain unavailable; sign-off and privacy workflows only partial |
| N11 / N14 | Deferred | Authenticated immutable amendments, invalidation and incident/rollback workflows |

## Complete 96-rule feasibility matrix

| Rule | Corrected TMT class | Required fields | Implementation |
| --- | --- | --- | --- |
| A01 | No | orthodontist_approved_policy, actual_attachment_tooth_surface_stage_map, verified_tooth_and_stage_identity, intentional_removal_metadata | DISABLED / REQUIRED_DATA_GUARD |
| A02 | No | orthodontist_approved_policy, actual_attachment_tooth_surface_stage_map, verified_stage_and_movements, approved_attachment_indications | DISABLED / REQUIRED_DATA_GUARD |
| A03 | No | orthodontist_approved_policy, two_approved_attachment_proposals, approved_conflict_resolution_policy | DISABLED / REQUIRED_DATA_GUARD |
| A04 | No | orthodontist_approved_policy, actual_attachment_start_end_stages, verified_plan_mode_and_stage_conventions, approved_timing_policy | DISABLED / REQUIRED_DATA_GUARD |
| A05 | No | output_attachment_placement_claims | ACTIVE / OUTPUT_GUARD |
| A06 | System | output_attachment_superiority_claims | ACTIVE / OUTPUT_GUARD |
| D01 | Yes | authorized_semantic_measurement | ACTIVE / EXECUTABLE |
| D02 | Yes | authorized_semantic_measurement | ACTIVE / EXECUTABLE |
| D03 | Yes | authorized_semantic_measurement, verified_tooth_group_map | ACTIVE / REQUIRED_DATA_GUARD |
| D04 | Yes | authorized_semantic_measurement, verified_tooth_group_map | ACTIVE / REQUIRED_DATA_GUARD |
| D05 | Yes | authorized_semantic_measurement, verified_tooth_group_map | ACTIVE / REQUIRED_DATA_GUARD |
| D06 | Yes | authorized_semantic_measurement | ACTIVE / EXECUTABLE |
| D07 | Yes | authorized_semantic_measurement | ACTIVE / EXECUTABLE |
| D08 | Yes | authorized_semantic_measurement | ACTIVE / EXECUTABLE |
| D09 | Yes | authorized_semantic_measurement, verified_tooth_group_map | ACTIVE / REQUIRED_DATA_GUARD |
| D10 | Yes | authorized_semantic_measurement | ACTIVE / EXECUTABLE |
| D11 | Yes | authorized_semantic_measurement | ACTIVE / EXECUTABLE |
| D12 | Yes | authorized_semantic_measurement | ACTIVE / EXECUTABLE |
| D13 | Yes | authorized_semantic_measurement, verified_pair_map_and_mirror_operations | ACTIVE / REQUIRED_DATA_GUARD |
| D14 | System | requested_assessments, verified_clinical_context | ACTIVE / EXECUTABLE |
| D15 | Yes | authorized_semantic_measurement | ACTIVE / EXECUTABLE |
| D16 | Extra | verified_case_plan_identity, verified_baseline_geometry_and_operations, verified_coordinate_frame, approved_comparison_operation | DEFERRED / DEFERRED |
| G01 | Yes | lexical_structure | ACTIVE / EXECUTABLE |
| G02 | Metadata | source_application, source_version | ACTIVE / EXECUTABLE |
| G03 | Metadata | notation, dentition, arch | ACTIVE / EXECUTABLE |
| G04 | Yes | tooth_identifier, notation, dentition | ACTIVE / EXECUTABLE |
| G05 | Metadata | arch | ACTIVE / EXECUTABLE |
| G06 | Yes | duplicate_scope | ACTIVE / EXECUTABLE |
| G07 | Metadata | axis | ACTIVE / EXECUTABLE |
| G08 | Yes | numeric_value, unit | ACTIVE / EXECUTABLE |
| G09 | Metadata | sign, direction | ACTIVE / EXECUTABLE |
| G10 | Yes | numeric_value | ACTIVE / EXECUTABLE |
| G11 | Metadata | reference_basis | ACTIVE / EXECUTABLE |
| G12 | Metadata | scope, stage_index, stage_kind | ACTIVE / EXECUTABLE |
| G13 | Metadata | plan_mode | ACTIVE / EXECUTABLE |
| G14 | Extra | verified_external_tooth_status | ACTIVE / REQUIRED_DATA_GUARD |
| G15 | Extra | verified_stage_dataset | ACTIVE / REQUIRED_DATA_GUARD |
| G16 | System | source_provenance | ACTIVE / EXECUTABLE |
| G17 | System | field_semantic_eligibility | ACTIVE / EXECUTABLE |
| G18 | Metadata | verified_tooth_group_map | ACTIVE / REQUIRED_DATA_GUARD |
| H01 | Request | requested_suitability_assessment, clinical_examination | ACTIVE / EXECUTABLE |
| H02 | Request | requested_periodontal_assessment, periodontal_records | ACTIVE / EXECUTABLE |
| H03 | Request | requested_root_bone_assessment, root_bone_records | ACTIVE / EXECUTABLE |
| H04 | Request | requested_occlusion_assessment, occlusal_records | ACTIVE / EXECUTABLE |
| H05 | Request | requested_ipr_assessment, contact_enamel_and_ipr_plan | ACTIVE / EXECUTABLE |
| H06 | Request | requested_extraction_surgery_assessment, clinical_diagnosis | ACTIVE / EXECUTABLE |
| H07 | Request | requested_prognosis, validated_patient_specific_outcomes | ACTIVE / EXECUTABLE |
| H08 | Request | requested_attachment_assessment, actual_attachment_plan | ACTIVE / EXECUTABLE |
| H09 | Request | requested_collision_assessment, validated_staged_geometry | ACTIVE / EXECUTABLE |
| H10 | System | report_review_status | ACTIVE / PARTIAL_SYSTEM_CONTROL |
| H11 | Request | requested_intervention_assessment, verified_clinical_exclusions | ACTIVE / EXECUTABLE |
| H12 | System | synthetic_data_confirmed, separate_server_cloud_authorization | ACTIVE / PARTIAL_SYSTEM_CONTROL |
| L01 | System | structured_findings, closed_output_templates | ACTIVE / OUTPUT_GUARD |
| L02 | System | exact_observation_snapshot | ACTIVE / OUTPUT_GUARD |
| L03 | System | finding_input_refs, source_evidence_refs | ACTIVE / OUTPUT_GUARD |
| L04 | System | finding_propositions, conflict_keys | ACTIVE / OUTPUT_GUARD |
| L05 | System | field_scoped_verification_states | ACTIVE / OUTPUT_GUARD |
| L06 | System | report_review_status | ACTIVE / PARTIAL_SYSTEM_CONTROL |
| N01 | System | verified_expected_axis_coverage | ACTIVE / EXECUTABLE |
| N02 | System | released_source_version | ACTIVE / EXECUTABLE |
| N03 | System | single_capture_boundary | ACTIVE / PARTIAL_SYSTEM_CONTROL |
| N04 | System | raw_text, raw_sha256, source_spans | ACTIVE / PARTIAL_SYSTEM_CONTROL |
| N05 | System | verified_pair_map_and_mirror_operations | ACTIVE / EXECUTABLE |
| N06 | System | verified_external_tooth_status | ACTIVE / EXECUTABLE |
| N07 | System | verified_stage_dataset | ACTIVE / EXECUTABLE |
| N08 | System | verified_coordinate_frame_and_operations | ACTIVE / EXECUTABLE |
| N09 | System | field_verification_states | ACTIVE / EXECUTABLE |
| N10 | System | trusted_structured_context, untrusted_literal_text | ACTIVE / OUTPUT_GUARD |
| N11 | System | authenticated_reviewer_identity, immutable_versioned_review_events, approval_invalidation_workflow | DEFERRED / DEFERRED |
| N12 | System | verified_treatment_objectives, clinical_endpoint | ACTIVE / REQUIRED_DATA_GUARD |
| N13 | System | rule_specific_eligibility_contract | ACTIVE / EXECUTABLE |
| N14 | System | incident_severity_policy, approved_escalation_workflow, reviewed_rollback_release_process | DEFERRED / DEFERRED |
| R01 | Yes | orthodontist_approved_policy, verified_tooth_group, verified_rotation, source_specific_review_policy, approved_exceptions_and_intent | DISABLED / REQUIRED_DATA_GUARD |
| R02 | Yes | orthodontist_approved_policy, verified_tooth_group, verified_rotation, approved_movement_size_bands | DISABLED / REQUIRED_DATA_GUARD |
| R03 | Yes | orthodontist_approved_policy, verified_anterior_group, verified_extrusion, approved_extrusion_policy | DISABLED / REQUIRED_DATA_GUARD |
| R04 | Yes | orthodontist_approved_policy, verified_posterior_group, verified_extrusion, approved_device_specific_policy | DISABLED / REQUIRED_DATA_GUARD |
| R05 | Yes | orthodontist_approved_policy, verified_lower_incisor_identity, verified_intrusion, approved_intrusion_policy | DISABLED / REQUIRED_DATA_GUARD |
| R06 | Yes | orthodontist_approved_policy, verified_tooth_group, verified_intrusion, root_support_and_occlusal_objectives, approved_intrusion_policy | DISABLED / REQUIRED_DATA_GUARD |
| R07 | Partial | orthodontist_approved_policy, verified_incisor_identity, verified_inclination, root_position_and_geometry, approved_root_control_review_policy | DISABLED / REQUIRED_DATA_GUARD |
| R08 | Yes | orthodontist_approved_policy, verified_angulation, verified_tooth_group, approved_angulation_review_policy | DISABLED / REQUIRED_DATA_GUARD |
| R09 | Yes | orthodontist_approved_policy, verified_posterior_group, verified_buccolingual_movement, bone_and_root_assessment, approved_transverse_review_policy | DISABLED / REQUIRED_DATA_GUARD |
| R10 | Yes | orthodontist_approved_policy, verified_upper_molar_identity, verified_distal_direction, staged_anchorage_context, approved_distalization_policy | DISABLED / REQUIRED_DATA_GUARD |
| R11 | Yes | orthodontist_approved_policy, verified_molar_identity, verified_mesial_direction, extraction_space_and_root_context, approved_mesialization_policy | DISABLED / REQUIRED_DATA_GUARD |
| R12 | Partial | orthodontist_approved_policy, verified_combination_axes, verified_directions_and_groups, approved_validated_interaction_matrix | DISABLED / REQUIRED_DATA_GUARD |
| R13 | No | orthodontist_approved_policy, actual_stage_dataset, verified_device_version_profile, approved_stage_policy | DISABLED / REQUIRED_DATA_GUARD |
| R14 | System | requested_assessment_context | ACTIVE / EXECUTABLE |
| R15 | Partial | orthodontist_approved_policy, verified_movement_group, actual_attachment_plan, approved_open_ended_review_policy | DISABLED / REQUIRED_DATA_GUARD |
| R16 | No | orthodontist_approved_policy, full_clinical_examination, occlusion_and_skeletal_periodontal_context, treatment_objectives, approved_full_case_rubric | DISABLED / REQUIRED_DATA_GUARD |
| T01 | No | orthodontist_approved_policy, actual_per_stage_values, verified_device_profile, orthodontist_approved_stage_limits | DISABLED / REQUIRED_DATA_GUARD |
| T02 | No | orthodontist_approved_policy, actual_stage_dataset, verified_baseline_geometry, verified_coordinate_transforms, approved_composition_operations_and_tolerance | DISABLED / REQUIRED_DATA_GUARD |
| T03 | No | orthodontist_approved_policy, actual_per_stage_values, verified_configured_constraint, configuration_history, approved_stage_policy | DISABLED / REQUIRED_DATA_GUARD |
| T04 | No | orthodontist_approved_policy, actual_stage_dataset, verified_intended_distalization_sequence, approved_anchorage_protocol | DISABLED / REQUIRED_DATA_GUARD |
| T05 | No | orthodontist_approved_policy, actual_stage_overlap, device_specific_validated_interaction_matrix, approved_interaction_policy | DISABLED / REQUIRED_DATA_GUARD |
| T06 | No | orthodontist_approved_policy, validated_3d_geometry, verified_alignment_and_staged_paths, validated_contact_engine | DISABLED / REQUIRED_DATA_GUARD |
| T07 | No | orthodontist_approved_policy, approved_ipr_plan, enamel_and_interproximal_contacts, stage_timing, clinical_review | DISABLED / REQUIRED_DATA_GUARD |
| T08 | No | orthodontist_approved_policy, staged_force_and_anchorage_strategy, crown_root_coordinates, approved_protocol | DISABLED / REQUIRED_DATA_GUARD |


The public API has no extra clinical-data contract or TEST_ONLY evidence authorization fields. AdditionalInputRequirements is a future integration checklist; TestRuleContext is private illustrative library evidence only. N01 expected coverage remains null in the legacy summary; explicit TEST_ONLY expected coverage is recorded in N01 findings, never synthesized into missing values.