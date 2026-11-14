# PMCEASY → Finova functional gap matrix

**Phase 6A, 14 November 2026. Research and proposed work only.** Target claims are tied to [the evidence report](PMCEASY_FUNCTIONAL_RESEARCH_REPORT.md); owning Finova references F01–F20 are in [the source audit](evidence/pmceasy-phase6a/finova-audit.md). A public demonstration is not clinical validation or our execution of the paid product. Target UI versions in recordings may differ from the current inaccessible product.

Status describes the compared capability under the stated boundary, not overall product completion. Conditional/private TEST_ONLY paths are never marked fully implemented for real vendor input. Multiple blockers may apply; each row has one primary status, with secondary blockers in its detail. Unknown target behavior is kept unknown even when a similar feature would be useful in Finova.

Complexity is a relative engineering estimate: **S** localized UI, **M** several contracts/components, **L** a validated subsystem, **XL** clinical/geometry system plus external evidence. It is not a time/cost promise. Priorities: **P0** Planning Assistant authority/evidence blocker, **P1** Planning Assistant interaction, **P2** later attachment work, **P3** later sequencing/account/product work. All proposed implementation requires review of this research first.

## Summary matrix

Gap IDs use GAP01–GAP23. They identify research gaps and are separate from the engine G-series rule IDs.

| ID | Capability | Status | Complexity | Priority |
| --- | --- | --- | --- | --- |
| GAP01 | Paste raw TMT through an explicit action | FULLY IMPLEMENTED | Existing | Preserve |
| GAP02 | Compact target-like display/run/review journey | PARTIALLY IMPLEMENTED | M | P1 |
| GAP03 | Guided modification-pass/tool navigation | NOT IMPLEMENTED | M | P1 |
| GAP04 | Adult/growing-patient tool distinction | NOT IMPLEMENTED | M UI / XL clinical | P0 policy, P1 UI |
| GAP05 | Dimension-organized CAD-comment output | PARTIALLY IMPLEMENTED | M UI / L policy | P1 |
| GAP06 | Localized tooth/group and summary findings | PARTIALLY IMPLEMENTED | Existing / L authorization | P0 |
| GAP07 | Actual CAD-change strategy comments | BLOCKED BY CLINICAL VALIDATION | XL | P0 |
| GAP08 | Whole-case/dimensional clinical reassurance | BLOCKED BY CLINICAL VALIDATION | XL | P0 boundary |
| GAP09 | Communicating selected output to external CAD | PARTIALLY IMPLEMENTED | M | P1 |
| GAP10 | Generalizing verified vendor normalization | BLOCKED BY DATA | L | P0 |
| GAP11 | Patient/plan/objective/reference context | BLOCKED BY DATA | L | P0 |
| GAP12 | Technician-comment resource library | NOT IMPLEMENTED | M / L clinical | P1/P3 |
| GAP13 | Saved favourites / membership resources | NOT IMPLEMENTED | L with auth/persistence | P3 |
| GAP14 | Functional/growing-treatment recommendations | BLOCKED BY CLINICAL VALIDATION | XL | P0 exclusion |
| GAP15 | Tooth-indexed attachment options / absence | NOT IMPLEMENTED | L | P2 |
| GAP16 | Attachment geometry/orientation/placement advice | BLOCKED BY DATA | XL | P2 |
| GAP17 | Sequencing report by arch/segment | NOT IMPLEMENTED | L | P3 |
| GAP18 | Side-specific anchorage/auxiliary advice | BLOCKED BY CLINICAL VALIDATION | XL | P3 |
| GAP19 | Collision-free/time-optimized performance claim | UNKNOWN / NOT PUBLICLY OBSERVABLE | XL if pursued | P3 / exclude claim |
| GAP20 | Per-comment edit/copy/select/share controls | UNKNOWN / NOT PUBLICLY OBSERVABLE | M if confirmed | P1 evidence |
| GAP21 | Extension / automatic CAD write-back | UNKNOWN / NOT PUBLICLY OBSERVABLE | L if justified | P3 evidence |
| GAP22 | Exact supported TMT/platform/version matrix | UNKNOWN / NOT PUBLICLY OBSERVABLE | L verification | P0 evidence |
| GAP23 | Standalone browser delivery | FULLY IMPLEMENTED | Existing | Preserve |

## Detailed gaps and prerequisites

