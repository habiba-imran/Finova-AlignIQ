# Finova AlignIQ — Phase 9 functional audit

14 November 2026, Asia/Karachi. **Synthetic engineering prototype; not clinical validation.**

## Verdict and acceptance criteria

Finova implements an independently built, connected browser/API prototype covering the three publicly observed workflow categories. It does **not** reproduce PMCEASY's demonstrated clinical decision-making. Macro computes bounded descriptive findings from admitted evidence; Micro attachment choices and Nano strategy notes are supplied fictional scenarios, validated and presented through real services. Ordinary input is genuinely parsed but cannot obtain released vendor semantics or clinical instructions. A successful demonstration must explain this distinction.

| Area | Verdict | Supporting evidence and practical limit |
| --- | --- | --- |
| A. Functional workflow completion | **PASS** for the bounded synthetic prototype | All three intake/inspection/review/evidence/DRAFT-export journeys execute over HTTP. Macro selected copying also works. This is not clinical workflow completion. |
| B. Independent synthetic input processing | **PARTIAL** | Generic tables/Markdown, exact lexical values and rejection/clarification work independently of fixed demos. Generated recovery uses independently checked original spans. New arbitrary input cannot obtain semantic descriptions or scenario choices through public endpoints. |
| C. Descriptive output quality | **PARTIAL** | Eligible Macro facts, precision, source references and abstention are deterministic and traceable. Closed Groq phrases cannot introduce clinical meaning. No independent clinician usability/quality study; ordinary-input output is largely unavailable. |
| D. Coverage of public PMCEASY categories | **PARTIAL** | Dimension-oriented Macro, tooth-indexed Micro and textual arch/segment/side Nano categories are represented. Observed treatment directives are not implemented; target algorithms/current paid behavior remain unknown. |
| E. Clinical decision-making | **FAIL — intentionally outside the authorized prototype** | No approved clinical predicates/policies, prescriptions, force/IPR calculations, optimized sequence, prognosis or sign-off. Software abstention passes; clinical capability does not. |
| F. Actual vendor compatibility | **NOT VERIFIED** | Zero authentic oracles and approved releases; no generalizing production semantic adapter/admission path. Recognizing a brand or parsing a vendor-like table is not compatibility. |
| G. Security and release readiness | **PARTIAL** | Bounded/sanitized requests, isolated TEST_ONLY paths, no automatic storage and provider restrictions pass engineering tests. No authentication, clinical/privacy release review, load assessment, signed amendments or incident workflow. Hosted readiness is unverified. |

No defensible single “completion percentage” follows from these different scopes. The project is suitable for an explicitly synthetic local engineering demonstration. It is not a clinical planning replacement or a verified ClinCheck/SureSmile companion.

## Audit method and owning evidence

This is a fresh source/runtime verification by the coding agent, not an independent orthodontist review or external security certification. The audit follows the [independent critical audit](docs/Orthodontic_TMT_Independent_Critical_Audit(2).md), [corrected v2](docs/FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md) and [blueprint](docs/FINOVA_ARCHITECTURE_BLUEPRINT.md). The Phase 3/4/5/6B/7/8 reports, full inventory/approval register, [Phase 6A research](docs/PMCEASY_FUNCTIONAL_RESEARCH_REPORT.md), [original gap matrix](docs/PMCEASY_FEATURE_GAP_MATRIX.md), roadmap and retained observation registers were reviewed against their owning services and tests.

Graphify located parser/recovery, semantic registry, rule execution, reporting and module consumers. Its AST graph is navigation evidence, not proof of runtime correctness. Fresh HTTP/library probes are reproducible with [audit_phase9.py](backend/scripts/audit_phase9.py); their sanitized results are retained in [functional-probes.json](evidence/phase9/functional-probes.json). Provider transport is forbidden during those probes except for one explicitly mocked failure. Baseline suites independently reproduced 952 backend and 181 frontend passes before targeted stabilization.

