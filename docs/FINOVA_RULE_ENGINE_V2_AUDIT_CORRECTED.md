**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

# **Finova AlignIQ  |  Corrected Clinical Rule Specification** 

_Audit-aligned v2.0 · 82 legacy IDs + 14 safeguards · NOT clinically approved_ 

**Status:** Audit-aligned engineering specification; **not clinical authorization** . 13 November 2026. 

**_Verdict:_** _GO for an internal, controlled TMT intake/descriptive interpretation prototype; NO-GO for clinical decision-support deployment or autonomous planning._ 

## **A. What changed from the original v1.0** 

This is a substantive correction of the previous 82-rule research document, not an endorsement of its originally proposed conditions. Every rule ID is preserved, but the independent audit disposition and correction now govern implementation. 

- All 82 legacy IDs retained: 49 READY engineering/observational/safety controls, 5 REVISE, 13 VALIDATE, 15 MORE DATA. 

- **READY is conditional** on real clipboard fixture verification and does not mean clinically validated. 

- **No numeric clinical threshold, attachment prescription, or staging limit ships by default.** 

- TMT total values cannot determine actual achieved movement, periodontal safety, attachments, IPR, prognosis, occlusion, sequencing or collisions. 

- Added N01–N14 cross-cutting safeguards from the audit; corrected total-vs-stage, reference-basis, comparison-mode and temporal-language defects. 

- Initial intended use: a verified _TMT interpretation and clinician review memo_ for qualified orthodontists, not a prescriptive treatment optimizer. 

## **B. Release/status interpretation** 

|**Audit status**|**Software meaning**|**Operational default**|
|---|---|---|
|**READY**|Technical gate, descriptive observation or<br>output/safety invariant with verified inputs|Implement once tested, only where fields<br>are verified|
|**REVISE**|Proposed rule wording/requirements are<br>incorrect or incomplete|Correct/merge; no unreviewed execution|
||Clinical candidate; expert must approve||
|**VALIDATE**|complete policy and evaluate representative|DISABLED|
||cases||
|**MORE DATA**|Cannot evaluate using ordinary total TMT<br>alone|CONTEXT_REQUIRED / NOT_EVALUATED|



## **C. Hard clinical and semantic boundaries** 

1. Never treat manufacturer _configuration_ values as biological safety limits (e.g. ClearCorrect staging preferences or historic Invisalign colored bands). 

2. Never convert planned values into actual movement, prognosis, risk percentage, root/bone status or optimized treatment decisions. 

3. ClinCheck plan mode (Align final / Doctor final / Comparison), notation and crown vs virtual-root basis are first-class metadata; SureSmile cumulative vs incremental, reference point and stage identifiers are distinct. 

4. A comparison/difference table is not an absolute prescription. A total table does not encode stage timing. Two rotation values cannot always be simply subtracted. 

5. Missing, unknown, unsupported, not applicable and explicit zero are distinct. A partial parse may produce independent descriptive results only for verified fields. 

6. Source/notation claims supplied by user are not evidence of source verification. Unknown vendor/version remains unverified, not auto-matched. 

7. Raw text is untrusted; protect privacy, reject unsafe instructions in pasted text and never send data to an LLM by default. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

## **D. Canonical input and evaluation contract** 

### **D1 — Provenance before interpretation** 

Capture a pseudonymous case ID, plan ID, source claim, detector result, adapter ID/version, notation, dentition, arch, source plan mode, movement scope, reference point, coordinate frame (if known), stage index (if any), raw clipboard content/hash, timestamp and operator-confirmation metadata. None of this is invented when absent. 

### **D2 — Each observed value must retain** 

- Raw row/header/cell token, literal direction code and sign, exact Decimal numerical representation, unit, source movement name/axis, normalized axis only if mapping is validated, plan/basis/stage/mode, field status, mapping ID and source line/column provenance. 

- Axis coverage mask: expected, present, unsupported, missing, explicit zero, independently observed; unknown is never zero. 

- Source-specific axis conversion; no generic label-based conversion between ClinCheck and SureSmile. 

{ 

"case_id": "demo-case-001", "plan_id": "plan-1", "source_claim": "ClinCheck", "adapter": {"id": null, "version": null, "verified": false}, 

"source_mode": "UNKNOWN", "scope": {"kind": "UNKNOWN", "stage": null}, "reference_basis": "UNKNOWN", "tooth_notation": "UNKNOWN", "measurements": [ {"raw_tooth": "13", "tooth_fdi": null, "raw_axis": "Rotation", "axis": null, "raw_value": "18 M", "magnitude_decimal": "18", "unit": "deg", "raw_direction": "M", "canonical_direction": null, "field_status": "SEMANTICS_UNKNOWN", "source_span": {"row": 4, "column": 3}} ] 

} 

_This is a schema illustration, not a verified ClinCheck serialized clipboard sample. The sample deliberately withholds tooth/direction interpretation._ 

### **D3 — Per-finding states and precedence** 

PARSE_INVALID, SEMANTICS_UNKNOWN, OBSERVED, REVIEW_ELIGIBLE, CONTEXT_REQUIRED, DISABLED, SUPPRESSED, CLINICIAN_SIGNED are **finding/evaluation states** , not a replacement for separate parsing, rule-policy and report-review state machines. 

Decision order: structural QA -> provenance/semantic eligibility -> field eligibility -> descriptive observations -> data sufficiency -> approved clinical policy -> conflicts/suppression -> authorized sign-off. Safety/abstention always outrank clinical review rules. 

### **D4 — Typed finding contract** 

{ 

"finding_id": "uuid", "rule_id": "D01", "rule_version": "2.0.0", "case_id": "demo-case-001", "tooth_id": null, "status": "SEMANTICS_UNKNOWN", "evaluated": false, "input_refs": ["row4:col3"], "observed_values": [], 

"source_metadata": {}, "policy_id": null, "evidence_ids": ["S01"], "missing_required_fields": ["tooth_notation", "direction_mapping"], 

"abstain_reason": "UNVERIFIED_SOURCE_SEMANTICS", "template_id": "needs_clarification_v1", "reviewer_status": "DRAFT" 

} 

## **E. Corrected, individual catalog of all 82 original rule IDs** 

**IMPORTANT:** The “Original proposal” below is a traceability record from v1, not authorization to implement the old trigger. The “Auditrequired implementation” paragraph supersedes the original trigger. 

### **G01–G18 • Input/data/semantic gates** 

#### **G01 — Non-empty structured input** 

**Disposition:** READY · **TMT dependence:** Yes · **Original references:** [S01], [S04] 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**Original proposal (trace only):** Needs raw clipboard payload. Proposed trigger: No tooth-movement cells or no recognizable table structure. 

**Audit-required implementation:** Sound structural gate. Define recognizable headers, minimum row/column cardinality, encoding and payload limits; an empty but valid zero-movement table must not be rejected merely for lacking nonzero values. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G02 — Reliable source identity** 