### GAP01 — Raw paste intake

1. **Target/evidence:** Public intake captions and recorded external TMT/companion workflow; P01, V02. Exact clipboard serialization remains unobserved.
2. **Finova:** Explicit raw textarea, unchanged logical text, preview/counts/Clear/examples and confirmation; F01–F04.
3. **Missing behavior:** None for the bounded paste/action capability. This does not establish vendor normalization or PMCEASY format compatibility.
4. **Data:** Synthetic text now; authentic exports for semantic support later.
5. **Algorithms/contracts:** Existing lexical parser and original-span provenance.
6. **Clinical validation:** No clinical claim from intake. Preserve abstention.
7. **Complexity:** Existing; format expansion is separate GAP10/GAP22 work.
8. **Priority/status:** Preserve / **FULLY IMPLEMENTED** engineering capability.

### GAP02 — Display/run/review journey

1. **Target/evidence:** V01 210s directly shows multiline intake, table-display action and preview; V02 100s shows a preview and assistant action. Indexed L02 corroborates a separate attachment action. Full current live behavior remains unobserved.
2. **Finova:** Parse Table → Create draft review → Create final report are separate actions; F03.
3. **Missing behavior:** A compact guided interaction/result surface; exact action parity must await target intake/control evidence. Three calls are not evidence of equivalent decisions.
4. **Data:** Authorized control walkthrough; synthetic cases for interaction design.
5. **Algorithms/contracts:** Explicit orchestration, unchanged raw/context/receipt binding, loading/error/invalidation and deterministic fallback.
6. **Clinical validation:** UI simplification must preserve current authority/cloud gates and unavailable results.
7. **Complexity:** M.
8. **Priority/status:** P1 / **PARTIALLY IMPLEMENTED**.

### GAP03 — Guided modification passes and modules

1. **Target/evidence:** P02 and V02 90s show a pass/tool navigation concept; V01 200/280s orders module use.
2. **Finova:** One workspace with parse/review/report sections; no modification-pass selector or specialist modules; F01/F03.
3. **Missing behavior:** Reviewed navigation and task-purpose state. A modification pass must not become an inferred aligner stage.
4. **Data:** Full current menu/options and transitions; explicit user purpose rather than inferred diagnosis.
5. **Algorithms/contracts:** Purpose claim distinct from source plan mode, stage index and clinical endpoint; N12 and invalidation.
6. **Clinical validation:** Orthodontist review of intended use, branching and exclusions before clinical routing.
7. **Complexity:** M.
8. **Priority/status:** P1 / **NOT IMPLEMENTED**.

### GAP04 — Adult/growing-patient distinction

1. **Target/evidence:** V01 200/280s and V02 90s show separate entries; one recorded sequencer branch is unavailable. This is historical UI evidence, not current entitlement.
2. **Finova:** No growth-status intake or patient-class routing; F01/F12.
3. **Missing behavior:** Both the interface claim and a validated clinical eligibility contract. Dentition or tooth number cannot establish growth status.
4. **Data:** Verified patient/growth context, examination and versioned tool applicability; target current availability.
5. **Algorithms/contracts:** Explicit class provenance, unknown/unsupported states and branch-specific required fields.
6. **Clinical validation:** Independent approved adult/growing policies; no inherited functional-treatment advice.
7. **Complexity:** M interface; XL clinical scope.
8. **Priority/status:** P0 policy/P1 UI / **NOT IMPLEMENTED**.

### GAP05 — Dimension-organized feedback

1. **Target/evidence:** V02 120s shows sagittal/transverse/vertical output rows containing CAD-directed text.
2. **Finova:** TOOTH/SUMMARY/UNAVAILABLE report sections and exact finding provenance; no equivalent dimension view; F14/F15.
3. **Missing behavior:** An independently designed grouped view and approved category-to-finding contract. A cosmetic axis table would not authorize its content.
4. **Data:** Canonical axis definitions, compatible reference/mode/scope, target output grouping examples.
5. **Algorithms/contracts:** Conditional D-series grouping, immutable finding IDs and field-local missing prerequisites.
6. **Clinical validation:** Descriptive grouping can remain synthetic/descriptive; modification directives require GAP07 approval.
7. **Complexity:** M UI; L policy integration.
8. **Priority/status:** P1 / **PARTIALLY IMPLEMENTED**.