The working tree changed during the audit: user-side frontend refinements and additional presentation tests appeared, and earlier implementation/audit files were committed by other work. Those changes were preserved. Current frontend tests/build/browser verification were repeated; this phase did not author that redesign. The source inventory and final verification below define the evaluated snapshot. The missing standalone original 82-rule v1 document remains a traceability limitation; original-proposal paragraphs in corrected v2 are not clinical approvals.

### What the target evidence establishes

The retained Phase 6A frames were inspected again: V02 120 seconds shows axis-organized clinical/CAD-directed output; V01 220 seconds shows tooth-indexed attachment options/alternatives/absence; V01 300/330 seconds shows arch/segment text and separate side-specific anchorage advice. Finova reproduces those **presentation and interaction categories independently**, using its own text/design. It deliberately does not adopt the numerical protocols or prescriptions visible in those recordings.

These are historical public recordings, not our execution of the paid tool. Eight original homepage assets remained unavailable in the retained research; private controls, exact clipboard serialization, hidden algorithms and current paid behavior were not observed. Phase 9 did not acquire private access or refresh those target observations. Per-comment selection is Finova functionality, not established PMCEASY control parity. No numbered timeline, dedicated companion 3D editor or automatic CAD integration is required by the available evidence. See the [23-gap re-evaluation](FINOVA_PMCEASY_FINAL_GAP_MATRIX.md).

## Actual end-to-end pipeline

1. **Explicit intake/automatic parsing.** Typing, module navigation and confirmation do not upload text. Parse Table calls `/api/v1/tmt/parse`; automatic means extraction/classification after that explicit action. [phase4.py](backend/app/parser/phase4.py) reuses the lexical parser and deterministic Markdown certification.
2. **Optional structural proposal.** Only a recoverable gap, development configuration, separate parser key and exact reproduction of a controlled recipe/seed allow Groq. [recovery.py](backend/app/parser/recovery.py) checks each proposed original-cell association independently; the model cannot replace values or supply semantics. Arbitrary messy pastes remain ineligible.
3. **Receipt replay.** Accepted associations are HMAC-bound to exact original raw/source/context, expire after 15 minutes and are re-proven in downstream requests. Process restart invalidates them. They are not a semantic authorization credential.
4. **Semantic verification.** [registry.py](backend/app/semantics/registry.py) has an empty approved-release set. [review_table](backend/app/review/service.py) admits only eligible fields and private exact-bound TEST_ONLY evidence. User context remains a claim; no generalizing released vendor adapter exists.
5. **Rule evaluation.** All 96 IDs remain in the ledger. Descriptive observers and guards operate under field-level prerequisites; clinical predicates remain disabled. Module routes re-evaluate original source instead of trusting client findings.
6. **Report assembly.** Macro [report service](backend/app/reports/service.py) groups eligible immutable facts and optionally requests approved wording. Micro/Nano assemble scenario content or unavailable entries with engine guard references. All facts, evidence and limitations are rendered locally.
7. **Explicit local export.** Copy/TXT use the authoritative server string; Macro selected export retains unavailable assessments and limitations. Exports are DRAFT and do not perform a provider request, CAD write or sign-off.

### Fresh input and failure probes

