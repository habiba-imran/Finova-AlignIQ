# Complete Phase 5 rule inventory

96 IDs, version 2.0.0. The audit and corrected v2 govern. The standalone original 82-rule research file is unavailable; only the corrected document’s original-proposal trace paragraphs are available. They are historical trace, never active policies. Source hashes and exact extracted text are recorded in `backend/app/review/catalog.json`.

ACTIVE means an engineering handler can run, including a required-data check or withholding control. It never means clinically approved. All 27 clinical predicates remain DISABLED. Three controls are DEFERRED. Additional group/pair/stage/status evidence currently has only a bound, private TEST_ONLY path; there is no production clinical-data intake.

Field-level missing evidence is not a negative result. Legacy `evaluated` remains true only for OBSERVED records; NOT_APPLICABLE has `predicate_result=false`, while withheld/disabled/suppressed has null. A mixed ledger status reports the limiting state; inspect linked findings for unaffected positive descriptions.

## A01 v2.0.0 — Attachment presence audit

1. **ID/version:** A01 / 2.0.0.
2. **Purpose (corrected):** Attachment presence cannot be audited from ordinary total TMT. Need independently imported attachment-tooth-and-stage map and handle intentional removal, lingual surfaces and multiple attachments.
3. **Source/evidence:** [Attachment presence audit](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 730); S05. Audit assessment: Attachment presence cannot be audited from ordinary total TMT. Need independently imported attachment-tooth-and-stage map and handle intentional removal, lingual surfaces and multiple attachments.
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, actual_attachment_tooth_surface_stage_map, verified_tooth_and_stage_identity, intentional_removal_metadata.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: actual_attachment_tooth_surface_stage_map, verified_tooth_and_stage_identity, intentional_removal_metadata. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 70. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: actual_attachment_tooth_surface_stage_map, verified_tooth_and_stage_identity, intentional_removal_metadata. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `a01_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, actual_attachment_tooth_surface_stage_map, verified_tooth_and_stage_identity, intentional_removal_metadata.

## A02 v2.0.0 — Attachment-to-movement review

1. **ID/version:** A02 / 2.0.0.
2. **Purpose (corrected):** Clinician-approved indications plus actual attachment presence and stage are required to assert omission. Literature on attachment performance is heterogeneous; do not promote a movement amount into a mandatory attachment rule.
3. **Source/evidence:** [Attachment-to-movement review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 740); S05, S07, S13. Audit assessment: Clinician-approved indications plus actual attachment presence and stage are required to assert omission. Literature on attachment performance is heterogeneous; do not promote a movement amount into a mandatoryattachment rule. l
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, actual_attachment_tooth_surface_stage_map, verified_stage_and_movements, approved_attachment_indications.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: actual_attachment_tooth_surface_stage_map, verified_stage_and_movements, approved_attachment_indications. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 70. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: actual_attachment_tooth_surface_stage_map, verified_stage_and_movements, approved_attachment_indications. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `a02_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, actual_attachment_tooth_surface_stage_map, verified_stage_and_movements, approved_attachment_indications.

## A03 v2.0.0 — Conflicting attachment preferences

1. **ID/version:** A03 / 2.0.0.
2. **Purpose (corrected):** Conflict-resolution is an engine policy and only meaningful when two approved attachment proposals exist. Do not select an attachment automatically based on arbitrary priority.
3. **Source/evidence:** [Conflicting attachment preferences](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 750); S03, S05. Audit assessment: Conflict-resolution is an engine policy and only meaningful when two approved attachment proposals exist. Do not select an attachment automaticallybased on arbitrary priority.
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, two_approved_attachment_proposals, approved_conflict_resolution_policy.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: two_approved_attachment_proposals, approved_conflict_resolution_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 70. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: two_approved_attachment_proposals, approved_conflict_resolution_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `a03_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, two_approved_attachment_proposals, approved_conflict_resolution_policy.

## A04 v2.0.0 — Attachment stage scheduling

1. **ID/version:** A04 / 2.0.0.
2. **Purpose (corrected):** Attachment timing demands start/end stage data, plan mode and stage conventions. Not part of a total TMT.
3. **Source/evidence:** [Attachment stage scheduling](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 764); S05, S07. Audit assessment: Attachment timing demands start/end stage data, plan mode and stage conventions. Not part of a total TMT.
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, actual_attachment_start_end_stages, verified_plan_mode_and_stage_conventions, approved_timing_policy.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: actual_attachment_start_end_stages, verified_plan_mode_and_stage_conventions, approved_timing_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 70. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: actual_attachment_start_end_stages, verified_plan_mode_and_stage_conventions, approved_timing_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `a04_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, actual_attachment_start_end_stages, verified_plan_mode_and_stage_conventions, approved_timing_policy.

## A05 v2.0.0 — Attachment geometry placement guard

1. **ID/version:** A05 / 2.0.0.
2. **Purpose (corrected):** Correct prohibition on numerical geometry placement from a TMT. Even with meshes, clinical/geometry validation is necessary; make the withholding guard globally active rather than waiting for geometry input.
3. **Source/evidence:** [Attachment geometry placement guard](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 774); S05, S13. Audit assessment: Correct prohibition on numerical geometry placement from a TMT. Even with meshes, clinical/geometry validation is necessary; make the withholding guard globally active rather than waitingforgeometryinput.
4. **Audit disposition:** MORE DATA.
5. **Required fields:** output_attachment_placement_claims.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Globally withhold exact placement. Geometry-based placement evaluation is not implemented. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 70. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Globally withhold exact placement. Geometry-based placement evaluation is not implemented.
10. **Implementation:** ACTIVE / OUTPUT_GUARD; handler identity `a05_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## A06 v2.0.0 — Conventional vs optimized comparison

1. **ID/version:** A06 / 2.0.0.
2. **Purpose (corrected):** A universal-superiority claim should be blocked immediately as an output safeguard, not treated as an automatic attachment selection candidate. S14 finds no significant overall superiority; note subgroup uncertainty.
3. **Source/evidence:** [Conventional vs optimized comparison](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 786); S13, S14. Audit assessment: A universal-superiority claim should be blocked immediately as an output safeguard, not treated as an automatic attachment selection candidate. S14 finds no significant overall superiority; note subgroupuncertainty.
4. **Audit disposition:** READY.
5. **Required fields:** output_attachment_superiority_claims.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Block universal attachment-superiority wording; no attachment choice is recommended. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 70. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Block universal attachment-superiority wording; no attachment choice is recommended.
10. **Implementation:** ACTIVE / OUTPUT_GUARD; handler identity `a06_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## D01 v2.0.0 — Movement inventory per tooth

1. **ID/version:** D01 / 2.0.0.
2. **Purpose (corrected):** Accurate if strictly a report of programmed, not achieved, movements with original basis, scope, plan mode and direction. Report omitted/missing dimensions separately.
3. **Source/evidence:** [Movement inventory per tooth](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 306); S01, S04. Audit assessment: Accurate if strictly a report of programmed, not achieved, movements with original basis, scope, plan mode and direction. Report omitted/missingdimensions separately.
4. **Audit disposition:** READY.
5. **Required fields:** authorized_semantic_measurement.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. List authorized nonzero programmed values without risk, threshold or achieved-movement claims. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** G01, G16, G17 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** List authorized nonzero programmed values without risk, threshold or achieved-movement claims.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `d01_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## D02 v2.0.0 — Multiple concurrent movement types

1. **ID/version:** D02 / 2.0.0.
2. **Purpose (corrected):** Rename to co-programmed movement axes, not concurrent movement. Total TMT does not show temporal overlap; simultaneity is a staging question.
3. **Source/evidence:** [Multiple concurrent movement types](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 316); S03, S13. Audit assessment: Rename to co-programmed movement axes, not concurrent movement. Total TMT does not show temporal overlap;simultaneityis a staging question. i
4. **Audit disposition:** REVISE.
5. **Required fields:** authorized_semantic_measurement.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Co-programmed nonzero axes only in an identical tooth/source/mode/basis/TOTAL/frame context; never temporal concurrency. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Co-programmed nonzero axes only in an identical tooth/source/mode/basis/TOTAL/frame context; never temporal concurrency.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `d02_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## D03 v2.0.0 — Rotation by tooth group

1. **ID/version:** D03 / 2.0.0.
2. **Purpose (corrected):** Safe tooth-group description, subject to verified numbering and rotation sign mapping. No inference that canine/premolar rotation will fail.
3. **Source/evidence:** [Rotation by tooth group](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 326); S09, S10. Audit assessment: Safe tooth-group description, subject to verified numbering and rotation sign mapping. No inference that canine/premolar rotation will fail.
4. **Audit disposition:** READY.
5. **Required fields:** authorized_semantic_measurement, verified_tooth_group_map.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Describe nonzero rotation only with explicit recognized tooth-group evidence. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01, G18 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Describe nonzero rotation only with explicit recognized tooth-group evidence.
10. **Implementation:** ACTIVE / REQUIRED_DATA_GUARD; handler identity `d03_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.

## D04 v2.0.0 — Extrusion by tooth group

1. **ID/version:** D04 / 2.0.0.
2. **Purpose (corrected):** Safe description of programmed extrusion; anterior/posterior grouping must rely on tooth map, and no clinical interpretation should follow automatically.
3. **Source/evidence:** [Extrusion by tooth group](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 336); S09, S13. Audit assessment: Safe description of programmed extrusion; anterior/posterior grouping must rely on tooth map, and no clinical interpretation should follow automatically.
4. **Audit disposition:** READY.
5. **Required fields:** authorized_semantic_measurement, verified_tooth_group_map.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Describe nonzero extrusion only with explicit tooth group and canonical EXTRUSION direction. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01, G18 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Describe nonzero extrusion only with explicit tooth group and canonical EXTRUSION direction.
10. **Implementation:** ACTIVE / REQUIRED_DATA_GUARD; handler identity `d04_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.

## D05 v2.0.0 — Intrusion by tooth group

1. **ID/version:** D05 / 2.0.0.
2. **Purpose (corrected):** Safe description of programmed intrusion. Highlighting mandibular incisors is a navigation preference, not evidence of danger.
3. **Source/evidence:** [Intrusion by tooth group](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 346); S09, S11. Audit assessment: Safe description of programmed intrusion. Highlighting mandibular incisors is a navigation preference,not evidence of danger. i
4. **Audit disposition:** READY.
5. **Required fields:** authorized_semantic_measurement, verified_tooth_group_map.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Describe nonzero intrusion only with explicit tooth group and canonical INTRUSION direction. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01, G18 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Describe nonzero intrusion only with explicit tooth group and canonical INTRUSION direction.
10. **Implementation:** ACTIVE / REQUIRED_DATA_GUARD; handler identity `d05_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.

## D06 v2.0.0 — Crown inclination/angulation inventory

1. **ID/version:** D06 / 2.0.0.
2. **Purpose (corrected):** Keep source-specific terms inclination and angulation. ClinCheck angular values are not changed by crown/root basis selection; neither alone specifies achieved root movement or torque control.
3. **Source/evidence:** [Crown inclination/angulation inventory](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 356); S01, S08. Audit assessment: Keep source-specific terms inclination and angulation. ClinCheck angular values are not changed by crown/root basis selection;neither alone specifies achieved root movement or torque control.
4. **Audit disposition:** READY.
5. **Required fields:** authorized_semantic_measurement.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Describe verified inclination/angulation values without inferring torque/root movement. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Describe verified inclination/angulation values without inferring torque/root movement.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `d06_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## D07 v2.0.0 — Buccolingual translation inventory

