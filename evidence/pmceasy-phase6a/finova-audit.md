# Finova implementation evidence for Phase 6A

Observed 14 November 2026, Asia/Karachi. This is an owning-source and bounded synthetic-library audit, not PMCEASY evidence, clinical verification, a new full-suite test result or a claim of deployed behavior. No application code, configuration, dependency, secret or graph was changed by this investigation.

## Scope and method

- Ran the required Graphify query before source searches; used its file/symbol locations and prior known source paths. Normal repository inspection was appropriate because Finova source is available; REA was not used to reinterpret our own repository.
- Loaded all 20 Markdown project/governing/report/verification documents in full for section/table inventory, content hashes and cross-source checks: 703,551 bytes. The complete manifest is [finova-document-source-inventory.json](finova-document-source-inventory.json). Governing audit/spec tables and restrictions were inspected; generated Phase 5 inventory was checked for all 96 IDs, all 12 attributes each and exact corrected-purpose agreement with the runtime catalog; the approval register contains 30 R/T/A entries. This is document inspection, not independent validation of cited medical literature.
- Inspected actual complete frontend intake/review/export components, parser orchestration and extraction, semantic release registry, rule definitions and additional-input/clinical preparation contracts, report eligibility/grouping/assembly/prompt contracts, API handlers, representative Phase 5 tests and browser report tests. Exact file hashes are in the manifest.
- Executed four fresh synthetic library/model probes plus a vendor-claim and untrusted-field rejection check. Provider generation was patched to raise if called, and **zero provider method calls** occurred. Results are [finova-local-probes.json](finova-local-probes.json).
- An initial in-process TestClient probe stalled in the restricted environment and was stopped. It supplies **no successful HTTP/browser evidence**. No full pytest/Vitest/Playwright rerun was needed or claimed in this research-only investigation. Prior 781/112/40 pass counts remain historical Phase 5 report results.
- No `.env.local`, credentials, patient input or vendor capture was read. No live Groq call was performed.

## Source evidence ledger

Paths below are relative to `C:/Finova AlignIQ`; line locators refer to this checkout and are anchored by the recorded source hashes.

