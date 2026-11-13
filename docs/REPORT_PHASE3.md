# Phase 3 — Groq wording, deterministic templates and final DRAFT reports

Status: implemented for internal synthetic development. **DRAFT — Requires Orthodontist Review. Prototype — not for clinical use.** No live Groq call or patient-specific clinical validation was performed. Authentic vendor captures/oracles/releases remain zero, and every clinical predicate remains disabled.

The user's Phase 3 scope is comment generation, not the blueprint's proposed activation of clinical policies. No Phase 2B policies or additional phases were started. All three documents and tables in `docs/`, `PARSER_PHASE1.md`, `PARSER_PHASE1_5.md`, `ENGINE_PHASE2A.md`, parser/semantic/review implementations, contracts, safeguards and frontend were reviewed. Original governing documents, prior contracts and clinical/semantic algorithms were preserved.

## Pipeline and trust

```text
Explicit synthetic-only report request
 -> unchanged deterministic parser
 -> unchanged semantic authorization / empty vendor release registry
 -> unchanged rule engine / output safeguards
 -> eligible descriptive findings + unavailable assessments
 -> local grouping, deterministic templates and protected source facts
 -> optional Groq Cloud wording selection on minimal nonclinical wording payload
 -> strict JSON, reference completeness and exact closed-language validation
 -> local facts + uncertainty + rule/provenance assembly
 -> final DRAFT report, readable UI, local Copy / UTF-8 TXT download
```

HTTP never accepts findings, semantic assessments, fixture paths, release overrides, test-mode switches or credentials. `/api/v1/reports/draft` recomputes its engine review from the raw submission. Source claims, zero values, versions and synthetic-data confirmation cannot grant semantic authority. Comparison values and unsupported source/mode/basis/scope/stage fields retain the existing abstention behavior. No clinical thresholds, attachment prescriptions, staging recommendations, success predictions, ML, auth, database or persistent patient records were added.

With no released authentic clipboard mappings, **all current pasted input produces template-based abstention reports and zero Groq calls**, regardless of the key. This is an intentional evidence gate. Development success paths use the existing exact-fixture verifier with explicitly invented TEST_ONLY semantics and a library-only test flag. Neither the HTTP API nor the UI can enable test semantics for arbitrary input. No fake vendor mapping or reviewer evidence was registered.

## Bounded Groq generation

Provider: **Groq Cloud only**, model `openai/gpt-oss-120b`, fixed HTTPS Chat Completions endpoint. The integration uses the already-installed `httpx`; no additional SDK/provider dependency is needed. No other provider was integrated, compared or called.

The model's responsibility is deliberately narrow: choose one of two approved professional wordings for each eligible comment unit. It is **not unrestricted free-form paraphrasing**. A general keyword blacklist cannot prove clinical entailment; this closed language makes output acceptance deterministic.

Each upstream item contains only an ephemeral alias such as `F0001`, known rule IDs, an internal finding-type code, and approved phrase alternatives. It contains **no raw table, cell/header text, measurements, tooth IDs, source claims/versions, patient/case/plan IDs, source hashes, clinical records or evidence locators**. Exact original values, canonical components, signs/directions, units, stage/frame/basis/mode/scope and source provenance are inserted **locally after wording validation**. The remote alias maps back to all underlying actual finding IDs in the final report.

Constrained system instructions prohibit new findings/advice, treating data as instructions, changed references and extra text. Requests use nonstreamed strict `json_schema` output; every object has required fields and `additionalProperties: false`. Returned text must also exactly equal an approved alternative for its referenced finding. Strict JSON alone is not sufficient evidence of safe content.

Official Groq documentation checked for this implementation:

