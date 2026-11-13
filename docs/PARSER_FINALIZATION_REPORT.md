# Parser finalization and Groq connectivity

Status: implemented for synthetic development. **Prototype — not for clinical use.** No clinical predicate, vendor mapping, authentic fixture release or real-patient transmission was enabled. This task ends at parser infrastructure and connectivity; clinical-rule activation has not begun.

## Governing requirements and review

The three complete documents in `docs/`, the Phase 1/1.5/2A/3 reports, existing parser/adapters, semantic fixture authorization, review/report services, JSON contracts and tests were reviewed. The independent audit and corrected v2 requirements take precedence over older draft proposals. Governing documents and earlier phase reports were preserved; the two original parser schemas retain their previous hashes.

Binding boundaries retained:

- Lexical extraction is not clinical normalization, vendor verification or assessment of achieved movement.
- Missing, invalid, ambiguous and unverified fields stay distinct from explicit zero; unknown direction/identity/basis/scope stays UNKNOWN.
- Numbering, axes, signs, crown/root/cusp references, plan comparisons and stage scopes require independent source evidence; none is inferred from a plausible table.
- Authentic captures, independent gold outputs, qualified reviews and a separate code-approved release are required for vendor authorization. The approval registry remains empty.
- Clinical thresholds, recommendations, attachments, sequencing and treatment suitability remain disabled; no old draft cutoff was implemented.
- No patient-data persistence, automatic provider upload, model-authored facts or LLM semantic authority is introduced. Real-patient cloud transmission has no environment/request override.

No required governing document was missing or unreadable. Existing Markdown audit/corrected-spec/architecture documents remain the authoritative supplied versions.

## Changes and architecture

```text
Unchanged logical textarea value + optional unverified context
  -> explicit Parse Table -> POST /api/v1/tmt/parse
  -> existing deterministic lexical parser
  -> automatic source indicators / syntax candidates / targeted clarifications
  -> raw + Decimal lexical preview, no cloud call

Only after structural failure, development permission, independent key,
exact shipped synthetic-example match and separate affirmative consent:
  -> explicit Try AI-assisted parsing -> POST /api/v1/tmt/parse/assisted
  -> deterministic parser first again
  -> independent versioned structural grammar certificate
  -> immutable original-cell span lattice -> bounded Groq structural proposal
  -> strict JSON + COMPLETE association equality against the certificate
  -> reject, or reuse lexical tooth/value routines with ORIGINAL cells/spans
  -> unverified lexical preview; no canonical/vendor/clinical authority

Existing explicit review/report actions
  -> independently reparse original raw input
  -> unchanged semantic release gate -> unchanged descriptive safeguards
  -> DRAFT report/templates; optional separately gated comment wording
```

The normal source dropdown is removed. Normal UI requests retain `source_claim: "Unknown"`, including after a source indicator is detected. Neither detected source nor a numbering syntax candidate is copied into verified metadata. Existing source-claim support remains in backend legacy contracts for compatibility.

The existing lexical value routines, numbering checks, label aliases, duplicate handling, Decimal precision, missing/zero distinctions and semantic release algorithms are retained. A library-only certified-grid parameter allows the new wrapper to reuse those routines; HTTP never accepts supplied grids, proposals, cell values, evidence overrides or findings. Existing `/api/parse` responses are unchanged. The generic parser/adapter version still identifies those existing lexical routines; the new pipeline and structural certificate have separate versions.

### Automatic detection

1. Existing deterministic layout detection uses explicit headers, recognized lexical aliases, delimiter candidates and orientation. Exactly one candidate is required; no nearest-format guess is made.
2. Brand words present in original text become evidence-backed **indicators**, not trusted declarations. Each indicator retains original line text and spans.
3. Two deliberately narrow documented signature pairs are also indicators: Align Final with Doctor Final; Displacement Type with Cusp Tip. A single generic label, tooth notation or movement value cannot identify a vendor.
4. One candidate produces `DETECTED_UNVERIFIED`; conflicting candidates produce `CONFLICT` and detected source Unknown; no candidate produces `UNKNOWN`. `verified_source` is always null in this release. Indicators can be spoofed by text, so none grants semantic authority.
5. Tooth tokens are compared with syntactic FDI/Universal/quadrant-token patterns. For example `13` fits multiple systems. Candidates are informational only; no anatomical identity, arch or dentition is assigned.
6. Targeted clarification entries identify unresolved source/version/notation/dentition/arch/mode/basis/scope/frame and affected measurement IDs. Supplied metadata remain claims, even where no longer listed as missing. Existing field-level parsing issues remain intact.

