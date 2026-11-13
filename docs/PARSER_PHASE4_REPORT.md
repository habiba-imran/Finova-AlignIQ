# Phase 4 — generic TMT parsing and validated structural recovery

Implemented for the explicitly bounded formats below. **Prototype — not for clinical use.** Clinical R-series predicates, attachments, sequencing and vendor semantic normalization remain disabled. This task stops at Phase 4; it does not authorize clinical activation or deployment.

## Review and retained boundaries

The governing documents in `docs/`, prior phase reports and `PARSER_FINALIZATION_REPORT.md`, existing parser/adapters, semantic authorization, review/report code, schemas, frontend and tests were reviewed. The audit and corrected v2 requirements retain precedence over older proposals. The supplied governing documents and historical implementation reports were preserved. Separately added deployment files were read and preserved; this task does not deploy or replace their configuration.

- Structure, lexical numbers and source indicators never establish clinical semantics or achieved movement.
- Original identifiers/cells/spans, Decimal precision and explicit zero versus missing remain intact.
- Unknown direction, notation, basis, plan mode, stage or scope remains UNKNOWN; no vendor convention is invented.
- Groq proposals, valid JSON, role-constrained IDs and synthetic claims cannot grant semantic authority.
- Accepted associations require independent original-text evidence; unresolved positions are quarantined without numerical acceptance.
- The authentic vendor manifest and code-controlled release registry remain empty. No clinical threshold or recommendation was added.

## Architecture and the two previous limitations

```text
Raw TMT -> deterministic lexical extraction -> structural quality/relevance
  -> optional automatic Groq recovery for controlled synthetic development inputs
  -> independent association validation / partial quarantine
  -> standardized lexical result -> existing semantic authorization
  -> existing descriptive findings / templates or separately gated wording
  -> DRAFT report
```

`backend/app/parser/phase4.py` is the normal intake orchestrator. Original parser/value/tooth routines remain reused. Complete Markdown outer-pipe tables now parse deterministically, without spending a provider call on the previous demonstration.

**The two-string restriction no longer constrains the normal pipeline.** A controlled recipe/seed generator can reproduce diverse original synthetic fixtures, including values, delimiters, wrapping and line endings. The server compares the submitted text against that reproduction; arbitrary text cannot be enrolled by a checkbox, prefix, uploaded expected output or hash. The UI has one Parse Table action, without a second AI button or cloud checkbox.

**Recovered lexical results now reach downstream processing.** The server issues a short-lived signed association receipt. Review/report requests send their original raw text/context and the opaque receipt, never trusted parsed JSON. The server rechecks signature, expiry, exact binding and independently recomputes the association proofs before reconstructing the lexical result. Existing semantic authorization runs on that result. No repeated Groq call is necessary for review/report.

Detailed module/authority flow is documented in `docs/PARSER_PHASE4_ARCHITECTURE.md`.

## Supported input formats and exact limits

### Deterministic path

Existing recognizable tooth-row/tooth-column tables with tabs, pipes, semicolons or consistent 2+ space delimiters retain their previous behavior and bounds. Blank lines, irregular cell padding, Unicode minus/degree signs, explicit units, literal direction suffixes, zero/missing markers and CR/LF/CRLF remain supported. Exactly one recognizable header/orientation/delimiter is required. Unknown labels alongside supported labels are retained with unsupported-field warnings.

Complete outer-pipe Markdown with an explicit separator row is now a deterministic extension. No model call is made merely because fields, source version, physical conventions or vendor identity are unverified.

### Recoverable structural witnesses

The model proposes original source cell IDs for tooth/label/value associations. The checker accepts only these independently defined forms:

