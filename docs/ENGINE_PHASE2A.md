# Phase 2A: deterministic draft descriptive review

Implemented for internal synthetic development only. **Prototype — not for clinical use.** No authentic vendor captures or approved vendor semantic releases exist. No clinical decision predicate is enabled. Stop after Phase 2A; Phase 2B requires separate review.

All three complete documents and tables in `docs/`, `PARSER_PHASE1.md`, `PARSER_PHASE1_5.md`, the five existing JSON schemas and the complete parser/semantic implementation were reviewed before changes. The audit/corrected v2 dispositions govern this implementation. No required document was missing or unreadable; the supplied audit is Markdown. Those documents, existing parser/semantic implementation, vendor catalog/release registry and existing JSON schemas are unchanged.

## Architecture and trust boundary

```text
RawTMTSubmission + optional explicit assessment-question codes
  -> existing private intake and synthetic-only confirmation
  -> existing deterministic lexical parser (unchanged)
  -> existing semantic assessment, with registry authorization rechecked
  -> per-field applicability/required-input checks and parser-gate reporting
  -> verified-only descriptive observers / requested-context abstentions
  -> disabled clinical/staging/attachment registry entries (no predicates)
  -> closed templates, exact source snapshots, deduplication, conflict quarantine
  -> deterministic content-addressed DRAFT report -> clinician inspection UI
```

New package `backend/app/review/`: `models.py` contracts, `registry.py` versioned catalog/topological dependency checks, `service.py` evaluation, `templates.py` context matrix/closed wording, `safeguards.py` output validation and consolidation. Plain Python/Pydantic; no rule framework or new dependencies.

`review_table()` accepts raw submissions, not client-supplied canonical measurements or semantic assessments. It calls both existing layers itself. A library caller may provide an exact `CheckedFixture`; the existing code-controlled release registry still decides authority and rejects mismatched/revoked evidence. There is no HTTP fixture path, verification flag, arbitrary policy, threshold, release override or test-only switch. The endpoint currently has no vendor mapping resolver, so every pasted input remains semantically unverified. Adding a future general adapter and evidence resolver is a separate reviewed change, not automatic activation by modifying a manifest.

Development tests explicitly pass **SYNTHETIC / TEST_ONLY** fixtures through the existing verifier with the library-only test flag. Test source/notation/tooth/direction conventions are invented and labeled. `TEST_ONLY` never becomes `VERIFIED` or a vendor release. Test observations retain TEST_ONLY provenance, have no verified report-level tooth ID, and cannot enable clinical analysis. Tests using canonical axis names define the meaning for that exact invented fixture; they are not ClinCheck/SureSmile dictionaries.

## Eligibility and deterministic behavior

Each observation requires all existing required semantic components: exact source/version, tooth identity/notation/dentition/arch, axis, unit, sign/direction, mode, basis, scope and coordinate frame; staged scopes additionally require stage index/kind. Zero stage is retained. Comparison data requires its source semantics but is still excluded from absolute-programmed-movement descriptions. The Phase 1.5 layer remains conservative about reference-basis completeness; this phase does not weaken it for angular fields or imply angular values change with basis selection.

Lexical missing/invalid/unsupported/ambiguous/duplicate fields cannot produce observations. Unknown numeric values never become zero. A zero alone never proves direction or tooth identity. Independent eligible fields remain observable when siblings abstain; all-zero inventory is withheld when a sibling is unknown. Expected coverage remains unknown, and absent tooth columns prove no tooth status.

G rules **consume** existing parser issues/status and semantic components; they do not implement another tokenizer, tooth map or numeric parser. G05 reports existing arch eligibility and quarantines conflicts; it never invents an independent arch marker. G14/G18 lack verified external tooth-status/group contracts and remain unavailable. G15 does not impose stage-order checks on total-only input. One stage value is not a timeline.

Dependencies are topologically ordered with stable tie-breaking; missing dependencies, duplicate IDs and cycles fail closed. D02/D10/D11 depend on D01's eligible nonzero inventory and share grouping/observation logic. A failure in one measurement does not globally block unrelated fields. Aggregated rule statuses report the limiting state while individual findings retain partial successes and abstentions.