`layout_recognized` describes recognized header/orientation structure, not complete extraction or vendor support. Numeric/field statuses, issues and coverage must still be inspected.

### Structural fallback and independent validation

The only shipped certificate grammar is **MARKDOWN_PIPE_V1**. It requires complete outer-pipe rows, an explicit Markdown separator row, exactly consistent widths and an independently recognizable orientation. Both tooth-row and tooth-column orientations are supported. Source line endings, Unicode, raw padding, explicit empty cells and original offsets remain intact. The structural separator is retained as a nonmeasurement line, never parsed as values.

The certifier refuses ragged rows, missing dividers, escaped pipes, a second divider/table, unassignable lines inside the table or nonblank trailing footers. It does not fill omitted cells, align whitespace, join multiline cells or repair corruption. Existing engineering limits also apply; assistance has an additional 8,000-character input bound and the shared 24,000-byte serialized prompt bound.

Each proven original cell receives an ID such as `L4C2` linked locally to its raw text, original line/column and zero-based Unicode-code-point offsets (end exclusive). Groq receives only these fixed synthetic cells and positions. Its strict output is:

```json
{
  "grammar": "MARKDOWN_PIPE_V1",
  "orientation": "TEETH_IN_ROWS",
  "rows": [
    ["L2C1", "L2C2", "L2C3"],
    ["L4C1", "L4C2", "L4C3"],
    ["L5C1", "L5C2", "L5C3"]
  ]
}
```

IDs are references to original text spans, not model-authored replacement values. The complete ordered grid must equal the independently certified grid: header, every body row, every column, and orientation. Extra/missing/duplicate IDs, row or column swaps, invented IDs/values, extra properties, wrong grammar, malformed/duplicate-key JSON and wrong orientation all reject the proposal. Swapping two cells with identical raw values still fails because their positions/associations differ. Valid JSON or valid substring positions alone cannot authorize extraction.

On acceptance, actual cells are read from the trusted original-span lattice, not model output. Tooth/value parsing, units and Decimal handling run locally. No cleaned intermediate table, guessed alignment, generated JSON values or span remapping is used. All canonical fields remain null and source semantics remain unverified. On rejection/failure, the original deterministic abstention is returned with a static reason; no partial AI repair is accepted.

**Deliberate limitation:** for this narrow grammar the independent certifier already derives the same grid. The model adds no information beyond a checked structural proposal; this exercises the hybrid boundary safely. This is not a claim that arbitrary damaged vendor clipboard text can be recovered. Wider grammars require independent deterministic association proofs and additional synthetic/adversarial tests; an LLM opinion cannot replace those proofs.

## Privacy, credentials and configuration

`GROQ_API_KEY` remains exclusively the comment-generation credential. `GROQ_API_KEY_2` is exclusively the parser credential. Neither is used as failover for the other. Existing private key files were not changed. Secrets are excluded from settings representation/serialization and never placed in the frontend, schemas, report output or graph artifacts.

Normal Parse Table is local-backend-only even when Groq is configured. The assisted route requires all of:

- `FINOVA_ENVIRONMENT=development` (default production).
- `FINOVA_PARSER_GROQ_ENABLED=true` (default false).
- A valid backend-only parser key.
- Deterministic structural failure, no assigned measurements, and a valid independent certificate.
- An exact UTF-8 hash match to one of **two unchanged shipped cloud-allowed synthetic examples**. A checkbox or synthetic prefix is insufficient. Changed values, arbitrary pastes and authentic captures are not eligible.
- `synthetic_data_confirmed: true` and separate strict `cloud_synthetic_consent: true` on the explicit action.

The missing/malformed catalog fails closed without breaking ordinary local intake. Normal tests do not load private env files. Future real-input transmission requires a separately approved privacy policy, actual deployment/data-handling authorization and affirmative user consent implemented through a reviewed code change. None of those gates can be claimed satisfied by setting a boolean in this release.

| Parser setting | Default / supported range |
| --- | --- |
| `GROQ_API_KEY_2` | Empty; server only |
| `FINOVA_ENVIRONMENT` | production; cloud allowed only in development |
| `FINOVA_PARSER_GROQ_ENABLED` | false |
| `GROQ_PARSER_MODEL` | openai/gpt-oss-120b; configurable model ID, actual strict-schema compatibility required |
| `GROQ_PARSER_TIMEOUT_SECONDS` | 8; 0.1–30 seconds |
| `GROQ_PARSER_MAX_COMPLETION_TOKENS` | 2048; 256–8192 |
| `GROQ_PARSER_REASONING_EFFORT` | low; low/medium/high |
| Parser temperature / retries | 0 / 0 |

Both services use the shared bounded Groq HTTPS transport, with independent settings/keys and schemas. Provider URL is fixed, redirects and environment proxies disabled, no tools or streaming. Existing comment retry policy is unchanged; parsing makes at most one attempt and never repairs/retries a failed response. A 429/503 returns abstention rather than ignoring the provider delay or rotating keys. No account quotas are assumed and no limit-circumvention mechanism exists.

The transport adds sanitized elapsed time, HTTP status, model-equality and numeric usage counters for connectivity checking. Provider model mismatch rejects content. These metrics do not place provider bodies or reasoning in API/report output. Existing comment wording still validates exact approved phrases/references and inserts all facts locally. No report semantic gate was weakened.

The optional explicit env loader imports known single-line settings only, supports plain/quoted values, performs no evaluation/interpolation, preserves existing process environment values and writes nothing. It is used only when an explicit development/probe command supplies `--env-file`; ordinary settings do not auto-discover secrets.

## API and schema contracts

Existing routes and request/response contracts remain available: health, `/api/parse`, `/api/v1/tmt/observations`, `/api/v1/reports/draft`.

New routes:

| Route | Request | Response / network behavior |
| --- | --- | --- |
| `POST /api/v1/tmt/parse` | Existing `RawTMTSubmission` | `AutomaticParseResult`; zero provider calls |
| `POST /api/v1/tmt/parse/assisted` | Existing submission plus required affirmative `cloud_synthetic_consent` | Same result with explicit BLOCKED/FAILED/REJECTED/ACCEPTED status; only gated synthetic provider access |

`AutomaticParseResult` preserves all existing lexical fields at the top level and adds required `pipeline`:

```text
pipeline.version = 1.0.0
pipeline.detection = detected_source, verified_source(null), status,
                     original evidence-backed indicators, notation_candidates,
                     layout_recognized
pipeline.assistance = available, status, reason, attempts, certificate,
                      origin, real_patient_transmission_enabled(false)
pipeline.clarifications[] = code, field, measurement_ids, message
```

Generated additions: `schemas/automatic-parse-result.v1.json`, `schemas/assisted-parse-request.v1.json`, `schemas/groq-structure.v1.json`. Existing parser, semantic, review and report JSON schemas are retained. The outer pipeline is not semantic evidence. A library caller invoking the existing semantic assessor must supply the lexical portion as `ParseResult`, excluding `pipeline`; the shipped review/report routes recompute their own parse and do not accept returned models.

All routes retain 1 MiB request-body bounds, strict validation, synthetic confirmation, sanitized error responses and `Cache-Control: no-store`. A blocked/failed assisted operation is a structured abstention response, not a successful extraction. No endpoint accepts raw provider output, credentials, fixture paths, arbitrary model settings or release flags from the browser.

## UI and raw input

The page retains the paste area, faithful monospaced raw preview, character/line count, Clear, original synthetic example, optional context claims and DRAFT report/export flow. Source selection is replaced by automatic source/verification status after Parse Table. Original values, lexical values, field warnings and targeted clarifications remain visible. A second clearly labeled synthetic Markdown example exercises the fallback boundary.

The AI action is rendered only when server eligibility is true. Its separate consent explicitly describes external transmission of bundled synthetic cells. Typing, loading examples, changing metadata, checking confirmation/consent and normal parsing never automatically contact Groq. Each attempt clears cloud consent. Loading prevents duplicate requests, failures retain raw input and earlier deterministic warnings, and editing input/context or revoking confirmation invalidates/aborts stale results. UI budgets are 20 seconds for local parsing and 35 seconds for assistance; browser cancellation is not a claim of remote erasure.

React text rendering remains inert; no HTML evaluation, storage, trimming, newline insertion or app-level cleanup is added. Browser textarea newline canonicalization remains expected. Raw source offsets are Python Unicode code points, not UTF-16 clipboard byte positions.

**Report boundary:** an accepted assisted preview does not flow into semantic authorization or replace review findings. Reviews/reports independently reparse the original text through the existing deterministic path. Thus the synthetic Markdown wrapper can have an assisted lexical preview and still produce an unavailable DRAFT review/report. The UI states this explicitly. No finding is invented to make a report appear complete.

## Documentation-inspired synthetic fixtures

The catalog is `examples/parser-finalization-synthetic.json`. Its five examples contain original invented numbers and independently specified orientations/raw values/Decimal expectations:

1. ClinCheck-style named plan views with tooth rows, Unicode minus, zero, blank and dash.
2. SureSmile-style movement/tooth intersections and cusp-tip context, with opaque quadrant tokens and missing markers.
3. Original Markdown tooth-row wrapper, cloud-allowed only as that exact synthetic text.
4. Original Markdown tooth-column wrapper, likewise exact synthetic text only.
5. Corrupted multispace alignment that must abstain.

These are not authentic clipboard captures, manually transcribed screenshots, vendor-certified formats, independently reviewed clinical gold or approved releases. Frontend assisted-response fixtures are explicitly generated with mocked transport; live probes do not confer vendor status on them.

References checked on 2026-11-13:

- [ClinCheck Pro 6 official guide, section 3.15](https://assets.ctfassets.net/vh25xg5i1h5l/qwpf6aq8qtSj0keD5bJzB/71bf896a5584a0a6311f52d03bce4581/MKT-0003721_Rev_J_User_Guide_ClinCheck_Pro_6-87-.pdf): named plan views and distinct tooth-reference choices motivate synthetic context. It does not establish clipboard serialization for this app.
- [SureSmile Tooth Movements help](https://docs.suresmile.com/suresmile_webhelp/treatment_planning/displacements_tab.htm): movement/tooth intersections, reference choices and setup/comparison context motivate synthetic tests. Setup revision labels, aligner stages, tooth displacement and intersection/gap rows must not be conflated. Its described conventions were not activated as mappings.
- [Comparing virtual setup software programs for clear aligner treatment](https://repositorio.pucrs.br/dspace/bitstream/10923/25185/2/Comparing_virtual_setup_software_programs_for_clear_aligner_treatment.pdf): a comparative study, not an authoritative clipboard/sign/axis codebook. It reinforces that cross-platform values must not be treated as equivalent. No study patient data, numerical thresholds or treatment policies were copied into fixtures or code.

The initial model/schema choices also follow [Groq structured outputs](https://console.groq.com/docs/structured-outputs), [Chat API](https://console.groq.com/docs/api-reference) and [rate-limit documentation](https://console.groq.com/docs/rate-limits). These do not imply vendor or clinical verification.

## Minimal live Groq checks

Explicitly authorized by this task; no live calls are part of ordinary tests. Keys were checked for presence without printing values. Both were available in ignored `.env.local`. No key file was modified.

At **2026-11-13 16:13:26 UTC**, the permitted host-network run produced:

| Service / independent credential | Authentication / requested model | Strict response validation | Elapsed | Prompt / completion / total tokens | Provider attempts |
| --- | --- | --- | --- | --- | --- |
| Comments / `GROQ_API_KEY` | HTTP 200; openai/gpt-oss-120b matched | GROQ_VALIDATED, exact approved phrase/reference | 2.2139 s | 430 / 101 / 531 | 1 |
| Structural parsing / `GROQ_API_KEY_2` | HTTP 200; openai/gpt-oss-120b matched | ALL_CELL_ASSOCIATIONS_CERTIFIED | 2.0543 s | 522 / 180 / 702 | 1 |

An earlier restricted-network run could not establish either connection: comments 1.1857 s and parser 0.8269 s, both GROQ_CONNECTION_ERROR, no HTTP status and no available usage. It did not establish authentication/model/schema results and was not represented as success. A single host-network rerun was used after that environmental failure; no provider-rate-limit retry or key rotation occurred. No further live requests were made.

Comment probing uses the actual comment prompt/schema/client/closed-wording validator on a fixed synthetic unavailable placeholder; it does not create or authorize clinical findings or exercise a real-patient report. Parser probing uses the actual immutable synthetic cell prompt/schema/client/association validator. Neither probe records keys, provider output/IDs/reasoning or diagnostic bodies. Missing keys are reported SKIPPED individually; that behavior is mocked in tests. The CLI requires `--live`, and otherwise makes zero calls. These two small successful calls establish connectivity and validation at that time, not production latency, capacity, retention guarantees or vendor/clinical compatibility.

## Supported and unsupported formats

| Variation | Behavior |
| --- | --- |
| Existing explicit tab/pipe/semicolon or consistent 2+ space grids | Existing deterministic behavior, rows or columns, unique recognizable header required |
| Irregular padding, blank lines, Unicode minus/degree, CR/LF/CRLF | Raw preserved; derived lexical Decimal only; explicit delimiter positions retained |
| Missing markers, explicit zero, duplicates, unknown units/labels | Existing separate statuses/issues; no invented zero, direction or merge |
| Complete outer-pipe Markdown with divider | New certified preview through explicit development assistance for the two exact allowed synthetic examples only |
| Ambiguous numbering, unknown source/version/basis/mode/scope | Retain tokens/claims and targeted clarifications; canonical values withheld |
| Source text/signature conflicts | Detected source Unknown / CONFLICT; no vendor selected |
| Ragged/corrupted/missing-middle alignment, unsupported wrappers | Abstain; no model guessing |
| CSV/quoted/escaped-pipe/multiline cells, merged/image/PDF/OCR tables, multiple tables | No new support; no OCR/transcription/cleanup path |
| Arbitrary synthetic paste or authentic input to cloud | Denied by exact shipped-example allowlist, even with a checkbox |
| Real vendor compatibility/canonical normalization | Disabled pending authentic reviewed evidence and release |

## Verification

Normal backend/provider tests use `httpx.MockTransport`; browser assisted-success transport is mocked explicitly. Existing real-API paths remain covered.

| Check | Observed result |
| --- | --- |
| Complete backend pytest | **453 passed**: all 372 earlier cases plus 81 finalization cases |
| Complete Vitest / React Testing Library | **101 passed**: 86 earlier cases retained/adapted plus 15 assistance cases |
| Complete Playwright | **32 passed** at 1440 / 1024 / 768 / 375 px: all 20 earlier paths plus 12 new cases |
| Additional screenshot/browser pass | New automatic-detection/disabled-cloud/mocked-assisted cases passed across the same four viewports |
| TypeScript / production Vite build | **Passed**; build runs `tsc --noEmit` before Vite |
| Backend startup | Fresh loopback Uvicorn startup exercised by browser tests |
| Dependency consistency | `pip check`: no broken requirements |
| Formatting | `git diff --check`: passed |
| Desktop/mobile visual review | Saved new intake/detection screens inspected; browser assertions confirm no horizontal page overflow |
| Original contracts/documents | Original parser schema and governing-document hashes retained |
| Private key file | `.env.local` remains ignored; no secret file was changed |
| Vendor verifier | **NO_AUTHENTIC_ORACLES**, Python exit 2 (confirmed directly); normalization remains disabled |
| Required Graphify refresh | **723 nodes / 2,276 edges / 28 communities**, AST-only, zero LLM token cost |

Coverage includes source candidates/conflicts, unknown and corrupt layouts, ambiguity, independent synthetic oracles, exact Unicode/line-ending provenance, retained Decimal/zero/missing distinctions, row/column and identical-value association attacks, malformed/duplicate-key/invented-output proposals, consent/catalog/development/disabled-cloud gates, missing configuration, separated/redacted secrets, missing catalog fail-closed behavior, 401/429/503/timeout/network failures, model mismatch and semantic abstention. Frontend checks cover loading/duplicate prevention, exact requests, safe errors, timeouts, stale responses, consent reset, denied assistance, raw-input preservation and strict returned pipeline validation. Existing review/report/export tests remain covered.

The initial frontend failures were tests referring to the intentionally removed selector and ambiguous text queries matching the hidden full JSON preview. Those tests were updated to retain metadata-invalidation coverage and scope status assertions. Node's browser-test runner required explicit JSON import attributes. Restricted Playwright startup stalled before collection and was stopped; approved normal local process access passed the suites. Existing upstream Starlette/httpx deprecation and environment color warnings remain non-failing. No unfinished test failure is represented as a pass.

## Updated project structure and changed files

```text
C:\Finova AlignIQ\
  README.md / .env.example / PARSER_FINALIZATION_REPORT.md
  docs/                                      unchanged governing documents
  PARSER_PHASE1.md / PARSER_PHASE1_5.md        unchanged historical reports
  ENGINE_PHASE2A.md / REPORT_PHASE3.md         unchanged historical reports
  examples/parser-finalization-synthetic.json new original synthetic catalog/oracles
  schemas/
    automatic-parse-result.v1.json            new
    assisted-parse-request.v1.json            new
    groq-structure.v1.json                    new; previous schemas retained
  backend/
    app/main.py                              adds two routes
    app/development_env.py                    explicit safe settings loader
    app/api/automatic_parse.py                new routes
    app/parser/
      service.py                             library-only original-cell grid reuse
      contracts.py / detection.py             new additive contracts/indicators
      certification.py / pipeline.py          new structural proof/orchestration
      cloud.py / synthetic.py                 independent settings/exact catalog gate
    app/reports/groq_client.py                shared transport + safe probe metrics
    app/semantics/ / app/review/               unchanged semantic/clinical policies
    scripts/export_schemas.py                 adds three contracts
    scripts/run_dev.py                        explicit loopback runner
    scripts/check_groq_connectivity.py        opt-in fixed synthetic live checks
    tests/test_health.py                      authorized route allowlist extension
    tests/test_parser_finalization.py         new adversarial/mock/privacy tests
  frontend/
    src/App.tsx / src/api/parse.ts            automatic/consented intake + validator
    src/components/ParserStatus.tsx           status + targeted clarification UI
    src/App.assisted.test.tsx                 new focused tests
    src/{App,App.parse,App.review,FinalReport}.test.tsx
                                              selector removal retains invalidation coverage
    src/test/fixtures/synthetic-parse-result.json
                                              additive pipeline test fixture
    src/test/fixtures/synthetic-automatic-unsupported.json
    src/test/fixtures/synthetic-assisted-parse-result.json
                                              new explicitly mocked synthetic fixtures
    e2e/automatic.spec.ts                     new real-API/mocked-cloud browser paths
    e2e/{parse,review,report}.spec.ts          new route / removed selector
  graphify-out/                              required AST-only refresh
```

No dependency, clinical registry, semantic mapping, private env file, authentication, database or extension change is required. The checkout already contained uncommitted/untracked files from preceding phases; this task does not stage, commit or publish them.

## PowerShell commands

Install/run defaults remain in README. Existing installations need no new packages. From a fresh checkout:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-access-log
```

In another terminal:

```powershell
Set-Location 'C:\Finova AlignIQ\frontend'
npm ci
npm run dev
```

Optional deliberate synthetic cloud-development setup, replacing the default backend command after stopping that backend:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
$env:FINOVA_ENVIRONMENT = 'development'
$env:FINOVA_PARSER_GROQ_ENABLED = 'true'
.\.venv\Scripts\python.exe scripts\run_dev.py --env-file ..\.env.local
```

Use only an existing private settings file or the backend process environment. Do not overwrite existing keys. Disable the flag/restart to return to deterministic-only behavior. The separate optional live CLI is explicit and potentially billable:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe scripts\check_groq_connectivity.py --live --env-file ..\.env.local
# --service comments / --service parser can limit this further.
```

Repeatable deterministic checks (no live Groq traffic):

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe scripts\export_schemas.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe scripts\verify_vendor_fixtures.py
# Expected vendor result: NO_AUTHENTIC_ORACLES, exit 2, not compatibility success.

Set-Location 'C:\Finova AlignIQ\frontend'
npx playwright install chromium  # Initial installation only, if not cached.
npm test
npm run build                    # Includes tsc --noEmit, then production Vite.
npm run test:e2e

Set-Location 'C:\Finova AlignIQ'
graphify update .                # AST-only, no LLM extraction.
git diff --check
```

## Exact remaining vendor-verification blockers

**Authentic captures: 0. Independently reviewed vendor oracles: 0. Approved release digests: 0. Verified vendor versions: none.** Published references, model success, screenshots, transcriptions and these synthetic tables cannot close that gate.

Required for every intended application/build/version, copy surface, locale and serialization variant:

1. Authorized, de-identified **verbatim logical clipboard text**, preserving original whitespace, Unicode, precision and line endings, with SHA-256; independently retained source-UI evidence. Do not add patient records to the repo, browser or cloud path.
2. Exact application/build/version, OS/browser, locale/decimal/unit conventions, copy surface, capture timestamp/operator, pseudonymous case/plan identifiers and existing authorization/de-identification references.
3. Independent tooth notation/dentition/arch and canonical identity evidence for both arches and mirrored teeth; every intended FDI/Universal/Palmer variant, missing/pontic/excluded status and unsupported dentitions explicitly recorded.
4. Every exported axis, unit, literal sign/direction code, precision and coordinate frame; positive/negative/unsigned/zero/missing variants for the relevant tooth/arch. Linear/angular references must be verified per field. No root/torque or cross-vendor equivalence is assumed.
5. ClinCheck Align Final, Doctor Final and Comparison captures with exact plan operands and source-defined difference/sign operation; matched crown-center and virtual-root-apex views where available.
6. SureSmile crown, cusp and any intended bracket-reference captures with distinct field meaning; actual available total/cumulative/incremental/stage views, independently identified baseline/endpoints/stage kinds. Setup/lab revision counters and global-alignment toggles need explicit meaning; no revision counter is assumed to be an aligner stage. Unsupported/not-offered variants must be recorded as such.
7. Source-confirmed missing markers, explicit zeros, absent axes and intersection/gap/IPR rows; all authentic header/orientation/delimiter/locale variants and clearly separated malformed/unsupported examples.
8. Independently authored lexical and field-level semantic gold (not copied from parser output), field-by-field evidence locators, raw/expected/source-evidence hashes and two distinct independent approving reviewers including an orthodontist. Reviewers bind those exact artifacts; unresolved components stay UNKNOWN.
9. Passing offline oracle/integrity checks, then a separate scoped code-reviewed release/adapter implementation and explicit approved digest registration. No nearest-version extrapolation or automatic release approval exists. Generalization beyond an identical fixture still needs separately validated versioned adapters.

The complete existing capture matrix and approval workflow remain in `backend/vendor_verification/README.md`. Wider structural parsing, authentic vendor compatibility, real-input privacy approval and clinical-rule activation are separate future work; none was silently authorized or started here.
