# Finova AlignIQ — Phase 5 implementation report

Completed 14 November 2026. Engineering completion within the available evidence; **not clinical validation or authorization for patient-specific recommendations**. Phase 5 stops here.

## Governing evidence and limitations

The [independent critical audit](docs/Orthodontic_TMT_Independent_Critical_Audit(2).md), [corrected v2 specification](docs/FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) and [architecture blueprint](docs/FINOVA_ARCHITECTURE_BLUEPRINT.md) govern. Previous parser, semantic-verification, Phase 2A, Phase 3 and Phase 4 contracts were retained. The **standalone original 82-rule research document is absent** from this checkout. This was reported before dependent implementation. The corrected v2 provides original-proposal trace paragraphs for all 82 IDs; these provide traceability, not approved triggers. No missing original requirements were reconstructed as clinical policy.

Binding boundaries applied:

- Lexical scalar/label/identifier recognition never establishes vendor or clinical semantics.
- Audit/corrected definitions override historical draft triggers and numerical examples.
- Unknown/missing values never become zero, inferred direction, healthy status or a negative clinical finding.
- Descriptions concern programmed values only; total co-programming is not simultaneity, stage behavior or achieved movement.
- Crown/root/cusp, mode, scope, device version and coordinate frames remain separate. No angular subtraction, composition, stage summation or total/stage-count division.
- Extra geometry, attachments, IPR, tooth status and examination information cannot be manufactured from TMT totals.
- Clinical policies remain unapproved; neither HTTP, environment settings, the browser nor Groq can activate them. Patient cloud processing and persistence remain unavailable.
- Outputs remain **DRAFT — Requires Orthodontist Review**; no sign-off, clinical release or production privacy certification is implied.

Audit dispositions are checked against the source tables: **49 READY, 5 REVISE, 13 VALIDATE, 15 MORE DATA**, plus **14 ADDITIONAL** safeguards. READY is a document disposition, not clinical approval. The [complete inventory](docs/RULE_ENGINE_PHASE5_INVENTORY.md) has all 12 requested attributes for each of the 96 IDs. `catalog.json` records exact corrected purposes, original traces, audit assessments, source IDs/line locations and document text hashes. Those hashes use UTF-8 document text with LF newlines for checkout portability; authentic clipboard evidence hashes still use their existing exact-artifact contracts.

Source-reference access limitations remain explicit in the [approval register](docs/CLINICAL_RULE_APPROVAL_REGISTER.md): historical manufacturer guidance is not a present-day safety threshold; partially accessible or abstract-only references remain limited. Phase 5 has not independently revalidated every cited publication. No paper or vendor example supplied an active cutoff.

## Implementation status

**66 ACTIVE engineering handlers/guards; 27 DISABLED clinical predicates; 3 DEFERRED controls.** These are not 96 completed clinical algorithms. ACTIVE includes conditional required-data checks and output safeguards. Positive anatomical group/pair/stage/status examples currently require private TEST_ONLY evidence. Ordinary public pasted input remains semantically unverified.