| Probe | Reproduced result |
| --- | --- |
| New clean 2-tooth / 2-axis synthetic table | Four declared cells: two numeric, one explicit zero and one missing. Raw text/hash preserved; zero eligible semantic observations in every normal module. |
| Complete outer-pipe Markdown | Deterministic extraction of an exact explicit zero; no Groq request. |
| Ragged ambiguous whitespace table | AMBIGUOUS_STRUCTURE, zero assigned positions; no guessed alignment or numeric replacement. |
| Product/price text | NOT_TMT; no provider call or invented tooth dataset. |
| SureSmile-labeled synthetic rotation | Structure recognized; source semantics remain UNVERIFIED and no attachment/sequence prescription follows from the large magnitude. |
| Arbitrary anchored/wrapped record | RECOVERABLE_STRUCTURE but no cloud call without controlled-fixture reproduction. Its missing structural output is disclosed, not silently repaired. |
| Authorized generated mixed rows / wrapped / partial | New cross-module tests certify a mocked proposal, replay its receipt into Macro/Micro/Nano, retain declared positions and prevent semantic promotion. Partial/quarantined state remains partial. |
| Context changed after receipt issuance | All three module routes return 409/reparse guidance, even with unchanged numeric text. |
| Visit fixed demos, then submit identical raw text normally | Nine cross-demo/normal-module combinations remain UNVERIFIED with zero eligible positions and no provider calls. No global enrollment/cache of trusted text is created. |
| Mocked Groq 429 for an eligible Macro demo | One modeled attempt; complete deterministic report, zero accepted model comments, explicit GROQ_RATE_LIMIT fallback. Existing transport tests additionally cover 401/503/timeouts/malformed/oversized/unsafe responses. |

Source values/spans, Unicode sign, Decimal precision and missing/zero separation are asserted in existing parser tests plus cross-module receipt replay. There is no rounding policy or numeric clinical cutoff introduced by this audit.

## Macro — Planning Assistant

The complete journey parses/inspects, runs a combined report request, presents Sagittal/Transverse/Vertical/Other/Unavailable, selects eligible comments, copies a selected or complete DRAFT and downloads exact TXT. Existing advanced separate review/report actions remain available. Source/context/purpose/consent changes invalidate results; mode/assessment changes invalidate the draft and selection.

The fixed example's **20 lexical positions / 4 eligible TEST_ONLY / 16 unavailable** run through the parser, checked fixture, semantic assessor and rule engine. Its five descriptive comment units are independently assembled from actual eligible findings: three dimension-specific descriptions, rotation and a distribution summary. Template prose is authored, but the measurements, field eligibility, finding membership and counts are computed. No supplied treatment strategy is hidden in Macro.

[planning/service.py](backend/app/planning/service.py) allows dimensional grouping only for the exact invented FINOVA-DEMO-1 convention and compatible evidence for every observation. Rotation/mixed summaries stay Other. No anatomical tooth identity, skeletal dimension assessment or clinical reassurance follows from the labels. A fifth numeric position intentionally lacks semantic evidence and remains withheld. Normal new inputs cannot get positive descriptions by copying this fixture or claiming its context.

The target's demonstrated CAD-change/IPR/auxiliary/root-control instructions are absent. Macro is a descriptive memo workflow, not an implementation of those clinical decisions. Selected export cannot hide unavailable assessments; checkboxes are absent on unavailable comments. Copying is a local communication aid, not direct CAD transfer.

## Micro — Attachment Interface

[attachments/service.py](backend/app/attachments/service.py) binds each entry to parsed original tooth/measurement references. Candidates, alternatives, toy geometry/orientation/placement and the no-attachment decision come from the separately hashed fixed scenario. There is **no attachment selection algorithm**: two candidates, one linked alternative and one explicit supplied no-attachment decision are authored inputs. One unknown and one withheld entry remain distinct.

The scenario is admitted only against the checked fixed source; authorized observation identities, same-tooth alternative relations and evidence references are validated. Original tokens 11–15 remain opaque; reserved verified identities remain null. Toy design IDs and surface/window labels prove neither anatomy nor placement feasibility. A05/A06/H08 guard references are not candidate triggers. A01–A04/R15 remain disabled even when a supplied candidate is displayed.

Normal numeric cells yield UNKNOWN attachment context; missing/unsupported information yields WITHHELD. Neither zeros, large movement nor absent fields produce “no attachment.” Complete export preserves every result/origin, supplied geometry, alternatives, references, prerequisites and 96-rule ledger. It is truthful supplied-content presentation, not clinical attachment computation or a verified attachment-plan importer.

## Nano — Sequencer