**Disposition:** READY · **TMT dependence:** Metadata · **Original references:** [S01], [S04] 

**Original proposal (trace only):** Needs source metadata / detected format. Proposed trigger: Source label unknown or conflicting with evidence in table. 

**Audit-required implementation:** Necessary but a pasted table may not identify its source; user-selected source is a claim, not verification. Confirm against signatures and make unmatched versions UNVERIFIED, not ClinCheck by default. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G03 — Tooth numbering convention** 

**Disposition:** READY · **TMT dependence:** Metadata · **Original references:** [S01], [S04] 

**Original proposal (trace only):** Needs source, numbering system, tooth IDs. Proposed trigger: Numbering convention unspecified/ambiguous (e.g. 13 means FDI vs Universal). 

**Audit-required implementation:** Critical. ClinCheck permits Universal, Palmer and FDI numbering; numeric 13 is ambiguous across systems. Require verified notation, plus arch context and a normalization lookup with exhaustive examples. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G04 — Tooth ID validity** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S01], [S04] 

**Original proposal (trace only):** Needs normalized tooth ID, dentition. Proposed trigger: Identifier outside permitted system, invalid quadrant/tooth, or unresolvable. 

**Audit-required implementation:** Sound technical validation only after notation and dentition are known. Support optional third molars, deciduous teeth, pontics and explicit unsupported identifiers; do not treat an absent row as an invalid tooth. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G05 — Arch association** 

**Disposition:** READY · **TMT dependence:** Metadata · **Original references:** [S01], [S04] 

**Original proposal (trace only):** Needs tooth ID, arch marker. Proposed trigger: A tooth ID and stated arch disagree. 

**Audit-required implementation:** Useful if the source actually provides an independent arch marker. A mismatch should quarantine an affected record rather than reinterpret its quadrant automatically. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G06 — Duplicate tooth records** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S01], [S04] 

**Original proposal (trace only):** Needs tooth + stage + plan scope. Proposed trigger: Same tooth/metric/stage repeated with inconsistent values. 

**Audit-required implementation:** Detect duplicate (case, plan, basis, scope, stage, tooth, axis) keys, not just repeated tooth numbers. Repeated columns may be legitimate plan comparisons and must not be combined. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G07 — Canonical movement label mapping** 

**Disposition:** READY · **TMT dependence:** Metadata · **Original references:** [S01], [S04] 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**Original proposal (trace only):** Needs raw movement header; source adapter. Proposed trigger: Movement label cannot be mapped unambiguously to named axis/movement. 

**Audit-required implementation:** Essential. Make an explicit adapter-specific dictionary for extrusion/intrusion, B/L, M/D, rotation, angulation and inclination. Preserve source name and axis; no generic cross-vendor conversion by label similarity alone. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G08 — Numeric, unit and precision integrity** 

**Disposition:** READY · **TMT dependence:** Yes · **Original references:** [S01], [S04] 

**Original proposal (trace only):** Needs raw numeric cell, declared unit. Proposed trigger: Non-numeric, mixed units, locale separator ambiguous, or physical units absent. 

**Audit-required implementation:** Correct engineering principle; specify decimal comma, unicode minus, empty cell, whitespace, thousands separators, exponent notation, NaN/Infinity and unexpected degree signs. Units may be implicit in a verified row header; lack of per-cell unit is not always an error. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G09 — Directional meaning verified** 

**Disposition:** READY · **TMT dependence:** Metadata · **Original references:** [S01], [S04] 

**Original proposal (trace only):** Needs source sign/direction mapping. Proposed trigger: Signed values or letter codes cannot be mapped to a known direction. 

**Audit-required implementation:** Top priority: validate letters and sign convention for each MOVEMENT axis, arch, tooth, platform and version. Direction labels for ClinCheck refer to the crown even in root basis; do not translate B inclination to lingual root torque without validated semantics. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G10 — Missing versus zero** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S01], [S04] 

**Original proposal (trace only):** Needs all movement values. Proposed trigger: Blank, dash, missing tooth, 0 and explicit no-movement are conflated. 

**Audit-required implementation:** Essential: distinguish explicit 0, blank, dash, excluded/absent tooth, and an unsupported movement field. Introduce an observed/expected axis coverage mask; nonlisted axes cannot be assumed zero. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G11 — Reference basis: crown/root/cusp** 

**Disposition:** READY · **TMT dependence:** Metadata · **Original references:** [S01], [S04] 

**Original proposal (trace only):** Needs source mode, displacement basis. Proposed trigger: Tooth basis missing or mixed when interpreting linear values. 

**Audit-required implementation:** Verified ClinCheck crown-center vs virtual-root-apex affects linear, not angular values. SureSmile crown center vs cusp tip is also distinct. Require basis metadata and disallow cross-basis arithmetic/comparisons. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G12 — Total versus stage mode** 

**Disposition:** READY · **TMT dependence:** Metadata · **Original references:** [S01], [S04] 

**Original proposal (trace only):** Needs plan stage info, cumulative/incremental. Proposed trigger: Stage-scope or comparison mode is ambiguous. 

**Audit-required implementation:** Verified SureSmile incremental/cumulative/total distinction. Total ClinCheck and last cumulative SureSmile stage are not automatically equivalent without same start/end, coordinate frame and content. No stage limits on a total-only paste. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

#### **G13 — Plan/comparison mode** 

**Disposition:** READY · **TMT dependence:** Metadata · **Original references:** [S01] 

**Original proposal (trace only):** Needs plan mode Align/Doctor/Difference. Proposed trigger: A difference/comparison view is treated as absolute planned movement. 

**Audit-required implementation:** Verified Align final, Doctor final and Comparison/difference distinction; a difference row is never the absolute programmed plan. Store plan ID and comparison operands; hold clinical rules if mode unconfirmed. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G14 — Absent/unmovable teeth** 

**Disposition:** REVISE · **TMT dependence:** Extra · **Original references:** [S03], [S04] 

**Original proposal (trace only):** Needs tooth present/absent status. Proposed trigger: Missing/excluded/fixed tooth carries movement. **Audit-required implementation:** The TMT alone cannot confirm that a tooth is absent, excluded, fixed or truly unmovable. A dash, pontic or absent column is insufficient. Only check contradictions against independently supplied verified presence/exclusion metadata. 

**Engineering migration:** Only enable consistency check when verified external tooth-status metadata exists; missing tooth columns/dashes prove nothing. 

#### **G15 — Stage ordering and identifiers** 

**Disposition:** READY · **TMT dependence:** Extra · **Original references:** [S04] 

**Original proposal (trace only):** Needs ordered stage indices if supplied. Proposed trigger: Duplicate/missing/out-of-sequence stages prevent verified timeline. 

**Audit-required implementation:** Sound only for actual stage datasets. Define indexed stages, stage zero, optional 

accommodation/overcorrection/passive stages, skipped stages, arch alignment, and duplicate handling; don't impose staged checks on total-only data. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G16 — Schema version and original evidence** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S19] 