Grouping is within **one exact capture**, using source/version, canonical tooth, notation/dentition/arch, mode, reference basis, scope, stage kind/index, coordinate frame and comparison context. There is no cross-case/plan join or imported plan arithmetic. D12 drops only tooth/arch from that key to count their distribution and reports coverage denominators separately. No magnitudes are summed, and counts do not imply difficulty. D02/D10/D11 apply only within the same TOTAL context and say **co-programmed**; simultaneity is unknown.

Output validation checks the closed rule/template contract, exact authorized serialized measurement snapshots (including Decimal precision, raw values, semantic components and source spans), source references, canonical tooth IDs and allowed descriptive conditions. Identical propositions merge with all triggering IDs and provenance. Contradictions are retained as SUPPRESSED conflict records, with references and no descriptive claim; no arbitrary priority winner is chosen. Different reference bases never join. Literature IDs are not fabricated as patient-specific evidence; accepted evidence references point to the actual fixture/release/locator. Audit evidence citations remain in the supplied source documents.

No current time, UUID, random order, external service, patient persistence or logging participates in evaluation. Finding IDs and the complete report ID derive from canonical serialized content. Same input/evidence/rules/questions reproduces byte-identical JSON. Material changes yield a new DRAFT identity; no signed report lifecycle is implemented.

## Exact rule disposition

All **96 IDs** (82 legacy plus N01–N14) are retained at rule version **2.0.0**, rule-set version **2.0.0-phase2a**, engine version **0.2.0**. The registry contains nullable policy/approval/threshold fields, all null, without an enable mechanism.

| IDs | Implemented behavior / remaining boundary |
| --- | --- |
| G01–G13, G16–G17 | Active reporting of existing lexical/semantic gates and field-scoped sufficiency. This is delegated validation, not new vendor verification. |
| G14 | Deferred consistency predicate: independently verified presence/exclusion/fixed-tooth data and a reviewed input contract are absent. |
| G15 | NOT_APPLICABLE without staged input; otherwise unavailable pending a real ordered stage dataset and convention. No ordering predicate. |
| G18 | Deferred tooth-group eligibility: no verified anatomical group-map contract. |
| D01 | Nonzero source-reported programmed inventory, preserving mode/basis/scope/direction/provenance. |
| D02, D10, D11 | Shared total-plan co-programming observer. Matching specializations merge their original IDs into D02 output. |
| D06–D08 | Canonical source inclination/angulation, buccolingual and mesiodistal inventories, with explicit nonclaims. No bodily/root/expansion/anchorage inference. |
| D12 | Counts eligible nonzero positions, distinct axes/teeth/arches by compatible context; separate eligible/global coverage denominators. |
| D14 | Missing-context inventory only for explicitly requested assessment codes; no generic exhaustive clinical-context list on each paste. |
| D15 | “All supported, observed axes are explicitly zero”; never “no movement.” Unknown siblings prevent this observation. |
| D03–D05, D09 | Deferred group descriptions: verified tooth-group/anatomical mapping absent. Generic eligible inventory still works. |
| D13 | Deferred paired comparison: verified anatomic pairing and mirrored conventions/valid operations absent. |
| D16 | Deferred deltas: same-patient baseline geometry, comparable coordinates and demonstrated operations absent. No subtraction. |
| R01–R13, R15–R16 | DISABLED. No orthodontist-approved clinical policies, predicates, thresholds or severity/risk bands. R13 also needs staged data; R16 requires full clinical context. |
| R14 | Active **system abstention only**, as corrected by audit. Not a clinical decision predicate or threshold. |
| T01–T08 | DISABLED. Need separately validated stage/geometry/IPR/anchorage data, composition operations and approved policies; no numeric ceilings. |
| A01–A04 | DISABLED. Need actual attachment plans, stages, geometry where relevant and approved policies. |
| A05, A06 | Active global withholding/output guards only: no exact attachment placement and no universal superiority claim. Geometry-dependent placement remains disabled. |
| H01–H09, H11 | Active consolidated requested-context matrix; retain distinct audit IDs. No conclusion follows from absent context. |
| H10 | DRAFT, clinician-review label and inspectable numeric/evidence trail. Authenticated sign-off/monitoring deferred. |
| H12 | Existing synthetic-only/private intake, bounded bodies, sanitized errors, no-store/in-memory/no third-party handling. No PHI detection/redaction, production encryption/access/retention certification. |
| L01–L05 | Closed facts/templates, exactness, traceability, explicit conflict/dedup and localized uncertainty controls. No LLM. |
| L06 | DRAFT-only state enforced. Reviewed/Approved/Rejected transitions require future authenticated, immutable workflow. |
| N01–N05, N07–N10, N12–N13 | Active bounded protections: disclose unknown coverage/layout/version; one-capture isolation; raw Unicode spans; verified-only signs/stage states; no composition; local abstention; untrusted text stays data; explicit requested purpose; rule eligibility. No new vendor maps or staged/clinical operation. |
| N06 | External tooth status required; unknown statuses withheld, never inferred. Import/contradiction predicate deferred. |
| N11, N14 | Deferred signed amendment and incident/rollback workflows. No sign-off or clinical deployment is offered. |