[sequencing/service.py](backend/app/sequencing/service.py) presents the six required sections. The fixed FINOVA-NANO-1 scenario supplies six fictional strategy/context statements, explicit upper/lower and segment/side identities and five metadata-only stage records. It does not derive those identities or statements from TMT magnitudes.

G15 checks actual supplied stage identifiers/order/kinds. Additional window checks reject missing/reversed/cross-arch references. N07 remains NOT_APPLICABLE for the underlying **TOTAL** movement observations; it does not claim stage-motion validation merely because a separate stage list exists. **NO_STAGE_MOVEMENT_BINDING** is explicit. Invalid/missing stage windows withhold dependent notes while independent supplied context remains supplied. N08 continues composition restrictions. R13/T01–T08 remain disabled.

Right/left notes retain only the matching fictional side's source references. An unresolved token retains UNKNOWN scope and withholding. Normal input has no invented arch/segment catalogs, stage list or timeline. No schedule optimization, simultaneity, force, auxiliary requirement, anchorage absence, safety, collision or duration claim is calculated. TXT retains original lexical values, supplied identities/stages/windows/origins, missing prerequisites and limitations.

## Groq's actual contribution

| Service | Boundary and value | Limitations |
| --- | --- | --- |
| `GROQ_API_KEY` — wording | Receives opaque finding aliases, rule/template IDs and a closed approved phrase list. Strict JSON/reference checks plus exact phrase equality; original values and evidence inserted locally. Can vary professional lead wording. | Chooses between authored alternatives; it does not add clinical intelligence. Optional external latency/cost has modest value over templates. Normal unverified input makes no call. |
| `GROQ_API_KEY_2` — structure | Proposes original span-ID associations for exactly reproducible generated synthetic fixtures, under role-specific schema and independent association proofs. Can recover bounded layout variations missed by the primary extractor. | Not general messy-vendor recovery. The checker already enumerates provable associations; the benchmark does not establish that an LLM is necessary or superior to an expanded deterministic parser. Missing/wrong proposals are quarantined. |

Both keys are backend-only and separate. No other provider was integrated. Micro/Nano wording is deterministic with provider=null and attempts=0. Wording cannot change facts/clinical meaning under its exact closed-language validator; unsupported text falls back. JSON schema compliance alone cannot validate structural associations or clinical meaning.

Per the brief, **one request per service** was made using fixed/generated synthetic material only, with no retries. Retained results exclude credentials, raw prompts, responses and provider diagnostics:

| Live check | Outcome | Elapsed | Prompt / completion / total tokens |
| --- | --- | --- | --- |
| Minimal wording transport/schema/validator probe | HTTP 200, requested model matched, GROQ_VALIDATED | 1.7697 s | 430 / 101 / 531 |
| Current Phase 4 wrapped recipe, seed 17 | HTTP 200, model matched, 4/4 original associations certified | 4.8054 s | 725 / 271 / 996 |

The wording probe uses an enum-only synthetic placeholder, **not a live end-to-end clinical or Macro quality test**. The parser probe exercises the current association recovery pipeline. These single measurements do not estimate latency distributions, capacity, general accuracy or clinical usefulness. [Wording result](evidence/phase9/groq-comments-smoke.json), [parser result and offline evaluation](evidence/phase9/parser-evaluation.json).

The independently declared synthetic corpus still yields deterministic-primary **96/240**, oracle-mocked hybrid **240/240**, with 36 mocked calls and zero calls for forbidden cases. That is validator/extraction plumbing evidence, not live model accuracy. Historical Phase 4 live results remain 10/12 with partial recovery; today's 4/4 smoke does not supersede or conceal those omissions. No real patient data was transmitted.

## The 96-rule inventory and execution states