| IDs | Behavior now |
| --- | --- |
| G01–G18 | Consume existing lexical and field-semantic gates; validate raw hash and source spans. G14 explicitly checks independently supplied movement permission; G18 requires a supplied tooth group. G15 validates actual ordered stage records when present; total-only input without stages is NOT_APPLICABLE. |
| D01–D15 | Exact nonzero/zero inventories, contextual distribution and corrected TOTAL co-programming; requested-context withholding. D03/04/05/09 add guarded group/direction descriptions. D13 compares independently paired magnitudes in compatible context, preserving both exact values, with no subtraction or pathologic-asymmetry claim. |
| D16 | DEFERRED. No trusted same-case/plan baseline geometry, coordinate/comparison operation or authorized historical-data intake. |
| R14 | Requested context-sensitive assessment withholding only. |
| R01–R13, R15–R16 | DISABLED. Individually specified prerequisites, classifications and unapproved policy parameters. Structural readiness checks for R01–R11 return no clinical predicate result. Isolated illustrative GT/GE plumbing is not a full clinical predicate. |
| T01–T08 | DISABLED prerequisite designs. Actual stage/device/configuration, geometry, contact/IPR and anchorage inputs are not reconstructed from totals. |
| A01–A04 | DISABLED. Need actual attachment-tooth/surface/stage plans, intent and approved indications/conflict/timing policies. |
| A05–A06 | Exact-placement withholding and universal-superiority wording guards only; no geometry-based placement or attachment selection. |
| H01–H09, H11 | Requested-assessment missing-data controls; no unsupported positive clinical conclusions. |
| H10, H12, L06 | Partial system controls: DRAFT status and current data-minimization/cloud gates. No authenticated sign-off, PHI detection or privacy-compliance certification. |
| L01–L05 | Closed templates, exact facts/provenance, deterministic deduplication, contradiction quarantine and localized uncertainty. |
| N01–N10, N12–N13 | Explicit expected coverage, vendor-version, capture isolation, raw evidence, pair/mirror/status/stage/frame, local uncertainty, untrusted-text and purpose/eligibility protections. N03/N04 are partial system protections: no verified patient/plan identity or byte-original browser clipboard capture. |
| N11, N14 | DEFERRED immutable authenticated amendments and incident/rollback workflows. |

Exact disabled IDs: **R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R15, R16, T01, T02, T03, T04, T05, T06, T07, T08, A01, A02, A03, A04**.

Exact deferred IDs: **D16, N11, N14**. Every other registered ID is an active engineering handler/guard, subject to its documented prerequisites and partial-system limitations. Clinical approval is **NOT APPROVED** for disabled predicates; withholding/engineering guards use **NOT APPLICABLE**, never APPROVED. The proposed clinical aspects of R14/A05/A06 also remain unapproved in the approval register.

## Architecture, order and authority

```text
Unchanged raw input / context / optional Phase 4 receipt
  → original parser or independently re-proven recovery associations
  → exact raw/source-span integrity checks
  → existing semantic assessor and code-controlled release registry
  → per-field eligible observation snapshots (Decimal + evidence)
  → deterministic rule order and rule-specific required-data checks
  → exact-fact safeguards → deduplication → contradiction quarantine
  → safety/abstention and closed language/provenance controls
  → Phase 3 Groq approved-wording choices or deterministic templates
  → output validation and local exact fact rendering
  → DRAFT report, inspectable findings and 96-rule ledger
```

No parser redesign, new public route, clinical execution switch or request-authorized semantic evidence was added. Both deterministic and recovered lexical results pass through the same semantic gates. A signed recovery receipt proves only locally rechecked structural associations, not semantics or approval. The approved vendor registry remains empty.

`execution_order` uses stable topological sorting with `(priority, rule_id)` selection after each dependency resolves. Input/provenance gates have priority 10, remaining G gates 20, prerequisite N controls 25, requested-context controls 30, descriptive predicates 40, clinical/staging preparations 50, attachment guards 70, safety/remaining protections 80 and output controls 90. Dependencies override ties: D01 follows G01/G16/G17; group observers also follow G18; D13 follows N05; R13 follows T01. Disabled R13/T01 record their potential duplicate concern for future approved policy; no stage concern executes now.

The common field snapshot enforces authorized source/version, numbering/dentition/arch, axis/unit/sign/direction, mode/basis/scope/frame and stage metadata when needed. Allowed descriptive modes are ALIGN_FINAL, DOCTOR_FINAL and the explicitly synthetic TEST_PLAN_MODE; comparison and unsupported modes do not become absolute observations. D02/D10/D11 additionally require TOTAL scope. A global invalid parse or mismatched raw digest blocks movement descriptions. Field span errors, missing semantics, incompatible context or an explicit forbidden-tooth movement block dependent positions only. Invalid actual stage sequences quarantine staged-scope observations without discarding independent TOTAL values.