### GAP06 — Localized and summary comments

1. **Target/evidence:** V02 120s has localized tooth/group content within an axis row; whole-case-style content also appears. This does not prove one row per tooth.
2. **Finova:** D01–D15 conditional descriptions, tooth/summary report grouping and extra-evidence TEST_ONLY guards; public input produces no authorized movement facts; F06–F10/F15.
3. **Missing behavior:** Real vendor authorization and appropriate approved non-descriptive policies. Preserve the distinction between target localization and a target tooth-by-tooth UI, which is unobserved for Planning Assistant.
4. **Data:** Authentic numbering/groups, axes, directions, basis/mode/scope/frame and any dependent clinical context.
5. **Algorithms/contracts:** D-series now; exact per-field adapters, R-series only after approval.
6. **Clinical validation:** Exact-wording/source trace and clinically approved applicability for suggestions.
7. **Complexity:** Existing framework; L evidence/adapter work.
8. **Priority/status:** P0 / **PARTIALLY IMPLEMENTED**.

### GAP07 — CAD modification strategy

1. **Target/evidence:** V02 120s visibly contains sagittal/transverse changes, IPR, auxiliary and root-control language; V02 150s later shows matching CAD text.
2. **Finova:** Reports are descriptive/withholding; all relevant R/T clinical candidates remain disabled; F11/F13/F16.
3. **Missing behavior:** Authorized clinical decision predicates and instructions. No demo number is an approved cutoff or overcorrection policy.
4. **Data:** Verified semantics, objectives, anatomy/examination, extraction/space/periodontal/root context, approved IPR and force strategy where applicable.
5. **Algorithms/contracts:** R07/R09–R11/R14–R16, T07/T08, H03/H05/H11 and N08/N12; new policies only if justified by the audited approval process.
6. **Clinical validation:** Rule-specific orthodontist-approved triggers/exclusions/wording plus independent adjudicated shadow evaluation and controlled release.
7. **Complexity:** XL; not an LLM prompt change.
8. **Priority/status:** P0 / **BLOCKED BY CLINICAL VALIDATION**, also data/implementation blocked.

### GAP08 — Clinical reassurance

1. **Target/evidence:** V02 120s contains a dimensional predictability reassurance. Its supporting context, policy and clinical validity are unknown.
2. **Finova:** Unknown values do not mean normal; R14/R16/H safeguards withhold such conclusions; F10/F11/F14.
3. **Missing behavior:** No plan to imitate unsupported reassurance. Equivalent justified behavior would need a separately validated endpoint and sufficiency criteria.
4. **Data:** Defined intended assessment, full required clinical context and measured validation outcomes.
5. **Algorithms/contracts:** R14/R16/H01/H07/N01/N12; no inference from counts, zeros or lack of flags.
6. **Clinical validation:** Exact patient-specific claim approval; never transfer marketing predictability language as a safety statement.
7. **Complexity:** XL.
8. **Priority/status:** P0 boundary / **BLOCKED BY CLINICAL VALIDATION**.

### GAP09 — Transfer to external CAD communication

1. **Target/evidence:** P01 instructs CAD communication; V02 120→150s shows matching text in output then external CAD. Transfer mechanism is not established.
2. **Finova:** Whole-report clipboard copy and TXT download work in source/tests; no CAD action; F17/F20.
3. **Missing behavior:** A compact technician-facing export/selection design, if confirmed useful. Do not call an automatic CAD integration missing parity when target automation is unknown.
4. **Data:** Authorized target transfer walkthrough and clinician workflow requirements; synthetic export cases.
5. **Algorithms/contracts:** Finding-bound selected export, original/edited text separation, draft/provenance retention and invalidation.
6. **Clinical validation:** Export cannot upgrade unverified or clinician-edited text into engine-approved advice.
7. **Complexity:** M for a local export flow; direct CAD integration would be separate L work.
8. **Priority/status:** P1 / **PARTIALLY IMPLEMENTED**.

### GAP10 — Generalizing vendor semantic normalization