**Original proposal (trace only):** Needs raw excerpt, normalized record, adapter version. Proposed trigger: Any output is missing source, raw evidence, rule-set version or parse provenance. 

**Audit-required implementation:** Strong provenance gate, but raw value retention and rule-version checks are system-owned metadata rather than TMT measurements. Block clinical comments for unverifiable findings; a parse-error message should still be deliverable. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G17 — Conflict and unsupported input handling** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S01], [S04], [S19] 

**Original proposal (trace only):** Needs all parsed fields. Proposed trigger: Platform fields are semantically inconsistent or adapter uncertain. 

**Audit-required implementation:** Correct fail-closed principle, yet use partial abstention: an unverified rotation must not suppress independently verified extrusion for the same case. Implement field-scoped blocking and report coverage. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **G18 — Recognized tooth types only** 

**Disposition:** READY · **TMT dependence:** Metadata · **Original references:** [S01], [S15] 

**Original proposal (trace only):** Needs dentition, FDI tooth map. Proposed trigger: Tooth type cannot be derived or user supplies primary dentition without supported pathway. 

**Audit-required implementation:** Appropriate: tooth-group logic requires verified adult/primary mapping. Distinguish permanent vs primary, mixed dentition, supernumeraries and nonteeth; avoid treating unexpected IDs as normal molars. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

### **D01–D16 • Descriptive observations** 

#### **D01 — Movement inventory per tooth** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S01], [S04] 

**Original proposal (trace only):** Needs tooth ID; all verified movement fields. Proposed trigger: One or more nonzero, verified planned movement values exist. 

**Audit-required implementation:** Accurate if strictly a report of programmed, not achieved, movements with original basis, scope, plan mode and direction. Report omitted/missing dimensions separately. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **D02 — Multiple concurrent movement types** 

**Disposition:** REVISE · **TMT dependence:** Yes _· Original references:_ * [S03], [S13] 

**Original proposal (trace only):** Needs D01 inventory. Proposed trigger: Two or more distinct movement axes are programmed in the same scope. 

**Audit-required implementation:** Rename to co-programmed movement axes, not concurrent movement. Total TMT does not show temporal overlap; simultaneity is a staging question. 

**Engineering migration:** Use term co-programmed within the same total plan. Do NOT assert concurrency; D10 and D11 should reuse this logic. 

#### **D03 — Rotation by tooth group** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S09], [S10] 

**Original proposal (trace only):** Needs rotation_deg; tooth class. Proposed trigger: Any verified nonzero rotation. 

**Audit-required implementation:** Safe tooth-group description, subject to verified numbering and rotation sign mapping. No inference that canine/premolar rotation will fail. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **D04 — Extrusion by tooth group** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S09], [S13] 

**Original proposal (trace only):** Needs vertical_mm; direction; tooth class. Proposed trigger: Any verified extrusion. 

**Audit-required implementation:** Safe description of programmed extrusion; anterior/posterior grouping must rely on tooth map, and no clinical interpretation should follow automatically. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **D05 — Intrusion by tooth group** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S09], [S11] 

**Original proposal (trace only):** Needs vertical_mm; direction; tooth class. Proposed trigger: Any verified intrusion. 

**Audit-required implementation:** Safe description of programmed intrusion. Highlighting mandibular incisors is a navigation preference, not evidence of danger. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **D06 — Crown inclination/angulation inventory** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S01], [S08] 

**Original proposal (trace only):** Needs angulation; inclination; reference definitions. Proposed trigger: One or both verified angular movements nonzero. 

**Audit-required implementation:** Keep source-specific terms inclination and angulation. ClinCheck angular values are not changed by crown/root basis selection; neither alone specifies achieved root movement or torque control. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

#### **D07 — Buccolingual translation inventory** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S01], [S08] 

**Original proposal (trace only):** Needs BL magnitude & direction; tooth class. Proposed trigger: Any verified BL translation. 

**Audit-required implementation:** Descriptive buccolingual displacement only. Neither skeletal/dental expansion nor bodily translation can be established from one-axis crown movement. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **D08 — Mesiodistal translation inventory** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S04], [S12] 

**Original proposal (trace only):** Needs MD magnitude & direction; tooth class. Proposed trigger: Any verified MD translation. 

**Audit-required implementation:** Descriptive mesiodistal displacement only. Do not infer space closure, anchorage loss, root movement or treatment speed. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **D09 — Molar distalization or mesialization indicator** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S12] 

**Original proposal (trace only):** Needs molar class; MD movement. Proposed trigger: Verified molar MD direction. 

**Audit-required implementation:** Valid molar movement label if mesial/distal convention is confirmed for that arch. Not a proof of sequential distalization or Class II correction. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **D10 — Combined rotation and vertical movement** 

**Disposition:** REVISE · **TMT dependence:** Yes _· Original references:_ * [S10], [S13] 

**Original proposal (trace only):** Needs rotation and extrusion/intrusion. Proposed trigger: Both rotation and verified vertical movement exist for same tooth. 

**Audit-required implementation:** Same-tooth rotation and vertical movement can co-exist in a total plan, but cannot be called temporally combined without stage values. Pure fact only; arguably redundant with D02. 

**Engineering migration:** Keep ID for traceability; implement via D02 shared co-programming logic, with no staging/concurrency claims. 

#### **D11 — Combined angular and translational movement** 

**Disposition:** REVISE · **TMT dependence:** Yes _· Original references:_ * [S08], [S13] 

**Original proposal (trace only):** Needs inclination/angulation; MD/BL translation. Proposed trigger: An angular movement co-occurs with translation. 

**Audit-required implementation:** The same total-vs-staged problem. Avoid implying bodily motion, root control or force-system interaction. Merge into a generic co-programming observation. 

**Engineering migration:** Keep ID for traceability; implement via D02 shared co-programming logic, no root/bodily motion inference. 

#### **D12 — Movement distribution summary** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S01], [S04] 

**Original proposal (trace only):** Needs all verified per-tooth movements. Proposed trigger: A table contains movements across one or both arches. 

**Audit-required implementation:** Count verified nonzero axes/tooth groups/arches with separate data-coverage denominators. Never sum degrees with millimeters or present case difficulty from counts. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **D13 — Opposite-side comparison (descriptive only)** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S01], [S04] 

**Original proposal (trace only):** Needs equivalent left/right tooth IDs and same scope. Proposed trigger: Corresponding teeth have different planned movements. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**Audit-required implementation:** Numerically compare paired anatomic teeth only within equivalent plan, basis and axis. Mirrored left/right signs require explicit convention; difference does not imply pathologic asymmetry. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **D14 — Missing key clinical context inventory** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S15], [S17], [S18] 

**Original proposal (trace only):** Needs source TMT and optional metadata. Proposed trigger: A fact needed by a prospective advanced rule is unavailable. 

**Audit-required implementation:** Useful data-availability report, but missing-context entries should be derived from requested decisions, not a generic exhaustive list on every paste. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **D15 — Single tooth zero movement** 