1. **ID/version:** D07 / 2.0.0.
2. **Purpose (corrected):** Descriptive buccolingual displacement only. Neither skeletal/dental expansion nor bodily translation can be established from one-axis crown movement.
3. **Source/evidence:** [Buccolingual translation inventory](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 370); S01, S08. Audit assessment: Descriptive buccolingual displacement only. Neither skeletal/dental expansion nor bodily translation can be established from one-axis crown movement.
4. **Audit disposition:** READY.
5. **Required fields:** authorized_semantic_measurement.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Describe verified buccolingual displacement without inferring expansion safety or bone housing. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Describe verified buccolingual displacement without inferring expansion safety or bone housing.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `d07_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## D08 v2.0.0 — Mesiodistal translation inventory

1. **ID/version:** D08 / 2.0.0.
2. **Purpose (corrected):** Descriptive mesiodistal displacement only. Do not infer space closure, anchorage loss, root movement or treatment speed.
3. **Source/evidence:** [Mesiodistal translation inventory](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 380); S04, S12. Audit assessment: Descriptive mesiodistal displacement only. Do not infer space closure, anchorage loss, root movement or treatment speed. i
4. **Audit disposition:** READY.
5. **Required fields:** authorized_semantic_measurement.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Describe verified mesiodistal displacement without inferring bodily/root movement. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Describe verified mesiodistal displacement without inferring bodily/root movement.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `d08_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## D09 v2.0.0 — Molar distalization or mesialization indicator

1. **ID/version:** D09 / 2.0.0.
2. **Purpose (corrected):** Valid molar movement label if mesial/distal convention is confirmed for that arch. Not a proof of sequential distalization or Class II correction.
3. **Source/evidence:** [Molar distalization or mesialization indicator](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 390); S12. Audit assessment: Valid molar movement label if mesial/distal convention is confirmed for that arch. Not a proof of sequential distalization or Class II correction.
4. **Audit disposition:** READY.
5. **Required fields:** authorized_semantic_measurement, verified_tooth_group_map.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Describe mesial/distal molar movement only with independently supplied MOLAR group and verified direction. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01, G18 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Describe mesial/distal molar movement only with independently supplied MOLAR group and verified direction.
10. **Implementation:** ACTIVE / REQUIRED_DATA_GUARD; handler identity `d09_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.

## D10 v2.0.0 — Combined rotation and vertical movement

1. **ID/version:** D10 / 2.0.0.
2. **Purpose (corrected):** Same-tooth rotation and vertical movement can co-exist in a total plan, but cannot be called temporally combined without stage values. Pure fact only; arguably redundant with D02.
3. **Source/evidence:** [Combined rotation and vertical movement](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 400); S10, S13. Audit assessment: Same-tooth rotation and vertical movement can co-exist in a total plan, but cannot be called temporallycombined without stage values. Pure fact only;arguablyredundant with D02.
4. **Audit disposition:** REVISE.
5. **Required fields:** authorized_semantic_measurement.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Use corrected TOTAL co-programming logic, deduplicated with D02; no temporal overlap inference. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Use corrected TOTAL co-programming logic, deduplicated with D02; no temporal overlap inference.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `d10_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## D11 v2.0.0 — Combined angular and translational movement

1. **ID/version:** D11 / 2.0.0.
2. **Purpose (corrected):** The same total-vs-staged problem. Avoid implying bodily motion, root control or force-system interaction. Merge into a generic co-programming observation.
3. **Source/evidence:** [Combined angular and translational movement](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 410); S08, S13. Audit assessment: The same total-vs-staged problem. Avoid implying bodily motion, root control or force-system interaction. Merge into ageneric co-programmingobservation. i
4. **Audit disposition:** REVISE.
5. **Required fields:** authorized_semantic_measurement.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Use corrected TOTAL angular/translational co-programming logic; no bodily/root-control conclusion. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Use corrected TOTAL angular/translational co-programming logic; no bodily/root-control conclusion.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `d11_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## D12 v2.0.0 — Movement distribution summary

1. **ID/version:** D12 / 2.0.0.
2. **Purpose (corrected):** Count verified nonzero axes/tooth groups/arches with separate data-coverage denominators. Never sum degrees with millimeters or present case difficulty from counts.
3. **Source/evidence:** [Movement distribution summary](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 420); S01, S04. Audit assessment: Count verified nonzero axes/tooth groups/arches with separate data-coverage denominators. Never sum degrees with millimeters orpresent case difficultyfrom counts.
4. **Audit disposition:** READY.
5. **Required fields:** authorized_semantic_measurement.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Count observed nonzero positions, axes, teeth and arches within compatible context; not case difficulty. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Count observed nonzero positions, axes, teeth and arches within compatible context; not case difficulty.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `d12_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## D13 v2.0.0 — Opposite-side comparison (descriptive only)

1. **ID/version:** D13 / 2.0.0.
2. **Purpose (corrected):** Numerically compare paired anatomic teeth only within equivalent plan, basis and axis. Mirrored left/right signs require explicit convention; difference does not imply pathologic asymmetry.
3. **Source/evidence:** [Opposite-side comparison (descriptive only)](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 430); S01, S04. Audit assessment: Numerically compare paired anatomic teeth only within equivalent plan, basis and axis. Mirrored left/right signs require explicit convention;difference does not imply pathologic asymmetry.
4. **Audit disposition:** READY.
5. **Required fields:** authorized_semantic_measurement, verified_pair_map_and_mirror_operations.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Compare two explicit paired magnitudes only after independent mirror/equivalence proof and identical source/mode/basis/scope/frame/unit. Preserve both exact values; no subtraction or pathologic-asymmetry inference. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01, N05 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Compare two explicit paired magnitudes only after independent mirror/equivalence proof and identical source/mode/basis/scope/frame/unit. Preserve both exact values; no subtraction or pathologic-asymmetry inference.
10. **Implementation:** ACTIVE / REQUIRED_DATA_GUARD; handler identity `d13_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.

## D14 v2.0.0 — Missing key clinical context inventory

1. **ID/version:** D14 / 2.0.0.
2. **Purpose (corrected):** Useful data-availability report, but missing-context entries should be derived from requested decisions, not a generic exhaustive list on every paste.
3. **Source/evidence:** [Missing key clinical context inventory](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 444); S15, S17, S18. Audit assessment: Useful data-availability report, but missing-context entries should be derived from requested decisions,not ageneric exhaustive list on every paste.
4. **Audit disposition:** READY.
5. **Required fields:** requested_assessments, verified_clinical_context.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Requested clinical assessments yield missing-context records; no unsolicited clinical inventory. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 30. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Requested clinical assessments yield missing-context records; no unsolicited clinical inventory.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `d14_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## D15 v2.0.0 — Single tooth zero movement

1. **ID/version:** D15 / 2.0.0.
2. **Purpose (corrected):** Use wording 'all supported, observed axes are zero'; missing/unsupported axes and absent teeth prevent a categorical 'no movement' conclusion.
3. **Source/evidence:** [Single tooth zero movement](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 454); S01, S04. Audit assessment: Use wording 'all supported, observed axes are zero'; missing/unsupported axes and absent teeth prevent a categorical 'no movement' conclusion.
4. **Audit disposition:** READY.
5. **Required fields:** authorized_semantic_measurement.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Describe explicit zeros only for supported observed axes with no unresolved sibling; unlisted axes remain unknown. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** D01 / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Describe explicit zeros only for supported observed axes with no unresolved sibling; unlisted axes remain unknown.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `d15_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## D16 v2.0.0 — Historical plan difference

1. **ID/version:** D16 / 2.0.0.
2. **Purpose (corrected):** Two plans need same patient, tooth, starting geometry/reference, compatible coordinates, stage and movement semantics. Equal basis alone does not make two rotations/paths subtractable; compute scalar deltas only where justified.
3. **Source/evidence:** [Historical plan difference](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 464); S01, S04. Audit assessment: Two plans need same patient, tooth, starting geometry/reference, compatible coordinates, stage and movement semantics. Equal basis alone does not make two rotations/paths subtractable; compute scalar deltas onlywherejustified.
4. **Audit disposition:** REVISE.
5. **Required fields:** verified_case_plan_identity, verified_baseline_geometry_and_operations, verified_coordinate_frame, approved_comparison_operation.
6. **TMT-only feasibility (governing classification):** Extra. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Withhold historical-plan calculation: no trusted same-case/plan binding, common baseline geometry or validated comparison operations. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 40. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Withhold historical-plan calculation: no trusted same-case/plan binding, common baseline geometry or validated comparison operations.
10. **Implementation:** DEFERRED / DEFERRED; handler identity `d16_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** ADDITIONAL_VERIFIED_MAP_OR_GEOMETRY_REQUIRED: verified_case_plan_identity, verified_baseline_geometry_and_operations, verified_coordinate_frame, approved_comparison_operation.

## G01 v2.0.0 — Non-empty structured input

1. **ID/version:** G01 / 2.0.0.
2. **Purpose (corrected):** Sound structural gate. Define recognizable headers, minimum row/column cardinality, encoding and payload limits; an empty but valid zero-movement table must not be rejected merely for lacking nonzero values.
3. **Source/evidence:** [Non-empty structured input](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 108); S01, S04. Audit assessment: Sound structural gate. Define recognizable headers, minimum row/column cardinality, encoding and payload limits; an empty but valid zero-movement table must not be rejected merely for lacking nonzero values.
4. **Audit disposition:** READY.
5. **Required fields:** lexical_structure.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Reject unsupported/invalid structure or global provenance failure before movement evaluation. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 10. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Reject unsupported/invalid structure or global provenance failure before movement evaluation.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g01_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G02 v2.0.0 — Reliable source identity