1. **Target/evidence:** External CAD/TMT is shown in V02, but PMCEASY’s actual convention mappings and vendor matrix are not exposed.
2. **Finova:** Empty vendor registry; exact-curated-fixture projection only; public routes supply no checked oracle; F05–F08.
3. **Missing behavior:** Reviewed **generalizing source/version adapters and production evidence admission/lookup**, as well as authentic fixtures. Adding a digest or environment flag is insufficient.
4. **Data:** Independently dual-reviewed consented/de-identified exports across notation, dentition, directions, locale, mode, basis, scope, stage and unsupported versions.
5. **Algorithms/contracts:** Deterministic versioned adapters, field provenance/status, partial abstention and fail-closed drift handling.
6. **Clinical validation:** Semantic/source review and formal code-controlled release; separate from approving clinical rules.
7. **Complexity:** L.
8. **Priority/status:** P0 / **BLOCKED BY DATA**, plus unimplemented adapter/admission work.

### GAP11 — Verified context beyond table values

1. **Target/evidence:** Demonstrated advice depends on concepts beyond magnitudes; whether off-screen context was supplied is unknown. No inference that PMCEASY uses TMT alone is made.
2. **Finova:** Context claims are unverified; private TEST_ONLY tooth/group/stage/pair/coverage contracts are not production verifiers/importers; F12.
3. **Missing behavior:** Case/plan/objective-bound independently verified external evidence admission.
4. **Data:** Status/exclusions, growth, plan identity, clinical objectives, attachment/stage plans and geometry/examinations appropriate to each dependent claim.
5. **Algorithms/contracts:** G14/G18, N01/N03/N05–N09/N12/N13; explicit evidence status and incompatible-context refusal.
6. **Clinical validation:** Define genuine sufficiency per intended decision; no default from absence or a checkbox.
7. **Complexity:** L.
8. **Priority/status:** P0 / **BLOCKED BY DATA**.

### GAP12 — Technician-comment resource library

1. **Target/evidence:** P04/L01 advertise a library; V02 90s shows dimensional/manual content links. Individual library entries/search behavior are not observed.
2. **Finova:** Closed generated report templates, not a browsable educational/technician library; F16/F17.
3. **Missing behavior:** An independently authored, evidence-reviewed content taxonomy and resource interaction; never copy the target library.
4. **Data:** Authorized target observation for navigation and licensed/independent reviewed content for Finova.
5. **Algorithms/contracts:** Provenance, versioned content, applicability/exclusions and distinction from generated case findings.
6. **Clinical validation:** Clinical statements and template indications require qualified review even without dynamic triggers.
7. **Complexity:** M interface, L content governance.
8. **Priority/status:** P1 investigation/P3 broad library / **NOT IMPLEMENTED**.

### GAP13 — Favourites and member resources

1. **Target/evidence:** P05/P06 advertise saved resources and educational/troubleshooting access; save/retrieve behavior unobserved.
2. **Finova:** No authentication, saved favourites, case persistence or resource portal; F17/F20.
3. **Missing behavior:** These account surfaces, if later justified; not necessary to the initial independent planning workflow.
4. **Data:** Entitled target walkthrough, retention/access requirements and independently authored content.
5. **Algorithms/contracts:** Future identity/authorization, versioned resources, minimal retention and deletion policies.
6. **Clinical validation:** Content governance and privacy/security review; a favourite is not clinical approval.
7. **Complexity:** L with auth/persistence; intentionally outside current work.
8. **Priority/status:** P3 / **NOT IMPLEMENTED**.

### GAP14 — Functional/growing-treatment advice

1. **Target/evidence:** P01 advertises functional support; recorded menus distinguish growing patients. Full questionnaires, outputs and current availability are unobserved.
2. **Finova:** No growth/functional decision module; ordinary TMT has no diagnostic eligibility; F11/F12/F20.
3. **Missing behavior:** A defined intended-use/data contract and validated branch-specific policy, not a renamed menu.
4. **Data:** Growth/skeletal/occlusal examination, treatment objectives and appliance/auxiliary context.
5. **Algorithms/contracts:** R14/R16/H01/H04/H11/N12; only add a new rule family after evidence/policy review.
6. **Clinical validation:** Specialist approval and independent evaluation; no assumptions from mixed dentition or age alone.
7. **Complexity:** XL.
8. **Priority/status:** P0 exclusion / **BLOCKED BY CLINICAL VALIDATION**.

### GAP15 — Attachment options and absence rows