**Disposition:** READY · **TMT dependence:** Yes _· Original references:_ * [S01], [S04] 

**Original proposal (trace only):** Needs verified zero values for tooth. Proposed trigger: All supported movement axes explicitly zero in a verified scope. 

**Audit-required implementation:** Use wording 'all supported, observed axes are zero'; missing/unsupported axes and absent teeth prevent a categorical 'no movement' conclusion. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **D16 — Historical plan difference** 

**Disposition:** REVISE · **TMT dependence:** Extra · **Original references:** [S01], [S04] 

**Original proposal (trace only):** Needs two explicit comparable plans. Proposed trigger: Two plans of same tooth, basis, and movement scope available. 

**Audit-required implementation:** Two plans need same patient, tooth, starting geometry/reference, compatible coordinates, stage and movement semantics. Equal basis alone does not make two rotations/paths subtractable; compute scalar deltas only where justified. 

**Engineering migration:** Disable numeric plan deltas until same patient, verified baseline geometry and source-compatible coordinate frame and operations. 

### **R01–R16 • Candidate clinical review** 

#### **R01 — Canine/premolar rotation review** 

**Disposition:** VALIDATE · **TMT dependence:** Yes _· Original references:_ * [S09], [S10], [S08] 

**Original proposal (trace only):** Needs tooth group, verified rotation magnitude, policy. Proposed trigger: Magnitude meets clinicianapproved tooth-specific review criterion. 

**Audit-required implementation:** Review prompt is plausible because rotational predictability varies; cited studies do not establish universal canine/premolar cutoffs. Needs tooth-, platform-, basis- and intent-specific trigger, exception list and blinded case validation. **Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R02 — Rotation magnitude band by tooth type** 

**Disposition:** VALIDATE · **TMT dependence:** Yes _· Original references:_ * [S02], [S10] 

**Original proposal (trace only):** Needs tooth group, rotation magnitude, approved band set. Proposed trigger: Comparable verified movement crosses an approved category boundary. 

**Audit-required implementation:** Only acceptable as a clearly labeled clinician-selected movement-size category, never a validated risk tier. Historical Invisalign categories are not contemporary cross-platform clinical thresholds. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R03 — Anterior extrusion review** 

**Disposition:** VALIDATE · **TMT dependence:** Yes _· Original references:_ * [S09], [S13] 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**Original proposal (trace only):** Needs anterior type, verified extrusion, policy. Proposed trigger: Relevant verified extrusion matches clinician-approved check. 

**Audit-required implementation:** Potential movement review only. Anterior extrusion studies are heterogeneous; absence of attachments/staging/occlusion means no specific auxiliary recommendation or prediction. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R04 — Posterior extrusion review** 

**Disposition:** VALIDATE · **TMT dependence:** Yes _· Original references:_ * [S02], [S09] 

**Original proposal (trace only):** Needs posterior type, verified extrusion, policy. Proposed trigger: Relevant verified extrusion matches clinician-approved check. 

**Audit-required implementation:** Posterior extrusion review is a candidate; historic manufacturer colors are a poor universal basis. Require device-specific rationale and limit language to 'review planned extrusion'. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R05 — Lower incisor intrusion review** 

**Disposition:** VALIDATE · **TMT dependence:** Yes _· Original references:_ * [S11], [S09] 

**Original proposal (trace only):** Needs lower incisor, verified intrusion, policy. Proposed trigger: Intrusion meets clinician-approved review criterion. 

**Audit-required implementation:** Lower-incisor intrusion deserves focused review, but S11 includes only eight studies, seven with serious bias, and measurement heterogeneity; do not derive a 1.5/2.0 mm default cutoff or a safety flag from its summary. **Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R06 — Other intrusion review** 

**Disposition:** VALIDATE · **TMT dependence:** Yes _· Original references:_ * [S09], [S08] 

**Original proposal (trace only):** Needs tooth class, verified intrusion, policy. Proposed trigger: Intrusion exceeds a validated clinicianconfigured criterion. 

**Audit-required implementation:** Other intrusion by group is a plausible policy only; root support, occlusal objectives, staging, baseline bite and appliance details are absent. No generalized success rating. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R07 — Incisor inclination / root control review** 

**Disposition:** VALIDATE · **TMT dependence:** Partial · **Original references:** [S08], [S13] 

**Original proposal (trace only):** Needs incisor, source-specific inclination, root basis if available. Proposed trigger: Clinician-approved inclination pattern/amount present. 

**Audit-required implementation:** Risk of misinterpreting crown inclination as root torque or periodontal root risk. Without actual rootposition/geometry, allow only a conditional 'review inclination/root-control strategy' prompt approved by an orthodontist. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R08 — Mesiodistal tipping/angulation review** 

**Disposition:** VALIDATE · **TMT dependence:** Yes _· Original references:_ * [S08], [S13] 

**Original proposal (trace only):** Needs verified MD angulation, tooth type, policy. Proposed trigger: Clinician-approved MD angulation review condition met. 

**Audit-required implementation:** Angular movement is observable, but space closure and control of roots are unobserved. Require a movement-specific criterion and do not infer need for mechanics. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R09 — Posterior transverse movement review** 

**Disposition:** VALIDATE · **TMT dependence:** Yes _· Original references:_ * [S08], [S15] 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**Original proposal (trace only):** Needs posterior BL translation, tooth type, policy. Proposed trigger: Configured review criterion met. **Audit-required implementation:** Posterior buccolingual displacement may invite review; TMT is insufficient to distinguish tipping/bodily expansion, assess bone envelope or compute arch expansion. Avoid threshold masquerading as periodontal safety. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R10 — Maxillary molar distalization review** 

**Disposition:** VALIDATE · **TMT dependence:** Yes _· Original references:_ * [S12], [S03] 

**Original proposal (trace only):** Needs verified upper molar distal MD movement; policy. Proposed trigger: Movement matches approved clinician-defined review condition. 

**Audit-required implementation:** Upper molar distal movement can be identified. S12 finds very-low-certainty evidence and cannot justify cross-system anchorage or overcorrection instructions; stage/anchorage adequacy requires more data. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R11 — Molar mesialization review** 

**Disposition:** VALIDATE · **TMT dependence:** Yes _· Original references:_ * [S12], [S15] 

**Original proposal (trace only):** Needs molar mesial MD movement; policy. Proposed trigger: Movement meets approved review criterion. 

**Audit-required implementation:** Molar mesial movement can be identified, but extraction status, space closure, anchorage and root trajectory are absent. Do not prescribe control mechanics. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R12 — Complex movement combination review** 

**Disposition:** VALIDATE · **TMT dependence:** Partial · **Original references:** [S03], [S13] 

**Original proposal (trace only):** Needs D02, movement directions, tooth group, combination matrix. Proposed trigger: Combination appears in expert-approved interacting-movement matrix. 

**Audit-required implementation:** Proposed interaction matrix is unbuilt and unsupported by transferable clinical validation. Vendor antagonistic/synergistic staging settings demonstrate configurability, not a scientifically validated universal matrix. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R13 — Staged versus total movement concern** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S03], [S04], [S06] 