1. **ID/version:** G02 / 2.0.0.
2. **Purpose (corrected):** Necessary but a pasted table may not identify its source; user-selected source is a claim, not verification. Confirm against signatures and make unmatched versions UNVERIFIED, not ClinCheck by default.
3. **Source/evidence:** [Reliable source identity](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 122); S01, S04. Audit assessment: Necessary but a pasted table may not identify its source; user-selected source is a claim, not verification. Confirm against signatures and make unmatched versions UNVERIFIED, not ClinCheck bydefault.
4. **Audit disposition:** READY.
5. **Required fields:** source_application, source_version.
6. **TMT-only feasibility (governing classification):** Metadata. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Use existing exact lexical/field-semantic states for source_application, source_version; unavailable fields abstain without vendor inference. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Use existing exact lexical/field-semantic states for source_application, source_version; unavailable fields abstain without vendor inference.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g02_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G03 v2.0.0 — Tooth numbering convention

1. **ID/version:** G03 / 2.0.0.
2. **Purpose (corrected):** Critical. ClinCheck permits Universal, Palmer and FDI numbering; numeric 13 is ambiguous across systems. Require verified notation, plus arch context and a normalization lookup with exhaustive examples.
3. **Source/evidence:** [Tooth numbering convention](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 132); S01, S04. Audit assessment: Critical. ClinCheck permits Universal, Palmer and FDI numbering; numeric 13 is ambiguous across systems. Require verified notation, plus arch context and a normalization lookup with exhaustive examples.
4. **Audit disposition:** READY.
5. **Required fields:** notation, dentition, arch.
6. **TMT-only feasibility (governing classification):** Metadata. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Use existing exact lexical/field-semantic states for notation, dentition, arch; unavailable fields abstain without vendor inference. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Use existing exact lexical/field-semantic states for notation, dentition, arch; unavailable fields abstain without vendor inference.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g03_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G04 v2.0.0 — Tooth ID validity

1. **ID/version:** G04 / 2.0.0.
2. **Purpose (corrected):** Sound technical validation only after notation and dentition are known. Support optional third molars, deciduous teeth, pontics and explicit unsupported identifiers; do not treat an absent row as an invalid tooth.
3. **Source/evidence:** [Tooth ID validity](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 142); S01, S04. Audit assessment: Sound technical validation only after notation and dentition are known. Support optional third molars, deciduous teeth, pontics and explicit unsupported identifiers; do not treat an absent row as an invalid tooth.
4. **Audit disposition:** READY.
5. **Required fields:** tooth_identifier, notation, dentition.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Use existing exact lexical/field-semantic states for tooth_identifier, notation, dentition; unavailable fields abstain without vendor inference. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Use existing exact lexical/field-semantic states for tooth_identifier, notation, dentition; unavailable fields abstain without vendor inference.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g04_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G05 v2.0.0 — Arch association

1. **ID/version:** G05 / 2.0.0.
2. **Purpose (corrected):** Useful if the source actually provides an independent arch marker. A mismatch should quarantine an affected record rather than reinterpret its quadrant automatically.
3. **Source/evidence:** [Arch association](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 152); S01, S04. Audit assessment: Useful if the source actually provides an independent arch marker. A mismatch should quarantine an affected record rather than reinterpret itsquadrant automatically.
4. **Audit disposition:** READY.
5. **Required fields:** arch.
6. **TMT-only feasibility (governing classification):** Metadata. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Use existing exact lexical/field-semantic states for arch; unavailable fields abstain without vendor inference. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Use existing exact lexical/field-semantic states for arch; unavailable fields abstain without vendor inference.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g05_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G06 v2.0.0 — Duplicate tooth records

1. **ID/version:** G06 / 2.0.0.
2. **Purpose (corrected):** Detect duplicate (case, plan, basis, scope, stage, tooth, axis) keys, not just repeated tooth numbers. Repeated columns may be legitimate plan comparisons and must not be combined.
3. **Source/evidence:** [Duplicate tooth records](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 162); S01, S04. Audit assessment: f Detect duplicate (case, plan, basis, scope, stage, tooth, axis) keys, not just repeated tooth numbers. Repeated columns maybe legitimateplan comparisons and must not be combined.
4. **Audit disposition:** READY.
5. **Required fields:** duplicate_scope.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Keep duplicate positions unresolved; the semantic field gate excludes ambiguous source associations. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Keep duplicate positions unresolved; the semantic field gate excludes ambiguous source associations.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g06_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G07 v2.0.0 — Canonical movement label mapping

1. **ID/version:** G07 / 2.0.0.
2. **Purpose (corrected):** Essential. Make an explicit adapter-specific dictionary for extrusion/intrusion, B/L, M/D, rotation, angulation and inclination. Preserve source name and axis; no generic cross-vendor conversion by label similarity alone.
3. **Source/evidence:** [Canonical movement label mapping](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 172); S01, S04. Audit assessment: Essential. Make an explicit adapter-specific dictionary for extrusion/intrusion, B/L, M/D, rotation, angulation and inclination. Preserve source name and axis; no generic cross-vendor conversion by label similarityalone.
4. **Audit disposition:** READY.
5. **Required fields:** axis.
6. **TMT-only feasibility (governing classification):** Metadata. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Use existing exact lexical/field-semantic states for axis; unavailable fields abstain without vendor inference. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Use existing exact lexical/field-semantic states for axis; unavailable fields abstain without vendor inference.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g07_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G08 v2.0.0 — Numeric, unit and precision integrity

1. **ID/version:** G08 / 2.0.0.
2. **Purpose (corrected):** Correct engineering principle; specify decimal comma, unicode minus, empty cell, whitespace, thousands separators, exponent notation, NaN/Infinity and unexpected degree signs. Units may be implicit in a verified row header; lack of per-cell unit is not always an error.
3. **Source/evidence:** [Numeric, unit and precision integrity](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 186); S01, S04. Audit assessment: Correct engineering principle; specify decimal comma, unicode minus, empty cell, whitespace, thousands separators, exponent notation, NaN/Infinity and unexpected degree signs. Units may be implicit in a verified row header;lack ofper-cell unit is not always an error.
4. **Audit disposition:** READY.
5. **Required fields:** numeric_value, unit.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Require parsed/exact-zero numeric state and a recognized lexical unit; no coercion or rounding. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Require parsed/exact-zero numeric state and a recognized lexical unit; no coercion or rounding.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g08_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G09 v2.0.0 — Directional meaning verified

1. **ID/version:** G09 / 2.0.0.
2. **Purpose (corrected):** Top priority: validate letters and sign convention for each MOVEMENT axis, arch, tooth, platform and version. Direction labels for ClinCheck refer to the crown even in root basis; do not translate B inclination to lingual root torque without validated semantics.
3. **Source/evidence:** [Directional meaning verified](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 196); S01, S04. Audit assessment: i Top priority: validate letters and sign convention for each MOVEMENT axis, arch, tooth, platform and version. Direction labels for ClinCheck refer to the crown even in root basis; do not translate B inclination to lingual root torque without validated semantics.
4. **Audit disposition:** READY.
5. **Required fields:** sign, direction.
6. **TMT-only feasibility (governing classification):** Metadata. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Use existing exact lexical/field-semantic states for sign, direction; unavailable fields abstain without vendor inference. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Use existing exact lexical/field-semantic states for sign, direction; unavailable fields abstain without vendor inference.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g09_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G10 v2.0.0 — Missing versus zero

1. **ID/version:** G10 / 2.0.0.
2. **Purpose (corrected):** Essential: distinguish explicit 0, blank, dash, excluded/absent tooth, and an unsupported movement field. Introduce an observed/expected axis coverage mask; nonlisted axes cannot be assumed zero.
3. **Source/evidence:** [Missing versus zero](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 206); S01, S04. Audit assessment: Essential: distinguish explicit 0, blank, dash, excluded/absent tooth, and an unsupported movement field. Introduce an observed/expected axis coverage mask;nonlisted axes cannot be assumed zero.
4. **Audit disposition:** READY.
5. **Required fields:** numeric_value.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Distinguish numeric zero from missing/invalid source cells; never fill missing data. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Distinguish numeric zero from missing/invalid source cells; never fill missing data.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g10_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G11 v2.0.0 — Reference basis: crown/root/cusp

1. **ID/version:** G11 / 2.0.0.
2. **Purpose (corrected):** Verified ClinCheck crown-center vs virtual-root-apex affects linear, not angular values. SureSmile crown center vs cusp tip is also distinct. Require basis metadata and disallow cross-basis arithmetic/comparisons.
3. **Source/evidence:** [Reference basis: crown/root/cusp](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 216); S01, S04. Audit assessment: i Verified ClinCheck crown-center vs virtual-root-apex affects linear, not angular values. SureSmile crown center vs cusp tip is also distinct. Require basis metadata and disallow cross-basis arithmetic/comparisons.
4. **Audit disposition:** READY.
5. **Required fields:** reference_basis.
6. **TMT-only feasibility (governing classification):** Metadata. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Use existing exact lexical/field-semantic states for reference_basis; unavailable fields abstain without vendor inference. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Use existing exact lexical/field-semantic states for reference_basis; unavailable fields abstain without vendor inference.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g11_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G12 v2.0.0 — Total versus stage mode

1. **ID/version:** G12 / 2.0.0.
2. **Purpose (corrected):** Verified SureSmile incremental/cumulative/total distinction. Total ClinCheck and last cumulative SureSmile stage are not automatically equivalent without same start/end, coordinate frame and content. No stage limits on a total-only paste.
3. **Source/evidence:** [Total versus stage mode](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 226); S01, S04. Audit assessment: Verified SureSmile incremental/cumulative/total distinction. Total ClinCheck and last cumulative SureSmile stage are not automatically equivalent without same start/end, coordinate frame and content. No stage limits on a total-only paste.
4. **Audit disposition:** READY.
5. **Required fields:** scope, stage_index, stage_kind.
6. **TMT-only feasibility (governing classification):** Metadata. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Use existing exact lexical/field-semantic states for scope, stage_index, stage_kind; unavailable fields abstain without vendor inference. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Use existing exact lexical/field-semantic states for scope, stage_index, stage_kind; unavailable fields abstain without vendor inference.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g12_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G13 v2.0.0 — Plan/comparison mode

1. **ID/version:** G13 / 2.0.0.
2. **Purpose (corrected):** Verified Align final, Doctor final and Comparison/difference distinction; a difference row is never the absolute programmed plan. Store plan ID and comparison operands; hold clinical rules if mode unconfirmed.
3. **Source/evidence:** [Plan/comparison mode](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 240); S01. Audit assessment: Verified Align final, Doctor final and Comparison/difference distinction; a difference row is never the absolute programmed plan. Store plan ID and comparison operands; hold clinical rules if mode unconfirmed.
4. **Audit disposition:** READY.
5. **Required fields:** plan_mode.
6. **TMT-only feasibility (governing classification):** Metadata. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Use existing exact lexical/field-semantic states for plan_mode; unavailable fields abstain without vendor inference. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Use existing exact lexical/field-semantic states for plan_mode; unavailable fields abstain without vendor inference.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g13_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G14 v2.0.0 — Absent/unmovable teeth