Conflict resolution occurs before final DRAFT assembly. Identical descriptive propositions retain all triggering IDs, literature IDs and source references. Contradictory propositions sharing a semantic key are suppressed with a conflict ID; priority never selects a winner. Different bases/modes/scopes/frames never join. Exact authorized serialized observation snapshots prevent altered values, precision, directions or provenance from leaking through output templates.

## Extra-input and clinical preparation contracts

`review/context.py` defines tooth group/status/explicit movement permission, actual stage records, independently paired teeth and expected coverage. Their private `TestRuleContext` must be TEST_ONLY, match the exact raw/source/context digest, have Unknown source claim and independently checked synthetic semantic evidence, and be passed through the private library test switch. Mismatches are ignored as unauthorizing evidence. Duplicate/conflicting pair or coverage declarations are refused. No public HTTP field accepts this contract.

The additional-input checklist names actual attachment-tooth/surface/stage maps; initial/final crown/root geometry; validated coordinate operations; contact/enamel assessment; approved IPR plan; occlusal/periodontal/root examination; objectives/exclusions; and source device/configuration history. It is a prerequisite design, not an implemented external-data importer or evidence verifier.

`review/clinical.py` individually classifies all 30 R/T/A candidates and lists exact missing requirements and unapproved parameter names, with production_enabled=false, policy_id=null and clinical_approver=null. R12 remains an unsupported interaction proposal pending a validated matrix; R16 is not TMT-evaluable. R05/R10 readiness also withholds anatomical arch identity; no lower/upper identity is guessed from an opaque ID. Even a structurally suitable field cannot create a clinical Finding. Illustrative policies require caller-supplied Decimal boundary/unit/axis and GT/GE comparator; they return TEST_ONLY comparator results only and are never used by the engine or HTTP pipeline.

See the [feasibility matrix](docs/RULE_FEASIBILITY_MATRIX.md) for TMT-only versus additional-data classification and the [approval register](docs/CLINICAL_RULE_APPROVAL_REGISTER.md) for each proposed predicate’s evidence limits, applicability, policy gaps, review questions and activation requirements.

## Contracts and backward compatibility

Request schemas/routes are unchanged. Additional public response metadata includes finding predicate_result/approval_status/evidence_ids; observation group/additional-evidence/pair references; and ledger evaluated/triggered, input refs, execution/kind, priority and approval/source IDs. Optional/defaulted additions allow historical JSON to deserialize. Engine output advances to **0.5.0**, rule set **2.0.0-phase5**, schema version remains **1.0.0**. The frontend accepts coherent historical 0.2.0/phase2a responses as well as modern 0.5.0/phase5 responses, validating the modern 96-ID ledger. External consumers pinning old engine versions must accept the declared new version before using new output.

Legacy `evaluated` means an OBSERVED record; NOT_APPLICABLE retains evaluated=false with predicate_result=false. Withheld/disabled/suppressed results have predicate_result=null. A rule ledger can contain evaluated=true while its limiting aggregate status is unavailable because another field abstained; linked individual findings preserve that distinction. A guard’s triggered=true means the engineering guard was applied, never a clinical concern.

Generated schemas: existing review-request, draft-review, rule-definition and final-draft-report plus `clinical-preparation.v1.json`, `candidate-input-readiness.v1.json`, `additional-input-requirements.v1.json`, and private/library-design `test-only-rule-context.v1.json`. None registers a policy-activation endpoint.

The UI adds a collapsible complete rule ledger, execution/implementation/approval state, missing prerequisites and withholding reasons, source reference IDs and group provenance. It visibly states DRAFT review and that unavailable/disabled does not mean normal. Raw formatting, inert rendering, Copy Report and TXT download remain intact.

## Project structure and changed areas