The current registry reproduces **49 READY, 5 REVISE, 13 VALIDATE, 15 MORE DATA, 14 ADDITIONAL** document dispositions. Execution remains **66 ACTIVE engineering handlers/guards, 27 DISABLED clinical predicates, 3 DEFERRED**. Runtime metadata further distinguishes 44 EXECUTABLE, 36 REQUIRED_DATA_GUARD, 8 OUTPUT_GUARD, 5 PARTIAL_SYSTEM_CONTROL and 3 DEFERRED entries. These axes overlap: REQUIRED_DATA_GUARD includes disabled clinical prerequisites and nine active conditional guards; it is not an additional count of implemented clinical algorithms.

| Classification | IDs and actual behavior |
| --- | --- |
| Descriptive/engineering | G01–G18 and D01–D15 subject to their individual evidence requirements; corrected co-programming, exact inventories, field coverage and provenance. |
| Conditional extra-data guards | G14/G15/G18, D03/D04/D05/D09/D13 and N12 require independent context; positive examples are private TEST_ONLY. R14 is a sufficiency/withholding guard. |
| Output/safety/system controls | A05/A06, H/L/N safeguards restrict claims and retain DRAFT/provenance. H10/H12/L06/N03/N04 are partial system controls, not complete authentication/privacy/approval workflows. |
| Disabled clinical predicates | R01–R13, R15–R16, T01–T08 and A01–A04: 27. Readiness checklists and isolated illustrative GT/GE comparators in clinical.py are not executable clinical recommendations. |
| Deferred | D16 historical comparisons, N11 signed amendments, N14 incident/rollback workflow. |

All three modules carry the complete actual engine ledger. Macro consumes eligible D findings as content. Micro uses source observations for identity/provenance and A/H/N findings for withholding; its choices are supplied. Nano uses source scope, actual stage structural checks and R/T/H/N prerequisites; its strategies are supplied. Displaying all 96 IDs does not mean that all 96 generated a clinical conclusion. Tests exercise OBSERVED, NOT_APPLICABLE, SEMANTICS_UNKNOWN, CONTEXT_REQUIRED, PARSE_INVALID, DISABLED and SUPPRESSED as appropriate; CLINICIAN_SIGNED is not available. The fixed demonstrations do not exercise every positive engineering branch, so full-suite library tests remain necessary.

## UI, privacy, security and remaining findings

Real Chromium tests exercise navigation, ordinary parsing, every fixed demo, unavailable/error/retry paths, copy/TXT, selected comments, keyboard activation/focus, stale invalidation, responsive containment and no storage writes. Current user-side presentation refinements were included in final verification; technical provenance remains expandable. A generated fixture is the appropriate way to demonstrate parser recovery; a loaded fixed module demo is already parsed and should proceed directly to its run action. Parse Table intentionally declassifies that demo. README now explains this easily misunderstood step.

| Finding | Status / consequence |
| --- | --- |
| P1: development generator available in production | **Fixed.** `/api/v1/development/synthetic` now requires exact development environment, consistent with its route/name. Previously it returned invented data only, with no semantic or provider authority; this was exposure of a development surface, not a patient-data bypass. Default/production/test/wrong-case and flag-override regression cases added. |
| P2: intermittent startup failure on the shared development server | **Isolated acceptance harness added and verified.** The current-source development run passed 111/112 but another page timed out before its input rendered. The affected scenario passed 10 focused repeats; the cause is not established. The complete suite passed **112/112** against a built preview and fresh backend on owned ports, with failure tracing. Five test files now compare exact API URLs against the page origin instead of a fixed port; request/path/privacy assertions, timeouts and zero-retry policy remain intact. No application behavior was changed to conceal the failures. Shared-development startup flakiness remains a documented limitation. |
| P2: current documentation mixed with historical reports | **Corrected in current entry points.** README links to moved reports, labels old Phase 5 counts historical, gives all-module demo startup and treats deployment files as configuration. This audit reconciles older claims below. Historical evidence/report bodies remain historical. |
| P2: exports differ in source snapshot detail | **Documented limitation.** Nano TXT includes all parsed lexical cells. Macro/Micro exports retain exact accepted observations, entry/source references and withholding, but are not full archives of every unverified raw cell. Raw/lexical preview remains available in the UI. Do not promise identical source archival across modules. |
| P2: detailed unavailable output can be verbose | **Remaining usability limitation.** Disclosure/pagination and current presentation improvements help; clinical prerequisites and full ledger are necessarily technical. No qualified user study or comprehensive accessibility certification was performed. |
| Release: no authentication/rate/concurrency control/PHI detection | **Open outside this phase.** A checkbox is not de-identification. No patient persistence is added, but browser/OS/clipboard/download/proxy/provider infrastructure privacy is not certified. Public exposure requires a separate security review. |
| Release: process-local recovery signing | **Explicit limitation.** Receipts expire/restart; multiworker requests can fail replay because keys differ. Use one local backend process and reparse when necessary. No patient cache/database exists. |
| Release: hosted demonstration | **NOT VERIFIED.** Vercel/Render config exists; a configured hostname is not evidence of a working deployment. Production refuses positive fixed demos. No deployment, hosted health test or production-demo authorization was performed. |