1. **ID/version:** G14 / 2.0.0.
2. **Purpose (corrected):** The TMT alone cannot confirm that a tooth is absent, excluded, fixed or truly unmovable. A dash, pontic or absent column is insufficient. Only check contradictions against independently supplied verified presence/exclusion metadata.
3. **Source/evidence:** [Absent/unmovable teeth](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 250); S03, S04. Audit assessment: i The TMT alone cannot confirm that a tooth is absent, excluded, fixed or truly unmovable. A dash, pontic or absent column is insufficient. Only check contradictions against independently supplied verifiedpresence/exclusion metadata.
4. **Audit disposition:** REVISE.
5. **Required fields:** verified_external_tooth_status.
6. **TMT-only feasibility (governing classification):** Extra. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Require independently supplied movement permission; nonzero/forbidden contradictions block only that field. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Require independently supplied movement permission; nonzero/forbidden contradictions block only that field.
10. **Implementation:** ACTIVE / REQUIRED_DATA_GUARD; handler identity `g14_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.

## G15 v2.0.0 — Stage ordering and identifiers

1. **ID/version:** G15 / 2.0.0.
2. **Purpose (corrected):** Sound only for actual stage datasets. Define indexed stages, stage zero, optional accommodation/overcorrection/passive stages, skipped stages, arch alignment, and duplicate handling; don't impose staged checks on total-only data.
3. **Source/evidence:** [Stage ordering and identifiers](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 258); S04. Audit assessment: i Sound only for actual stage datasets. Define indexed stages, stage zero, optional accommodation/overcorrection/passive stages, skipped stages, arch alignment, and duplicate handling;don't impose staged checks on total-onlydata.
4. **Audit disposition:** READY.
5. **Required fields:** verified_stage_dataset.
6. **TMT-only feasibility (governing classification):** Extra. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Actual stage records only: detect duplicate IDs/indices, order and unresolved stage-zero kind. Gaps or absent stage zero do not imply missing data. Total-only capture without stages is NOT_APPLICABLE. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Actual stage records only: detect duplicate IDs/indices, order and unresolved stage-zero kind. Gaps or absent stage zero do not imply missing data. Total-only capture without stages is NOT_APPLICABLE.
10. **Implementation:** ACTIVE / REQUIRED_DATA_GUARD; handler identity `g15_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.

## G16 v2.0.0 — Schema version and original evidence

1. **ID/version:** G16 / 2.0.0.
2. **Purpose (corrected):** Strong provenance gate, but raw value retention and rule-version checks are system-owned metadata rather than TMT measurements. Block clinical comments for unverifiable findings; a parse-error message should still be deliverable.
3. **Source/evidence:** [Schema version and original evidence](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 270); S19. Audit assessment: Strong provenance gate, but raw value retention and rule-version checks are system-owned metadata rather than TMT measurements. Block clinical comments for unverifiable findings; a parse-error message should still be deliverable.
4. **Audit disposition:** READY.
5. **Required fields:** source_provenance.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Validate raw digest, versions and exact cell/header/tooth source spans; quarantine affected positions. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 10. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Validate raw digest, versions and exact cell/header/tooth source spans; quarantine affected positions.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g16_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G17 v2.0.0 — Conflict and unsupported input handling

1. **ID/version:** G17 / 2.0.0.
2. **Purpose (corrected):** Correct fail-closed principle, yet use partial abstention: an unverified rotation must not suppress independently verified extrusion for the same case. Implement field-scoped blocking and report coverage.
3. **Source/evidence:** [Conflict and unsupported input handling](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 280); S01, S04, S19. Audit assessment: Correct fail-closed principle, yet use partial abstention: an unverified rotation must not suppress independently verified extrusion for the same case. Implement field-scoped blocking and report coverage.
4. **Audit disposition:** READY.
5. **Required fields:** field_semantic_eligibility.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Evaluate semantic readiness per position and retain field-specific missing prerequisites. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Evaluate semantic readiness per position and retain field-specific missing prerequisites.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `g17_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## G18 v2.0.0 — Recognized tooth types only

1. **ID/version:** G18 / 2.0.0.
2. **Purpose (corrected):** Appropriate: tooth-group logic requires verified adult/primary mapping. Distinguish permanent vs primary, mixed dentition, supernumeraries and nonteeth; avoid treating unexpected IDs as normal molars.
3. **Source/evidence:** [Recognized tooth types only](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 290); S01, S15. Audit assessment: Appropriate: tooth-group logic requires verified adult/primary mapping. Distinguish permanent vs primary, mixed dentition, supernumeraries and nonteeth; avoid treating unexpected IDs as normal molars.
4. **Audit disposition:** READY.
5. **Required fields:** verified_tooth_group_map.
6. **TMT-only feasibility (governing classification):** Metadata. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Require independently supplied recognized permanent tooth-group evidence; no inferred FDI/Universal grouping. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 20. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Require independently supplied recognized permanent tooth-group evidence; no inferred FDI/Universal grouping.
10. **Implementation:** ACTIVE / REQUIRED_DATA_GUARD; handler identity `g18_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.

## H01 v2.0.0 — No clinical suitability diagnosis from TMT

1. **ID/version:** H01 / 2.0.0.
2. **Purpose (corrected):** Clinically appropriate scope guard. No plan suitability, diagnosis or guarantee from a movement table; visible on exported reports and API responses.
3. **Source/evidence:** [No clinical suitability diagnosis from TMT](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 798); S15, S16, S18. Audit assessment: Clinically appropriate scope guard. No plan suitability, diagnosis or guarantee from a movement table;visible on exported reports and API responses.
4. **Audit disposition:** READY.
5. **Required fields:** requested_suitability_assessment, clinical_examination.
6. **TMT-only feasibility (governing classification):** Request. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `h01_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## H02 v2.0.0 — Periodontal condition unknown

1. **ID/version:** H02 / 2.0.0.
2. **Purpose (corrected):** Sound withholding guard for periodontal claims; periodontium cannot be assessed from TMT or virtual root coordinates. Do not interpret missing data as healthy periodontium.
3. **Source/evidence:** [Periodontal condition unknown](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 808); S17, S18. Audit assessment: Sound withholding guard for periodontal claims; periodontium cannot be assessed from TMT or
4. **Audit disposition:** READY.
5. **Required fields:** requested_periodontal_assessment, periodontal_records.
6. **TMT-only feasibility (governing classification):** Request. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `h02_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## H03 v2.0.0 — Root resorption/bone boundary unknown

1. **ID/version:** H03 / 2.0.0.
2. **Purpose (corrected):** Sound withholding guard for root resorption, root proximity and bone housing. A virtual root apex position is not a radiographic/biological risk assessment.
3. **Source/evidence:** [Root resorption/bone boundary unknown](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 818); S15, S17, S21. Audit assessment: Sound withholding guard for root resorption,rootproximityand bone housing. A virtual root apex
4. **Audit disposition:** READY.
5. **Required fields:** requested_root_bone_assessment, root_bone_records.
6. **TMT-only feasibility (governing classification):** Request. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `h03_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## H04 v2.0.0 — Occlusal contacts not inferable

1. **ID/version:** H04 / 2.0.0.
2. **Purpose (corrected):** Sound; total movement does not show occlusal contact distribution or final bite. Neither transverse nor vertical TMT arithmetic is an occlusion simulator.
3. **Source/evidence:** [Occlusal contacts not inferable](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 832); S04, S15. Audit assessment: Sound; total movement does not show occlusal contact distribution or final bite. Neither transverse nor vertical TMT arithmetic is an occlusion simulator.
4. **Audit disposition:** READY.
5. **Required fields:** requested_occlusion_assessment, occlusal_records.
6. **TMT-only feasibility (governing classification):** Request. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `h04_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## H05 v2.0.0 — No unseen IPR planning

1. **ID/version:** H05 / 2.0.0.
2. **Purpose (corrected):** Sound; even when movement suggests crowding or space creation, no IPR amount/site may be derived from total TMT alone.
3. **Source/evidence:** [No unseen IPR planning](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 842); S06, S15. Audit assessment: Sound; even when movement suggests crowding or space creation, no IPR amount/site may be derived from total TMT alone.
4. **Audit disposition:** READY.
5. **Required fields:** requested_ipr_assessment, contact_enamel_and_ipr_plan.
6. **TMT-only feasibility (governing classification):** Request. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `h05_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## H06 v2.0.0 — No extraction/surgery recommendations

1. **ID/version:** H06 / 2.0.0.
2. **Purpose (corrected):** Sound; do not recommend extractions, surgery, adjunctive device substitution or contraindications from TMT without full assessment.
3. **Source/evidence:** [No extraction/surgery recommendations](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 852); S15, S16, S18. Audit assessment: Sound; do not recommend extractions, surgery, adjunctive device substitution or contraindications from TMT without full assessment.
4. **Audit disposition:** READY.
5. **Required fields:** requested_extraction_surgery_assessment, clinical_diagnosis.
6. **TMT-only feasibility (governing classification):** Request. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `h06_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## H07 v2.0.0 — No predicted success probability

1. **ID/version:** H07 / 2.0.0.
2. **Purpose (corrected):** Sound. No patient-level success rate, treatment duration or risk percentage from clinical population averages or rules; any future predictor needs separate validated data and evaluation.
3. **Source/evidence:** [No predicted success probability](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 862); S08, S21. Audit assessment: Sound. No patient-level success rate, treatment duration or risk percentage from clinical population averages or rules;anyfuturepredictor needs separate validated data and evaluation.
4. **Audit disposition:** READY.
5. **Required fields:** requested_prognosis, validated_patient_specific_outcomes.
6. **TMT-only feasibility (governing classification):** Request. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `h07_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## H08 v2.0.0 — No absolute attachment prescriptions

1. **ID/version:** H08 / 2.0.0.
2. **Purpose (corrected):** Sound; no mandatory size, orientation or tooth-surface location from movement table. Avoid 'missing attachment' claims when attachment plan unobserved.
3. **Source/evidence:** [No absolute attachment prescriptions](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 872); S05, S07, S13. Audit assessment: Sound; no mandatory size, orientation or tooth-surface location from movement table. Avoid 'missingattachment' claims when attachmentplan unobserved.
4. **Audit disposition:** READY.
5. **Required fields:** requested_attachment_assessment, actual_attachment_plan.
6. **TMT-only feasibility (governing classification):** Request. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `h08_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## H09 v2.0.0 — No claims of collision-free staging