- [Structured Outputs](https://console.groq.com/docs/structured-outputs): GPT-OSS-120B strict JSON schema support and closed-object requirements.
- [Chat API reference](https://console.groq.com/docs/api-reference): model/settings, `max_completion_tokens`, supported reasoning efforts and nonstreamed messages. The unsupported Chat `store` parameter is intentionally omitted; no provider-retention guarantee is inferred from an unsupported flag.
- [Rate limits](https://console.groq.com/docs/rate-limits): 429 `Retry-After` handling. Account limits are not hardcoded as universal quotas.

Exact validation rejects unknown, duplicate or missing finding aliases; extra JSON fields; duplicate JSON keys; malformed JSON; truncation/refusal/tool output; altered wording, numbers, identifiers, negations or punctuation; and any extra unsupported claim. Unsupported individual phrases fall back per comment; invalid batch structure/references reject the entire batch. No safety or measurement check is delegated back to an LLM. An accepted phrase cannot modify the locally rendered fact block or required limitations.

To reduce repetition, compatible per-tooth findings are grouped within the same exact source context. A specialized inventory can replace its generic introduction while all triggering rule/finding IDs and source measurements remain. Distribution summaries remain separate; incompatible bases/scopes/frames never join. Identical unavailable propositions share one message with their full references. Conflicts/suppressed findings remain unavailable and are never sent for wording. No new sums, stage arithmetic, plan subtraction or clinical inference occurs.

## Configuration and privacy

Settings live in `backend/app/reports/settings.py`, read from **backend process environment**. `.env.example` is a template; it is not automatically loaded. Standard Templates require no credentials. Secrets are excluded from settings representation/serialization and never returned in API responses. No frontend environment variable or bundle contains the key.

| Environment variable | Default / permitted range |
| --- | --- |
| `GROQ_API_KEY` | Empty; backend secret only |
| `FINOVA_GROQ_SYNTHETIC_ENABLED` | `false`; explicit server permission for eligible TEST_ONLY wording |
| `GROQ_MODEL` | `openai/gpt-oss-120b`; other models rejected |
| `GROQ_TEMPERATURE` | `0`; allowed 0–0.3 |
| `GROQ_MAX_COMPLETION_TOKENS` | `2048`; 256–4096 |
| `GROQ_REASONING_EFFORT` | `low`; low/medium/high |
| `GROQ_TIMEOUT_SECONDS` | `6`; 0.1–8 per-attempt budget and HTTP operation timeout |
| `GROQ_MAX_RETRIES` | `0`; at most one optional retry |
| `GROQ_MAX_RETRY_DELAY_SECONDS` | `1`; 0–1 seconds |
| `GROQ_MAX_WORDING_FINDINGS` | `16`; 1–24 comment units per single batch |

PowerShell configuration in the **backend terminal** (masked entry; do not paste actual keys into source/commands):

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
$groqSecret = Read-Host 'Groq API key' -AsSecureString
$env:GROQ_API_KEY = [System.Net.NetworkCredential]::new('', $groqSecret).Password
Remove-Variable groqSecret
$env:FINOVA_GROQ_SYNTHETIC_ENABLED = 'true'
$env:GROQ_MODEL = 'openai/gpt-oss-120b'
$env:GROQ_TEMPERATURE = '0'
$env:GROQ_MAX_COMPLETION_TOKENS = '2048'
$env:GROQ_REASONING_EFFORT = 'low'
$env:GROQ_TIMEOUT_SECONDS = '6'
$env:GROQ_MAX_RETRIES = '0'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-access-log
```

Use the existing frontend terminal/run instructions. To disable optional wording, set the synthetic flag to `false` or remove the key from the backend environment. Invalid settings safely fall back to templates without echoing configuration values.

**Real-patient transmission is permanently disabled in this phase.** No environment variable or request flag authorizes it. Even a future authorized-vendor finding is refused by the current remote-wording gate. Enabling a real clinical workflow requires separately approved privacy/data-handling configuration, deployment controls and a reviewed code change; setting a boolean is not proof of privacy approval. Synthetic confirmation is not PHI detection. The current user cannot obtain source verification by labeling real input synthetic.

No raw input, secrets, provider payloads or clinical information are logged by application code. No automatic uploads, browser storage, telemetry or patient-data database were added. The endpoint has the existing bounded private intake, sanitized validation failures and no-store responses. Groq redirects and environment proxies are disabled; no custom endpoint override exists. Provider diagnostics/bodies are not surfaced in report errors. Application data remain in memory; user-initiated copy/download is an explicit local export, not automatic retention.

## Failures and resource bounds

No eligible findings, no key, disabled synthetic permission, invalid configuration, real-data domain or excessive eligible batch size means **zero provider calls**, with an explicit reason and templates. No prefix batch is sent and no findings are dropped to satisfy a provider limit.

Groq failures, invalid responses and unsupported wording produce a usable template report. Defaults make exactly one request, with **no automatic retry**. An optional single retry is limited to 429/503 with a valid `Retry-After` no longer than the configured one-second allowance. Missing, invalid or longer delays cause immediate template fallback rather than early retry. Numeric and HTTP-date headers are handled. Timeouts/connection failures are not retried because the prior request may already have been processed. Prompt size is capped at 24,000 bytes and decoded response at 128 KiB. A monotonic per-attempt budget also stops successive slow response chunks; an in-progress HTTP operation remains bounded by its own timeout. No tools, streaming, unbounded repair loop or multi-provider fallback is used.

The existing 512-position review limit and parser/body/text limits remain. Frontend report requests time out at 30 seconds, abort stale display requests, and never retry automatically. An already submitted provider operation may finish after browser cancellation; cancellation is not a claim of remote erasure. Unavailable UI messages paginate by 10; complete findings/exports remain in memory.

## API and contracts

Existing routes/contracts are unchanged:

- `GET /api/health` — retains the historical `phase: 1` field for compatibility.
- `POST /api/parse` — lexical parsing only.
- `POST /api/v1/tmt/observations` — Phase 2A DRAFT review.

New route: **`POST /api/v1/reports/draft`**.

Request: existing strict `ReviewSubmission` plus `comment_mode: AUTO | GROQ | TEMPLATES` (default AUTO). Both AUTO and explicit GROQ fall back safely; the UI presents Groq AI with automatic fallback and Standard Templates. Groq is used by default only when configured **and** exact TEST_ONLY evidence is eligible. The endpoint accepts no supplied findings, API key, real-data permission, evidence path or clinical policy.

Response: `FinalDraftReport`, schema `1.0.0`, report version `0.3.0`, containing:

- Branding/title, literal **DRAFT — Requires Orthodontist Review**, and `clinical_analysis_enabled: false`.
- Complete unchanged `engine_review`, including evidence domain, source claims, coverage, all findings and 96 rule evaluations.
- Generation mode actually used, static fallback reason, attempts, accepted/eligible counts, model/provider when called, closed-validation version and literal false real-patient transmission.
- Grouped comments with all finding/rule IDs, nullable verified tooth ID, evidence status, exact original/normalized measurements, input/evidence references, missing fields, evaluation statuses and wording source/fallback.
- Mandatory limitations and authoritative UTF-8 plain-text `export_text`.

Report IDs hash content excluding `report_id` and derived `export_text`, avoiding a self-reference cycle. TXT includes the resulting ID. Same input/rules/template mode reproduces the same result; Groq's selection can vary and produces a different draft ID if accepted wording changes. No timestamp/reviewer identity or approval is invented.

Generated schemas: `schemas/report-request.v1.json`, `schemas/final-draft-report.v1.json`, `schemas/groq-wording.v1.json`. Existing schema files remain unchanged. The route-allowlist test expands only for the authorized new endpoint.

## Report UI and local export

Existing paste/parse/review UI remains. After **Create draft review**, the final-report panel offers two modes and a separate **Create final report** action. No request happens merely from typing, selecting a mode or displaying the panel. The server rechecks the same unchanged input rather than trusting a previously displayed finding object.

The report shows branding, DRAFT badge, source claims explicitly labeled unverified, actual semantic evidence status, verified metadata with individual observations (otherwise UNKNOWN), available counts, tooth-wise comments, distribution summary, unavailable assessments, rule/provenance details and limitations. TEST_ONLY is never displayed as vendor VERIFIED. Literal markup renders as inert React text, not HTML/Markdown instructions. Long content wraps within all tested viewport sizes.

**Copy Report** writes the server's exact report string to the Clipboard API. Windows may serialize line endings as CRLF; logical text is preserved without promising byte-original clipboard fidelity. **Download Report (TXT)** creates a local UTF-8 Blob with a fixed, nonpatient filename and revokes its object URL. Browser tests compare downloaded bytes exactly and clipboard text after Windows newline serialization. Neither operation makes a server/provider request. Disclaimers, DRAFT status, all rule evaluation statuses and source/finding references appear in both exports. No CSV/formula or HTML export is introduced.

Changing raw/source/context/consent/clear/demo or requested assessment unmounts and invalidates the report; changing comment mode invalidates its prior result/export and aborts stale requests. Clipboard/download failures show static local guidance, and the full export preview remains available. Copy/download does not constitute clinical approval.

## Examples and project additions

- `frontend/src/test/fixtures/synthetic-final-report.json`: complete actual unverified-input abstention report; no Groq call.
- `frontend/src/test/fixtures/synthetic-groq-report.json`: invented TEST_ONLY success produced with **mocked** Groq, not live/vendor evidence.
- `examples/phase3-synthetic-template-report.txt`: complete deterministic TEST_ONLY example with exact `−1.2300 M`, magnitude `1.2300`, source context and provenance.
- `examples/phase3-synthetic-groq-report.txt`: same invented evidence with validated mocked wording; facts remain local and unchanged.

The example structured finding remains a Phase 2A D01 result: OBSERVED only under explicit TEST_ONLY semantics, raw value `−1.2300 M`, signed Decimal `-1.2300`, magnitude `1.2300`, opaque test tooth/axis/direction and retained source spans. For arbitrary pasted vendor input, D01 instead returns SEMANTICS_UNKNOWN, `evaluated: false`, no observations and explicit missing fields. Comment generation never changes that status.

```text
backend/app/reports/
  __init__.py  settings.py  models.py  templates.py
  prompt.py    validation.py  groq_client.py  service.py
backend/app/api/reports.py
backend/app/main.py                        # adds only report router
backend/scripts/export_schemas.py          # exports three additional contracts
backend/tests/test_reports.py
backend/tests/test_health.py               # exact route allowlist expansion
frontend/src/api/report.ts
frontend/src/components/FinalReportPanel.tsx
frontend/src/components/DraftReviewPanel.tsx # mounts separate final-report panel
frontend/src/App.tsx                        # phase badge / accurate export notice
frontend/src/FinalReport.test.tsx
frontend/src/test/fixtures/synthetic-{final,groq}-report.json
frontend/e2e/report.spec.ts
schemas/{report-request,final-draft-report,groq-wording}.v1.json
examples/phase3-synthetic-{template,groq}-report.txt
.env.example  README.md  REPORT_PHASE3.md
graphify-out/                              # required AST-only refresh
```

## Validation and remaining gates

Run all checks using the existing installed dependencies:

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

All provider tests use MockTransport with invented text and synthetic test keys; no live Groq call, key validation request, Claude call or provider comparison was performed. There is no live smoke endpoint/CLI in this phase; example success is explicitly mocked. The client uses current official API documentation, but live account/model/schema compatibility and practical latency are therefore **not measured**. No deployed service or clinical sign-off was created.

Remaining blockers are unchanged: authentic, authorized clipboard serialization for each exact ClinCheck/SureSmile build/copy surface/locale; independently checked numbering/dentition/arch, tooth-specific signs/directions, units/precision, modes/comparison operands, crown/root/cusp bases, coordinates and stage/scope/kind variants; consent/de-identification and reviewer evidence; independently authored gold outputs and code-approved releases. See `backend/vendor_verification/README.md` for the exact matrix. Screenshots and these invented examples do not replace raw clipboard captures.

Clinical activation separately needs exact orthodontist-approved policies, applicability/exceptions/wording, independent multi-reader case evaluation, governance/release/rollback and privacy/security/legal readiness. No R/T/A clinical predicate was enabled, no threshold was invented, no source mapping was fabricated, and this phase stops at the final **DRAFT** report workflow.

## Final observed test results

| Check | Result |
| --- | --- |
| Complete backend pytest | **372 passed**: all 288 prior tests plus 84 new report/provider/privacy cases |
| Complete Vitest / React Testing Library | **86 passed**: all 55 prior tests plus 31 report/export cases |
| Complete real-API Playwright | **20 passed** at 1440 / 1024 / 768 / 375 px, including all 16 prior paths |
| TypeScript and Vite production build | **Passed** |
| Backend dependency consistency | `pip check`: no broken requirements |
| Formatting | `git diff --check` passed |
| Backend startup | Fresh server startup exercised through Playwright |
| Desktop/mobile visual inspection | Report screenshots inspected; browser assertions confirmed no page overflow |
| Vendor verifier | `NO_AUTHENTIC_ORACLES`, expected exit 2; zero approved releases |
| Graphify AST refresh | Completed: 612 nodes, 1,828 edges, 26 communities; no LLM labeling/extraction |

Tests cover exact local Decimal/sign/direction preservation, template independence, minimal payloads, secret redaction, success/mixed fallback, JSON/reference/duplicate-key failures, unsupported clinical claims, injection, unverified/zero/missing/comparison/duplicate/conflict restrictions, disabled policies, settings, byte/time/batch bounds, 429/503 retry handling, privacy/API errors, responsive reports, raw input preservation, copy/download and stale-result invalidation. Real clipboard tests account for Windows CRLF serialization; downloaded UTF-8 content is compared exactly.

Early test corrections were limited to short pytest parameter IDs for Windows temporary paths, a TypeScript test annotation, initial favicon-load timing and native clipboard newline expectations. No clinical policy was changed. One final sandboxed backend invocation stalled before test reporting and was stopped; approved local execution passed the full final suite. Existing upstream Starlette/httpx deprecation and environment color warnings remain non-failing. All Groq responses in tests/examples were mocked; no live Groq verification or other-provider testing occurred.