No Groq key-shaped value was found by the frontend source/build pattern scan; inspected key settings and ignored environment-file loading remain backend-only. The scan is not exhaustive secret detection. Requests are bounded before validation; unknown fields and malformed requests produce sanitized errors. Existing tests cover inert markup, path/policy/source/trust injection, corrupted fixtures, forged receipts and environment/request bypasses. No arbitrary raw table can enroll in TEST_ONLY. No app persistence, telemetry, CAD write-back or sign-off endpoint is added. These are bounded source/test findings, not a penetration-test or compliance claim.

## Documentation reconciliation

| Historical statement | Current interpretation |
| --- | --- |
| Phase 0 blueprint says parser/engine are future work | Historical phase authorization; later explicit implementation produced the bounded pipeline. Clinical restrictions still govern. |
| Phase 3 says no live provider test; old manual report steps | True for that phase. Later parser finalization/Phase 4 and the two Phase 9 probes add limited live evidence; combined Macro action coexists with legacy Advanced actions. |
| Parser finalization's two-example/manual/preview-only limitation | Legacy assisted endpoint remains. Current normal Phase 4 intake uses generated fixtures and receipt replay; arbitrary input is still cloud-ineligible. |
| Phase 6A matrix says no specialist modules | Accurate at research time. GAP15/17 now have executable synthetic interfaces; clinical/geometry/strategy functionality remains blocked. |
| Phase 6B says Micro/Nano unavailable; Phase 7 says Nano unavailable | Historical scope only. Both are available now under Phase 7/8; older test counts are not current totals. |
| 96 rules / 66 active / READY | Inventory, engineering execution and audit dispositions respectively; none implies 96 clinical algorithms or clinical approval. |
| “Synthetic authorization” / fixed scenario | Code-owned evidence admission for invented data. UI confirmation, environment availability and model output cannot authorize arbitrary clinical content. |
| Health response `phase: 1` | Compatibility field retained deliberately; not the current project implementation phase. |
| Deployment guide describes stateless hosting | Raw processing has no persistence, but recovery signatures are ephemeral and process-local. Configured URLs and build success do not prove hosted availability. |

## Verification

Final verification completed against the finished UI snapshot. The backend/governing source is unchanged from the 960-test run; application source remained unchanged through frontend tests, build and browser acceptance. No clinical assertion is inferred from test counts.