```text
backend/
  app/review/
    catalog.json        audited 96-record document provenance
    registry.py         typed identity, priority, requirements and fixed execution states
    models.py           additive finding/observation/ledger metadata
    checks.py           independent raw/span and metadata checks
    context.py          private extra-evidence contracts and stage consistency
    clinical.py         disabled preparations, readiness and isolated illustrative plumbing
    service.py          guarded descriptive execution and structured abstention
    safeguards.py       exact facts, deduplication and conflict quarantine
    templates.py        closed descriptive/withholding wording
  app/reports/
    service.py          existing assembly + new descriptive grouping
    templates.py        closed alternatives and local provenance rendering
  scripts/
    build_rule_catalog.py
    build_phase5_artifacts.py
    export_schemas.py
  tests/
    test_phase5.py
    fixtures/phase5_rule_cases.json
frontend/
  src/App.tsx
  src/api/review.ts
  src/components/DraftReviewPanel.tsx
  src/Phase5.test.tsx
  src/test/fixtures/synthetic-phase5-review.json
  e2e/review.spec.ts
  package.json / package-lock.json
schemas/                response and library preparation designs
docs/
  RULE_ENGINE_PHASE5_INVENTORY.md
  CLINICAL_RULE_APPROVAL_REGISTER.md
  RULE_FEASIBILITY_MATRIX.md
examples/
  phase5-rule-matrix.md
  phase5-synthetic-finding.json
  phase5-synthetic-draft-report.json
  phase5-synthetic-draft-report.txt
RULE_ENGINE_PHASE5_REPORT.md
README.md
graphify-out/           required AST-only graph refresh
```

The original governing documents, private environment files, deployment settings, parser algorithms and vendor-release authorization are not modified. Vite was patched from 7.3.6 to 7.3.8 and Vitest from 4.1.11 to 4.1.12 after the requested dependency audit identified development-tool advisories. No major-version or feature migration was made.

## Tests and reproducibility

The hand-specified [synthetic cases](backend/tests/fixtures/phase5_rule_cases.json) define disabled/deferred ID sets, group positive/negative/zero cases and paired Decimal equality/difference independently of parser output. No vendor aliases, tooth maps or clinical cutoffs are fabricated. Private fixture construction uses the existing hash-checked synthetic mechanics only.

Validation on the completed implementation:

| Check | Result |
| --- | --- |
| Complete pytest suite | **781 passed** |
| Vitest/React Testing Library | **112 passed** |
| Playwright Chromium, real API | **40 passed**, desktop/laptop/tablet/mobile |
| TypeScript (`tsc --noEmit`, part of build) | Passed |
| Vite production build | Passed |
| `pip check` | No broken requirements |
| `npm ls --depth=0` | All declared dependencies resolved |
| `npm audit --audit-level=high` after patch | 0 vulnerabilities |
| AST-only `graphify update .` | Completed; no semantic/LLM extraction |

The new backend tests cover each of 96 IDs, exact audit disposition/source integrity, default execution states, all input-gate positive paths, dependency/priority stability, group/direction predicates, zero versus missing, paired magnitude boundaries and incompatible basis/mode/frame/unit/direction/scope, external tooth-status contradiction locality, stage ordering/duplicates/baseline/gaps and scope-local quarantine, expected coverage, unsupported modes, bound TEST_ONLY evidence, public bypass rejection, all candidate preparations, Decimal comparator boundaries, provenance tampering, exact report integration and forged-output suppression. Existing tests retain missing/unknown components, comparison abstention, source ambiguity, conflict/deduplication, disabled policies, arbitrary raw text/injections, parser-recovery receipts, mocked provider traffic and reproducibility. Frontend/browser tests retain unchanged raw input, accessible controls, no storage, error/loading states and complete copy/download behavior; new checks validate the Phase 5 contract and inspectable ledger.

The backend emits one non-failing upstream Starlette/httpx TestClient deprecation warning; Playwright emits a non-failing NO_COLOR/FORCE_COLOR environment warning. Restricted sandbox fixture access and npm DNS initially failed; tests/registry checks were rerun with normal local process/network access. No live Groq or patient-data provider call was performed in Phase 5. Test provider requests use mock transports.

PowerShell commands (installation and two-terminal startup remain in README):

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe scripts\build_rule_catalog.py
.\.venv\Scripts\python.exe scripts\export_schemas.py
.\.venv\Scripts\python.exe scripts\build_phase5_artifacts.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check