“Active” here describes engineering/synthetic paths, not vendor compatibility or clinical authorization. Registry entries with additional-data status still return explicit unavailable assessments.

## HTTP and output contract

New route **POST `/api/v1/tmt/observations`**. Existing `/api/parse` and `/api/health` remain unchanged; the historical health `phase: 1` field is retained for compatibility. Public documentation endpoints remain disabled.

The request extends the same strict raw submission with `requested_assessments: []` (optional). Supported question codes: SUITABILITY, PERIODONTAL, ROOT_BONE, OCCLUSION, IPR, EXTRACTION_SURGERY, PROGNOSIS, ATTACHMENTS, COLLISIONS, COMPLEX_INTERVENTION. These request an explanation of unavailability, never authorize a treatment decision. Duplicate/unknown codes, client verification flags and arbitrary extra fields are rejected. Existing sanitized validation-error wording remains backward compatible.

New generated contracts:

- `schemas/review-request.v1.json`
- `schemas/draft-review.v1.json`
- `schemas/rule-definition.v1.json`

A report contains rule/finding/evaluation versions; content hash; source metadata; coverage; requested questions; DRAFT review status; limitations; and localized findings. Each finding has its rule/version and merged triggering rules, nullable verified tooth ID, applicability/evaluated flags, finding type, exact source observations, source references/spans, evidence references, missing fields, abstention reason and conflict group. OBSERVED system controls are not movement/clinical findings; distinguish finding_type. NOT_APPLICABLE means no descriptive condition, never no clinical concern. Tests and UI distinguish TEST_ONLY observations from vendor verification.

Compact **actual unverified-response excerpt**, from the synthetic fixture (not the full schema):

```json
{
  "schema_version": "1.0.0",
  "review_status": "DRAFT",
  "intended_for": "CLINICIAN_REVIEW",
  "evidence_domain": "UNVERIFIED",
  "clinical_analysis_enabled": false,
  "coverage": { "declared_positions": 1, "eligible_positions": 0, "unavailable_positions": 1, "expected_axes": null },
  "findings": [{
    "rule_id": "D01", "rule_version": "2.0.0", "tooth_id": null,
    "status": "SEMANTICS_UNKNOWN", "applicable": null, "evaluated": false,
    "finding_type": "UNAVAILABLE", "observed_measurements": [],
    "input_refs": ["measurements/measurement-1"],
    "abstain_reason": "SEMANTICS_NOT_AUTHORIZED", "review_status": "DRAFT"
  }]
}
```

The full generated synthetic example is `frontend/src/test/fixtures/synthetic-draft-review.json`. Backend tests additionally produce TEST_ONLY observations, for example magnitude `1.2300`, lexical scalar `-1.2300`, raw value `−1.2300 M`, opaque test tooth/axis/direction, TEST_ONLY component evidence, and no verified report-level tooth ID. These demonstrate plumbing only.

Engineering bounds: existing 1 MiB/body, 100,000-character raw input and parser limits remain. Review is limited to **512 declared measurement positions**, to bound finding expansion; above that the whole review returns a compact DRAFT with REVIEW_POSITION_ENGINEERING_LIMIT, no truncation or partial-prefix evaluation. The lexical parser still returns its full result within its existing limits. This is a resource bound, not a clinical cutoff. Frontend review requests time out after 20 seconds, have no automatic retries, paginate unavailable findings by 25, and retain the full response only in memory.

## Frontend and files

After parsing, the existing lexical preview remains. A separate **Create draft review** action optionally requests one unavailable assessment, sends raw input again to the same local backend, and renders descriptions/unavailable records/source/coverage/limitations. All output is visibly DRAFT for clinician review. Analyze remains disabled. Editing text/source/context, consent revocation, Clear/demo or requested question invalidates results and aborts stale requests. Literal markup remains inert text. Full JSON/evidence is inspectable, without a sign-off action or browser storage.