**Original proposal (trace only):** Needs stage context, configured movement limits. Proposed trigger: Only when per-stage values and approved limits exist. 

**Audit-required implementation:** Misclassified under TMT-only clinician rules: per-stage scrutiny requires stage-level input, a devicespecific profile and clinician approval. Merge with T01; never divide a total by stage count as a substitute. 

**Engineering migration:** Move to staged T01 module; never operate from total movement or total/stage-count division. 

#### **R14 — Clinical-context-sensitive threshold withheld** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S15], [S16], [S17] 

**Original proposal (trace only):** Needs patient clinical context; clinician policy. Proposed trigger: Review policy requires patient data absent from TMT. 

**Audit-required implementation:** Sound abstention control, not a clinical numeric threshold. Move into global data-sufficiency/safety policy; absent patient context must yield 'cannot assess', not normal/low risk. 

**Engineering migration:** Reclassify as system sufficiency/abstention control; not a numeric clinical review rule. 

#### **R15 — Attachment strategy merits review** 

**Disposition:** VALIDATE · **TMT dependence:** Partial · **Original references:** [S07], [S13], [S14] 

**Original proposal (trace only):** Needs verified movement group, approved attachment policy. Proposed trigger: Approved movementspecific attachment-review criterion met. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

##### **FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**Audit-required implementation:** Review question from movement alone is permissible only as open-ended, not as implied attachment deficiency. To check whether a required attachment is absent, acquire an actual attachment plan as in A02. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **R16 — Potential complexity of whole case** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S08], [S16] 

**Original proposal (trace only):** Needs verified findings, patient context if available. Proposed trigger: Clinician-approved rubric has all required data. 

**Audit-required implementation:** Whole-case clinical complexity requires occlusion, malocclusion, skeletal/periodontal assessment and treatment objectives. Keep disabled as case score; S15's CAT-CAT classification itself uses models, radiographs and examinations. **Engineering migration:** No whole-case complexity score from TMT; defer until full patient/geometry/clinical rubric. 

### **T01–T08 • Stage/geometry/IPR** 

#### **T01 — Per-stage movement ceilings** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S03], [S04], [S06] 

**Original proposal (trace only):** Needs per-stage magnitudes, source profile, verified configured limits. Proposed trigger: Any movement at stage k exceeds approved configured ceiling. 

**Audit-required implementation:** Valid technical comparison only with actual per-stage values, manufacturer/version profile and clinician-approved limit. ClearCorrect 0.3 mm/3 deg is a setting, not a safety limit; source profile must match. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **T02 — Cumulative/incremental consistency** 

###### **Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S04] 

**Original proposal (trace only):** Needs both cumulative and incremental for each stage. Proposed trigger: Sum of increments fails to reconcile to cumulative under defined axis conventions and tolerance. 

**Audit-required implementation:** Do not blindly sum angular increments or mixed-reference translations. Define coordinate frames and valid source operations; compare only values whose composition semantics are demonstrated, with a justified numeric tolerance. 

**Engineering migration:** No naive sums of signed rotations or mixed coordinate frames; use proven transforms only. 

#### **T03 — Maximal stages override warning** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S03] 

**Original proposal (trace only):** Needs stage count, configured policy, actual stage movements. Proposed trigger: A stage-count setting results in an observed limit exceedance. 

**Audit-required implementation:** An observed threshold exceedance can be reported if actual stage values exist, but the claim that 'maximal stages override caused it' needs staging config/history or counterfactual evidence. Rephrase as observed constraint exceedance. 

**Engineering migration:** If valid staged data and approved policy, say observed configured limit exceedance; never infer causal stagecount override. 

#### **T04 — Sequential distalization pattern review** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S03], [S12] 

**Original proposal (trace only):** Needs full stage order, molar sequence, anchorage plan. Proposed trigger: Observed order differs from clinician-approved intended protocol. 

**Audit-required implementation:** Sequence comparison needs stage-by-stage positions plus a verified intended 

distalization/anchorage protocol; total TMT has no order. No universal sequence shall be hardcoded. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **T05 — Movement overlap interaction review** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S03] 

**Original proposal (trace only):** Needs stage events per tooth, approved antagonistic/synergistic matrix. Proposed trigger: Clinicianapproved interaction constraint violated. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**Audit-required implementation:** Requires staged overlap and an expert-approved, device-specific interaction policy. A cliniciandesigned rule is not proven beneficial absent case evaluations. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **T06 — Staging interferences from supplied geometry** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S04] 

**Original proposal (trace only):** Needs validated 3D meshes/contact/interference results. Proposed trigger: Geometry tool provides measured collision/interference. 

**Audit-required implementation:** TMT lacks shape/surface data. Require independently validated geometry/contact engine, accurate alignment and numeric output; vendor colored UI cells alone are not portable collision evidence. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **T07 — IPR timing and quantity review** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S06], [S15] 

**Original proposal (trace only):** Needs approved interproximal IPR plan + tooth geometry/contacts. Proposed trigger: Patient and devicespecific approved constraints violated. 

**Audit-required implementation:** IPR sites and quantities require approved IPR/contact plan, crown/enamel considerations, stage timing and clinician review. Never infer site or amount by summing mesiodistal displacement. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **T08 — Anchorage and root balancing review** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S03], [S12], [S15] 

**Original proposal (trace only):** Needs stage plan, anchorage plan, root/crown movement data. Proposed trigger: Clinician-approved protocol finds a constraint mismatch. 

**Audit-required implementation:** Anchorage/root balancing requires staged force strategy and root/crown coordinates; virtual apex movement is not a periodontal exam. Policy mismatch only, not automatic biomechanical diagnosis. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

### **A01–A06 • Attachments** 

#### **A01 — Attachment presence audit** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S05] 

**Original proposal (trace only):** Needs attachment plan, tooth ID, stage. Proposed trigger: Attachment listed for tooth outside accepted tooth/stage mapping. 

**Audit-required implementation:** Attachment presence cannot be audited from ordinary total TMT. Need independently imported attachment-tooth-and-stage map and handle intentional removal, lingual surfaces and multiple attachments. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **A02 — Attachment-to-movement review** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S05], [S07], [S13] 

**Original proposal (trace only):** Needs clinician-approved attachment indications, measured movements. Proposed trigger: Approved indication met and planned attachment absent. 

**Audit-required implementation:** Clinician-approved indications plus actual attachment presence and stage are required to assert omission. Literature on attachment performance is heterogeneous; do not promote a movement amount into a mandatory attachment rule. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **A03 — Conflicting attachment preferences** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S03], [S05] 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**Original proposal (trace only):** Needs attachment candidate priorities, tooth type, rule set. Proposed trigger: Two approved attachment rules conflict on same tooth. 

**Audit-required implementation:** Conflict-resolution is an engine policy and only meaningful when two approved attachment proposals exist. Do not select an attachment automatically based on arbitrary priority. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **A04 — Attachment stage scheduling** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S05], [S07] 