| ID | Current capability / boundary | Owning evidence |
| --- | --- | --- |
| F01 | Finova is a standalone single-page React workspace with raw intake, examples, Clear and optional context claims. There is no module switch to an Attachment Interface or Sequencer. | `frontend/src/App.tsx:13`, `:110`, `:130`, `:155`, `:185`, `:201` |
| F02 | Raw textarea state receives the browser value unchanged; raw preview renders the same string as inert React text. Counts are display metadata. Edits revoke confirmation/results. This is logical text preservation, not clipboard-byte preservation. | `frontend/src/App.tsx:14`, `:24`, `:40`, `:141`, `:173` |
| F03 | An explicit synthetic-data confirmation and Parse Table action sends input to the backend. Clinical Analyze is disabled. Parse, draft review and final report are three distinct explicit actions. | `frontend/src/App.tsx:52`, `:185–201`; `frontend/src/components/DraftReviewPanel.tsx:48–84`; `frontend/src/components/FinalReportPanel.tsx:48–103` |
| F04 | Generic row/column tables and deterministic complete Markdown recognition exist. Ambiguous unanchored layouts abstain; recovery is an optional independently checked structural proposer for server-reproducible generated synthetic text only. | `backend/app/parser/service.py:19–140`; `backend/app/parser/phase4.py:18–80`; `backend/app/parser/contracts.py:58–78`; fresh local probes |
| F05 | Lexical source/number/label extraction is intentionally not semantic normalization. Canonical tooth/axis/direction remain null in the lexical contract and semantics_verified is literal false. | `backend/app/domain/models.py:103–151` |
| F06 | Vendor release registry is empty. Synthetic evidence can only be TEST_ONLY when the private library flag is supplied; actual reviewed artifacts also need a code-approved digest. | `backend/app/semantics/registry.py:9–27` |
| F07 | Public review/report routes accept original submission and optional structural receipt, not trusted findings, semantic evidence or policies. Their handler calls supply no CheckedFixture or test-only switch. | `backend/app/api/review.py:12–16`; `backend/app/api/reports.py:12–16`; `backend/app/review/service.py:45–70`; `backend/app/reports/service.py:184–194` |
| F08 | Current semantic infrastructure is **exact-curated-fixture projection**, not a generalizing source/version adapter for new arbitrary pastes. Collecting samples and adding a release digest alone would not make public input normalize: production adapter/evidence lookup/admission still needs a reviewed implementation. | `docs/PARSER_PHASE1_5.md` architecture/field projection sections; `backend/app/semantics/registry.py:18–27`; `backend/app/review/service.py:45–68`; public handlers in F07 |
| F09 | Engine runtime has 96 IDs: 66 ACTIVE engineering handlers/guards, 27 DISABLED clinical predicates and 3 DEFERRED controls. ACTIVE is not clinical authorization. D16/N11/N14 remain deferred. | `backend/app/review/registry.py:97–178`; fresh runtime count in probes |
| F10 | Nonzero/zero descriptions, compatible-context co-programming and distribution are implemented; group/pair descriptions require extra admitted evidence. Ordinary public pastes yield no authorized measurement observations. | `backend/app/review/service.py:68–128`, `:215–313`; local probes; `backend/app/review/templates.py:10–23` |
| F11 | R01–R13/R15–R16, T01–T08 and A01–A04 are disabled. R14 is an abstention guard; A05/A06 are exact-placement/superiority wording guards. No clinical policy, approver or threshold is populated. | `backend/app/review/registry.py:113–125`, `:137–173`; `backend/app/review/clinical.py:12–77`; `backend/app/review/service.py:169–172`, `:315–333` |
| F12 | Group/status, actual stage, expected-coverage and paired-direction contracts exist only as bound private TEST_ONLY evidence. These are not public clinical-data importers or independent verifiers of geometry/examination records. | `backend/app/review/context.py:10–105`, especially `:45–60`, `:62–95` |
| F13 | Clinical preparation/readiness is a checklist, always production_enabled=false, predicate_result=null. Illustrative comparator examples are isolated TEST_ONLY plumbing, not complete R predicates or patient advice. | `backend/app/review/clinical.py:46–56`, `:81–122`, `:125–151` |
| F14 | UI displays descriptive findings separately from unavailable assessments; exposes raw/normalized values, source spans, literature IDs, missing fields and full 96-rule ledger; DRAFT boundary is visible. | `frontend/src/components/DraftReviewPanel.tsx:7–28`, `:71–99` |
| F15 | Reports group eligible findings as TOOTH or SUMMARY; unavailable/suppressed/disabled records are consolidated separately. Exact local measurements and rule/provenance are preserved. These are descriptive sections, not CAD modification instructions or whole-case complexity judgments. | `backend/app/reports/service.py:37–99`, `:101–129`; `backend/app/reports/models.py:26–42`; `frontend/src/components/FinalReportPanel.tsx:107–136` |
| F16 | Groq wording generation is **closed choice between approved alternatives**, not unrestricted clinical reasoning or free-form technician instructions. Public UNVERIFIED input yields no eligible findings and zero Groq attempts; even future vendor evidence is currently refused by the real-patient transmission gate. | `backend/app/reports/service.py:37–59`, `:132–159`; `backend/app/reports/prompt.py:20–25`; `backend/app/reports/models.py:45–55`; local probes |
| F17 | Whole-report copy and UTF-8 TXT download exist, locally. There is no per-comment copy, select/deselect, editing, approval, shared link, PDF export or direct CAD application action in the inspected UI/contracts. This negative finding is bounded to the current source components/routes, not an assertion about external deployment add-ons. | `frontend/src/components/FinalReportPanel.tsx:70–92`, `:132–136`; report/API model fields; `frontend/e2e/report.spec.ts:32–65` assertions (existing test, not rerun) |
| F18 | No attachment-design diagram/3D tooth map, selectable attachment candidates, size/shape/orientation output contract or geometry/attachment plan intake is implemented. A-series names and prerequisite booleans must not be counted as an Attachment Interface. | `backend/app/review/clinical.py:37–42`, `:66–73`; `backend/app/review/context.py:45–60`; app component tree; closed report contract `backend/app/reports/models.py:26–74` |
| F19 | No sequencing schedule/timeline, stage allocation optimizer, anchorage suggestion, IPR decision or contact/collision engine is implemented. StageRecord can validate explicit toy IDs/order/kinds; this does not create sequencing. | `backend/app/review/context.py:20–26`, `:98–107`; `backend/app/review/clinical.py:29–36`; disabled T registry; app component tree |
| F20 | No extension, CAD injection/automation, authenticated sign-off, case database or report persistence exists in the inspected app. Existing deployment instructions describe a standalone Vite frontend/FastAPI backend and explicitly no auth/database. Future intended-use, privacy/security and authenticated review remain separate gates. | `docs/DEPLOYMENT.md:1–17`, processing/routing/data-boundary sections; `backend/app/main.py:14–28`; API handlers; frontend app/export code; governing audit and blueprint |

## Fresh bounded probe results

All four cases were explicitly invented synthetic text. No vendor semantics, anatomical identity or clinical evidence was supplied.

| Case | Lexical result | Normalized measurement eligibility | Report |
| --- | --- | --- | --- |
| Tab-separated tooth rows, Unicode minus and explicit zero | PARSED_UNVERIFIED; 2 positions; exact `-1.2300` and `0.00`; raw preserved | All canonical axes null; UNVERIFIED; 0 eligible | STANDARD_TEMPLATES; NO_ELIGIBLE_FINDINGS; 0 provider attempts; DRAFT |
| Tab-separated tooth columns | PARSED_UNVERIFIED; 2 positions; exact decimal strings; raw preserved | Same abstention | Same abstention report |
| Complete outer-pipe Markdown | PARSED_UNVERIFIED; 1 position; raw preserved | Same abstention | Same abstention report |
| Unanchored numbers without a recognizable header | UNSUPPORTED; UNKNOWN orientation; no assigned positions; raw preserved | UNVERIFIED; 0 eligible | Same abstention report |

Every review retained 96 ledger records. A claimed ClinCheck platform/version plus FDI, upper arch, Align Final, crown-center and total claims still yielded UNVERIFIED/0 eligible. Strict models rejected extra test_only, test_context, checked, clinical_analysis_enabled and threshold fields. These probes corroborate core library behavior; they do not establish current browser/deployment health, PMCEASY compatibility or clinical correctness.

## Planning comment mapping grounded in our current code

This mapping identifies Finova rule families that *could* correspond to target comment classes after the parent investigation establishes those classes. It does not assert that PMCEASY uses these rules or that a visible target suggestion is justified.

| Comment class | Descriptive basis available conditionally | Proposed review candidates | Still required |
| --- | --- | --- | --- |
| Rotation by tooth/group | D01/D03 | R01/R02 | Verified numbering/dentition/group, axis/unit/sign/direction/source/version/mode/basis/scope; approved trigger/category and exclusions for any review suggestion |
| Extrusion/intrusion | D04/D05 | R03–R06 | Verified direction/group/arch; clinical and appliance/occlusal/root context where needed; approved review policy |
| Inclination/angulation | D06 | R07/R08 | Distinguish source angular definition from root movement; root geometry/clinical assessment where claimed; approved wording/trigger |
| Buccolingual/transverse displacement | D07 | R09 | No inference of bodily expansion, arch width or bone safety; verified semantics plus additional clinical context/policy |
| Mesiodistal/molar displacement | D08/D09 | R10/R11 | Verified arch/group/direction; no inference of sequence/anchorage/extraction/root trajectory; staged/clinical context for such decisions |
| Multiple axes in one total plan | D02/D10/D11 | R12 | Only co-programming is descriptive; temporal overlap/interaction needs actual staged data and validated policy |
| Distribution/paired magnitudes/explicit zero | D12/D13/D15 | No direct complexity/risk conclusion | Verified expected coverage and pair equivalence/mirror convention where applicable; never infer missing axes as zero |
| Clinical context insufficient | D14/R14 + H/N | Withholding only | Requested intent and genuinely verified examination/geometry/objective data; absence never means normal |
| Attachment/size/shape/orientation/placement | A05/A06/H08 withhold | R15/A01–A04 disabled | Actual plan/geometry, independently reviewed indications and module-specific validation; total TMT insufficient |
| Stages/sequencing/IPR/anchorage | G15/N07 descriptive consistency only | R13/T01–T08 disabled | Actual staged values and IDs/kinds, geometry, source/config profile, approved intended sequence/force/contact/IPR strategy; no reconstruction from totals |

## Gaps that are independent of clinical decision-making

Subject to confirming target observations, a future independent Planning Assistant could simplify the three-action journey, present a compact technician-facing draft, and add per-comment copy/select/edit controls while preserving the distinction between machine findings and clinician-authored text. These are missing interaction contracts, not authority to generate clinical modifications. Any editing/review feature needs clear invalidation/provenance requirements so a user edit cannot be presented as an engine-approved fact. Whole-report copy/TXT need not be rebuilt.

## Documentation reconciliation and residual unknowns

- Root `PARSER_PHASE4_REPORT.md` and `docs/PARSER_PHASE4_REPORT.md` are **different files/content**, both historical Phase 4 descriptions. The root version includes explicit final 584/104/40 results; the docs version describes additional detail and refers to final results without the same final-result section. Their hashes are retained. Use current source/probes to judge present behavior, not filename precedence.
- Phase 1’s Markdown limitation and parser-finalization’s two-example/manual-action/preview-only restrictions are historical. Current `phase4.py` and current UI supersede them structurally. They do not supersede source/clinical authorization.
- Earlier Phase 2A deferred group/pair/status/stage descriptions have Phase 5 guarded private TEST_ONLY paths; they still are not public clinically verified features.
- `docs/DEPLOYMENT.md` is a deployment guide, not evidence that a hosted app is currently deployed or healthy. No deployment URLs were independently tested in this subtask.
- The missing standalone original 82-rule document remains explicitly marked unavailable in the runtime catalog. Corrected v2 historical trace paragraphs are not a replacement clinical approval.
- The authentic manifest and release registry remain empty. No paid PMCEASY runtime, proprietary algorithm, authentic vendor clipboard serialization or clinically approved Finova normalization is inferred from any of these files.

## Suggested use in the final gap matrix

Treat raw intake, explicit run/status, raw/lexical preview and whole-report copy/TXT as implemented engineering capabilities. Treat tooth-wise/summary *descriptive report architecture* as conditionally implemented; do not mark actual vendor planning recommendations fully implemented. Classify generalizing vendor normalization as BLOCKED BY DATA **and** an unimplemented validated adapter/admission path. Classify clinical modification suggestions as BLOCKED BY CLINICAL VALIDATION and any required extra data. Attachment visualization/selection and sequencing presentation/algorithms are NOT IMPLEMENTED, with separate data/clinical blockers. Target behaviors not actually observable must remain UNKNOWN / NOT PUBLICLY OBSERVABLE regardless of our local scaffolding.