1. **ID/version:** H09 / 2.0.0.
2. **Purpose (corrected):** Sound; cannot promise collision-free motion or safe stage transitions without 3D models and path validation.
3. **Source/evidence:** [No claims of collision-free staging](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 882); S04. Audit assessment: Sound; cannot promise collision-free motion or safe stage transitions without 3D models and path validation.
4. **Audit disposition:** READY.
5. **Required fields:** requested_collision_assessment, validated_staged_geometry.
6. **TMT-only feasibility (governing classification):** Request. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `h09_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## H10 v2.0.0 — Monitoring and clinician sign-off

1. **ID/version:** H10 / 2.0.0.
2. **Purpose (corrected):** Required draft/review label and sign-off workflow. Human-review flag alone is insufficient if clinicians cannot inspect the numeric evidence and rationale.
3. **Source/evidence:** [Monitoring and clinician sign-off](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 894); S18, S19. Audit assessment: Required draft/review label and sign-off workflow. Human-review flag alone is insufficient if clinicians cannot inspect the numeric evidence and rationale.
4. **Audit disposition:** READY.
5. **Required fields:** report_review_status.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Always mark DRAFT; authenticated clinician sign-off and review invalidation workflow are not implemented. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Always mark DRAFT; authenticated clinician sign-off and review invalidation workflow are not implemented.
10. **Implementation:** ACTIVE / PARTIAL_SYSTEM_CONTROL; handler identity `h10_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Always mark DRAFT; authenticated clinician sign-off and review invalidation workflow are not implemented. Full system workflow remains outside this phase.

## H11 v2.0.0 — Context-dependent exclusions

1. **ID/version:** H11 / 2.0.0.
2. **Purpose (corrected):** Appropriate abstention but overlaps H01-H03/H06; consolidate implementation as a contextrequirement matrix while preserving distinct audit codes.
3. **Source/evidence:** [Context-dependent exclusions](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 902); S15, S16. Audit assessment: Appropriate abstention but overlaps H01-H03/H06; consolidate implementation as a context- requirement matrix whilepreservingdistinct audit codes.
4. **Audit disposition:** READY.
5. **Required fields:** requested_intervention_assessment, verified_clinical_exclusions.
6. **TMT-only feasibility (governing classification):** Request. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** On an explicit dependent assessment request, return CONTEXT_REQUIRED with examination/data prerequisites; otherwise NOT_APPLICABLE. No positive clinical claim.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `h11_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## H12 v2.0.0 — Privacy and data minimization

1. **ID/version:** H12 / 2.0.0.
2. **Purpose (corrected):** Privacy guard essential but source S18 is not a jurisdiction-specific data-protection law. Require explicit PHI policy, redaction, retention, encryption, access control and no unsanctioned LLM transmission.
3. **Source/evidence:** [Privacy and data minimization](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 912); S18, S20. Audit assessment: Privacy guard essential but source S18 is not a jurisdiction-specific data-protection law. Require explicit PHI policy, redaction, retention, encryption, access control and no unsanctioned LLM transmission.
4. **Audit disposition:** READY.
5. **Required fields:** synthetic_data_confirmed, separate_server_cloud_authorization.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Current synthetic confirmation, no-persistence design and separate cloud gates only; no PHI detector, full privacy compliance or de-identification claim. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Current synthetic confirmation, no-persistence design and separate cloud gates only; no PHI detector, full privacy compliance or de-identification claim.
10. **Implementation:** ACTIVE / PARTIAL_SYSTEM_CONTROL; handler identity `h12_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Current synthetic confirmation, no-persistence design and separate cloud gates only; no PHI detector, full privacy compliance or de-identification claim. Full system workflow remains outside this phase.

## L01 v2.0.0 — Only rule-approved facts in comments

1. **ID/version:** L01 / 2.0.0.
2. **Purpose (corrected):** Important invariant. Prefer templates backed by typed structured findings; unconstrained LLM prose cannot be guaranteed clinically correct by prompt instructions alone. Validate/reject generated claims if any LLM is used.
3. **Source/evidence:** [Only rule-approved facts in comments](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 924); S19, S20. Audit assessment: Important invariant. Prefer templates backed by typed structured findings; unconstrained LLM prose cannot be guaranteed clinically correct by prompt instructions alone. Validate/reject generated claims if anyLLM is used.
4. **Audit disposition:** READY.
5. **Required fields:** structured_findings, closed_output_templates.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Accept only closed templates bound to structured facts; reject injected or unsupported wording. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 90. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Accept only closed templates bound to structured facts; reject injected or unsupported wording.
10. **Implementation:** ACTIVE / OUTPUT_GUARD; handler identity `l01_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## L02 v2.0.0 — Measurement exactness

1. **ID/version:** L02 / 2.0.0.
2. **Purpose (corrected):** Essential deterministic token/measurement preservation: compare normalized tooth, numeric value, sign/direction, scope and basis, not approximate prose similarity. Never silently alter precision.
3. **Source/evidence:** [Measurement exactness](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 934); S01, S19. Audit assessment: Essential deterministic token/measurement preservation: compare normalized tooth, numeric value, sign/direction, scope and basis, not approximate prose similarity. Never silently alter precision.
4. **Audit disposition:** READY.
5. **Required fields:** exact_observation_snapshot.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Compare exact observation snapshots, Decimal precision, original identifiers and source evidence; reject mutations. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 90. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Compare exact observation snapshots, Decimal precision, original identifiers and source evidence; reject mutations.
10. **Implementation:** ACTIVE / OUTPUT_GUARD; handler identity `l02_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## L03 v2.0.0 — Per-finding traceability

1. **ID/version:** L03 / 2.0.0.
2. **Purpose (corrected):** Require finding-to-source map for each clinical sentence; labels from literature are provenance, not evidence of a patient-specific conclusion. Keep raw display links.
3. **Source/evidence:** [Per-finding traceability](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 944); S19. Audit assessment: Require finding-to-source map for each clinical sentence; labels from literature are provenance, not evidence of apatient-specific conclusion. Keepraw displaylinks.
4. **Audit disposition:** READY.
5. **Required fields:** finding_input_refs, source_evidence_refs.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Retain source spans, field evidence, input references and all triggering rule versions. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 90. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Retain source spans, field evidence, input references and all triggering rule versions.
10. **Implementation:** ACTIVE / OUTPUT_GUARD; handler identity `l03_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## L04 v2.0.0 — Deduplicate and resolve conflicts

1. **ID/version:** L04 / 2.0.0.
2. **Purpose (corrected):** Deduplicate only identical clinical propositions; retain all triggering rule IDs and source fields. Report real contradictions instead of dropping lower-priority findings silently.
3. **Source/evidence:** [Deduplicate and resolve conflicts](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 956); S03, S19. Audit assessment: Deduplicate only identical clinical propositions; retain all triggering rule IDs and source fields. Report real contradictions instead of droppinglower-priorityfindings silently.
4. **Audit disposition:** READY.
5. **Required fields:** finding_propositions, conflict_keys.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Merge identical propositions while retaining triggering IDs; quarantine contradictions instead of choosing one. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 90. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Merge identical propositions while retaining triggering IDs; quarantine contradictions instead of choosing one.
10. **Implementation:** ACTIVE / OUTPUT_GUARD; handler identity `l04_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## L05 v2.0.0 — Uncertainty disclosure

1. **ID/version:** L05 / 2.0.0.
2. **Purpose (corrected):** Make unsupported/missing-context states explicit and localized to each finding; distinguish 'not evaluated' from 'evaluated and no concern flagged'.
3. **Source/evidence:** [Uncertainty disclosure](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 964); S08, S19. Audit assessment: Make unsupported/missing-context states explicit and localized to each finding; distinguish 'not evaluated' from 'evaluated and no concern flagged'.
4. **Audit disposition:** READY.
5. **Required fields:** field_scoped_verification_states.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Preserve localized uncertainty and suppress unsupported facts without converting abstention to a negative. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 90. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Preserve localized uncertainty and suppress unsupported facts without converting abstention to a negative.
10. **Implementation:** ACTIVE / OUTPUT_GUARD; handler identity `l05_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## L06 v2.0.0 — Final clinician review status

1. **ID/version:** L06 / 2.0.0.
2. **Purpose (corrected):** Maintain Draft -> Reviewed -> Approved or Rejected with authorized reviewer identity, timestamps, immutable version and reapproval on content changes. Approval is not delegated to the LLM.
3. **Source/evidence:** [Final clinician review status](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 974); S18, S19. Audit assessment: l Maintain Draft -> Reviewed -> Approved or Rejected with authorized reviewer identity, timestamps, immutable version and reapproval on content changes. Approval is not delegated to the LLM.
4. **Audit disposition:** READY.
5. **Required fields:** report_review_status.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. DRAFT output label only; no authenticated signature or final clinical approval. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 90. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** DRAFT output label only; no authenticated signature or final clinical approval.
10. **Implementation:** ACTIVE / PARTIAL_SYSTEM_CONTROL; handler identity `l06_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** DRAFT output label only; no authenticated signature or final clinical approval. Full system workflow remains outside this phase.

## N01 v2.0.0 — Table completeness / expected coverage

1. **ID/version:** N01 / 2.0.0.
2. **Purpose (corrected):** Define required headers, tooth columns, arch, expected axes and a coverage mask; partial inputs remain explicitly partial.
3. **Source/evidence:** [Table completeness / expected coverage](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 986); None. Audit assessment: Define required headers, tooth columns, arch, expected axes and a coverage mask; partial inputs remain explicitly partial.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** verified_expected_axis_coverage.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Require independently supplied expected coverage; report exact missing axis/position pairs, never zero-fill. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 25. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Require independently supplied expected coverage; report exact missing axis/position pairs, never zero-fill.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `n01_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.

## N02 v2.0.0 — Unknown format and layout drift

1. **ID/version:** N02 / 2.0.0.
2. **Purpose (corrected):** Detect unrecognized revisions, reordered and transposed variants; never silently select a closest-match adapter.
3. **Source/evidence:** [Unknown format and layout drift](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 988); None. Audit assessment: Detect unrecognized revisions, reordered and transposed variants; never silently select a closest-match adapter.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** released_source_version.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Require a released vendor semantic version; TEST_ONLY and unknown vendor claims cannot satisfy this vendor-release guard. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 25. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Require a released vendor semantic version; TEST_ONLY and unknown vendor claims cannot satisfy this vendor-release guard.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `n02_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## N03 v2.0.0 — Case / plan identity isolation

1. **ID/version:** N03 / 2.0.0.
2. **Purpose (corrected):** Use separate pseudonymous case and plan identities, protect against cross-patient and crossplan joins.
3. **Source/evidence:** [Case / plan identity isolation](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 990); None. Audit assessment: Use separate pseudonymous case and plan identities, protect against cross-patient and crossplan joins.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** single_capture_boundary.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. One capture per submission, no cross-capture combination. Patient/plan identity cannot be independently established. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 25. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** One capture per submission, no cross-capture combination. Patient/plan identity cannot be independently established.
10. **Implementation:** ACTIVE / PARTIAL_SYSTEM_CONTROL; handler identity `n03_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** One capture per submission, no cross-capture combination. Patient/plan identity cannot be independently established. Full system workflow remains outside this phase.

## N04 v2.0.0 — Unicode and raw evidence preservation

1. **ID/version:** N04 / 2.0.0.
2. **Purpose (corrected):** Retain original clipboard text in controlled memory; normalize unicode minus, NBSP and decimal conventions only in derived tokens.
3. **Source/evidence:** [Unicode and raw evidence preservation](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 992); None. Audit assessment: Retain original clipboard text in controlled memory; normalize unicode minus, NBSP and decimal conventions only in derived tokens.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** raw_text, raw_sha256, source_spans.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Preserve logical Unicode input, validate hash/spans. Browser newline canonicalization is allowed; not byte-original clipboard preservation. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 10. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Preserve logical Unicode input, validate hash/spans. Browser newline canonicalization is allowed; not byte-original clipboard preservation.
10. **Implementation:** ACTIVE / PARTIAL_SYSTEM_CONTROL; handler identity `n04_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Preserve logical Unicode input, validate hash/spans. Browser newline canonicalization is allowed; not byte-original clipboard preservation. Full system workflow remains outside this phase.