**Original proposal (trace only):** Needs attachment start/end stages and staging plan. Proposed trigger: Planned attachment stage differs from clinician-configured timing. 

**Audit-required implementation:** Attachment timing demands start/end stage data, plan mode and stage conventions. Not part of a total TMT. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **A05 — Attachment geometry placement guard** 

**Disposition:** MORE DATA · **TMT dependence:** No · **Original references:** [S05], [S13] 

**Original proposal (trace only):** Needs 3D crowns, surfaces, attachment geometry. Proposed trigger: A proposed placement cannot be verified without surface geometry. 

**Audit-required implementation:** Correct prohibition on numerical geometry placement from a TMT. Even with meshes, 

clinical/geometry validation is necessary; make the withholding guard globally active rather than waiting for geometry input. 

**Engineering migration:** Make withholding exact placement from TMT a globally enabled safety guard; geometry-dependent placement remains separate. 

#### **A06 — Conventional vs optimized comparison** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S13], [S14] 

**Original proposal (trace only):** Needs attachment type and validated case-specific evidence. Proposed trigger: System asked to claim one shape is universally superior. 

**Audit-required implementation:** A universal-superiority claim should be blocked immediately as an output safeguard, not treated as an automatic attachment selection candidate. S14 finds no significant overall superiority; note subgroup uncertainty. 

**Engineering migration:** Reclassify as universal-superiority claim filter, always enabled, not a recommendation engine. 

### **H01–H12 • Safety/abstention** 

#### **H01 — No clinical suitability diagnosis from TMT** 

**Disposition:** READY · **TMT dependence:** Request · **Original references:** [S15], [S16], [S18] 

**Original proposal (trace only):** Needs TMT-only request. Proposed trigger: User asks if patient is safe/eligible for aligners from movement numbers alone. 

**Audit-required implementation:** Clinically appropriate scope guard. No plan suitability, diagnosis or guarantee from a movement table; visible on exported reports and API responses. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **H02 — Periodontal condition unknown** 

**Disposition:** READY · **TMT dependence:** Request · **Original references:** [S17], [S18] 

**Original proposal (trace only):** Needs periodontal examination/radiography absent. Proposed trigger: Specific plan relies on periodontal support not included in TMT. 

**Audit-required implementation:** Sound withholding guard for periodontal claims; periodontium cannot be assessed from TMT or virtual root coordinates. Do not interpret missing data as healthy periodontium. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **H03 — Root resorption/bone boundary unknown** 

**Disposition:** READY · **TMT dependence:** Request · **Original references:** [S15], [S17], [S21] 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**Original proposal (trace only):** Needs root and alveolar bone assessment absent. Proposed trigger: Requested judgment requires roots or alveolar housing. 

**Audit-required implementation:** Sound withholding guard for root resorption, root proximity and bone housing. A virtual root apex position is not a radiographic/biological risk assessment. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **H04 — Occlusal contacts not inferable** 

**Disposition:** READY · **TMT dependence:** Request · **Original references:** [S04], [S15] 

**Original proposal (trace only):** Needs occlusion/3D contacts not supplied. Proposed trigger: Asked to claim final occlusion, contact or interference from total TMT. 

**Audit-required implementation:** Sound; total movement does not show occlusal contact distribution or final bite. Neither transverse nor vertical TMT arithmetic is an occlusion simulator. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **H05 — No unseen IPR planning** 

**Disposition:** READY · **TMT dependence:** Request · **Original references:** [S06], [S15] 

**Original proposal (trace only):** Needs IPR and enamel/contact data absent. Proposed trigger: Asked to prescribe precise interproximal reduction. 

**Audit-required implementation:** Sound; even when movement suggests crowding or space creation, no IPR amount/site may be derived from total TMT alone. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **H06 — No extraction/surgery recommendations** 

**Disposition:** READY · **TMT dependence:** Request · **Original references:** [S15], [S16], [S18] 

**Original proposal (trace only):** Needs patient history, radiographs, full setup unavailable. Proposed trigger: Asked for extraction, surgical or appliance replacement decision. 

**Audit-required implementation:** Sound; do not recommend extractions, surgery, adjunctive device substitution or contraindications from TMT without full assessment. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **H07 — No predicted success probability** 

**Disposition:** READY · **TMT dependence:** Request · **Original references:** [S08], [S21] 

**Original proposal (trace only):** Needs TMT only; no validated model. Proposed trigger: Output suggests a patient-specific probability or time-to-result. 

**Audit-required implementation:** Sound. No patient-level success rate, treatment duration or risk percentage from clinical population averages or rules; any future predictor needs separate validated data and evaluation. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **H08 — No absolute attachment prescriptions** 

**Disposition:** READY · **TMT dependence:** Request · **Original references:** [S05], [S07], [S13] 

**Original proposal (trace only):** Needs movement data without approved clinical + 3D input. Proposed trigger: Asked for mandatory attachment type/size/position. 

**Audit-required implementation:** Sound; no mandatory size, orientation or tooth-surface location from movement table. Avoid 'missing attachment' claims when attachment plan unobserved. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **H09 — No claims of collision-free staging** 

**Disposition:** READY · **TMT dependence:** Request · **Original references:** [S04] 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**Original proposal (trace only):** Needs no 3D geometry and staged path. Proposed trigger: Asked whether movements are collision free. **Audit-required implementation:** Sound; cannot promise collision-free motion or safe stage transitions without 3D models and path validation. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **H10 — Monitoring and clinician sign-off** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S18], [S19] 

**Original proposal (trace only):** Needs any clinical output. Proposed trigger: A report includes patient-specific planning comments. **Audit-required implementation:** Required draft/review label and sign-off workflow. Human-review flag alone is insufficient if clinicians cannot inspect the numeric evidence and rationale. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **H11 — Context-dependent exclusions** 

**Disposition:** READY · **TMT dependence:** Request · **Original references:** [S15], [S16] 

**Original proposal (trace only):** Needs dentition, crown morphology, compliance unknown. Proposed trigger: Asked to determine appropriateness of complex intervention. 

**Audit-required implementation:** Appropriate abstention but overlaps H01-H03/H06; consolidate implementation as a contextrequirement matrix while preserving distinct audit codes. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **H12 — Privacy and data minimization** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S18], [S20] 

**Original proposal (trace only):** Needs TMT input and user-supplied metadata. Proposed trigger: Patient identifying data present when unnecessary for analysis. 

**Audit-required implementation:** Privacy guard essential but source S18 is not a jurisdiction-specific data-protection law. Require explicit PHI policy, redaction, retention, encryption, access control and no unsanctioned LLM transmission. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

### **L01–L06 • Output/sign-off** 

#### **L01 — Only rule-approved facts in comments** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S19], [S20] 

**Original proposal (trace only):** Needs structured findings. Proposed trigger: Generator proposes a new diagnosis, threshold, or intervention. 