1. **Target/evidence:** V01 220/240s and V02 330s show tooth-indexed textual candidates, alternatives and explicit no-attachment output.
2. **Finova:** No attachment result model, choice table or module UI; A-series registry entries are not this interface; F18.
3. **Missing behavior:** Both result presentation and authorized indication logic. A no-attachment statement is a clinical assertion, not missing data.
4. **Data:** Actual attachment-tooth/surface/stage plan, verified tooth identity, source naming/geometry and approved indications.
5. **Algorithms/contracts:** R15/A01–A04; preserve alternatives, absence versus unknown, provenance and abstention.
6. **Clinical validation:** Exact indication/omission/alternative policies, exclusions and comparison evidence; A06 blocks universal superiority.
7. **Complexity:** L UI/contracts; clinical data/policy also blocked.
8. **Priority/status:** P2 / **NOT IMPLEMENTED**.

### GAP16 — Attachment geometry and placement

1. **Target/evidence:** Recorded rows contain dimension, orientation, bevel/location and optimized-option language. No dedicated companion 3D geometry engine was seen.
2. **Finova:** A05 withholds exact placement; no crown mesh, surface anchor or attachment geometry contract; F18.
3. **Missing behavior:** Verified geometric representation, placement feasibility and clinically approved output. A synthetic diagram can demonstrate UI only.
4. **Data:** Crown/root/reference geometry, actual attachment catalogue/design, placement surfaces and stage-bound plan.
5. **Algorithms/contracts:** Geometry IDs/units/frame, candidate/alternative relation, A05/H08/N08 safeguards and separately validated placement checks.
6. **Clinical validation:** Geometry/clinical validation before dimensions/orientation/placement become patient recommendations.
7. **Complexity:** XL.
8. **Priority/status:** P2 / **BLOCKED BY DATA**, also clinical validation.

### GAP17 — Sequencing report

1. **Target/evidence:** V01 330s shows arch/segment sequencing statements. A numbered stage timetable/export was not observed.
2. **Finova:** No sequencing output/UI/optimizer; StageRecord only validates supplied toy sequence data; F19.
3. **Missing behavior:** A typed textual sequencing report and authorized strategy logic. Do not require an invented target timeline for parity.
4. **Data:** Actual staged values, identifiers/kinds/arch correspondence, intended sequence and source device/configuration profile.
5. **Algorithms/contracts:** G15/N07, R13/T01–T05/T08 and N08; composition only with validated operations.
6. **Clinical validation:** Source-/device-specific approved staging strategy and independent case evaluation.
7. **Complexity:** L presentation; XL clinical subsystem.
8. **Priority/status:** P3 / **NOT IMPLEMENTED**.

### GAP18 — Anchorage and auxiliaries

1. **Target/evidence:** V01 330s has separate side-specific anchorage notes, including prescriptive auxiliary details and a negative-need statement.
2. **Finova:** No anchorage/force strategy engine; T08/H11 withhold; F11/F19.
3. **Missing behavior:** A defensible clinical strategy contract and policy. Do not reproduce the demonstration’s amounts, timing or absence claims.
4. **Data:** Clinical objectives, root/support/occlusal context, staged force/anchorage strategy and approved appliance protocol.
5. **Algorithms/contracts:** T08/R10/R11/R14/H11/N12; no inference from movement totals.
6. **Clinical validation:** Orthodontist-approved indications, contraindications and exact wording with adjudicated evaluation.
7. **Complexity:** XL.
8. **Priority/status:** P3 / **BLOCKED BY CLINICAL VALIDATION**.

### GAP19 — Collision and treatment-time claims

1. **Target/evidence:** P01 advertises benefits. No actual collision proof, simulation, optimization objective, stage allocation or duration validation was observed.
2. **Finova:** No collision/contact engine or duration prediction; H07/H09 withhold; F19.
3. **Missing behavior:** The target’s implementation/performance is unknown. Do not convert a claim into a parity acceptance test.
4. **Data:** Validated 3D paths/contact geometry and outcome evidence if this scope is later approved.
5. **Algorithms/contracts:** T02/T06/T08 plus validated transform/contact models, not scalar table arithmetic.
6. **Clinical validation:** Separate technical geometry and clinical/outcome studies; never claim safety from no detected issue.
7. **Complexity:** XL.
8. **Priority/status:** P3/exclude unsupported claim / **UNKNOWN / NOT PUBLICLY OBSERVABLE**.

### GAP20 — Per-comment controls and sharing