Set-Location 'C:\Finova AlignIQ\frontend'
npm ci
npm test
npm run build
npm run test:e2e
npm ls --depth=0
npm audit --audit-level=high

Set-Location 'C:\Finova AlignIQ'
graphify update .
```

## Synthetic finding and complete draft report

The complete [finding JSON](examples/phase5-synthetic-finding.json), [draft report JSON](examples/phase5-synthetic-draft-report.json), and [readable complete TXT report](examples/phase5-synthetic-draft-report.txt) use explicit **TEST_ONLY** semantics and an opaque synthetic tooth identity. Original tooth token `13` is preserved; no real anatomical meaning is inferred. An illustrative nonzero rotation describes magnitude `1.2300`, lexical scalar `-1.2300`, original cell `−1.2300 M`, group CANINE from a private toy oracle, source spans and field-level evidence. It is a descriptive finding with predicate_result=true and clinical approval NOT APPLICABLE, not an R-series trigger. All clinical predicates remain disabled in its full ledger. This is not a patient report or authentic vendor fixture.

The generator creates only explicitly synthetic checked-in examples and temporary synthetic verification artifacts; production inputs remain in memory without persistence. The complete TXT includes all descriptive comments, withholding reasons, limitations, evidence refs and the 96-rule ledger.

## Remaining vendor and clinical release blockers

Authentic ClinCheck/SureSmile captures, independently reviewed expected semantic outputs and approved releases are still **zero**. The exact sample/metadata checklist is in [vendor verification](backend/vendor_verification/README.md). Required evidence includes:

1. Each actual application/build, copy surface, locale, OS/browser and serialized layout intended for support, with consent/de-identification references and immutable raw/source-UI/expected artifact hashes.
2. Both arches and mirrored teeth, each actually supported notation/dentition, every axis/unit/literal sign/direction variant, positive/negative/unsigned/zero/missing values and precise tooth/status/group identity. No absent-column inference.
3. ClinCheck Align Final, Doctor Final and Comparison with explicit operand plan IDs/operation; crown-center versus virtual-root reference definitions per field. Do not equate root-view angles with achieved root torque.
4. SureSmile crown-center/cusp-tip variants, incremental/cumulative/total and stage-specific exports where available; baseline, intermediate/final, active/accommodation/correction/overcorrection/passive semantics, stage IDs and arch correspondence. No invented unavailable vendor variants.
5. Exact source version/mode/basis/scope/frame, baseline/endpoint definitions, original headers/tokens/precision/spans and **two independent reviews of each field assertion**, unresolved items explicitly UNKNOWN. Code-controlled release and unsupported-version rejection remain separate gates.
6. Independently verified case/plan-bound attachment maps, stage records, crown/root/3D/contact geometry, IPR plans, tooth status and clinical examinations where each candidate needs them. Future production evidence admission requires its own reviewed implementation; private TEST_ONLY context is not that infrastructure.
7. Exact versioned orthodontist-approved clinical applicability/trigger/exclusions/severity/wording, rule-specific policy parameters, preregistered multi-reader shadow study/adjudication and critical-miss/over-flag evaluation, formal controlled release and rollback. None is supplied or approved here.
8. Authenticated immutable reviewer amendments/sign-off/invalidation, incident workflows, jurisdictional intended-use/privacy/security/regulatory release review. These are not created merely by a DRAFT label or an all-passing synthetic test suite.

The missing standalone original research remains a traceability limitation for historical comparison; it does not authorize using legacy threshold fragments as policy. No clinical rule activation, live vendor processing, real-patient Groq authorization, deployment or later phase was started.

## Complete 96-rule implementation matrix

Each row refers to v2.0.0. Full per-rule purpose, evidence, fields, applicability, dependencies, expected behavior and blockers are in the linked inventory above. The following matrix distinguishes executable guards from non-executable preparations and deferred workflows.

| Rule v2.0.0 | Audited purpose | Disposition | Execution | Implementation kind |
| --- | --- | --- | --- | --- |
| A01 | Attachment presence audit | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| A02 | Attachment-to-movement review | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| A03 | Conflicting attachment preferences | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| A04 | Attachment stage scheduling | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| A05 | Attachment geometry placement guard | MORE DATA | ACTIVE | OUTPUT_GUARD |
| A06 | Conventional vs optimized comparison | READY | ACTIVE | OUTPUT_GUARD |
| D01 | Movement inventory per tooth | READY | ACTIVE | EXECUTABLE |
| D02 | Multiple concurrent movement types | REVISE | ACTIVE | EXECUTABLE |
| D03 | Rotation by tooth group | READY | ACTIVE | REQUIRED_DATA_GUARD |
| D04 | Extrusion by tooth group | READY | ACTIVE | REQUIRED_DATA_GUARD |
| D05 | Intrusion by tooth group | READY | ACTIVE | REQUIRED_DATA_GUARD |
| D06 | Crown inclination/angulation inventory | READY | ACTIVE | EXECUTABLE |
| D07 | Buccolingual translation inventory | READY | ACTIVE | EXECUTABLE |
| D08 | Mesiodistal translation inventory | READY | ACTIVE | EXECUTABLE |
| D09 | Molar distalization or mesialization indicator | READY | ACTIVE | REQUIRED_DATA_GUARD |
| D10 | Combined rotation and vertical movement | REVISE | ACTIVE | EXECUTABLE |
| D11 | Combined angular and translational movement | REVISE | ACTIVE | EXECUTABLE |
| D12 | Movement distribution summary | READY | ACTIVE | EXECUTABLE |
| D13 | Opposite-side comparison (descriptive only) | READY | ACTIVE | REQUIRED_DATA_GUARD |
| D14 | Missing key clinical context inventory | READY | ACTIVE | EXECUTABLE |
| D15 | Single tooth zero movement | READY | ACTIVE | EXECUTABLE |
| D16 | Historical plan difference | REVISE | DEFERRED | DEFERRED |
| G01 | Non-empty structured input | READY | ACTIVE | EXECUTABLE |
| G02 | Reliable source identity | READY | ACTIVE | EXECUTABLE |
| G03 | Tooth numbering convention | READY | ACTIVE | EXECUTABLE |
| G04 | Tooth ID validity | READY | ACTIVE | EXECUTABLE |
| G05 | Arch association | READY | ACTIVE | EXECUTABLE |
| G06 | Duplicate tooth records | READY | ACTIVE | EXECUTABLE |
| G07 | Canonical movement label mapping | READY | ACTIVE | EXECUTABLE |
| G08 | Numeric, unit and precision integrity | READY | ACTIVE | EXECUTABLE |
| G09 | Directional meaning verified | READY | ACTIVE | EXECUTABLE |
| G10 | Missing versus zero | READY | ACTIVE | EXECUTABLE |
| G11 | Reference basis: crown/root/cusp | READY | ACTIVE | EXECUTABLE |
| G12 | Total versus stage mode | READY | ACTIVE | EXECUTABLE |
| G13 | Plan/comparison mode | READY | ACTIVE | EXECUTABLE |
| G14 | Absent/unmovable teeth | REVISE | ACTIVE | REQUIRED_DATA_GUARD |
| G15 | Stage ordering and identifiers | READY | ACTIVE | REQUIRED_DATA_GUARD |
| G16 | Schema version and original evidence | READY | ACTIVE | EXECUTABLE |
| G17 | Conflict and unsupported input handling | READY | ACTIVE | EXECUTABLE |
| G18 | Recognized tooth types only | READY | ACTIVE | REQUIRED_DATA_GUARD |
| H01 | No clinical suitability diagnosis from TMT | READY | ACTIVE | EXECUTABLE |
| H02 | Periodontal condition unknown | READY | ACTIVE | EXECUTABLE |
| H03 | Root resorption/bone boundary unknown | READY | ACTIVE | EXECUTABLE |
| H04 | Occlusal contacts not inferable | READY | ACTIVE | EXECUTABLE |
| H05 | No unseen IPR planning | READY | ACTIVE | EXECUTABLE |
| H06 | No extraction/surgery recommendations | READY | ACTIVE | EXECUTABLE |
| H07 | No predicted success probability | READY | ACTIVE | EXECUTABLE |
| H08 | No absolute attachment prescriptions | READY | ACTIVE | EXECUTABLE |
| H09 | No claims of collision-free staging | READY | ACTIVE | EXECUTABLE |
| H10 | Monitoring and clinician sign-off | READY | ACTIVE | PARTIAL_SYSTEM_CONTROL |
| H11 | Context-dependent exclusions | READY | ACTIVE | EXECUTABLE |
| H12 | Privacy and data minimization | READY | ACTIVE | PARTIAL_SYSTEM_CONTROL |
| L01 | Only rule-approved facts in comments | READY | ACTIVE | OUTPUT_GUARD |
| L02 | Measurement exactness | READY | ACTIVE | OUTPUT_GUARD |
| L03 | Per-finding traceability | READY | ACTIVE | OUTPUT_GUARD |
| L04 | Deduplicate and resolve conflicts | READY | ACTIVE | OUTPUT_GUARD |
| L05 | Uncertainty disclosure | READY | ACTIVE | OUTPUT_GUARD |
| L06 | Final clinician review status | READY | ACTIVE | PARTIAL_SYSTEM_CONTROL |
| N01 | Table completeness / expected coverage | ADDITIONAL | ACTIVE | EXECUTABLE |
| N02 | Unknown format and layout drift | ADDITIONAL | ACTIVE | EXECUTABLE |
| N03 | Case / plan identity isolation | ADDITIONAL | ACTIVE | PARTIAL_SYSTEM_CONTROL |
| N04 | Unicode and raw evidence preservation | ADDITIONAL | ACTIVE | PARTIAL_SYSTEM_CONTROL |
| N05 | Mirrored tooth sign conventions | ADDITIONAL | ACTIVE | EXECUTABLE |
| N06 | External tooth-status metadata | ADDITIONAL | ACTIVE | EXECUTABLE |
| N07 | Stage and overcorrection states | ADDITIONAL | ACTIVE | EXECUTABLE |
| N08 | Coordinate frame and composition | ADDITIONAL | ACTIVE | EXECUTABLE |
| N09 | Field-scoped abstention | ADDITIONAL | ACTIVE | EXECUTABLE |
| N10 | Input/output claims filter | ADDITIONAL | ACTIVE | OUTPUT_GUARD |
| N11 | Immutable report amendments | ADDITIONAL | DEFERRED | DEFERRED |
| N12 | Clinical intended purpose | ADDITIONAL | ACTIVE | REQUIRED_DATA_GUARD |
| N13 | Rule-dependent eligibility | ADDITIONAL | ACTIVE | EXECUTABLE |
| N14 | Incident and rollback workflow | ADDITIONAL | DEFERRED | DEFERRED |
| R01 | Canine/premolar rotation review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R02 | Rotation magnitude band by tooth type | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R03 | Anterior extrusion review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R04 | Posterior extrusion review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R05 | Lower incisor intrusion review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R06 | Other intrusion review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R07 | Incisor inclination / root control review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R08 | Mesiodistal tipping/angulation review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R09 | Posterior transverse movement review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R10 | Maxillary molar distalization review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R11 | Molar mesialization review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R12 | Complex movement combination review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R13 | Staged versus total movement concern | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| R14 | Clinical-context-sensitive threshold withheld | READY | ACTIVE | EXECUTABLE |
| R15 | Attachment strategy merits review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R16 | Potential complexity of whole case | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T01 | Per-stage movement ceilings | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T02 | Cumulative/incremental consistency | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T03 | Maximal stages override warning | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T04 | Sequential distalization pattern review | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T05 | Movement overlap interaction review | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T06 | Staging interferences from supplied geometry | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T07 | IPR timing and quantity review | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T08 | Anchorage and root balancing review | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |

