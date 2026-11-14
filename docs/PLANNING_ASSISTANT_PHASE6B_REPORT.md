# Finova AlignIQ — Phase 6B implementation

14 November 2026, Asia/Karachi. **Synthetic engineering prototype — not for clinical use.** This phase implements the Planning Assistant interaction and fixed synthetic demonstration. It does not establish clinical parity with PMCEASY or authorize vendor semantics, treatment changes or patient processing.

## Implemented experience

Choose a review purpose → paste synthetic TMT → confirm synthetic input → Parse Table → inspect original cells and exact lexical values → Run Planning Assistant → review organized descriptive DRAFT comments → select/copy comments or copy/download the complete DRAFT.

Macro is the primary usable Planning Assistant. Micro opens an explicit unavailable Attachment Interface explanation; Nano opens an explicit unavailable Sequencer explanation. Neither executes an engine. These are flexible review purposes, not aligner stage numbers, patient-eligibility decisions or a mandatory three-pass clinical protocol. Switching purpose cancels requests and clears results while retaining original text.

The existing Finova identity, teal palette, system fonts, Lucide icons and React/Tailwind stack are retained. The workspace adds purpose cards, a progress indicator, a clearly labeled demonstration entry, bounded scrollable movement tables with sticky headings, dimension cards, a selection/export area and expandable technical evidence. No new application dependency or copied PMCEASY asset, branding, proprietary library text or hidden algorithm is introduced. The existing certifi pin was patched from 2026.7.22 to 2026.10.18 after the requested dependency audit reported PYSEC-2026-4320; the installed virtual environment and requirements pin now match. The fixed version was checked against its [primary PyPI release](https://pypi.org/project/certifi/2026.10.18/).

The original raw text and lexical parser outputs remain visible. Source indicators, verification state, missing fields, unsupported structure and recoverable structure remain available through the existing parser panels. Acknowledging recognizable structure is not semantic or clinical approval. The main report action combines engine review and report wording on the backend. Prior separate review/report actions remain under the expandable Advanced section for regression compatibility and detailed engineering inspection.

## What was reused and preserved

- Phase 4 automatic detection, deterministic extraction, optional gated Groq structural recovery and signed recovery receipts. No vendor selector is introduced.
- Existing exact Decimal parsing, original text/cells/signs/units/tooth tokens, source spans and raw SHA-256 binding.
- Existing read-only synthetic fixture verifier, field-level semantic assessor and empty code-controlled vendor release registry.
- Unmodified Phase 5 rule registry, dependencies, eligibility, local abstention, conflict/deduplication and output safeguards. All **96 IDs** remain accounted for: **66 engineering handlers/guards, 27 disabled clinical predicates, 3 deferred controls**. No threshold or clinical activation was added.
- Phase 3 report generation, constrained Groq phrase selection, strict output validation and deterministic template fallback. Facts and exact measurements remain locally assembled. The old report contract and export are preserved inside the additive planning envelope.
- Existing input size/privacy controls, sanitized validation errors, no-store responses, no persistence, inert React text rendering and explicit local copy/download.

The governing corrected specification, independent clinical audit and architecture blueprint remain unchanged. The Phase 6A research/report/gap matrix and evidence limitations govern target observations. Public frames establish only recorded workflow/output categories; they do not supply clipboard oracles, clinical rules, present-day paid behavior or proven copy-button mechanics. Per-comment selection is an independent Finova interaction requested for this phase. The original standalone v1 82-rule document remains unavailable; historical trace paragraphs are not approvals.

## Additive transport and orchestration

| Route | Request / result | Authority |
| --- | --- | --- |
| `POST /api/v1/planning/draft` | Existing strict ReportSubmission → PlanningDraft | Reuses report route revalidation, original raw/context/receipt and normal semantic gates. No test authority or supplied findings accepted. |
| `POST /api/v1/development/planning-demo/input` | DemoRequest → fixed parsed DemoInput | Requires server development environment and explicit demo enablement; no uploaded raw text or evidence. |
| `POST /api/v1/development/planning-demo/draft` | DemoRequest → fixed PlanningDraft | Recomputes the shipped synthetic input through parser, fixture verifier, semantics, rules and report service. |

DemoRequest accepts only `comment_mode: AUTO | GROQ | TEMPLATES`. No fixture identity/path, raw text, context, test switch, source claim or semantic evidence is accepted. Both demo routes require **FINOVA_ENVIRONMENT=development** and **FINOVA_PLANNING_DEMO_ENABLED=true**, otherwise return 404. Missing/invalid fixed evidence returns a sanitized 503. Existing privacy middleware applies. The development env-file loader accepts the new nonsecret demo setting; it still never prints secret values.

PlanningDraft v1 contains the unchanged FinalDraftReport, five ordered presentation sections and complete planning `export_text`. Every comment appears exactly once in the section index. The complete export adds the dimensional index, scope explanations and explicit synthetic label where appropriate, then retains the entire original report TXT, limitations, source facts and 96-rule ledger. New schemas are `planning-draft.v1.json`, `planning-demo-input.v1.json` and `planning-demo-request.v1.json`; prior contracts remain intact.

Frontend requests validate the report, comment membership/coverage, unavailable-section separation, raw hash, source/context, requested assessment and wording mode. Demo responses must be TEST_ONLY; normal planning responses cannot introduce TEST_ONLY authority. No network request is initiated merely by typing, choosing purpose or selecting wording. A repeated click while pending is refused. Abort controllers and revision checks discard stale results; timeouts show retry guidance without automatic retry. Input/context/consent/purpose changes unmount the result and invalidate selection/export. Wording/assessment changes invalidate the affected draft and pending response. Result focus moves after React commits the output.

## Dimension assignment

`backend/app/planning/service.py` implements a presentation-only, deny-by-default mapping for the explicitly invented FINOVA-DEMO-1 convention. It does not use raw English label matching as authorization.

All required observation components must have TEST_ONLY evidence; source/version, opaque numbering, synthetic dentition/arch, mode, basis, scope and frame must exactly match the demo convention. Unit and direction must be compatible. A comment is placed in a dimension only if **every** measurement belongs to that same dimension and one compatible source context:

| Demo canonical values | Presentation | Explicit limitation |
| --- | --- | --- |
| MESIODISTAL + mm + MESIAL/DISTAL | Sagittal | Programmed displacement only; no sagittal relationship, space-closure or correction strategy. |
| BUCCOLINGUAL + mm + BUCCAL/LINGUAL | Transverse | No skeletal expansion, bodily translation, arch-width or bone-limit conclusion. |
| EXTRUSION + mm + EXTRUSION | Vertical | No bite adequacy, contact or clinical vertical assessment. |
| Rotation, mixed distributions, unknown/incompatible convention or context | Other observations | No forced reinterpretation, splitting or duplicated dimensional placement. |
| Unavailable comments | Unavailable assessments | Reasons and missing fields are preserved; no observation selection. |

No production vendor dimension mapping was added. Future verified data with no approved presentation convention stays Other. Empty dimensions explain that sufficiently authorized data are unavailable, and expressly withhold complete clinical assessment. Finding/comment IDs, exact observations and original field-specific abstentions are unchanged. Mixed report comments are not split to create an appearance of dimensional coverage.

## Executable Finova Synthetic Demonstration

The fixed raw table and exact expected artifact/record are under `backend/app/planning/fixtures/`. The independently authored convention is displayed in the UI and specified by `backend/scripts/build_planning_demo.py`:

- Raw tokens **11–15** identify **DEMO_11–DEMO_15**, opaque synthetic entities; neither FDI nor Universal anatomy is inferred. DEMO_ARCH/SYNTHETIC do not assert a real arch or dentition. No group/status/pair/stage authority is supplied.
- Millimeters for linear movement, degrees for rotation; unsigned magnitude plus explicit D/B/E directions for distal/buccal/extrusion. Rotation M is the opaque DEMO_ROTATION_M direction. No mirrored-side or unknown-sign inference.
- Basis DEMO_CROWN_POINT, frame FINOVA_LOCAL_AXES_V1, mode TEST_PLAN_MODE, scope TOTAL. No achieved movement, staged dataset, root geometry, diagnosis or clinical strategy.
- Hand-specified semantic assertions authorize exactly four positions: **1.2300 D**, **0.4500 B**, **0.200 E**, **2.500 M**. The **3.000 M** value intentionally has no semantic evidence. Dashes are missing, never zero.

The ordinary Phase 4 parser extracts 20 positions (five rows, four axes). The existing verifier checks raw/expected file hashes and exact lexical equality before the unchanged assessor/engine admits four TEST_ONLY positions. Sixteen positions remain unavailable. The resulting five descriptive comment units are three single-dimension comments, one rotation comment and one mixed distribution summary. The latter two remain Other. All disabled predicates remain disabled.

Runtime only reads fixed shipped artifacts and uses in-memory computation. The generator writes only invented repository assets during explicit developer execution; it does not run on HTTP. Semantic assertions are independently defined in the generator. Its lexical snapshot is produced by the parser and checked against independent exact-value/span assertions in tests; it is a structural regression artifact, **not an independent vendor oracle or fabricated human review**. Rebuilding is not clinical certification.

The UI never submits its raw demo text to the demonstration draft route. Editing any loaded text/context removes the demo state and prior output. Even an exact copy of the shipped raw table through normal parse/review/report/planning routes stays UNVERIFIED. A prefix, checkbox, browser flag, arbitrary upload, hash claim or request path cannot enroll user content in the TEST_ONLY domain. Direct demo-route calls can only analyze the fixed bundled example.

Reproduce/start commands are in [README](README.md#fixed-finova-synthetic-demonstration). `build_planning_demo.py --frontend-fixtures` regenerates the fixed evidence and actual deterministic HTTP-shaped frontend test responses. No key or live network provider is required.

## Comments, copy and export

The readable view presents the original approved template lead and exact original values with localized raw tooth tokens. Full immutable engine comments, finding IDs, rule IDs/versions, evidence locators, components, original spans and withholding reasons are expandable. Nothing is edited or promoted into an approved clinical note.

Individual checkboxes appear only for eligible OBSERVED descriptive comments with measurements, accepted evidence, no missing fields and no abstain reasons. Reviewers can select individual comments, select all eligible comments, clear selection and copy the selected set. Unknown and unavailable assessments have no selection control. Selection does not change the original report or engine facts.

Selected export contains the immutable selected text with finding/rule/comment IDs and source/evidence refs, DRAFT status, synthetic/domain label, report/raw digest, rule-set version and subset disclosure. It also includes **all unavailable comments/missing-information states and all limitations**, so a selection cannot hide contextual abstention. Omitted comments do not become negative findings. No edited text or clinical approval is implied.

Complete copy and TXT download use the server's complete planning export string. TXT is a local UTF-8 Blob, fixed nonpatient filename and revoked object URL. Clipboard errors leave the draft and export preview available. Windows may serialize clipboard line endings as CRLF; tests normalize only that transport difference. Downloaded text is compared exactly. Neither operation calls a provider/backend or sends anything to a technician/CAD application.

## Groq and data handling

Groq remains the only provider. `GROQ_API_KEY` belongs to the existing bounded comment service; `GROQ_API_KEY_2` remains the separate structural fallback key. Demo activation does not enable either provider gate. Deterministic templates make zero provider calls. AUTO uses the existing synthetic wording permission/key and minimal approved-phrase payload, strict validation, bounds and fallback; raw tables, identifiers, measurements and clinical data are not sent for wording. Real-patient transmission remains disabled.

The demo is a deterministic recognizable table, so structural recovery is unnecessary and makes no provider call. Ordinary arbitrary pasted text remains ineligible for cloud structural processing. Tests mock provider transports; no live Groq call, real patient input, vendor release, deployment, clinical sign-off or external CAD integration was performed.

## Gap mapping and remaining work

| Phase 6A gap | Phase 6B result | Remaining boundary |
| --- | --- | --- |
| GAP02 — guided display/run/review | Implemented independent two-action parse/inspect → assistant/report journey, loading/errors, original values and stale invalidation. | No claim of exact current paid-interface replication. |
| GAP03 — modification-pass navigation | Macro/Micro/Nano purpose navigation; Macro functional, specialist modules explicitly unavailable. | No patient routing, growth classification, fixed pass count or clinical eligibility engine. |
| GAP05 — dimension-organized comments | Five-section view, explicit fixed-convention mapping, unavailability and conservative Other placement; dimensional export index. | Real vendor dimensional interpretation and clinical conclusions remain blocked. |
| GAP06 — localized descriptive findings | Real engine demo retains localized original tokens/exact values/provenance, plus partial abstention and summary. | Anatomical vendor/tooth-group authorization still needs authentic evidence and released adapters. |
| GAP09 — technician communication | Individual/all selection, selected-copy, whole-copy, full TXT and complete context/provenance. | Manual local communication only; no sending, share service or CAD write-back. |
| GAP07 — clinical CAD-change recommendations | **Not completed; blocked by clinical validation and data.** | No R/T/attachment/IPR/anchorage/overcorrection strategy or invented cutoff. |

GAP04/10/11/14 vendor, growth and clinical-context gaps remain. GAP08 clinical reassurance is withheld. GAP12/13 resource libraries, favourites and identity/persistence are not implemented. GAP15–18 Attachment Interface and Sequencer/anchorage algorithms are out of scope. GAP19–22 unobserved target performance/integration/controls/support-matrix facts remain unknown; the new Finova controls are not evidence of PMCEASY implementation. GAP01/23 existing raw intake/standalone web architecture remain preserved. This task does not start another phase.

## Verification

Final results are recorded below after completing the required checks. Automated success establishes bounded software behavior, not clinical safety or authentic vendor compatibility.

| Check | Result |
| --- | --- |
| Full backend pytest | **828 passed**, including 47 new Planning Assistant cases. |
| Full frontend Vitest | **132 passed** (112 retained + 20 new cases). |
| Real-API Chromium integration | **56 passed** (40 retained + 16 new journeys), including the final rerun after the security/presentation changes; four widths 1440/1024/768/375, plus landscape navigation. |
| TypeScript and production build | Passed (`tsc --noEmit && vite build`). |
| Backend dependency consistency | `pip check`: no broken requirements. |
| npm dependency tree | All declared direct dependencies resolved. |
| npm advisory audit | **0 vulnerabilities** with registry access. |
| Python advisory audit | **No known vulnerabilities** in pinned requirements after certifi patch (`uvx --from pip-audit pip-audit -r requirements.txt --no-deps --disable-pip`). Fully pinned file; no hashes or broader environment audit claimed. |
| New JSON schema consistency | All three schemas match the owning Pydantic models. |
| Graphify / diff checks | `graphify update .` completed, AST-only/no LLM: **1003 nodes, 3490 edges, 43 communities**. `git diff --check` passed. Graphify skips unsupported extensions such as CSS and emits no-symbol notices for three browser test files; this is not a complete semantic-document refresh. |

New tests cover server-only demo activation and production refusal, raw/trust/path injection rejection, exact fixed evidence and source spans, reproducibility, partial abstention, all 96 records/27 disabled predicates, ordinary exact-demo-copy refusal, dimension unknown/unit/direction/basis/mode/scope/frame mismatch, missing evidence and compound comments, constrained mocked Groq success/payload/failure, real complete user journey, keyboard purpose navigation, selection/copy/export, no network on selection/export, no storage, stale invalidation, errors/retry and responsive containment. Existing tests are retained; legacy path tests now explicitly open the new Advanced disclosure. No regression expectation was weakened.

Initial checks found a real result-focus timing bug and fixed it with a post-commit effect. One test fixture selected a different wording mode from its response and was corrected. An initial route-allowlist test was extended for the three authorized additive routes. Sandboxed browser/backend runs stalled and were stopped; normal local process access was used for full validation. Initial npm DNS failed in the sandbox; the registry-backed audit succeeded. Any final residual gaps are reported here rather than counted as passing.

The initial browser pass also encountered a transient Chromium ERR_NO_BUFFER_SPACE navigation and one missing response; both complete subsequent runs passed with no retries configured. Upstream Starlette/httpx deprecation and NO_COLOR/FORCE_COLOR warnings remain non-failing. Python audit warns that the fully pinned requirements lack hashes; its result is bounded to that file. No failing check was silently skipped. Desktop and mobile intake/draft screenshots were visually inspected; the movement region scrolls locally without horizontal page overflow, keyboard result focus is asserted and off-screen skip-link clipping was corrected for scrolled captures.

Existing Phase 6A evidence edits/untracked research documents and pre-existing graph changes were present at task start and were preserved. No commit, push, deployment, real-patient test or new phase was performed.