1. **Target/evidence:** Sampled output/transfer frames do not establish edit/select/copy buttons, reusable links, PDF or save semantics.
2. **Finova:** Whole-report copy/TXT exists; no per-comment editing/selection, sign-off or shared links; F17.
3. **Missing behavior:** Target control observation first. Finova improvements would currently be independent UX proposals, not proven target parity gaps.
4. **Data:** Entitled/current control walkthrough including error/invalidation behavior; synthetic UX cases.
5. **Algorithms/contracts:** Immutable engine result versus clinician-authored amendment, source links and draft invalidation.
6. **Clinical validation:** Editing must not imply engine approval; authenticated sign-off is a separate N11/L06 workflow.
7. **Complexity:** M local UX; L authenticated sharing/sign-off.
8. **Priority/status:** P1 evidence / **UNKNOWN / NOT PUBLICLY OBSERVABLE**.

### GAP21 — Extension or automatic CAD integration

1. **Target/evidence:** P04/P05 and V02 support website/manual-companion use. Side-by-side windows/matching text do not prove an extension or automated API.
2. **Finova:** Standalone SPA/API, no extension/injection/CAD write-back; F20.
3. **Missing behavior:** None can be specified as target parity until an actual integration is observed and authorized.
4. **Data:** Official supported integration documentation and authorized action trace; vendor API/licensing boundaries.
5. **Algorithms/contracts:** Only then consider explicit user-controlled export/integration with audit/invalidation; no browser scraping assumptions.
6. **Clinical validation:** Preserve clinician review and source/plan binding for any write operation.
7. **Complexity:** L if justified.
8. **Priority/status:** P3 evidence / **UNKNOWN / NOT PUBLICLY OBSERVABLE**.

### GAP22 — Supported input formats and source versions

1. **Target/evidence:** A TMT is advertised/demonstrated, but no authoritative format/version/locale matrix or authentic clipboard fixture was acquired. ClinCheck is visibly used in a recording; SureSmile support was not independently established.
2. **Finova:** Generic lexical orientations/delimiters and abstention work; no verified ClinCheck/SureSmile semantics; F04–F08.
3. **Missing behavior:** An evidence-backed target support list and Finova’s own independently verified support matrix. Do not conflate the two.
4. **Data:** Original de-identified clipboard artifacts with source UI/version, mode/basis/scope and dual-reviewed semantic assertions.
5. **Algorithms/contracts:** Versioned deterministic adapters and drift fixtures, Decimal/raw provenance and explicit unsupported cases.
6. **Clinical validation:** Semantic verification first, clinical policy separately. A video pixel table is not a clipboard oracle.
7. **Complexity:** L.
8. **Priority/status:** P0 evidence / **UNKNOWN / NOT PUBLICLY OBSERVABLE**.

### GAP23 — Standalone browser delivery

1. **Target/evidence:** Public website entry, subscription terms and online-device claims; P03–P05.
2. **Finova:** React/Vite standalone workspace and FastAPI backend; F01/F20.
3. **Missing behavior:** None for this delivery class. No assertion of equal hosting, entitlement, service reliability or clinical function.
4. **Data:** Existing local application; hosted deployment health was not checked in this phase.
5. **Algorithms/contracts:** Existing web/API boundary; no extension required for the observed companion pattern.
6. **Clinical validation:** Delivery architecture grants no clinical authority.
7. **Complexity:** Existing.
8. **Priority/status:** Preserve / **FULLY IMPLEMENTED** architectural capability.

## Independent implementation findings

The fresh [local probes](evidence/pmceasy-phase6a/finova-local-probes.json) preserve raw text/Decimal precision for rows, columns and Markdown, abstain on unsupported unanchored input, retain the 96-rule ledger and reject trust-injection fields. Public-style inputs remain UNVERIFIED, with zero eligible observations and no provider calls. Registry counts are 66 active engineering guards/handlers, 27 disabled clinical predicates and 3 deferred controls—not clinical completion.

The reported Phase 5 781/112/40 test counts were not rerun here and are not used as proof of every feature. Actual source and bounded library probes ground this matrix. No hosted health, live provider, current paid target or new HTTP/browser test success is claimed. Remaining implementation order and acceptance criteria are in [the roadmap](PMCEASY_RECONSTRUCTION_ROADMAP.md).