**Audit-required implementation:** Important invariant. Prefer templates backed by typed structured findings; unconstrained LLM prose cannot be guaranteed clinically correct by prompt instructions alone. Validate/reject generated claims if any LLM is used. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **L02 — Measurement exactness** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S01], [S19] 

**Original proposal (trace only):** Needs provenance values. Proposed trigger: Comment changes tooth ID, unit, direction, stage, or rounding outside policy. 

**Audit-required implementation:** Essential deterministic token/measurement preservation: compare normalized tooth, numeric value, sign/direction, scope and basis, not approximate prose similarity. Never silently alter precision. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **L03 — Per-finding traceability** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S19] 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**Original proposal (trace only):** Needs finding ID, source ID, version. Proposed trigger: A sentence has no corresponding rule finding. **Audit-required implementation:** Require finding-to-source map for each clinical sentence; labels from literature are provenance, not evidence of a patient-specific conclusion. Keep raw display links. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **L04 — Deduplicate and resolve conflicts** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S03], [S19] 

**Original proposal (trace only):** Needs ordered findings. Proposed trigger: Rules generate duplicate or contradictory review comments. **Audit-required implementation:** Deduplicate only identical clinical propositions; retain all triggering rule IDs and source fields. Report real contradictions instead of dropping lower-priority findings silently. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **L05 — Uncertainty disclosure** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S08], [S19] 

**Original proposal (trace only):** Needs missing inputs and evidence strength. Proposed trigger: A clinical decision is unsupported or evidence is indirect. 

**Audit-required implementation:** Make unsupported/missing-context states explicit and localized to each finding; distinguish 'not evaluated' from 'evaluated and no concern flagged'. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

#### **L06 — Final clinician review status** 

**Disposition:** READY · **TMT dependence:** System · **Original references:** [S18], [S19] 

**Original proposal (trace only):** Needs report workflow and reviewer. Proposed trigger: No authorized clinician sign-off exists. 

**Audit-required implementation:** Maintain Draft -> Reviewed -> Approved or Rejected with authorized reviewer identity, timestamps, immutable version and reapproval on content changes. Approval is not delegated to the LLM. 

**Engineering migration:** Implement only under the audit conditions and the global source/field eligibility gates; do not copy the legacy trigger verbatim. 

## **F. Additional essential safeguards N01–N14** 

**N01 — Table completeness / expected coverage.** Define required headers, tooth columns, arch, expected axes and a coverage mask; partial inputs remain explicitly partial. 

**N02 — Unknown format and layout drift.** Detect unrecognized revisions, reordered and transposed variants; never silently select a closest-match adapter. 

**N03 — Case / plan identity isolation.** Use separate pseudonymous case and plan identities, protect against cross-patient and crossplan joins. 

**N04 — Unicode and raw evidence preservation.** Retain original clipboard text in controlled memory; normalize unicode minus, NBSP and decimal conventions only in derived tokens. 

**N05 — Mirrored tooth sign conventions.** Apply signed direction logic only through verified source-, tooth-, arch- and version-specific maps. 

**N06 — External tooth-status metadata.** Keep pontic, unerupted, impacted, extracted, excluded, fixed and mixed-dentition statuses from verified external data only. 

**N07 — Stage and overcorrection states.** Represent baseline/zero, active, accommodation, correction, overcorrection and passive stages explicitly. 

**N08 — Coordinate frame and composition.** Track coordinate frame, initial geometry and supported transform operations; ban unproven sum/subtraction of movements. 

**N09 — Field-scoped abstention.** Suppress only findings that depend on an unverified metric; report coverage for unaffected fields. 

**N10 — Input/output claims filter.** Treat pasted text as untrusted data; prevent unsupported advice and prompt-injection instructions from altering outputs. 

**N11 — Immutable report amendments.** Tie signed report to content, rules, source and version; revoke sign-off after material changes. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**N12 — Clinical intended purpose.** Record the requested clinical question, treatment objective and endpoint separately from movement magnitudes. 

**N13 — Rule-dependent eligibility.** Require each rule to declare source/version, required fields, valid basis, scope, plan mode, semantics and abstention outcome. 

**N14 — Incident and rollback workflow.** Before any clinical use, define error severity, incident logging, escalation, remediation and rapid rollback. 

## **G. Rule consolidation and responsibility map** 

|**Original IDs**|**v2 design decision**|
|---|---|
|**D02 / D10 / D11**|One shared co-programmed-axis observer. These are not evidence<br>movements occur concurrently. Keep legacy IDs for tracking.|
|**R13 / T01**|Single staged-context gate; R13 remains not evaluable from total<br>TMT.<br>i f|
|**R14 / G17 / N09**|Shared field-scoped sufficiency and abstention policy; no invented<br>clinical thresholds.|
|**A05 / H08**|Global guard against exact attachment placement/shape claims<br>from TMT.<br>i|
|**A06 / L01**|Output guard against unqualified attachment superiority.|
|**H01–H11**|Consolidated missing-context matrix with separate externally<br>traceable audit IDs.<br>i|
|**D16 / T02 / N08**|Enforce coordinate geometry and scientifically valid transform<br>composition; no naive subtraction/summation.|



## **H. Rule policy registry (future implementation; no clinical thresholds populated)** 

rule_id: R01 version: 0.0.0-draft name: canine_premolar_rotation_review policy_status: DISABLED clinical_approver: null approved_at: null allowed_sources_and_versions: [] allowed_modes: [] allowed_reference_bases: [] allowed_scopes: [] applicable_dentition: [] applicable_tooth_groups: [] required_fields: [verified_tooth_type, verified_rotation] params: {review_threshold_deg: null} exceptions: [] output_template_id: null evidence_ids: [S09, S10] clinical_fixture_ids: [] fallback_status: CONTEXT_REQUIRED 

A clinical rule may become active only after complete clinician-approved policy definition, case-based evaluation, formal release decision, and change-controlled versioning. A technical developer entering a numerical cutoff is **not** clinical approval. 

## **I. Testing and release gates** 

**Parser gate:** Real consented/de-identified clipboard examples from target ClinCheck and SureSmile versions, double-checked by human reviewers against the source UI; verify numbering, sign, directions, stage, crown/root/cusp reference, source mode, variants and missing fields. Supported fixtures must match the verified gold record exactly; unsupported format/version must fail explicitly. 

**Algorithmic gate:** 100% passing deterministic oracle tests for implemented rule paths, boundary/missing-value cases, duplicate/conflict tests, mirrored signs, noncommuting transform prohibitions and field-scoped abstention. Correct behavior includes explicit refusal on unsupported input. 

**Clinical gate:** Approval by qualified orthodontist(s) of each exact trigger, scope, exclusion, wording and severity, plus a preregistered independent multi-reader shadow study with adjudication, critical-miss and over-flag rate reporting. No simplistic “95% accurate” safety promise. 

**Privacy/output gate:** Injections in pasted text, PII handling, XSS/CSV formula payloads, exact numeric and directional preservation, approved templates, no unapproved model API calls, versioned clinician sign-off and review invalidation on changes. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