## N05 v2.0.0 — Mirrored tooth sign conventions

1. **ID/version:** N05 / 2.0.0.
2. **Purpose (corrected):** Apply signed direction logic only through verified source-, tooth-, arch- and version-specific maps.
3. **Source/evidence:** [Mirrored tooth sign conventions](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 994); None. Audit assessment: Apply signed direction logic only through verified source-, tooth-, arch- and version-specific maps.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** verified_pair_map_and_mirror_operations.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Require explicit paired identifiers, directions and independently asserted equivalence; do not infer mirrored signs. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 25. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Require explicit paired identifiers, directions and independently asserted equivalence; do not infer mirrored signs.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `n05_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.

## N06 v2.0.0 — External tooth-status metadata

1. **ID/version:** N06 / 2.0.0.
2. **Purpose (corrected):** Keep pontic, unerupted, impacted, extracted, excluded, fixed and mixed-dentition statuses from verified external data only.
3. **Source/evidence:** [External tooth-status metadata](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 996); None. Audit assessment: Keep pontic, unerupted, impacted, extracted, excluded, fixed and mixed-dentition statuses from verified external data only.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** verified_external_tooth_status.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Require explicit independently supplied tooth status; cannot infer status from absence or magnitude. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 25. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Require explicit independently supplied tooth status; cannot infer status from absence or magnitude.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `n06_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.

## N07 v2.0.0 — Stage and overcorrection states

1. **ID/version:** N07 / 2.0.0.
2. **Purpose (corrected):** Represent baseline/zero, active, accommodation, correction, overcorrection and passive stages explicitly.
3. **Source/evidence:** [Stage and overcorrection states](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 998); None. Audit assessment: Represent baseline/zero, active, accommodation, correction, overcorrection and passive stages explicitly.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** verified_stage_dataset.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Require actual staged data when staged semantics apply; no stage-count/stage-kind inference from totals. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 25. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Require actual staged data when staged semantics apply; no stage-count/stage-kind inference from totals.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `n07_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** Additional evidence intake is library-only TEST_ONLY; no production authorization path. Missing evidence causes structured abstention.

## N08 v2.0.0 — Coordinate frame and composition

1. **ID/version:** N08 / 2.0.0.
2. **Purpose (corrected):** Track coordinate frame, initial geometry and supported transform operations; ban unproven sum/subtraction of movements.
3. **Source/evidence:** [Coordinate frame and composition](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 1000); None. Audit assessment: Track coordinate frame, initial geometry and supported transform operations; ban unproven sum/subtraction of movements.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** verified_coordinate_frame_and_operations.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Require compatible coordinate semantics and withhold on missing dependent fields. No geometric/transform composition implemented. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 25. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Require compatible coordinate semantics and withhold on missing dependent fields. No geometric/transform composition implemented.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `n08_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## N09 v2.0.0 — Field-scoped abstention

1. **ID/version:** N09 / 2.0.0.
2. **Purpose (corrected):** Suppress only findings that depend on an unverified metric; report coverage for unaffected fields.
3. **Source/evidence:** [Field-scoped abstention](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 1002); None. Audit assessment: Suppress only findings that depend on an unverified metric; report coverage for unaffected fields.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** field_verification_states.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Keep uncertainty field-local; independent authorized fields can retain descriptive observations. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 25. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Keep uncertainty field-local; independent authorized fields can retain descriptive observations.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `n09_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## N10 v2.0.0 — Input/output claims filter

1. **ID/version:** N10 / 2.0.0.
2. **Purpose (corrected):** Treat pasted text as untrusted data; prevent unsupported advice and prompt-injection instructions from altering outputs.
3. **Source/evidence:** [Input/output claims filter](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 1004); None. Audit assessment: Treat pasted text as untrusted data; prevent unsupported advice and prompt-injection instructions from altering outputs.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** trusted_structured_context, untrusted_literal_text.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Treat all pasted content as literal untrusted text; it cannot set authority, policy, evidence or output templates. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Treat all pasted content as literal untrusted text; it cannot set authority, policy, evidence or output templates.
10. **Implementation:** ACTIVE / OUTPUT_GUARD; handler identity `n10_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## N11 v2.0.0 — Immutable report amendments

1. **ID/version:** N11 / 2.0.0.
2. **Purpose (corrected):** Tie signed report to content, rules, source and version; revoke sign-off after material changes.
3. **Source/evidence:** [Immutable report amendments](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 1006); None. Audit assessment: Tie signed report to content, rules, source and version; revoke sign-off after material changes.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** authenticated_reviewer_identity, immutable_versioned_review_events, approval_invalidation_workflow.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Deferred: authenticated reviewer identity, immutable versioned amendments and invalidation workflow unavailable. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Deferred: authenticated reviewer identity, immutable versioned amendments and invalidation workflow unavailable.
10. **Implementation:** DEFERRED / DEFERRED; handler identity `n11_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** FUTURE_AUTHORIZED_WORKFLOW_REQUIRED: authenticated_reviewer_identity, immutable_versioned_review_events, approval_invalidation_workflow.

## N12 v2.0.0 — Clinical intended purpose

1. **ID/version:** N12 / 2.0.0.
2. **Purpose (corrected):** Record the requested clinical question, treatment objective and endpoint separately from movement magnitudes.
3. **Source/evidence:** [Clinical intended purpose](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 1012); None. Audit assessment: Record the requested clinical question, treatment objective and endpoint separately from movement magnitudes.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** verified_treatment_objectives, clinical_endpoint.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Withhold requested clinical purpose/endpoint assessment absent verified objectives; magnitude is not treatment intent. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 30. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Withhold requested clinical purpose/endpoint assessment absent verified objectives; magnitude is not treatment intent.
10. **Implementation:** ACTIVE / REQUIRED_DATA_GUARD; handler identity `n12_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## N13 v2.0.0 — Rule-dependent eligibility

1. **ID/version:** N13 / 2.0.0.
2. **Purpose (corrected):** Require each rule to declare source/version, required fields, valid basis, scope, plan mode, semantics and abstention outcome.
3. **Source/evidence:** [Rule-dependent eligibility](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 1014); None. Audit assessment: Require each rule to declare source/version, required fields, valid basis, scope, plan mode, semantics and abstention outcome.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** rule_specific_eligibility_contract.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Apply common semantic eligibility plus rule-specific allowed domain/mode/scope and additional input checks. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 25. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Apply common semantic eligibility plus rule-specific allowed domain/mode/scope and additional input checks.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `n13_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## N14 v2.0.0 — Incident and rollback workflow

1. **ID/version:** N14 / 2.0.0.
2. **Purpose (corrected):** Before any clinical use, define error severity, incident logging, escalation, remediation and rapid rollback.
3. **Source/evidence:** [Incident and rollback workflow](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 1016); None. Audit assessment: Before any clinical use, define error severity, incident logging, escalation, remediation and rapid rollback.
4. **Audit disposition:** ADDITIONAL.
5. **Required fields:** incident_severity_policy, approved_escalation_workflow, reviewed_rollback_release_process.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Deferred: incident triage, escalation and approved rollback workflow unavailable. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 80. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Deferred: incident triage, escalation and approved rollback workflow unavailable.
10. **Implementation:** DEFERRED / DEFERRED; handler identity `n14_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** FUTURE_AUTHORIZED_WORKFLOW_REQUIRED: incident_severity_policy, approved_escalation_workflow, reviewed_rollback_release_process.

## R01 v2.0.0 — Canine/premolar rotation review

1. **ID/version:** R01 / 2.0.0.
2. **Purpose (corrected):** Review prompt is plausible because rotational predictability varies; cited studies do not establish universal canine/premolar cutoffs. Needs tooth-, platform-, basis- and intent-specific trigger, exception list and blinded case validation.
3. **Source/evidence:** [Canine/premolar rotation review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 476); S08, S09, S10. Audit assessment: Review prompt is plausible because rotational predictability varies; cited studies do not establish universal canine/premolar cutoffs. Needs tooth-, platform-, basis- and intent-specific trigger, exception list and blinded case validation.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_tooth_group, verified_rotation, source_specific_review_policy, approved_exceptions_and_intent.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_tooth_group, verified_rotation, source_specific_review_policy, approved_exceptions_and_intent. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_tooth_group, verified_rotation, source_specific_review_policy, approved_exceptions_and_intent. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r01_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_tooth_group, verified_rotation, source_specific_review_policy, approved_exceptions_and_intent.

## R02 v2.0.0 — Rotation magnitude band by tooth type

1. **ID/version:** R02 / 2.0.0.
2. **Purpose (corrected):** Only acceptable as a clearly labeled clinician-selected movement-size category, never a validated risk tier. Historical Invisalign categories are not contemporary cross-platform clinical thresholds.
3. **Source/evidence:** [Rotation magnitude band by tooth type](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 484); S02, S10. Audit assessment: Only acceptable as a clearly labeled clinician-selected movement-size category, never a validated risk tier. Historical Invisalign categories are not contemporarycross-platform clinical thresholds.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_tooth_group, verified_rotation, approved_movement_size_bands.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_tooth_group, verified_rotation, approved_movement_size_bands. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_tooth_group, verified_rotation, approved_movement_size_bands. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r02_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_tooth_group, verified_rotation, approved_movement_size_bands.

## R03 v2.0.0 — Anterior extrusion review

1. **ID/version:** R03 / 2.0.0.
2. **Purpose (corrected):** Potential movement review only. Anterior extrusion studies are heterogeneous; absence of attachments/staging/occlusion means no specific auxiliary recommendation or prediction.
3. **Source/evidence:** [Anterior extrusion review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 494); S09, S13. Audit assessment: Potential movement review only. Anterior extrusion studies are heterogeneous; absence of attachments/staging/occlusion means no specific auxiliaryrecommendation orprediction.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_anterior_group, verified_extrusion, approved_extrusion_policy.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_anterior_group, verified_extrusion, approved_extrusion_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_anterior_group, verified_extrusion, approved_extrusion_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r03_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_anterior_group, verified_extrusion, approved_extrusion_policy.