```text
backend/app/review/{__init__,models,registry,service,templates,safeguards}.py
backend/app/api/review.py
backend/app/main.py                         # adds only the versioned route
backend/scripts/export_schemas.py           # exports three additional schemas
backend/tests/test_review.py                # synthetic evidence/readiness/engine/API tests
backend/tests/test_health.py                # exact authorized route allowlist expanded
frontend/src/api/review.ts
frontend/src/api/parse.ts                   # exposes existing raw_sha256 field to TypeScript
frontend/src/components/DraftReviewPanel.tsx
frontend/src/App.tsx                        # separate action/panel + accurate transmission notice
frontend/src/App.review.test.tsx
frontend/src/test/fixtures/synthetic-draft-review.json
frontend/e2e/review.spec.ts
schemas/{review-request,draft-review,rule-definition}.v1.json
ENGINE_PHASE2A.md
README.md
graphify-out/                              # required AST-only refresh
```

No parser or semantic algorithms/policies, old schemas or original documents were modified. The route allowlist test was intentionally expanded for the authorized new endpoint; the old health/parse behavior assertions remain. This is an API scope update, not a clinical policy change to satisfy a test.

## Commands and remaining gates

Install/run commands remain in README. In PowerShell:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe scripts\export_schemas.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check

Set-Location 'C:\Finova AlignIQ\frontend'
npm test
npm run build
npm run test:e2e
```

Authentic vendor verification is still blocked by absent captures, not by missing code placeholders. For **each exact intended product build, clipboard surface and locale**, obtain ClinCheck Align Final/Doctor Final/Comparison with operands and crown/root views; SureSmile crown-center/cusp-tip, incremental/cumulative/stage-zero/intermediate/final and actual stage-kind variants; both arches, intended notation/dentition, all axes/signs/directions, explicit zero/missing/excluded values and actual serialization variants. Do not fabricate a vendor feature or sample to fill a matrix cell.

Every capture needs authorized raw text/encoding/hash; source version/environment and operator/time; pseudonymous case/plan/operand IDs; independently confirmed notation/dentition/arch/tooth status; axes/units/precision and per-tooth/arch signs/directions/frame; per-field basis, mode, scope and stage semantics; source-evidence locators; independently authored expected outputs; consent/de-identification references; and two independent approving reviewers including an orthodontist bound to all three artifacts. See `backend/vendor_verification/README.md` for the precise matrix. Independently authorize exact mappings/releases; TEST_ONLY is never a substitute.

Before Phase 2B, review this rule catalog, output contracts/templates, engineering limit and synthetic oracles. Add verified group/pair/baseline/stage/status input contracts only when evidence exists. Clinical predicates require exact orthodontist-approved source/device/patient/intent-specific policies, exceptions/wording/comparators, independent multi-reader case evaluation and release/change control. Sign-off/amendments, privacy/security/legal review and incident/rollback are separate prerequisites before clinical use. There are **no deviations that relax the audit**; additional-data functions are explicitly deferred and D02/D10/D11, R14, A05/A06 use the audit corrections.

## Final validation

| Check | Observed result |
| --- | --- |
| Complete backend pytest suite | **288 passed**: 192 previous tests plus 96 new engine/readiness/API cases |
| Complete frontend Vitest/RTL suite | **55 passed**: 30 previous plus 25 new |
| Complete real-API Playwright suite | **16 passed**, all four viewports, including all 12 previous paths |
| TypeScript / Vite production build | **Passed** |
| `pip check` | No broken requirements |
| Existing source documents and parser schemas | Original hashes retained; all existing schema parity tests pass |
| Repository formatting check | `git diff --check` passed |
| Required Graphify refresh | AST-only success: 489 nodes, 1,350 edges, 19 communities; no LLM labeling |

The prior route-allowlist test was expanded for the single authorized new endpoint; its health/parse assertions remain. An early new test assumed finding order instead of selecting its source measurement; that test was corrected without changing policy. Sandboxed browser startup and one final backend invocation stalled before test reporting and were stopped; approved local execution passed the complete final suites. Existing upstream Starlette TestClient/httpx deprecation and browser environment color warnings remain non-failing.

Validation is synthetic technical validation only. Authentic captures, independently reviewed vendor oracles and approved vendor releases remain **zero**. No Phase 2B work has begun.
