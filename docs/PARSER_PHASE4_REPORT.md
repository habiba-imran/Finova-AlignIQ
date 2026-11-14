# Phase 4 — generic TMT parsing and validated recovery

Implemented for the bounded formats below. **Prototype — not for clinical use.** Vendor semantic normalization, clinical R-series predicates, attachments and sequencing remain disabled. This task stops after Phase 4; it does not authorize clinical activation or deployment.

## Review and safety boundaries

The governing audit, corrected v2 specification, final architecture blueprint, prior phase reports, `PARSER_FINALIZATION_REPORT.md`, parser/adapters, semantic authorization, review/report services, schemas, frontend and tests were reviewed. Audit/corrected v2 requirements retain precedence over older drafts. Original governing documents and historical reports were preserved. Separately added deployment documents/configuration were read and preserved, not deployed by this task.

- Structure, lexical numbers and source indicators never establish clinical semantics or achieved movement.
- Original source values, identifiers, spans, Decimal precision and zero/missing distinctions remain intact.
- Unknown notation, direction, basis, mode, stage or scope stays UNKNOWN; no vendor convention is invented.
- JSON validity, role-constrained IDs, model confidence or repeated model agreement cannot grant authority.
- Associations require independent original-text evidence; unresolved positions retain raw data without accepted numeric values.
- Authentic vendor captures, independently reviewed oracles and approved release digests remain zero. No clinical threshold or recommendation was added.

## Updated architecture

```text
Raw TMT -> deterministic extraction -> structural quality/relevance
  -> optional automatic Groq recovery for controlled synthetic development inputs
  -> independent association validation and quarantine
  -> standardized lexical result -> existing semantic authorization
  -> existing descriptive findings -> templates / separately gated comment wording
  -> DRAFT report
```

`backend/app/parser/phase4.py` orchestrates normal intake. Original lexical/value/tooth routines are reused. Complete Markdown outer-pipe tables now parse deterministically, without calling Groq for the previous demonstration.

The normal pipeline is no longer restricted to two literal examples. A controlled recipe/seed generator can reproduce diverse original synthetic fixtures. The backend compares submitted text with that reproduction; arbitrary text cannot be enrolled through a prefix, checkbox, hash, uploaded expected output or free-text parameter. The normal UI has one Parse Table action and no second AI action/cloud checkbox.

Accepted recovery is no longer preview-only. A short-lived signed receipt carries accepted source-span IDs. Review/report requests submit original raw text/context plus that receipt, not trusted parsed JSON. The backend checks signature, expiry and exact input binding, then recomputes independent association proofs before reconstructing the lexical result. Existing semantic authorization runs afterward. Review/report do not repeat a Groq request.

Module/authority details: `docs/PARSER_PHASE4_ARCHITECTURE.md`.

## Supported input formats and recovery limits

Deterministic extraction retains recognizable tooth-row/tooth-column tables with tabs, pipes, semicolons or consistent 2+ space delimiters. It preserves irregular padding, blank lines, Unicode minus/degree signs, explicit units, literal direction suffixes, zero/missing markers and CR/LF/CRLF. Exactly one recognizable header/orientation/delimiter is required. Unknown labels alongside supported labels remain unsupported fields with original values retained.

Complete outer-pipe Markdown with an explicit divider is now deterministic. Unknown source/version/physical conventions do not trigger Groq.

| Recoverable variation | Independently checked evidence | Limit |
| --- | --- | --- |
| Mixed tab/pipe/semicolon grids | One explicit header and complete equal-width ordinal rows | No ragged/missing-middle repair |
| Transposed mixed grids | Explicit movement corner, tooth headers, movement rows and complete ordinal cells | No guessed column order |
| Inconsistent spacing in records | Explicit `Tooth: token` / `Tooth=token` scope and explicit `label: value` / `label=value` fields | Spaces alone never establish mapping |
| Recoverable line wrapping | Complete explicit label ending in `:`/`=`, followed immediately by one parseable value-only line | No joining digits or multiline numeric tokens |
| Transposed records | Explicit `Movement: label` scope followed by `tooth: value` fields | Tooth syntax is retained, not anatomically normalized |
| Fragments/disrupted header delimiters | Individually complete anchored records or complete ordinal rows under one explicit mixed header | Unrelated/unprovable fragments stay unresolved |

These are generic grammars, not verified vendor clipboard formats. Free visual alignment, ambiguous unanchored columns, merged cells, OCR/images/PDFs, quoted CSV/escaped-pipe cells, multitable joins, concatenated values and ambiguous header wrapping are not reconstructed by guessing.

Recovery bounds: **8,000 characters, 200 physical lines, 512 association positions, 1,600 referenced cells**. Oversized proofs abstain as a whole, without a transmitted prefix. Existing 100,000-character / 1 MiB intake, number/cell/grid bounds and 512-position review limit remain. Receipts are limited to 100,000 characters. Existing provider prompt/response bounds and timeout/token settings remain.

## Classification and automatic fallback

Typed `pipeline.quality.classification` distinguishes:

- `STRUCTURALLY_RECOGNIZED`: assignable structure; semantics may remain unknown.
- `PARTIAL`: existing positions with structural gaps.
- `RECOVERABLE_STRUCTURE`: baseline extraction failed but independently checkable associations exist.
- `AMBIGUOUS_STRUCTURE`: TMT-like input whose associations cannot be proven.
- `UNSUPPORTED_FORMAT`: possible TMT with unsupported structure/headers.
- `NOT_TMT`: empty/irrelevant content, numerical noise, product/conversation text without TMT structure, or detected hostile markup/instructions.

These classifications supplement the backward-compatible lexical statuses. Classification is conservative, not an infallible topic or PHI detector. Generic movement labels do not identify a vendor. All-zero values, missing axes and partially unsupported labels do not make a recognizable TMT irrelevant.

Groq is considered only for provable structural gaps. Successful extraction, irrelevant text, unprovable alignment and purely semantic issues make zero provider calls. Ambiguous numeric/unit conventions are not repaired by the model. A plausible arbitrary paste is still ineligible because server reproduction of a controlled synthetic fixture is independently required.

## Independent validation and partial abstention

Each original cell has an ID derived from exact zero-based Unicode-code-point start/end offsets. Original substrings, starting line/column and role candidates are retained. The dynamic strict schema enumerates allowable IDs separately for tooth/label/value roles. Groq supplies IDs, never replacement source values.

Every proposed triple must also belong to the independently proven association relation. Unknown IDs, wrong tooth/label/value combinations, duplicate value references and unsupported relationships reject or quarantine the affected position. Swapping equal-valued cells still fails when their original positions differ. Confidence scores and model voting are not used.

Accepted original cells pass through the existing deterministic numeric parser. Missing stays missing, explicit zero retains precision, and unsupported units/suffixes remain unresolved. No model text becomes source truth.

Partial recovery retains independently valid positions. Other identifiable original positions retain raw values/provenance with **AMBIGUOUS** numeric/field status and null accepted Decimal values. Unassignable fragments remain in `unparsed_lines` with issues. Omitted proposals are never converted to missing source cells or zero. Receipt replay reproduces that quarantine; unresolved structure additionally withholds zero-inventory statements. Existing duplicate safeguards remain.

The checker can enumerate the supported witness relations deterministically. The comparison below is against the shipped primary extractor; it does not prove an LLM is necessary or superior to a broader future deterministic implementation. The model remains an optional proposer with no semantic authority.

## Synthetic dataset and independent gold

`examples/phase4-synthetic-dataset.json` contains **78 original fixtures**, 13 recipes × seeds `0, 1, 2, 3, 7, 17`, covering:

1. Clean supported tables.
2. Irregular deterministic spacing/blank lines.
3. Six recoverable recipes: mixed rows/columns, wrapped values, labeled fragments, disrupted delimiter headers and partial fragments.
4. Ambiguous/corrupted alignment.
5. Irrelevant/product input.
6. Adversarial markup/instructions.
7. Unknown vendor conventions/unsupported labels.
8. Incomplete clinical metadata.

The generator declares original cells, exact Decimal expectations and offsets while constructing source, **before parsing**. `build_phase4_dataset.py` imports construction/contracts only, not extraction. Gold is not copied from parser output. There are **60 supported tables / 240 declared positions** and 18 negative/ambiguous cases. Both orientations, signs, Unicode, high precision, zero/missing and three newline encodings are represented.

Additional tests cover duplicates, unknown labels, empty/long input, malformed proposals, interrupted record scopes, transposed records, blank cells, resource limits and metamorphic padding/separator variants. These are not authentic clipboard captures, human-reviewed clinical gold or vendor releases.

The generator accepts a closed recipe enum and integer seed `0..1,000,000`, never user text. Authorization permits the controlled original rendering or its predefined browser-newline rendering; only expected text is derived for comparison, never submitted raw state.

## Quantitative comparison

### Independent-gold oracle-mocked benchmark

This isolates extraction/decision/validation from model variability. The mock proposes independently declared gold IDs. **These results are not live Groq accuracy.**

| Metric | Deterministic primary | Hybrid with oracle-mocked proposals |
| --- | --- | --- |
| Correct declared positions | 96/240 (40%) | 240/240 (100%) |
| Complete supported tables | 24/60 | 60/60 |
| Additional recovered positions | — | 144 |
| Provider calls | 0 | 36 mocked |
| Calls for 18 irrelevant/ambiguous/adversarial cases | 0 | 0 |

Counts include correctly retained missing positions, not invented numbers. Separate adversarial proposal tests verify rejection of incorrect associations despite valid JSON.

### Bounded live Groq checks

Six small fixed generated-synthetic requests were made, all using the independent parser key, requested `openai/gpt-oss-120b`, no retries/key rotation. Comment credentials/configuration were unchanged. Credentials/provider output/reasoning were not printed or persisted.

Initial role-unconstrained probes returned HTTP 200/model matches but **0/12 certified positions**, and were safely rejected. Times: 2.8146 / 1.8343 / 2.1535 seconds; total tokens: 774 / 901 / 880. JSON compliance was not accepted as correctness. Role-specific ID enums and explicit verbatim-ID instructions were then added without relaxing proof checks.

Final contract, seed 17:

| Recipe | Correct positions | Outcome | Elapsed | Prompt / completion / total tokens |
| --- | --- | --- | --- | --- |
| Mixed rows | 4/4 | All certified | 2.1639 s | 652 / 316 / 968 |
| Wrapped records | 4/4 | All certified | 2.2693 s | 725 / 295 / 1,020 |
| Labeled fragments | 2/4 | Partial; other positions quarantined | 2.1631 s | 725 / 235 / 960 |

Final live result: **10/12 (83.3%)**, compared with deterministic primary 0/12 on those same three formatting cases. No incorrect association was accepted. The fragment case is incomplete, not complete success; no extra requests chased a better sample. This tiny smoke sample is not a general accuracy, latency, capacity or vendor benchmark. Model omission/recall remains a limitation.

## Privacy and authorization

Default configuration remains cloud-disabled. Automatic recovery requires development environment, explicit server feature permission, backend-only `GROQ_API_KEY_2`, a recoverable structural gap, exact server reproduction of the generated fixture and explicit Parse Table. The existing intake checkbox is a claim, **not** authorization. There is no second cloud checkbox.

No arbitrary fixture enrollment, client-supplied trusted oracle, synthetic-prefix approval, real-patient exception or model-confidence override exists. Editing generated text clears its UI identity; forged identities fail reproduction. Server-generated text cannot become vendor VERIFIED.

401/429/503, timeout/connection errors, malformed output and unprovable proposals safely fall back/abstain. Parsing makes at most one attempt, with no automatic repair, retry, account rotation or quota bypass. Current model/timeout/token/reasoning configuration remains. Strict output IDs are constrained dynamically by role.

Future clinical-input cloud processing requires separately approved privacy/data handling, appropriate provider arrangements and an authorization mechanism implemented through reviewed changes. None was enabled here. No patient persistence, telemetry or automatic upload on typing/loading/confirmation was added.

## Downstream semantic/report integration

Receipts contain version, expiry, input/source/context binding hash and accepted span IDs, authenticated by HMAC-SHA256. They contain no raw source values or API key. Signing keys live only in process memory; expiry is 15 minutes and restart invalidates receipts. No input cache/database exists.

Every review/report request verifies the receipt and recomputes association proofs against exact original source. Even correctly signed unsupported associations fail. Expired/tampered/context-changed receipts return HTTP 409 with static reparse guidance. Browser-supplied findings or parsed JSON are not accepted.

`review_table` resolves lexical evidence before the existing semantic assessor. Vendor input remains UNVERIFIED with zero eligible observations absent released mappings. The vendor release registry stays empty.

An isolated Python test demonstrates generated messy source → mocked Groq proposal → proof validation → receipt replay → existing semantic assessor with explicit **TEST_ONLY** bookkeeping → three invented descriptive positions → mocked closed-wording Groq/templates → DRAFT report. Independent gold is asserted before constructing its exact in-memory TEST_ONLY snapshot. This is trusted library-only synthetic bookkeeping, not the authentic offline fixture-verification/reviewer process. Toy canonical identity/axis/direction labels are opaque and are not vendor mappings. HTTP cannot enable the test-only switch or submit checked evidence. Without that library switch, the same fixture still abstains. No human review/authentic evidence was fabricated.

Public UI reports remain abstention reports until actual source mappings are independently released. The engineering flow is connected; clinical authorization is not bypassed.

## APIs and schemas

- `POST /api/v1/tmt/parse`: raw submission plus optional `synthetic_fixture: {recipe, seed}`; runs Phase 4 automatically.
- `POST /api/v1/development/synthetic`: closed recipe/seed → original synthetic source/identity/category; rejects free text/unknown fields.
- `pipeline.quality`: typed classification/count/unresolved-line assessment; `pipeline.recovery_receipt`: nullable opaque receipt.
- Assistance adds `SPAN_ASSOCIATIONS_V1`.
- Review/report requests add optional `recovery_receipt`; invalid evidence returns HTTP 409. Existing DRAFT/semantic response contracts remain.
- Legacy `/api/parse` is unchanged. Legacy explicit `/api/v1/tmt/parse/assisted` remains for compatibility; the UI no longer uses it, and its old two-example limit does not constrain Phase 4.

New schemas: `pipeline-parse-request.v1.json`, `groq-recovery.v1.json`, `synthetic-generator-request.v1.json`. Automatic-result/review-request/report-request schemas gain additive fields. Original lexical, semantic, finding and final-report outputs remain unchanged. Runtime provider schemas additionally enumerate IDs by role. Strict private intake validation, size bounds and no-store headers remain.

## Frontend

Users paste, confirm existing synthetic intake and choose Parse Table. There is no vendor selector, second AI action or extra cloud checkbox. Generated examples carry a server-reproducible identity; arbitrary pastes remain cloud-ineligible.

Concise statuses show parsed/partial/AI recovery/clarification/unsupported outcomes; implementation codes and attempt counts are collapsed under Parsing details. Original/lexical values, unresolved fields and warnings remain. Raw state, preview/counts, inert React rendering, Clear and report/copy/TXT behavior are preserved. Edits/context/confirmation changes invalidate results and abort stale requests. Receipts remain in component memory and travel with original text to downstream requests, never browser persistence.

## Final verification

| Check | Result |
| --- | --- |
| Complete backend pytest | **584 passed**, including all 453 previous cases plus 131 Phase 4 cases |
| Complete frontend Vitest/RTL | **104 passed** |
| Complete browser suite | **40 passed** at 1440 / 1024 / 768 / 375 px, fresh backend startup |
| TypeScript / production Vite build | **Passed** |
| Dependency consistency | `pip check`: no broken requirements |
| Formatting | `git diff --check`: passed |
| Visual review | Desktop/mobile intake/status screenshots inspected; no page overflow asserted |
| Original governing docs / lexical schemas | Prior SHA-256 values retained |
| Authentic fixture verifier | `NO_AUTHENTIC_ORACLES`, Python exit 2; normalization disabled |
| Graphify | **832 nodes / 2,792 edges / 40 communities**, AST-only, no LLM extraction |