## R04 v2.0.0 — Posterior extrusion review

1. **ID/version:** R04 / 2.0.0.
2. **Purpose (corrected):** Posterior extrusion review is a candidate; historic manufacturer colors are a poor universal basis. Require device-specific rationale and limit language to 'review planned extrusion'.
3. **Source/evidence:** [Posterior extrusion review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 508); S02, S09. Audit assessment: i Posterior extrusion review is a candidate; historic manufacturer colors are a poor universal basis. Require device-specific rationale and limit language to 'reviewplanned extrusion'.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_posterior_group, verified_extrusion, approved_device_specific_policy.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_posterior_group, verified_extrusion, approved_device_specific_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_posterior_group, verified_extrusion, approved_device_specific_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r04_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_posterior_group, verified_extrusion, approved_device_specific_policy.

## R05 v2.0.0 — Lower incisor intrusion review

1. **ID/version:** R05 / 2.0.0.
2. **Purpose (corrected):** Lower-incisor intrusion deserves focused review, but S11 includes only eight studies, seven with serious bias, and measurement heterogeneity; do not derive a 1.5/2.0 mm default cutoff or a safety flag from its summary.
3. **Source/evidence:** [Lower incisor intrusion review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 518); S09, S11. Audit assessment: Lower-incisor intrusion deserves focused review, but S11 includes only eight studies, seven with serious bias, and measurement heterogeneity; do not derive a 1.5/2.0 mm default cutoff or a safety flagfrom its summary.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_lower_incisor_identity, verified_intrusion, approved_intrusion_policy.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_lower_incisor_identity, verified_intrusion, approved_intrusion_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_lower_incisor_identity, verified_intrusion, approved_intrusion_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r05_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_lower_incisor_identity, verified_intrusion, approved_intrusion_policy.

## R06 v2.0.0 — Other intrusion review

1. **ID/version:** R06 / 2.0.0.
2. **Purpose (corrected):** Other intrusion by group is a plausible policy only; root support, occlusal objectives, staging, baseline bite and appliance details are absent. No generalized success rating.
3. **Source/evidence:** [Other intrusion review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 526); S08, S09. Audit assessment: Other intrusion by group is a plausible policy only; root support, occlusal objectives, staging, baseline bite and appliance details are absent. Nogeneralized success rating.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_tooth_group, verified_intrusion, root_support_and_occlusal_objectives, approved_intrusion_policy.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_tooth_group, verified_intrusion, root_support_and_occlusal_objectives, approved_intrusion_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_tooth_group, verified_intrusion, root_support_and_occlusal_objectives, approved_intrusion_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r06_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_tooth_group, verified_intrusion, root_support_and_occlusal_objectives, approved_intrusion_policy.

## R07 v2.0.0 — Incisor inclination / root control review

1. **ID/version:** R07 / 2.0.0.
2. **Purpose (corrected):** Risk of misinterpreting crown inclination as root torque or periodontal root risk. Without actual rootposition/geometry, allow only a conditional 'review inclination/root-control strategy' prompt approved by an orthodontist.
3. **Source/evidence:** [Incisor inclination / root control review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 536); S08, S13. Audit assessment: Risk of misinterpreting crown inclination as root torque or periodontal root risk. Without actual root- position/geometry, allow only a conditional 'review inclination/root-control strategy' prompt approved byan orthodontist.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_incisor_identity, verified_inclination, root_position_and_geometry, approved_root_control_review_policy.
6. **TMT-only feasibility (governing classification):** Partial. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_incisor_identity, verified_inclination, root_position_and_geometry, approved_root_control_review_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_incisor_identity, verified_inclination, root_position_and_geometry, approved_root_control_review_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r07_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_incisor_identity, verified_inclination, root_position_and_geometry, approved_root_control_review_policy.

## R08 v2.0.0 — Mesiodistal tipping/angulation review

1. **ID/version:** R08 / 2.0.0.
2. **Purpose (corrected):** Angular movement is observable, but space closure and control of roots are unobserved. Require a movement-specific criterion and do not infer need for mechanics.
3. **Source/evidence:** [Mesiodistal tipping/angulation review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 546); S08, S13. Audit assessment: Angular movement is observable, but space closure and control of roots are unobserved. Require a movement-specific criterion and do not infer need for mechanics.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_angulation, verified_tooth_group, approved_angulation_review_policy.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_angulation, verified_tooth_group, approved_angulation_review_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_angulation, verified_tooth_group, approved_angulation_review_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r08_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_angulation, verified_tooth_group, approved_angulation_review_policy.

## R09 v2.0.0 — Posterior transverse movement review

1. **ID/version:** R09 / 2.0.0.
2. **Purpose (corrected):** Posterior buccolingual displacement may invite review; TMT is insufficient to distinguish tipping/bodily expansion, assess bone envelope or compute arch expansion. Avoid threshold masquerading as periodontal safety.
3. **Source/evidence:** [Posterior transverse movement review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 556); S08, S15. Audit assessment: Posterior buccolingual displacement may invite review; TMT is insufficient to distinguish tipping/bodily expansion, assess bone envelope or compute arch expansion. Avoid threshold masqueradingasperiodontal safety.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_posterior_group, verified_buccolingual_movement, bone_and_root_assessment, approved_transverse_review_policy.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_posterior_group, verified_buccolingual_movement, bone_and_root_assessment, approved_transverse_review_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_posterior_group, verified_buccolingual_movement, bone_and_root_assessment, approved_transverse_review_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r09_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_posterior_group, verified_buccolingual_movement, bone_and_root_assessment, approved_transverse_review_policy.

## R10 v2.0.0 — Maxillary molar distalization review

1. **ID/version:** R10 / 2.0.0.
2. **Purpose (corrected):** Upper molar distal movement can be identified. S12 finds very-low-certainty evidence and cannot justify cross-system anchorage or overcorrection instructions; stage/anchorage adequacy requires more data.
3. **Source/evidence:** [Maxillary molar distalization review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 568); S03, S12. Audit assessment: Upper molar distal movement can be identified. S12 finds very-low-certainty evidence and cannot justify cross-system anchorage or overcorrection instructions; stage/anchorage adequacy requires more data.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_upper_molar_identity, verified_distal_direction, staged_anchorage_context, approved_distalization_policy.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_upper_molar_identity, verified_distal_direction, staged_anchorage_context, approved_distalization_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_upper_molar_identity, verified_distal_direction, staged_anchorage_context, approved_distalization_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r10_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_upper_molar_identity, verified_distal_direction, staged_anchorage_context, approved_distalization_policy.

## R11 v2.0.0 — Molar mesialization review

1. **ID/version:** R11 / 2.0.0.
2. **Purpose (corrected):** Molar mesial movement can be identified, but extraction status, space closure, anchorage and root trajectory are absent. Do not prescribe control mechanics.
3. **Source/evidence:** [Molar mesialization review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 578); S12, S15. Audit assessment: Molar mesial movement can be identified, but extraction status, space closure, anchorage and root trajectoryare absent. Do notprescribe control mechanics.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_molar_identity, verified_mesial_direction, extraction_space_and_root_context, approved_mesialization_policy.
6. **TMT-only feasibility (governing classification):** Yes. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_molar_identity, verified_mesial_direction, extraction_space_and_root_context, approved_mesialization_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_molar_identity, verified_mesial_direction, extraction_space_and_root_context, approved_mesialization_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r11_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_molar_identity, verified_mesial_direction, extraction_space_and_root_context, approved_mesialization_policy.

## R12 v2.0.0 — Complex movement combination review

1. **ID/version:** R12 / 2.0.0.
2. **Purpose (corrected):** Proposed interaction matrix is unbuilt and unsupported by transferable clinical validation. Vendor antagonistic/synergistic staging settings demonstrate configurability, not a scientifically validated universal matrix.
3. **Source/evidence:** [Complex movement combination review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 588); S03, S13. Audit assessment: Proposed interaction matrix is unbuilt and unsupported by transferable clinical validation. Vendor antagonistic/synergistic staging settings demonstrate configurability, not a scientifically validated universal matrix.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_combination_axes, verified_directions_and_groups, approved_validated_interaction_matrix.
6. **TMT-only feasibility (governing classification):** Partial. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_combination_axes, verified_directions_and_groups, approved_validated_interaction_matrix. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_combination_axes, verified_directions_and_groups, approved_validated_interaction_matrix. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r12_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_combination_axes, verified_directions_and_groups, approved_validated_interaction_matrix.

## R13 v2.0.0 — Staged versus total movement concern

1. **ID/version:** R13 / 2.0.0.
2. **Purpose (corrected):** Misclassified under TMT-only clinician rules: per-stage scrutiny requires stage-level input, a devicespecific profile and clinician approval. Merge with T01; never divide a total by stage count as a substitute.
3. **Source/evidence:** [Staged versus total movement concern](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 598); S03, S04, S06. Audit assessment: Misclassified under TMT-only clinician rules: per-stage scrutiny requires stage-level input, a device- specific profile and clinician approval. Merge with T01; never divide a total by stage count as a substitute. f
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, actual_stage_dataset, verified_device_version_profile, approved_stage_policy.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: actual_stage_dataset, verified_device_version_profile, approved_stage_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** T01 / T01. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: actual_stage_dataset, verified_device_version_profile, approved_stage_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r13_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, actual_stage_dataset, verified_device_version_profile, approved_stage_policy.

## R14 v2.0.0 — Clinical-context-sensitive threshold withheld

1. **ID/version:** R14 / 2.0.0.
2. **Purpose (corrected):** Sound abstention control, not a clinical numeric threshold. Move into global data-sufficiency/safety policy; absent patient context must yield 'cannot assess', not normal/low risk.
3. **Source/evidence:** [Clinical-context-sensitive threshold withheld](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 608); S15, S16, S17. Audit assessment: Sound abstention control, not a clinical numeric threshold. Move into global data-sufficiency/safety policy;absentpatient context mustyield 'cannot assess',not normal/low risk.
4. **Audit disposition:** READY.
5. **Required fields:** requested_assessment_context.
6. **TMT-only feasibility (governing classification):** System. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Withhold requested suitability/context-sensitive conclusions when necessary examination/context is absent. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 30. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Withhold requested suitability/context-sensitive conclusions when necessary examination/context is absent.
10. **Implementation:** ACTIVE / EXECUTABLE; handler identity `r14_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPLICABLE. None. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No activation blocker for this engineering guard; measurement descriptions still require released field-level semantics (currently no vendor release).

## R15 v2.0.0 — Attachment strategy merits review

1. **ID/version:** R15 / 2.0.0.
2. **Purpose (corrected):** Review question from movement alone is permissible only as open-ended, not as implied attachment deficiency. To check whether a required attachment is absent, acquire an actual attachment plan as in A02.
3. **Source/evidence:** [Attachment strategy merits review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 618); S07, S13, S14. Audit assessment: Review question from movement alone is permissible only as open-ended, not as implied attachment deficiency. To check whether a required attachment is absent, acquire an actual attachmentplan as in A02.
4. **Audit disposition:** VALIDATE.
5. **Required fields:** orthodontist_approved_policy, verified_movement_group, actual_attachment_plan, approved_open_ended_review_policy.
6. **TMT-only feasibility (governing classification):** Partial. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: verified_movement_group, actual_attachment_plan, approved_open_ended_review_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: verified_movement_group, actual_attachment_plan, approved_open_ended_review_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r15_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, verified_movement_group, actual_attachment_plan, approved_open_ended_review_policy.

## R16 v2.0.0 — Potential complexity of whole case

1. **ID/version:** R16 / 2.0.0.
2. **Purpose (corrected):** Whole-case clinical complexity requires occlusion, malocclusion, skeletal/periodontal assessment and treatment objectives. Keep disabled as case score; S15's CAT-CAT classification itself uses models, radiographs and examinations.
3. **Source/evidence:** [Potential complexity of whole case](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 632); S08, S15, S16. Audit assessment: Whole-case clinical complexity requires occlusion, malocclusion, skeletal/periodontal assessment and treatment objectives. Keep disabled as case score; S15's CAT-CAT classification itself uses models,radiographs and examinations.
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, full_clinical_examination, occlusion_and_skeletal_periodontal_context, treatment_objectives, approved_full_case_rubric.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: full_clinical_examination, occlusion_and_skeletal_periodontal_context, treatment_objectives, approved_full_case_rubric. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: full_clinical_examination, occlusion_and_skeletal_periodontal_context, treatment_objectives, approved_full_case_rubric. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `r16_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, full_clinical_examination, occlusion_and_skeletal_periodontal_context, treatment_objectives, approved_full_case_rubric.

## T01 v2.0.0 — Per-stage movement ceilings

1. **ID/version:** T01 / 2.0.0.
2. **Purpose (corrected):** Valid technical comparison only with actual per-stage values, manufacturer/version profile and clinician-approved limit. ClearCorrect 0.3 mm/3 deg is a setting, not a safety limit; source profile must match.
3. **Source/evidence:** [Per-stage movement ceilings](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 642); S03, S04, S06. Audit assessment: Valid technical comparison only with actual per-stage values, manufacturer/version profile and clinician-approved limit. ClearCorrect 0.3 mm/3 deg is a setting, not a safety limit; source profile must match. i
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, actual_per_stage_values, verified_device_profile, orthodontist_approved_stage_limits.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: actual_per_stage_values, verified_device_profile, orthodontist_approved_stage_limits. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / R13. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: actual_per_stage_values, verified_device_profile, orthodontist_approved_stage_limits. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `t01_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, actual_per_stage_values, verified_device_profile, orthodontist_approved_stage_limits.

## T02 v2.0.0 — Cumulative/incremental consistency

1. **ID/version:** T02 / 2.0.0.
2. **Purpose (corrected):** Do not blindly sum angular increments or mixed-reference translations. Define coordinate frames and valid source operations; compare only values whose composition semantics are demonstrated, with a justified numeric tolerance.
3. **Source/evidence:** [Cumulative/incremental consistency](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 652); S04. Audit assessment: Do not blindly sum angular increments or mixed-reference translations. Define coordinate frames and valid source operations; compare only values whose composition semantics are demonstrated, with ajustified numeric tolerance.
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, actual_stage_dataset, verified_baseline_geometry, verified_coordinate_transforms, approved_composition_operations_and_tolerance.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: actual_stage_dataset, verified_baseline_geometry, verified_coordinate_transforms, approved_composition_operations_and_tolerance. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: actual_stage_dataset, verified_baseline_geometry, verified_coordinate_transforms, approved_composition_operations_and_tolerance. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `t02_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, actual_stage_dataset, verified_baseline_geometry, verified_coordinate_transforms, approved_composition_operations_and_tolerance.

## T03 v2.0.0 — Maximal stages override warning

1. **ID/version:** T03 / 2.0.0.
2. **Purpose (corrected):** An observed threshold exceedance can be reported if actual stage values exist, but the claim that 'maximal stages override caused it' needs staging config/history or counterfactual evidence. Rephrase as observed constraint exceedance.
3. **Source/evidence:** [Maximal stages override warning](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 662); S03. Audit assessment: An observed threshold exceedance can be reported if actual stage values exist, but the claim that 'maximal stages override caused it' needs staging config/history or counterfactual evidence. Rephrase as observed constraint exceedance. i
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, actual_per_stage_values, verified_configured_constraint, configuration_history, approved_stage_policy.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: actual_per_stage_values, verified_configured_constraint, configuration_history, approved_stage_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: actual_per_stage_values, verified_configured_constraint, configuration_history, approved_stage_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `t03_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, actual_per_stage_values, verified_configured_constraint, configuration_history, approved_stage_policy.

## T04 v2.0.0 — Sequential distalization pattern review

1. **ID/version:** T04 / 2.0.0.
2. **Purpose (corrected):** Sequence comparison needs stage-by-stage positions plus a verified intended distalization/anchorage protocol; total TMT has no order. No universal sequence shall be hardcoded.
3. **Source/evidence:** [Sequential distalization pattern review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 672); S03, S12. Audit assessment: Sequence comparison needs stage-by-stage positions plus a verified intended distalization/anchorage protocol; total TMT has no order. No universal sequence shall be hardcoded. i
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, actual_stage_dataset, verified_intended_distalization_sequence, approved_anchorage_protocol.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: actual_stage_dataset, verified_intended_distalization_sequence, approved_anchorage_protocol. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: actual_stage_dataset, verified_intended_distalization_sequence, approved_anchorage_protocol. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `t04_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, actual_stage_dataset, verified_intended_distalization_sequence, approved_anchorage_protocol.

## T05 v2.0.0 — Movement overlap interaction review

1. **ID/version:** T05 / 2.0.0.
2. **Purpose (corrected):** Requires staged overlap and an expert-approved, device-specific interaction policy. A cliniciandesigned rule is not proven beneficial absent case evaluations.
3. **Source/evidence:** [Movement overlap interaction review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 684); S03. Audit assessment: Requires staged overlap and an expert-approved, device-specific interaction policy. A clinician- designed rule is notproven beneficial absent case evaluations.
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, actual_stage_overlap, device_specific_validated_interaction_matrix, approved_interaction_policy.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: actual_stage_overlap, device_specific_validated_interaction_matrix, approved_interaction_policy. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: actual_stage_overlap, device_specific_validated_interaction_matrix, approved_interaction_policy. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `t05_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, actual_stage_overlap, device_specific_validated_interaction_matrix, approved_interaction_policy.

## T06 v2.0.0 — Staging interferences from supplied geometry

1. **ID/version:** T06 / 2.0.0.
2. **Purpose (corrected):** TMT lacks shape/surface data. Require independently validated geometry/contact engine, accurate alignment and numeric output; vendor colored UI cells alone are not portable collision evidence.
3. **Source/evidence:** [Staging interferences from supplied geometry](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 698); S04. Audit assessment: TMT lacks shape/surface data. Require independently validated geometry/contact engine, accurate alignment and numeric output;vendor colored UI cells alone are notportable collision evidence.
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, validated_3d_geometry, verified_alignment_and_staged_paths, validated_contact_engine.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: validated_3d_geometry, verified_alignment_and_staged_paths, validated_contact_engine. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: validated_3d_geometry, verified_alignment_and_staged_paths, validated_contact_engine. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `t06_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, validated_3d_geometry, verified_alignment_and_staged_paths, validated_contact_engine.

## T07 v2.0.0 — IPR timing and quantity review

1. **ID/version:** T07 / 2.0.0.
2. **Purpose (corrected):** IPR sites and quantities require approved IPR/contact plan, crown/enamel considerations, stage timing and clinician review. Never infer site or amount by summing mesiodistal displacement.
3. **Source/evidence:** [IPR timing and quantity review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 708); S06, S15. Audit assessment: IPR sites and quantities require approved IPR/contact plan, crown/enamel considerations, stage timingand clinician review. Never infer site or amount bysummingmesiodistal displacement.
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, approved_ipr_plan, enamel_and_interproximal_contacts, stage_timing, clinical_review.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: approved_ipr_plan, enamel_and_interproximal_contacts, stage_timing, clinical_review. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: approved_ipr_plan, enamel_and_interproximal_contacts, stage_timing, clinical_review. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `t07_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, approved_ipr_plan, enamel_and_interproximal_contacts, stage_timing, clinical_review.

## T08 v2.0.0 — Anchorage and root balancing review

1. **ID/version:** T08 / 2.0.0.
2. **Purpose (corrected):** Anchorage/root balancing requires staged force strategy and root/crown coordinates; virtual apex movement is not a periodontal exam. Policy mismatch only, not automatic biomechanical diagnosis.
3. **Source/evidence:** [Anchorage and root balancing review](FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) (line 718); S03, S12, S15. Audit assessment: Anchorage/root balancing requires staged force strategy and root/crown coordinates; virtual apex movement is not aperiodontal exam. Policymismatch only,not automatic biomechanical diagnosis.
4. **Audit disposition:** MORE DATA.
5. **Required fields:** orthodontist_approved_policy, staged_force_and_anchorage_strategy, crown_root_coordinates, approved_protocol.
6. **TMT-only feasibility (governing classification):** No. Even “Yes” requires independently released semantics; lexical detection is insufficient.
7. **Applicability/exclusions:** Verified rule-specific fields and compatible source/version/mode/basis/scope; otherwise abstain. Non-executable clinical preparation only: staged_force_and_anchorage_strategy, crown_root_coordinates, approved_protocol. Production always DISABLED; no approved numerical or categorical policy. Exclude: Unverified or ambiguous dependent fields, Cross-basis/mode/frame operations without verified mapping, No inference of achieved movement.
8. **Dependencies/conflicts:** None / None. Priority 50. Contradictory propositions are quarantined globally; R13/T01 must eventually deduplicate identical stage concerns.
9. **Deterministic behavior:** Non-executable clinical preparation only: staged_force_and_anchorage_strategy, crown_root_coordinates, approved_protocol. Production always DISABLED; no approved numerical or categorical policy.
10. **Implementation:** DISABLED / REQUIRED_DATA_GUARD; handler identity `t08_v2` is a registry locator, not clinical approval.
11. **Clinical review:** NOT APPROVED. Exact policy and exclusions, Orthodontist approval, Independent multi-reader case evaluation, Controlled release and rollback. No clinical approver, policy or threshold is populated.
12. **Blocker/deferral:** No approved source-specific clinical policy or released clinical validation; orthodontist_approved_policy, staged_force_and_anchorage_strategy, crown_root_coordinates, approved_protocol.