| Form | Independent evidence | Recovery limits |
| --- | --- | --- |
| Mixed explicit delimiters | One explicit header and complete ordinal rows split by tab/pipe/semicolon, with equal widths | No missing-middle or ragged-row repair; numeric tooth syntax only for this ordinal grammar |
| Transposed mixed grids | Explicit movement corner, tooth headers, recognized movement row and complete ordinal values | No axis/direction inference or guessed column order |
| Inconsistent spaces in labeled records | Explicit `Tooth: token` or `Tooth=token` scope, followed by explicit `label: value` / `label=value` fields | Spaces do not establish association; unknown interruptions end scope |
| Value-only line wrapping | A complete explicit label ending in `:`/`=`, immediately followed by one independently parseable value-only physical line | No joining split digits, multi-line numbers or guessed missing cells |
| Transposed movement records | Explicit `Movement: label` scope followed by literal `tooth: value` fields | Tooth syntax retained without anatomical conversion |
| Table fragments / disrupted header delimiters | Individually complete anchored records or complete ordinal rows beneath one explicit mixed header | Independent fragments can survive while unrelated/unprovable fragments remain unresolved |

These forms provide recovery beyond the former Markdown-only wrapper. They are generic grammars, not purported vendor clipboard formats. Free visual alignment, merged cells, OCR/images/PDF tables, quoted CSV/escaped-pipe cells, multi-table joins, concatenated values, missing delimiters or ambiguous header wrapping are not reconstructed by guessing. The original text remains available for clarification.

Recovery has engineering bounds of 8,000 characters, 200 physical lines, 512 association positions and 1,600 referenced cells. Oversized proof sets abstain as a whole, not a transmitted prefix. Existing 100,000-character / 1 MiB intake, numeric/cell/grid and 512-position review limits remain. Existing prompt/response byte bounds and parser timeout/token settings remain in force. Receipts are bounded to 100,000 characters.

## Classification and fallback decisions

The typed `pipeline.quality` distinguishes:

- `STRUCTURALLY_RECOGNIZED`: assignable structure; clinical/semantic unknowns may remain.
- `PARTIAL`: existing structural positions with gaps.
- `RECOVERABLE_STRUCTURE`: no reliable baseline extraction, but independently checkable new associations exist.
- `AMBIGUOUS_STRUCTURE`: TMT-like input whose associations cannot be proven.
- `UNSUPPORTED_FORMAT`: possible TMT with unsupported structure/headers.
- `NOT_TMT`: empty, irrelevant, numerical noise, conversation/product content without tooth/movement structure, or detected hostile markup/instructions.

These are input-quality classifications; original lexical statuses remain backward compatible. The classification gate is conservative, not an infallible topic/PHI detector. It does not infer a vendor from common movement labels. All-zero values, missing axes and partially unsupported labels do not make an otherwise recognizable TMT irrelevant.

Groq is considered only for provable structural gaps. Successful deterministic extraction, irrelevant text, unprovable alignment and purely semantic problems produce zero cloud calls. A value whose only issue is an ambiguous numeric/unit convention is not repaired by the model. Common signs/directions/units remain lexical tokens, not verified physical meanings.

Even an unusually plausible or malicious arbitrary paste cannot pass cloud authorization: its text must also match a controlled server-generated fixture. Embedded instructions are inert, and the input classifier blocks the shipped adversarial examples before transmission.

## Independent validation and partial abstention

Each source cell has a stable ID derived from its exact zero-based Unicode-code-point start/end offsets. Its raw substring, one-based starting line/column and role candidates are retained. The dynamic strict schema restricts each output ID to the corresponding tooth/label/value role. Groq cannot provide new cell values in that schema.

Role validity alone is insufficient. Every proposed triple must belong to the independently proven association relation. Unknown IDs, swapped teeth/labels/values, duplicate value references and unsupported mappings are rejected. Identical raw numbers at different locations cannot be swapped just because their text agrees. Confidence scores and repeated model votes are not used.

Accepted source cells go through the existing deterministic numeric parser. Missing markers remain missing, explicit zeros retain exact precision, and unsupported units/suffixes remain unresolved. No model text becomes source truth.