No automated test failures remain. Initial live ID-selection failures and final partial fragment recall are reported above. The legacy Markdown/API equality test was adapted for intentional deterministic improvement. Fifteen manual-assistance UI tests were adapted to the automatic workflow, retaining error/authorization/abstention coverage; browser cases retain raw/privacy checks. A restricted backend invocation stalled before collection and was stopped; normal approved local process execution passed the final full suite. Existing Starlette/httpx, color and Git newline notices were non-failing.

The bounded engineering criteria are met on the declared grammars/corpus: supported deterministic extraction, incremental live recovery, rejection/quarantine of unprovable mappings, zero irrelevant calls, no semantic invention, downstream integration and regression preservation. This does **not** establish universal TMT support or production clinical readiness.

Remaining engineering limitations: unanchored ambiguous layouts need more independently proved grammars; the generated corpus is small and not representative clinical/vendor validation; live results cover only three final examples; model omissions remain possible. Process-local receipts require one backend process. Multiworker/distributed receipts need a separately managed signing-key/deployment design. No production patient-data deployment validation is claimed.

## Vendor verification still required

Authentic captures, independently reviewed vendor oracles, approved releases and verified versions are **zero**. Each intended ClinCheck/SureSmile build/copy surface/locale needs:

1. Authorized de-identified verbatim logical clipboard captures, preserving whitespace, Unicode, units, precision/newlines, with hashes and independent source-UI evidence.
2. Exact build/version, copy surface, OS/browser/locale, capture/operator/authorization metadata and pseudonymous plan references.
3. Independently confirmed notation/dentition/arch/canonical tooth identities, including mirrored teeth and every intended numbering variant.
4. Per-axis units/signs/directions/frame/reference basis; crown/root/cusp/bracket bases stay distinct. Missing markers/tooth status need confirmation.
5. ClinCheck Align Final/Doctor Final/Comparison with operands/source operation and matched crown/root views where supported.
6. SureSmile reference/scope/stage views with verified stage kinds/endpoints; setup/lab revisions cannot be assumed aligner stages.
7. Independently authored lexical/semantic gold, field-level evidence locators and two approving reviewers including an orthodontist, binding exact artifact hashes.
8. Passing offline checks, then a separate scoped code-reviewed adapter/release approval. No near-version/cross-vendor extrapolation.

The full capture matrix remains in `backend/vendor_verification/README.md`. Guides, screenshots, generated fixtures and Groq success are not authentic evidence. No clinical activation began.

## Files and reproducible commands

New core modules: `backend/app/parser/{phase4,recovery,generated,receipts}.py`; additive contracts in `contracts.py`. Updated API review/report routes and review lexical resolution. New scripts `build_phase4_dataset.py`, `evaluate_phase4.py`; new `test_phase4.py`. UI/api/status/review/report receipt wiring and automatic tests were updated. Added original corpus, small frontend example/response fixture, three schemas and `docs/PARSER_PHASE4_ARCHITECTURE.md`. README and AST graph were updated. No dependency or secret file was changed. Concurrent deployment additions were preserved; this task did not deploy, stage, commit or push them.

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

Install/two-terminal default startup remain in README; no new package is needed. Optional controlled-synthetic cloud development, backend terminal:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
$env:FINOVA_ENVIRONMENT = 'development'
$env:FINOVA_PARSER_GROQ_ENABLED = 'true'
.\.venv\Scripts\python.exe scripts\run_dev.py --env-file ..\.env.local
```

Use already-private credentials; do not overwrite existing keys/files. Optional live evaluation is explicit and bounded:

```powershell
.\.venv\Scripts\python.exe scripts\evaluate_phase4.py --live 3 --env-file ..\.env.local
# Narrow further: --live 1 --live-recipes wrapped
```

Without `--live`, provider traffic is oracle-mocked. Missing parser credentials produce SKIPPED. Only aggregate validation/timing/usage prints. Real-input privacy approval, vendor compatibility and clinical activation remain separate future gates.
