# Finova AlignIQ — Phase 8: Sequencer / Nano Review

14 November 2026, Asia/Karachi. **Synthetic engineering prototype; no clinical sequencing or anchorage prescription.** Phase 8 stops here. The empty vendor registry and all clinical-policy restrictions remain intact.

## Implemented workflow and evidence boundary

**Nano → paste or inspect synthetic TMT → Parse Table → Run Sequencing Review → upper/lower, segment and right/left anchorage sections → inspect evidence → copy/download DRAFT.** Macro Planning Assistant and Micro Attachment Interface retain their existing services, demos and exports. The shared navigation now makes Nano usable rather than a placeholder. Purpose changes retain original text and invalidate results, demo state, pending requests and exports.

The [Phase 6A research](docs/PMCEASY_FUNCTIONAL_RESEARCH_REPORT.md), [gap matrix](docs/PMCEASY_FEATURE_GAP_MATRIX.md), [roadmap](docs/PMCEASY_RECONSTRUCTION_ROADMAP.md), public observation register and retained V01 300/330-second frames support an arch/segment textual report and separate right/left anchorage notes. This implementation reproduces those **presentation/workflow categories independently**, using Finova styling and original fictional content. A numbered stage schedule, recovered algorithm, clinical optimization, exact current paid-product behavior and automatic CAD integration were not established by that evidence and are not claimed.

The corrected specification, independent audit, Phase 5 inventory and earlier phase reports govern the safety boundaries. Existing report relocations into `docs/` were present at task start and were preserved; no root-document deletion was reversed. Macro/Micro historical reports are not rewritten to imply they had Nano functionality earlier.

## Architecture and additive contracts

| Owning files | Responsibility |
| --- | --- |
| `backend/app/sequencing/models.py` | Versioned strict frozen intake/scenario/report/entry/stage-window models; explicit origins, side separation, source binding and no approval promotion. |
| `backend/app/sequencing/service.py` | Existing parser/resolver + review engine, conservative unavailable output, supplied-content assembly, structural stage checks and exact TXT rendering. No clinical strategy calculator. |
| `backend/app/sequencing/demo.py`, `fixtures/` | Read-only, hash-checked fixed fictional scenario and exact synthetic input binding. |
| `backend/app/api/sequencing.py` | Normal input and separately gated fixed-demo routes; no evidence/strategy importer. |
| `backend/scripts/build_sequencer_demo.py` | Explicit developer reproduction of original fictional data and actual service-shaped frontend response fixtures. |
| `frontend/src/api/sequencing.ts`, `components/SequencingWorkspace.tsx` | Validated transport, six organized sections, stage availability, source details and local exports. |

Routes:

- `POST /api/v1/sequencing/draft`: original raw text, source/context claims, affirmative synthetic confirmation and optional Phase 4 recovery receipt only. Rechecks the receipt and unchanged semantic/clinical gates. No stage records, strategies, arch mappings, clinical permissions, provider options or supplied findings are accepted.
- `POST /api/v1/development/sequencer-demo/input`: empty JSON object only; returns the fixed parsed synthetic input and explicit conventions.
- `POST /api/v1/development/sequencer-demo/draft`: empty JSON object only; revalidates fixed source/scenario data through real application services.

Both demonstration routes require server **FINOVA_ENVIRONMENT=development** and **FINOVA_SEQUENCER_DEMO_ENABLED=true**. Otherwise they return 404, including when the flag alone is set in production. This flag controls **route availability**, not clinical or uploaded-data authority. Macro/Micro demo flags remain independent. There is no public production switch for TEST_ONLY semantics or supplied strategies. No request parameter can enroll arbitrary data; even an identical demo table through the normal route remains UNVERIFIED. Fixed-file corruption or binding failures return sanitized 503 errors; stale/forged recovery receipts return 409/reparse guidance. Existing no-store/nosniff, bounded input, sanitized validation, memory-only processing and privacy gates apply.

Schemas: `sequencing-request.v1.json`, `sequencing-draft.v1.json`, `sequencing-demo-input.v1.json`, `sequencing-demo-request.v1.json`. Prior contracts and core parser/semantic/rule implementations are unchanged. No dependency is added.

Report entries distinguish **SUPPLIED_SYNTHETIC**, **STRUCTURAL_OBSERVATION**, **UNKNOWN**, **WITHHELD** and **DISABLED**, retaining original token/reference pairs, source measurement IDs, stage kinds/window IDs where allowed, side, evidence/finding refs, missing prerequisites, scope, DRAFT and NOT APPROVED. `VERIFIED_OBSERVATION` is reserved and rejected in this phase because no released verified sequencing path exists. Verified arch/segment/tooth fields remain null/empty. Fictional identity fields are separate; they never masquerade as verified anatomy. Clinical policy IDs remain null and clinical_predicate_evaluated=false.