| Check | Result |
| --- | --- |
| Full backend suite | **960 passed**, one upstream warning; 952 baseline + 8 cross-module/environment cases. |
| Full frontend suite | **190 passed across 13 files**, after the user confirmed UI work was finished. |
| Full Chromium / real-API suite | **112 passed in 5.6 minutes**, no skipped tests/retries, using the production bundle and fresh isolated backend/preview. All 11 browser spec files run at 1440/1024/768/375 widths; responsive scenarios additionally check 672 px. Shared-development runs remain separately recorded: **111/112** after UI completion and **99/100** during editing; both failures preceded the first input/navigation interaction. Focused repetition passed **10/10**. |
| TypeScript / production build | **Passed** on the finished UI (`tsc --noEmit && vite build`); 1915 modules, no source drift after the build. |
| API/schema contracts | **32 schemas regenerated identically**, with no schema changes; contract tests included in 960 backend passes. |
| Dependency checks | `pip check` clean; npm dependencies resolved; npm audit **0 vulnerabilities**; pinned Python requirements **no known vulnerabilities**. No dependency change in Phase 9. |
| Authentic vendor gate | **NO_AUTHENTIC_ORACLES**, expected verifier exit **2**; zero reviewed captures/releases. This is an open compatibility gate, not a vendor pass. |
| Secret/link/format/source snapshot | Finished frontend source/production bundle secret-pattern scan found no key-shaped matches; `.env.local` is ignored. README and all three new documents have no broken file links. `git diff --check` passed. Source/build identities retained and post-browser drift check passed. |
| Graphify / visual inspection | Final AST-only refresh completed: **1230 nodes, 4351 edges, 57 communities**, no LLM calls. Desktop and 375 px intake/Macro/Micro/Nano screenshots inspected: readable stacked content, separate states, visible DRAFT/synthetic labels and wrapped export controls. Browser tests assert containment/keyboard/reduced motion. Historical target frames were inspected again. |

Evidence: [verification summary](evidence/phase9/verification-summary.json), [backend log](evidence/phase9/backend-tests.log), [frontend log](evidence/phase9/frontend-tests.log), [production-preview browser log](evidence/phase9/production-browser-tests.log), [shared development browser log](evidence/phase9/browser-tests.log), [startup repeat log](evidence/phase9/startup-diagnostics.log), [build log](evidence/phase9/build.log), [npm advisory result](evidence/phase9/npm-audit.json), [Python advisory result](evidence/phase9/python-audit.log). Logs/browser screenshots are local ignored QA artifacts; the JSON probes, source identities, verification summary and this report carry the durable conclusions. No test was deliberately skipped or weakened to obtain a passing result. Current presentation tests are included in the final suite rather than attributing their extra cases to Phase 9.

An initial sandboxed audit-probe invocation stalled and was stopped; normal local execution completed. A fresh-server browser invocation refused occupied port 8000 before collecting tests. Shared-server runs leave existing processes undisturbed; their two startup failures are not hidden. The final `playwright.audit.config.ts` starts and stops its own backend on 8019 and built preview on 5179, with both Groq flags false and only fixed synthetic demos available. Existing developer servers were not stopped. Existing backend deprecation/color-environment warnings and pip-audit's unhashed-pin warning remain non-failing. Graphify skips unsupported extensions (including CSS/hash sidecars), may model no symbols in browser test files and uses deterministic hub names after communities change; it is a code AST refresh, not semantic extraction. Browser cancellation prevents stale UI display, not guaranteed cancellation/erasure of an already submitted provider request.

## Final presentation claims and stopping point

Responsible claim: **“An independently implemented PMCEASY-inspired synthetic review prototype with exact lexical parsing, controlled evidence/rules, three module workflows, traceable DRAFT exports and bounded optional Groq assistance.”** Demonstrate Macro rule-derived descriptions; explicitly name Micro choices and Nano strategy notes as supplied examples. Show an ordinary pasted table abstaining and distinguish missing from zero.

Do not claim proprietary algorithm recovery, exact paid-product parity, 96 working clinical algorithms, verified ClinCheck/SureSmile support, patient-ready processing, generated treatment prescriptions, attachment optimization, clinical sequencing/anchorage, collision safety, treatment time prediction or clinical approval. The [completion checklist](FINOVA_PROJECT_COMPLETION_CHECKLIST.md) separates submission/demo readiness from software, vendor, clinical and deployment blockers. Phase 9 stops with this audit and targeted stabilization; no next phase or deployment is started.