When only some associations are acceptable, independently valid positions survive. The other originally identifiable positions retain raw values and provenance with `AMBIGUOUS` numeric/field status and null accepted Decimal values. Unassignable fragments remain in `unparsed_lines` with source issues. No omitted proposal is converted into an absent source cell or zero. Reviews reconstitute that same quarantine; unresolved structure additionally withholds categorical zero inventory. Existing duplicate-field safeguards still apply.

The verifier can enumerate the supported witness relations deterministically. The measured comparison is against the shipped primary extraction path; it does not establish that an LLM is information-theoretically necessary or superior to a broader future deterministic grammar implementation. The model remains an optional structural proposer with no semantic authority.

## Controlled synthetic dataset and independent gold

`examples/phase4-synthetic-dataset.json` contains **78 original fixtures**: 13 recipes × 6 seeds (`0, 1, 2, 3, 7, 17`). Categories cover all requested groups:

1. Clean supported grids.
2. Irregular deterministic spacing/blank lines.
3. Six recoverable formatting recipes: mixed rows, mixed columns, wrapped values, labeled fragments, disrupted delimiter headers and partially disrupted fragments.
4. Ambiguous/corrupted alignment.
5. Irrelevant conversation/product-style input.
6. Adversarial markup/instructions.
7. Unknown vendor conventions/unsupported labels.
8. Unsupported/incomplete clinical metadata.

The source-construction generator declares original tooth/label/value strings, exact Decimal expectations and original offsets as it emits the fixture, before any parser runs. `build_phase4_dataset.py` imports the generator/contracts only, not extraction. Gold is not produced by copying parser output. The supported corpus has **60 tables / 240 declared positions**, including missing markers; the remaining 18 are negative/ambiguous cases. Both orientations, signs, Unicode, very high precision, explicit zeros and three newline encodings are represented.

Additional tests cover duplicates, unknown labels, empty/long input, malformed reconstruction, mixed separators, record-scope interruption, transposed records, literal missing cells, oversized proof sets and metamorphic padding/separator variants. These invented fixtures are never labeled authentic vendor captures, human-reviewed clinical gold or approved source mappings.

The generator accepts a closed recipe enum and a bounded integer seed (`0..1,000,000`); it accepts no user text. Source identity permits either the original controlled rendering or its predefined browser-newline rendering. Only expected text is derived for that comparison; submitted raw state is never normalized or rewritten.

## Quantitative comparison

### Repeatable independent-gold oracle-mocked benchmark

This isolates extraction, decision and validation behavior from model variability. Its mocked provider proposes the independently declared gold IDs. **It is not a measurement of live Groq accuracy.**

| Metric | Deterministic primary | Hybrid with oracle-mocked proposals |
| --- | --- | --- |
| Correctly assigned declared positions | 96/240 (40%) | 240/240 (100%) |
| Complete supported synthetic tables | 24/60 | 60/60 |
| Recovered additional positions | — | 144 |
| Provider calls | 0 | 36 mocked, one per recoverable fixture |
| Calls for 18 irrelevant/ambiguous/adversarial fixtures | 0 | 0 |

Counts include correctly retained missing positions, not invented numeric values. Separate adversarial proposal tests verify that incorrect/unprovable proposals cannot achieve this result by passing JSON/schema checks alone.

### Bounded actual Groq probes

Six small, fixed generated-synthetic requests were made in total, all with the parser key, requested model `openai/gpt-oss-120b`, no retries and no key rotation. No report-comment credential/configuration was changed. Keys/provider bodies/reasoning/outputs were not printed or retained.

The initial three role-unconstrained probes returned HTTP 200/model matches but **0/12 independently accepted positions**, and were safely rejected. Their elapsed times were 2.8146 / 1.8343 / 2.1535 seconds and total token counts 774 / 901 / 880. Valid structured JSON was not treated as correctness. This exposed a model-ID selection weakness; the prompt and dynamic schema were tightened to constrain IDs by original role, without relaxing association validation.

The final three probes used the tightened contract:

| Original synthetic recipe, seed 17 | Correct positions | Outcome | Elapsed | Prompt / completion / total tokens |
| --- | --- | --- | --- | --- |
| Mixed delimiter rows | 4/4 | All associations certified | 2.1639 s | 652 / 316 / 968 |
| Wrapped value records | 4/4 | All associations certified | 2.2693 s | 725 / 295 / 1,020 |
| Same-line labeled fragments | 2/4 | Partial recovery; remaining positions quarantined | 2.1631 s | 725 / 235 / 960 |

Final live result: **10/12 positions (83.3%)**, versus 0/12 for deterministic primary extraction on those same three formatting cases. No incorrect association was accepted. The fragment result is incomplete, not represented as complete success. No extra requests were made to chase a better sample. This is a tiny engineering smoke sample, not a general model-accuracy, latency or vendor benchmark. Model omission/recall remains a limitation; partial abstention is part of the supported behavior.

## Privacy and automatic cloud authorization

Normal configuration remains cloud-disabled. Automatic recovery requires all of:

1. Development environment and explicit server parser feature permission.
2. The independent backend-only `GROQ_API_KEY_2`; report `GROQ_API_KEY` is unchanged.
3. A quality gate identifying independently recoverable structural positions.
4. Exact server reproduction of the controlled synthetic recipe/seed and allowed newline rendering.
5. The user's explicit Parse Table request. Existing intake synthetic-data confirmation remains a claim; it does not supply cloud authority.

There is no arbitrary fixture enrollment/upload, client-supplied trusted oracle, synthetic-prefix authorization, provider confidence override or real-patient exception. Editing a generated example clears its UI authorization identity; forged identities fail server reproduction. Even unchanged generated text can never become vendor VERIFIED.

Provider 401/429/503, timeouts, connection problems, malformed/schema-invalid output and unprovable IDs safely return deterministic fallback or explicit abstention. Parsing performs no automatic repair call, retry, account rotation or quota bypass. Default timeout/model/token/reasoning controls are retained from parser finalization. Role-specific enums are built dynamically for strict structured output.

Future automatic processing of actual clinical input requires separately approved data handling/privacy, appropriate provider arrangements and an authorization mechanism implemented through a reviewed change. None was fabricated or enabled here. No patient-data persistence, external telemetry or automatic upload on typing/loading/confirmation was added.

## Downstream semantic/report integration

Receipts contain version, expiry, a hash binding raw text/source/context and accepted source-span IDs, authenticated with HMAC-SHA256. They contain no raw cells, clinical values or API key. The signing secret exists only in process memory. Receipts expire after 15 minutes; process restart invalidates them. There is no input cache or database.

On each review/report request, the server verifies the receipt and recomputes the structural witnesses from exact original input before lexical reconstruction. A valid signature with unsupported associations still fails. Tampered, expired or context-changed receipts return HTTP 409 with static reparse guidance. The browser cannot send trusted findings or standardized measurements.

`review_table` now resolves that validated lexical result before the existing semantic assessor. Arbitrary vendor inputs—including recovered lexical values—remain UNVERIFIED, with zero eligible clinical/descriptive measurements unless existing exact source evidence authorizes them. The vendor release registry remains empty.

An isolated Python test demonstrates the full required flow: generated messy input → mocked Groq structural proposal → original-span validation → receipt replay → existing semantic assessor with explicit **TEST_ONLY** bookkeeping → three eligible invented descriptive positions → mocked closed-wording Groq/templates → DRAFT report. Independent gold is asserted before creating its exact TEST_ONLY snapshot. Its canonical identity/axis/direction names are opaque toy labels, not vendor mappings. The test-only switch/checked evidence are library-only; HTTP has no way to enable this domain for arbitrary input. Omitting that library switch still yields semantic abstention, even with the same fixture. No fabricated reviewer or authentic evidence is created.

This proves the engineering connection through the existing semantic gates, not vendor compatibility. Public UI reports remain abstention reports until genuine mappings are independently released.