Backend/client validation refuses unknown references, altered original tokens, duplicate entries, missing sections, misplaced side notes, invalid windows/kinds, altered source scope, missing evidence for supplied content, provider/approval promotion and synthetic results in a normal response. Fictional arch/segment/side references must agree; each side note retains only that side's original source references. The unresolved token retains UNKNOWN scope rather than inheriting another position's TOTAL evidence. Parsed source hashes bind to the same engine review. The full original lexical preview and immutable engine findings remain inspectable.

## Fictional demonstration and source authority

The fixed source reuses the checked Phase 6B synthetic raw/expected fixture: five opaque tooth tokens, four eligible TEST_ONLY movement positions and deliberate partial abstention. The original semantic evidence still says DEMO_ARCH and TOTAL; it is not modified to claim upper/lower anatomy. A separately authored **FINOVA-NANO-1** scenario adds fictional upper/lower roles, segment/side identities, six statements and five metadata-only stage records. Its JSON hash and exact source raw digest are checked before assembly. The scenario is never accepted from HTTP.

| Supplied data | Demonstration behavior |
| --- | --- |
| DEMO_UPPER, DEMO_LOWER | Explicit fictional upper/lower role labels; no inference from tokens 11–15. |
| DEMO_U_A / DEMO_U_B | Separate fictional right/left upper segments with source references. The authored example lists U-A before U-B; the engine does not choose this order. |
| DEMO_L_A / DEMO_L_B | Explicit fictional lower segments/sides, independent of the source's opaque numbering convention. |
| Upper stage records | Supplied baseline and two ACTIVE metadata records with stable IDs/indices. No per-stage movement values. |
| Lower stage records | Supplied baseline and PASSIVE metadata record. No timing, force, adequacy or movement allocation follows from that kind. |
| Right/left anchorage notes | Separately supplied fictional context notes. No force, appliance, auxiliary, requirement or negative-need decision is specified. |
| Unresolved source token | Segment/order withheld rather than anatomical identity invented. |
| Disabled clinical decisions | R13/T-series states and prerequisites remain explicit in the report. |

Every supplied statement has its exact scenario hash/row locator and **SUPPLIED_SCENARIO** origin. Statements are original authored inputs, not engine output, a proprietary protocol or a clinically approved policy. The positive structural observation concerns metadata validation only. Remaining clinical context is still missing even for supplied examples.