**Deployment gate:** Product intended use, jurisdiction-specific regulatory/legal analysis, information-security review, retention and audit policies, monitoring and incident rollback. Until then, synthetic data/internal demo only. 

## **J. Original 21-source evidence register with audit limitations** 

All statuses below describe the independent audit of the source _for high-level relevance_ , not validation of patient-specific thresholds. S06/S07/S09 were incompletely accessible and must not be treated as fully reviewed clinical authorities. 

- **[S01] ClinCheck Pro 6 User Guide: Tooth Movement Table** — Align Technology / ClinCheck user guide. https://storagy-adventcore-ppr.s3.amazonaws.com/storage/7eb29931-ffda-4e28-a15f-cb100d8db964.pdf. Audit: VERIFIED. Manufacturer / format definitions. 

- **[S02] Invisalign Quick Start Guide: ClinCheck Tooth Movement Assessment** — Invisalign (historical guideline). https://s3.amazonaws.com/storagy-gati-production-us/docs/10%20Key%20Points%20for%20Effective%20ClinCheck%20Softwar e%20Communication_emea-en-en.pdf. Audit: VERIFIED / HISTORICAL. Manufacturer / historical movement bands; NOT a current safety standard. 

- **[S03] SureSmile: Generate the staged model sequence (DIY Step 4)** — SureSmile Help. https://docs.suresmile.com/suresmile_webhelp/DIY_Aligners/DIY_Step_4.htm. Audit: VERIFIED. Manufacturer / constraints, priority and sequencing design. 

- **[S04] SureSmile: Review staged model sequence (Aligner Step 4)** — SureSmile Help. https://docs.suresmile.com/suresmile_webhelp/Aligners/Aligner_Step_4.htm. Audit: VERIFIED. Manufacturer / incremental vs cumulative, interference and staged checks. 

- **[S05] SureSmile: Using Attachments** — SureSmile Help. 

   - https://docs.suresmile.com/suresmile_webhelp/treatment_planning/Using_Attachments.htm. Audit: VERIFIED. Manufacturer / attachment workflow. 

- **[S06] ClearCorrect: Clinical Preferences** — ClearCorrect / Straumann Help. https://support.clearcorrect.com/s/article/ClinicalPreferences?language=en_US. Audit: PARTIALLY VERIFIED. Manufacturer / configurable staging, IPR and expansion preferences. 

- **[S07] ClearCorrect: Engagers (Attachments)** — ClearCorrect / Straumann Help. https://support.clearcorrect.com/s/article/engagers-also-known-as-attachments?language=en_US. Audit: PARTIALLY VERIFIED. Manufacturer / attachments and clinician review. 

- **[S08] Clear aligner therapy: scoping review of treatment prediction and limitations** — Peer-reviewed review (2026). https://pmc.ncbi.nlm.nih.gov/articles/PMC13402403/. Audit: VERIFIED ABSTRACT. Review / heterogeneous movement accuracy, limited transferability. 

- **[S09] Predictability of tooth movement with clear aligner systems** — Seminars in Orthodontics (2026). https://www.sciencedirect.com/science/article/pii/S1073874625000532. Audit: METADATA VERIFIED / FULL TEXT LIMITED. Review / type-specific predictability categories. 

- **[S10] Evaluating clinical success of rotational movements: systematic review** — Dentistry Journal (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC12564582/. Audit: VERIFIED. Systematic review / rotation and staging. 

- **[S11] Predictability of lower incisor intrusion: systematic review** — Journal of Clinical Medicine (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC12429061/. Audit: VERIFIED. Systematic review / lower incisor intrusion. 

- **[S12] Predictability of mesiodistal movement of molars: systematic review** — Angle Orthodontist (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC12422387/. Audit: VERIFIED. Systematic review / molar translation and anchorage. 

- **[S13] Clear Aligner Attachments: A Comprehensive Review** — Turkish Journal of Orthodontics (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC12485647/. Audit: VERIFIED. Review / biomechanics, attachment types and limits. 

- **[S14] Optimized vs conventional attachments: systematic review and meta-analysis** — Journal of Oral Biology and Craniofacial Research (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC12329106/. Audit: VERIFIED. Systematic review / comparative evidence. 

- **[S15] Expert consensus on clinical strategies for clear aligner treatment** — International Journal of Oral Science (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC11904224/. Audit: VERIFIED. Expert consensus / planning, constraints, patient assessment and IPR. 

- **[S16] Indications and limits of clear aligner therapy: modified Delphi consensus** — Progress in Orthodontics (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC12321729/. Audit: VERIFIED ABSTRACT. Consensus / clinical suitability and evidence gaps. 

- **[S17] Expert consensus on orthodontic treatment with periodontal disease** — International Journal of Oral Science (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC11965299/. Audit: VERIFIED. Consensus / periodontal checks require patient assessment. 

- **[S18] FDA: Clear Dental Aligners** — US Food and Drug Administration (2026). https://www.fda.gov/medical-devices/dentaldevices/clear-dental-aligners. Audit: VERIFIED. Regulator / supervised treatment and clinical context. 

- **[S19] FDA: Clinical Decision Support Software, January 2026** — US Food and Drug Administration (2026). https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software. Audit: VERIFIED. Regulator / clinician review, transparency; jurisdiction-dependent. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

- **[S20] WHO: Ethics and governance of AI for health (large multimodal models)** — World Health Organization (2024). https://www.who.int/publications-detail-redirect/9789240084759/. Audit: VERIFIED; DATE NUANCE. Governance / generative text risks and evaluation. 

- **[S21] Why digitally predicted tooth movement fails: biology-digital mismatch** — Saudi Dental Journal (2026). 

   - https://pubmed.ncbi.nlm.nih.gov/42842148/. Audit: VERIFIED. Narrative review / patient biology vs geometric plans. 

## **K. Change log / original-document correction summary** 

- v1 Clinical thresholds: withheld; no universal cutoffs inferred from historical manufacturer bands or staging preferences. 

- v1 “concurrent” language: replaced by “co-programmed” when only total TMT values exist. 

- v1 attachment/staging expectations: moved to extra-data-only modules; A06 handled as output guard. 

- v1 unknown-format behavior: fail-closed with source/version and field-level certainty, not best-effort coercion. 

- v1 absent tooth rule: requires externally verified tooth-status data. 

- v1 two-plan comparison: requires same baseline geometry and coordinate semantics; raw angular subtraction prohibited without proven operations. 

- v1 confidence language: descriptive observations are not predictions of clinical success or technical safety. 

- v2 adds N01–N14 and 3 distinct state machines (field parse, rule evaluation, report review). 

### **Release authorization** 

**Approved now:** project scaffolding, raw-text UI, future schema design and test harness. **Conditionally next:** verified parsing and descriptive facts. **Not approved:** patient-specific clinical advice, automatic attachment decisions, sequencing, risk scores or live clinical use. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