## API and schema changes

- `POST /api/v1/tmt/parse`: existing raw submission plus optional `synthetic_fixture: {recipe, seed}`. It runs the Phase 4 flow automatically; successful/irrelevant/unapproved inputs make no provider call.
- `POST /api/v1/development/synthetic`: a recipe/seed request returns generated synthetic source/identity/category. Unknown fields/free text are rejected; no caller text can be enrolled.
- `pipeline.quality`: typed structural/relevance assessment; `pipeline.recovery_receipt`: nullable opaque receipt.
- Assistance supports `SPAN_ASSOCIATIONS_V1` in addition to the preserved legacy certificate.
- Review/report requests accept optional `recovery_receipt`; responses retain their existing DRAFT/semantic contracts. Invalid receipt → HTTP 409.
- Legacy `/api/parse` remains unchanged. Legacy explicit `/api/v1/tmt/parse/assisted` remains available for compatibility; the normal UI no longer uses it, and its old two-example restriction does not constrain the Phase 4 route.

New schemas: `pipeline-parse-request.v1.json`, `groq-recovery.v1.json`, `synthetic-generator-request.v1.json`. Automatic result, review request and report request schemas gain the additive fields. Original lexical, semantic, finding and final-report output schemas remain unchanged. The dynamic provider schema further enumerates IDs by role at request time. Private intake errors, request bounds and no-store headers remain.

## Frontend behavior

Users paste, confirm the existing synthetic-only intake notice and select Parse Table. There is no vendor/format selector, second AI action or additional cloud consent checkbox. Generated development examples carry a recipe identity; the server must reproduce them before automatic recovery. Arbitrary pasted input remains ineligible for cloud processing.

Concise statuses show parsed, partially parsed, AI-assisted recovery, needs clarification or unsupported input. Internal codes/attempt counts are collapsed under Parsing details. Original/lexical values, unresolved positions and targeted warnings remain visible. Raw textarea state, monospaced preview, counts, inert React rendering, Clear and reports/copy/TXT behavior are retained. Edit/context/confirmation invalidation and stale response aborts remain. Receipts stay in component memory, travel with original raw input to review/report and are never stored in browser persistence.

## Validation and completion status

Final suite results and graph refresh are recorded after the final checks below. Existing behavior is retained; the legacy test comparing Markdown abstention with normal intake was updated for the intentional deterministic improvement. The 15 manual-assistance UI tests were adapted to cover automatic loading/errors/authorization/abstention instead of testing removed UI controls. Browser cases similarly retain privacy/raw-preservation coverage while testing the one-action flow.

The bounded generic parser engineering criteria are met on the declared grammars/corpus: deterministic supported extraction, measured incremental live recovery, rejection/quarantine of unprovable associations, zero irrelevant cloud calls, no semantic invention, downstream integration and regression preservation. This does not imply universal TMT support or production clinical readiness. The live fragment recall limitation is explicit.

Remaining limits requiring review:

- Free visual alignment and fundamentally ambiguous/unanchored source text remain unsupported; more grammars need independent proofs and separate gold cases.
- The 78-case generated corpus is an engineering corpus, not a representative independently collected clinical/vendor validation dataset. Live results cover only three final examples.
- Live model omissions remain possible; partial abstention is intentional. Confidence, schema compliance or repeated sampling cannot close that gap.
- Receipt keys are process-local; use one backend process for this development workflow. Multiworker/distributed receipt support and broader deployment hardening require a separate signing-key/deployment design. Restart/expiry produces a safe reparse requirement.
- Real-input cloud privacy/provider authorization remains unimplemented and disabled. No patient-data deployment validation is claimed.

## Remaining vendor-verification requirements

Authentic captures, independently reviewed vendor oracles, approved releases and verified source versions are still **zero**. Required for each supported exact ClinCheck/SureSmile build, copy surface and locale:

1. Authorized, de-identified verbatim logical clipboard captures with original whitespace, units, precision, Unicode/line endings and artifact hashes, plus independent source-UI evidence.
2. Source/build/version, copy surface, OS/browser/locale, capture/operator/authorization metadata and pseudonymous case/plan references.
3. Independently confirmed numbering/dentition/arch and canonical tooth identities, including mirrored teeth and every intended notation variant.
4. Per-axis units, literal signs/directions, coordinate frame and reference point; crown/root/cusp/bracket bases must remain distinct. Missing markers and tooth status need source confirmation.
5. ClinCheck Align Final/Doctor Final/Comparison captures with exact operands and source-defined operation; matched crown-center/root-apex views where supported.
6. SureSmile supported reference choices and total/cumulative/incremental/stage views, independently identified stage kinds/endpoints; setup/lab revision counters must not be assumed aligner stages.
7. Independently authored lexical/semantic gold with field-level evidence locators; two distinct approving reviewers including an orthodontist, binding exact raw/expected/source-evidence hashes.
8. Passing offline oracle checks followed by a separate scoped code-reviewed adapter/release approval. No near-version or cross-vendor extrapolation is permitted.

The exact capture matrix remains in `backend/vendor_verification/README.md`. Published guides, screenshots, generated examples and successful Groq calls are not authentic clipboard evidence.

## Files and commands

```text
backend/app/parser/
  phase4.py           orchestration/classification
  recovery.py         independent witnesses, proposal checks, quarantine
  generated.py        controlled synthetic source + independent gold
  receipts.py         stateless binding/reverification
  contracts.py        additive typed contracts
backend/app/api/{automatic_parse,review,reports}.py
backend/app/review/{models,service}.py
backend/scripts/{build_phase4_dataset,evaluate_phase4,export_schemas}.py
backend/tests/test_phase4.py
frontend/src/{App,App.assisted.test,App.review.test,FinalReport.test}.tsx
frontend/src/phase4Example.json
frontend/src/api/{parse,review,report}.ts
frontend/src/components/{ParserStatus,DraftReviewPanel,FinalReportPanel}.tsx
frontend/e2e/automatic.spec.ts
frontend/src/test/fixtures/synthetic-phase4-recovery.json
examples/phase4-synthetic-dataset.json
schemas/{pipeline-parse-request,groq-recovery,synthetic-generator-request}.v1.json
schemas/{automatic-parse-result,review-request,report-request}.v1.json
docs/PARSER_PHASE4_ARCHITECTURE.md
README.md / PARSER_PHASE4_REPORT.md / graphify-out/
```

Install/run defaults and existing two-terminal setup remain in README. No dependency was added. Reproduce deterministic checks with:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe scripts\build_phase4_dataset.py
.\.venv\Scripts\python.exe scripts\evaluate_phase4.py
.\.venv\Scripts\python.exe scripts\export_schemas.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check

Set-Location 'C:\Finova AlignIQ\frontend'
npm test
npm run build
npm run test:e2e
```

Optional generated-synthetic cloud development, in the backend terminal:

```powershell
$env:FINOVA_ENVIRONMENT = 'development'
$env:FINOVA_PARSER_GROQ_ENABLED = 'true'
.\.venv\Scripts\python.exe scripts\run_dev.py --env-file ..\.env.local
```

With the frontend running, load the generated recovery example, confirm synthetic intake and choose Parse Table. Loading/confirmation does not transmit to Groq. The parser key must already be held privately; do not overwrite existing keys/files. Production/default configuration remains disabled.

Optional, intentionally live and bounded evaluation (at most three fixed generated requests):

```powershell
.\.venv\Scripts\python.exe scripts\evaluate_phase4.py --live 3 --env-file ..\.env.local
# Narrower example: --live 1 --live-recipes wrapped
```

Without `--live`, provider calls are oracle-mocked. Missing parser credentials produce SKIPPED live output. No sensitive payload or credential prints. No CLI call enables vendor semantics or changes the comment credential. No commit, push, deployment or clinical activation was performed by this task.