The UI and TXT prominently identify **SYNTHETIC DEMONSTRATION — NOT CLINICAL ADVICE** and **DRAFT — Requires Orthodontist Review**. Reproduction/startup commands are in [README](README.md#sequencer--nano-review). The generator writes only invented repository assets during explicit developer execution; runtime only reads fixed assets and computes in memory. No credentials or live provider call are required.

## Exact stage and anchorage boundaries

The real Phase 5 **StageRecord**, **TestRuleContext**, input digest admission and **stage_errors** checker are reused. The fixed demo supplies stage metadata through a private, exact-source-bound TEST_ONLY context. G15 reports actual supplied ID/order consistency. Duplicate IDs/indices, invalid order and an index-zero record with a nonbaseline kind are rejected as structural inconsistencies. Global ambiguous IDs and cross-arch, missing or reversed window references receive additional presentation validation. No absent baseline/gap is silently reconstructed; original stage kinds/indices are preserved.

**NO_STAGE_MOVEMENT_BINDING** is explicit in the contract and TXT. Source movement scope remains TOTAL under its checked synthetic semantics; the extra records contain no stage-bound measurements. Therefore **N07 remains NOT_APPLICABLE to the TOTAL movement values**, even when G15 checks the separately supplied record set. The report does not upgrade metadata checks into stage-motion validation. Original source scope/index/mode/basis/frame claims remain separately unverified and are exported as claims.

If stage records/window consistency fails or records are missing, dependent supplied statements become WITHHELD with no window/kind claims. Independent fictional anchorage context notes remain explicitly supplied; unrelated TOTAL observations remain eligible under their original evidence. This is field-scoped abstention, not selection of a replacement sequence. Normal claimed INCREMENTAL scope or a claimed stage index without actual evidence yields missing-data guards, not a reconstructed schedule.

G15/N07/N08, R13/T01–T08 prerequisites and H/N safeguards retain their owning semantics. N08 continues coordinate/composition restrictions and partial abstention. The engine still accounts for **96 IDs: 66 engineering handlers/guards, 27 disabled clinical predicates, 3 deferred controls**. R13/T01–T08 and all other previously disabled predicates remain disabled. No stage ceiling, cutoff, clinical sequence/anchorage protocol, force amount, wear duration, treatment time, simultaneity claim, movement sum/composition or collision/safety conclusion is introduced.

Ordinary input has no fictional identity/record list and only UNKNOWN/WITHHELD/DISABLED entries. Upper/lower assignment is withheld; original values stay in the parsed source. No absent stage record implies simultaneous movement, and neither right nor left unknown context implies “no anchorage required.” Explicit zero and missing cells remain separate lexical states and cannot create strategies.

## UI, reporting and privacy

Nano shares existing raw intake, automatic parser preview and Finova design tokens/components. Its output presents upper/lower sections, segment notes and right/left anchorage cards, then missing/disabled assessments. Stage availability is visible; records and structural details are expandable rather than a fabricated timeline. Original values, provenance, scope/kinds, missing prerequisites and the complete rule ledger are accessible. Responsive cards stack on small screens; keyboard navigation and post-render result focus are retained. Loading, empty, error, disabled-demo, explicit retry and export-failure states are implemented. No sign-off/edit/approval control is added.

Requests happen only on explicit load/parse/run actions. Abort controllers, timeouts and revision guards prevent stale responses and duplicate runs; input/context/consent/purpose changes clear output and exports. Macro and Micro remain independent. Source text is rendered inertly; no browser storage, telemetry, patient persistence or CAD write-back is added.

Nano uses **deterministic wording only**, provider=null and attempts=0. The existing Groq descriptive wording and parser recovery services, keys and gates remain unchanged; they are not repurposed to invent sequencing or anchorage content. This phase makes no live Groq call. Existing privacy gates still prevent arbitrary patient/raw-data cloud processing.

Copy/TXT uses the server's exact complete UTF-8 report: DRAFT/synthetic labels, every statement and origin, original token/value precision, source hashes/claims, fictional identities, stage IDs/kinds/windows, explicit lack of movement binding, missing prerequisites, all limitations and the 96-rule ledger. Blob filenames contain a nonpatient report digest and object URLs are revoked. Clipboard failures leave the preview/download available. Export makes no backend, provider or external CAD request. Windows clipboard newline serialization is normalized only in tests; downloaded bytes are compared exactly.

## GAP17 / GAP18 mapping and remaining gaps

| Gap | Phase 8 result | Remaining limitation |
| --- | --- | --- |
| GAP17 — arch/segment sequencing report | Working independent textual interface, real fixed-demo pipeline, source/stage metadata checks, unknown/withheld states and DRAFT export. | Clinical order selection, verified source/stage-movement ingestion, device policies and validated movement operations remain unimplemented/blocked. No recovered hidden algorithm or optimal schedule is claimed. |
| GAP18 — side-specific anchorage | Separate right/left context sections, supplied fictional notes, exact provenance and missing-context withholding. | No clinical anchorage/auxiliary requirement, force calculation or negative-need conclusion. Actual policies, clinical/geometry/force context and independent validation remain necessary. |

Clinical/vendor release blockers from Phases 5–7 remain: authentic reviewed captures, released generalizing mappings, actual stage/plan/geometry context, independently approved policies and clinical validation. This is an engineering review prototype, not clinical functional parity. No optimization, timeline, force engine, 3D editor, authentication, persistence or production patient handling is added. No next phase is started.

## Verification

| Check | Result |
| --- | --- |
| Complete backend pytest | **952 passed** (882 retained + 70 new Nano cases). |
| Complete frontend tests | **181 passed** (154 retained + 27 new Nano cases). |
| Playwright / Chromium / real API | **80 passed** (68 retained + 12 new Nano cases), including Macro/Micro regression and Nano at 1440/1024/768/375 widths. Final run status is passed with no failed tests. |
| TypeScript / production build | Passed (`tsc --noEmit && vite build`). |
| New schemas | All four match owning Pydantic models in tests. |
| Dependencies / advisory audits | `pip check` clean; all direct npm dependencies resolved. npm audit: **0 vulnerabilities**; isolated pip-audit on fully pinned requirements: **no known vulnerabilities**. No project dependency changes. |
| Formatting / Graphify / visual QA | `git diff --check` passed. AST-only `graphify update .` completed without LLM calls: **1181 nodes, 4167 edges, 56 communities**. Desktop, tablet and mobile Nano draft screenshots visually inspected: readable wrapping, stacked cards, separate side notes and visible DRAFT/synthetic labels. |

Tests cover fixed fictional output/origin, arch/segment/side separation, missing/inconsistent stages, kind/window/reference failures, TOTAL versus claimed stage scope, opaque identity, zero versus missing, no inferred schedules/anchorage absence, disabled predicates, unauthorized raw/stage/strategy/policy/path injection, production demo refusal, identical-demo-paste refusal, exact values/provenance/export, provider-call prohibition, stale responses and lifecycle, accessible interactions and responsive containment. Existing tests are retained; earlier Nano-placeholder assertions are updated to the newly authorized intake behavior. One test initially read a deliberately corrupted monkeypatched fixture during a later assertion; it now saves the valid reference first. Nano and one pre-existing Micro focus assertion now wait for the post-commit effect rather than racing it; the required focus result is unchanged. No safety assertion was removed or threshold activated.

Non-failing upstream Starlette/httpx deprecation and environment color warnings remain. Python audit is bounded to the pinned requirements file and warns that hashes are absent. Graphify skips unsupported extensions (including CSS and hash sidecars) and reports no modeled symbols in three browser test files; its update is an AST code refresh, not complete semantic-document extraction. No live Groq/patient test, vendor release, clinical approval, commit, push or deployment was performed.
