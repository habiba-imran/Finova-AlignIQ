# Finova AlignIQ

Phase 8 adds **Sequencer / Nano Review**: separate upper/lower arch, segment and right/left anchorage sections, missing-stage explanations, a fixed fictional demonstration and exact DRAFT copy/TXT export. Macro Planning Assistant and Micro Attachment Interface remain available. **Prototype — not for clinical use. Do not paste real patient data.** See [the Phase 8 report](SEQUENCER_PHASE8_REPORT.md), [the Phase 7 report](ATTACHMENT_INTERFACE_PHASE7_REPORT.md) and [the Phase 6B report](docs/PLANNING_ASSISTANT_PHASE6B_REPORT.md).

Choose **Macro** → paste synthetic TMT → confirm synthetic input → **Parse Table** → inspect exact values → **Run Planning Assistant** → review Sagittal / Transverse / Vertical / Other / Unavailable → select and copy eligible comments or copy/download the complete DRAFT. Choose **Micro** for Attachment Interface or **Nano** for Sequencer, described below. Review passes are not aligner stages and do not determine what a patient needs. Earlier separate Macro review/report controls remain under **Advanced** after parsing.

Ordinary vendor input remains **UNVERIFIED**, with zero authorized observations and no Groq transmission. Use the separately enabled **Finova Synthetic Demonstration** below to exercise positive descriptive results. The fixed demo has invented opaque tooth identities, explicitly defined units/directions/basis/mode/scope, and partial abstention; it is not a vendor adapter or a clinical policy. Full/selected exports retain DRAFT status, uncertainty and provenance. No clinician editing, sign-off or automatic CAD integration is implemented.

The React/TypeScript/Vite/Tailwind frontend preserves raw input and submits it only through explicit actions after synthetic-data confirmation. Python/FastAPI/Pydantic returns exact Decimal evidence, traceable findings and draft reports. **Arbitrary pasted input never goes to Groq.** Parse Table may automatically recover a server-reproduced generated synthetic fixture only when development cloud testing is explicitly enabled. There is no second AI action or cloud checkbox. Accepted source associations are independently checked and can reach reviews/reports through a short-lived receipt, followed by the unchanged semantic gates. Comment generation retains its separate key and approved-wording validation. Clinical predicates remain disabled; no clinical recommendations, ML, authentication, database, patient-data persistence or Chrome extension is implemented.

See [the Phase 5 implementation report](docs/RULE_ENGINE_PHASE5_REPORT.md), [the complete 96-rule inventory](docs/RULE_ENGINE_PHASE5_INVENTORY.md), [the clinical approval register](docs/CLINICAL_RULE_APPROVAL_REGISTER.md) and [the feasibility matrix](docs/RULE_FEASIBILITY_MATRIX.md). There are **66 active engineering handlers/guards, 27 disabled clinical predicates and 3 deferred controls**. Active does not mean clinically approved. Extra tooth-group/status, pair, coverage and stage evidence currently has only a private, exact-input-bound TEST_ONLY library path. User-submitted HTTP input cannot authorize it or activate policies. The separate development demonstrations accept no uploaded text or semantic claims and use only fixed, server-owned TEST_ONLY artifacts.

The standalone original 82-rule research document is unavailable in this checkout. The corrected v2 retains original-proposal trace paragraphs; those are historical context only. The independent audit and corrected v2 govern the inventory and behavior.

See [the Phase 4 report](docs/PARSER_PHASE4_REPORT.md) and [the Phase 4 architecture note](docs/PARSER_PHASE4_ARCHITECTURE.md) for the parser contracts, exact formats/limits, independent gold, benchmark, live results and remaining restrictions. The oracle-mocked benchmark improves 96/240 to 240/240 positions; final live probes recovered 10/12, with the other positions quarantined. Neither result verifies a vendor.

See [PARSER_FINALIZATION_REPORT.md](docs/PARSER_FINALIZATION_REPORT.md) for the historical parser-finalization work. Phase 4 replaces its two-example/manual-action/preview-only limitations in the normal intake pipeline. Earlier phase reports below record historical results.

See [the Phase 3 implementation report](docs/REPORT_PHASE3.md) for the pipeline, configuration, API/schemas, changed files, examples, validation and limitations. Copy Report and Download Report (TXT) make explicit local exports with draft status, disclaimers and provenance.

**Vendor compatibility is unverified.** Generic structure/number recognition does not establish ClinCheck or SureSmile semantics. Existing parser canonical fields remain null. The new review endpoint returns unavailable movement assessments for unverified pasted input. Authentic vendor fixtures are still required before the audited vendor-release gate can close. Development observations use isolated TEST_ONLY evidence, never vendor mappings.

See [Phase 2A architecture, exact rule dispositions, output examples and remaining gates](docs/ENGINE_PHASE2A.md). Phase 3 does not activate Phase 2B/clinical policies or authorize an additional phase.

See [the Phase 1 architecture and contract](docs/PARSER_PHASE1.md) for the schema, supported/unsupported formats, field states, engineering limits, decisions requiring review, and vendor verification checklist.

Phase 1.5 added a separate offline/library semantic assessment, strict fixture/review contracts, read-only oracle verification and an **empty** code-controlled release registry. These remain unchanged, as do all existing schemas. See [the Phase 1.5 architecture and compatibility review](docs/PARSER_PHASE1_5.md) and [the precise authentic-capture workflow/matrix](backend/vendor_verification/README.md). Authentic captures, independently reviewed vendor expected outputs and approved releases are all **zero**.

## Deployment

Production hosting is split: the Vite frontend on Vercel and the FastAPI backend on Render, connected by a Vercel `/api` rewrite. See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for the step-by-step guide, required environment variables, verification commands and free-tier caveats. The checked-in `render.yaml` and `frontend/vercel.json` contain the defaults (replace the placeholder Render URL before deploying the frontend).

## Prerequisites

- Windows PowerShell, Node.js 22.12+ (tested with 24.12.0), npm, and Python 3.12+ (tested with 3.12.10).
- Registry access for initial installation, or equivalent cached packages. Standard Templates require no credentials. Optional Groq wording uses backend-only environment settings in `.env.example`; see configuration below.

## Install in PowerShell

```powershell
Set-Location 'C:\Finova AlignIQ\frontend'
npm ci

Set-Location 'C:\Finova AlignIQ\backend'
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Use the virtual environment's Python directly; activation and execution-policy changes are unnecessary. If `python` is unavailable, use `py -3.12` to create the environment. If `ensurepip` fails, repair the Python installation's pip support before retrying.

For browser tests, install Chromium once (or use the matching existing Playwright browser cache):

```powershell
Set-Location 'C:\Finova AlignIQ\frontend'
npx playwright install chromium
```

## Run in two PowerShell terminals

Backend, terminal 1:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-access-log
```

Frontend, terminal 2:

```powershell
Set-Location 'C:\Finova AlignIQ\frontend'
npm run dev
```

Open [the local workspace](http://127.0.0.1:5173). Both servers bind to loopback. The raw input UI works without the backend; parsing/review need it running. Vite proxies `/api` to `http://127.0.0.1:8000`, so no cross-origin endpoint is needed. Restart older backend processes before testing new routes. Stop servers with Ctrl+C.

Try **Load synthetic example**, inspect the untouched raw preview, optionally supply context claims, confirm synthetic data, then choose **Parse Table**. Source indicators are automatic; there is no vendor selector. Choose **Run Planning Assistant** to recompute review and wording in one request. Current ordinary pasted inputs remain semantically unverified, so the report explains unavailable assessments without calling Groq. Selectable observations are available only when their evidence is authorized. Editing input/context, Clear/demo, switching purpose or revoking confirmation invalidates results; changing assessment or wording invalidates the draft and selections. No automatic uploads or retries occur. Legacy separate actions remain in the expandable Advanced section.

## Fixed Finova Synthetic Demonstration

Start the local backend with both development controls explicitly set (keep these disabled in production):

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
$env:FINOVA_ENVIRONMENT = 'development'
$env:FINOVA_PLANNING_DEMO_ENABLED = 'true'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-access-log
```

Use the frontend startup above. Click **Load Finova planning demo**, inspect its conventions and movement table, choose **Deterministic templates** for an entirely offline pipeline, then **Run Planning Assistant**. Four positions become TEST_ONLY descriptive observations; a fifth numeric value deliberately lacks semantic evidence, and missing cells remain missing. The three dimensions each contain one comment; rotation and the mixed distribution summary remain Other. No group/anatomical identity is inferred from opaque tokens 11–15.

The input and draft development routes accept only a wording mode, never raw text, fixture paths, flags or semantic evidence. The server verifies the shipped raw/expected hashes and exact parser oracle with the existing read-only fixture verifier. Copying the identical demo text into normal intake still yields UNVERIFIED abstention. Editing text/context, clearing, changing purpose or revoking consent removes demo authority and prior results in the browser. The demo flag never permits patient data or activates clinical rules. Optional Groq wording still separately requires `GROQ_API_KEY` and `FINOVA_GROQ_SYNTHETIC_ENABLED=true`; deterministic mode makes no provider call. No key is needed for the demonstration.

Reproduce the invented assets, frontend response fixtures and schemas:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe scripts/build_planning_demo.py --frontend-fixtures
.\.venv\Scripts\python.exe scripts/export_schemas.py
```

These commands write only fixed synthetic repository assets. HTTP processing remains in memory and read-only. The semantic assertions are independently specified in the generator; the parser snapshot is a structural regression artifact, not an independent vendor oracle or a human clinical review.

## Attachment Interface / Micro Review

Choose **Micro**, paste synthetic TMT, confirm synthetic input and **Parse Table**. After inspecting the original and parsed values, choose **Run Attachment Review**. Normal pasted input produces only unknown/withheld rows because vendor mapping, actual attachment plans and clinical policies are absent. Large or zero movement values do not create attachment decisions. Expand a row to inspect its evidence, missing prerequisites and original references. Use **Copy attachment DRAFT** or **Download attachment DRAFT (TXT)** for an explicit local export. No approval or clinical sign-off is recorded.

For the positive illustrative workflow, start the local backend with separate server-owned development permission:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
$env:FINOVA_ENVIRONMENT = 'development'
$env:FINOVA_ATTACHMENT_DEMO_ENABLED = 'true'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-access-log
```

In Micro, click **Load Finova attachment demo**, inspect the conventions/table, then **Run Attachment Review**. The fixed scenario has two supplied candidates, one linked alternative, one explicit supplied no-attachment decision, one unknown and one withheld row. Invented DEMO_TILE design IDs, toy dimensions/orientation/surface/window references are authored demonstration data, never inferred from TMT values or selected by an LLM. Opaque tooth tokens 11–15 have no anatomical/vendor numbering claim. Supplied no attachment is distinct from unknown or withheld. The existing semantic fixture and raw/expected hashes are rechecked; the separately hashed attachment scenario must bind to the same exact input. No arbitrary text or request flag can enroll new TEST_ONLY evidence. Even the identical demo table pasted through the normal route stays unverified.

The Micro module uses deterministic templates with **zero LLM calls**, including in the demo. All 96 rule IDs remain accounted for; A01–A04/R15 remain disabled, and A05/A06/H08/N safeguards continue to withhold clinical attachment decisions. No production vendor path, validated geometry, 3D editor, attachment prescription, CAD write-back or clinical staging engine is added. Keep demo flags false in production; each requires the development environment and its own server availability flag.

Rebuild the independently authored synthetic scenario, response fixtures and schemas:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe scripts/build_attachment_demo.py --frontend-fixtures
.\.venv\Scripts\python.exe scripts/export_schemas.py
```

Additive routes: `POST /api/v1/attachments/draft` accepts raw synthetic input/context and an optional recovery receipt; `POST /api/v1/development/attachment-demo/input` and `/draft` accept **only an empty JSON object**. They never accept uploaded decisions, geometry, fixture paths or semantic authority. New schema files are `attachment-{request,draft,demo-input,demo-request}.v1.json`. Runtime input/output stays in memory; fixed repository demonstration files are read-only during requests.

## Sequencer / Nano Review

Choose **Nano**, paste synthetic TMT, confirm synthetic input and **Parse Table**, then **Run Sequencing Review**. Ordinary input produces an unavailable DRAFT with separate upper/lower, segment and right/left anchorage sections. Original values, explicit zero and missing cells remain distinct. No anatomical arch is inferred from a token, no stage record is reconstructed from totals or a claimed index, and unknown anchorage never means anchorage is unnecessary.

For the executable fictional demonstration, start the local backend with:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
$env:FINOVA_ENVIRONMENT = 'development'
$env:FINOVA_SEQUENCER_DEMO_ENABLED = 'true'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-access-log
```

In Nano, select **Load Finova sequencing demo**, inspect the conventions/source values, then **Run Sequencing Review**. Six fictional statements describe supplied upper/lower arch, segment and side-specific contexts. A separate fixed five-record dataset illustrates stage-ID/order/kind checks. Its records carry no per-stage movements: **NO_STAGE_MOVEMENT_BINDING**. Supplied window IDs are metadata references, not generated stage allocations or a clinical timetable. An unresolved source token and disabled assessments remain explicitly withheld. The output visibly states **SYNTHETIC DEMONSTRATION — NOT CLINICAL ADVICE**.

The server verifies the bundled semantic fixture and separately hashed scenario against the same exact input. Only this fixed scenario can be read through the demo routes; the environment flag controls route availability and never grants authority to uploaded text or strategies. Even an identical table through normal intake stays UNVERIFIED. Source/context/consent/purpose changes cancel pending requests and invalidate results/exports. No sign-off, force calculation, clinical schedule, stage ceiling, duration, auxiliary, geometry optimization or collision conclusion is provided. R13/T01–T08 remain disabled. Nano uses deterministic wording and makes **zero LLM calls**.

Reproduce the fixed data, actual service response fixtures and schemas:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe scripts/build_sequencer_demo.py --frontend-fixtures
.\.venv\Scripts\python.exe scripts/export_schemas.py
```

New routes: `POST /api/v1/sequencing/draft` accepts only original synthetic input/context and an optional recovery receipt; `POST /api/v1/development/sequencer-demo/input` and `/draft` accept **an empty JSON object only**. No stage dataset, strategy, path, clinical permission or provider override is accepted from a browser. New contracts are `schemas/sequencing-{request,draft,demo-input,demo-request}.v1.json`. Copy/TXT retains every statement's origin, exact source values, stage references/kinds, missing prerequisites, limitations and the complete 96-rule ledger. No external software is contacted by export.

Health check:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/health'
```

Expected JSON: `{"status":"ok","service":"finova-aligniq","phase":1}` (historical compatibility field). Normal intake uses `POST /api/v1/tmt/parse`; explicit assistance uses `POST /api/v1/tmt/parse/assisted`. Legacy `POST /api/parse`, observations and draft-report routes are retained. Public OpenAPI/Swagger/ReDoc routes remain disabled. Inputs must not be placed in URLs or logs.

Optional synthetic API smoke check:

```powershell
$syntheticRequest = @{
  raw_text = "# SYNTHETIC`nTooth`tRotation (deg)`n13`t-1.2300 M`n"
  source_claim = 'Unknown'
  synthetic_data_confirmed = $true
} | ConvertTo-Json
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/parse' -Method Post -ContentType 'application/json; charset=utf-8' -Body $syntheticRequest
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/tmt/observations' -Method Post -ContentType 'application/json; charset=utf-8' -Body $syntheticRequest
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/reports/draft' -Method Post -ContentType 'application/json; charset=utf-8' -Body $syntheticRequest
```

## Test and build in PowerShell

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check

Set-Location 'C:\Finova AlignIQ\frontend'
npm test
npm run build
npm run test:e2e
```

Playwright runs the real frontend/backend path at 1440, 1024, 768 and 375 px. It starts the servers if needed, or reuses running local servers; both must use the current code. It uses only invented text. Synthetic screenshots/reports in `test-results/` are ignored. In an execution sandbox that blocks local event-loop/socket access, API and browser tests may need the host's approved local execution path.

Optional UI watch mode:

```powershell
Set-Location 'C:\Finova AlignIQ\frontend'
npm run test:watch
```

Optional build preview (build first; keep the backend running):

```powershell
Set-Location 'C:\Finova AlignIQ\frontend'
npm run preview
```

Open [the local build preview](http://127.0.0.1:4173). Its `/api` proxy also targets the local backend. This is a development preview, not deployment approval.

Regenerate machine-readable contracts after an intentional API model change:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe scripts\export_schemas.py
```

Schemas are exported with response Decimal values as strings, preserving precision rather than binary floating-point approximations. The backend tests verify that checked-in schemas match the Pydantic models.

## Raw text and privacy behavior

- Textarea state stores `event.target.value` directly. It is never trimmed, cleaned, split, normalized or aligned by the frontend. Counting is separate. The server receives that unchanged logical string only after an explicit parse, review or report action.
- Raw preview renders a React text child with `white-space: pre-wrap`, `overflow-wrap: anywhere`, and `tab-size: 4`. Literal script/HTML is inert in raw and structured previews. Long rows wrap through CSS; wrapping adds no stored newline.
- Browser textarea CRLF/CR canonicalization is expected; byte-for-byte clipboard fidelity is not promised. API raw text is otherwise preserved exactly, and derived parser tokens retain spans into it.
- Character counts use Unicode code points, including whitespace/newlines, not grapheme clusters. Empty input has 0 lines; otherwise each newline adds a line, including a trailing blank line.
- Normal intake sends source claim Unknown. Detected source indicators and syntax candidates never populate verified metadata. Version, notation, basis, mode, scope and stage claims remain unverified. Synthetic demos reset context and never establish vendor compatibility.
- Raw text/results remain in application memory until an explicit local copy/download. There are no browser-storage writes, analytics, third-party scripts/fonts or persistent backend writes. Comment Groq calls contain only aliases, rule IDs/types and approved wording alternatives. Phase 4 recovery transmits source cells/positions only after server reproduction of a controlled synthetic fixture and development gates, as part of explicit Parse Table. API responses are `no-store`; validation failures do not echo raw input. Documented backend commands disable access logging.
- This prototype does not detect/redact PHI or certify browser/OS/infrastructure behavior. Use synthetic text only. Refreshing or closing the page discards application state.

## Documentation and release boundaries

All three documents now supplied in `docs/` were read completely before Phase 1 changes, including all tables. They are unchanged. The audit and architecture were supplied as Markdown. Their absence during Phase 0 is historical and no longer a documentation blocker.

The audit/corrected v2 override older ideas. READY does not mean clinically validated. Manufacturer configurations never become biological thresholds. Planned movement does not prove achieved movement, safety, anatomy, sequence, attachments, IPR, occlusion, collisions, prognosis or treatment outcomes. Phase 1 still returns lexical evidence only. Phase 2A separates descriptive rule evaluation and draft safeguards; clinical predicates stay disabled and vendor observations stay unavailable.

## Current project tree

```text
Finova AlignIQ/
├── .env.example
├── .gitattributes
├── .gitignore
├── README.md
├── PARSER_PHASE1.md
├── PARSER_PHASE1_5.md
├── ENGINE_PHASE2A.md
├── REPORT_PHASE3.md
├── examples/phase3-synthetic-template-report.txt / phase3-synthetic-groq-report.txt
├── docs/                              # user documents, unchanged
│   ├── FINOVA_ARCHITECTURE_BLUEPRINT.md
│   ├── FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md
│   └── Orthodontic_TMT_Independent_Critical_Audit(2).md
├── schemas/
│   ├── parse-request.v1.json
│   ├── parse-result.v1.json
│   ├── vendor-fixture-manifest.v1.json
│   ├── vendor-fixture-expected.v1.json
│   ├── semantic-assessment.v1.json
│   ├── review-request.v1.json / draft-review.v1.json / rule-definition.v1.json
│   └── report-request.v1.json / final-draft-report.v1.json / groq-wording.v1.json
├── frontend/
│   ├── package.json / package-lock.json
│   ├── index.html / tsconfig.json
│   ├── vite.config.ts / tailwind.config.ts / postcss.config.js
│   ├── playwright.config.ts
│   ├── e2e/parse.spec.ts / review.spec.ts / report.spec.ts
│   ├── public/favicon.svg
│   └── src/
│       ├── main.tsx / App.tsx / styles.css / syntheticExample.ts
│       ├── App.test.tsx / App.parse.test.tsx / App.review.test.tsx / FinalReport.test.tsx
│       ├── api/parse.ts / review.ts / report.ts
│       ├── components/ContextFields.tsx / ParseResults.tsx / DraftReviewPanel.tsx
│       ├── components/FinalReportPanel.tsx
│       └── test/
│           ├── setup.ts
│           ├── fixtures/synthetic-parse-result.json / synthetic-draft-review.json
│           └── fixtures/synthetic-final-report.json / synthetic-groq-report.json
└── backend/
    ├── requirements.txt / pytest.ini
    ├── scripts/export_schemas.py
    ├── scripts/verify_vendor_fixtures.py
    ├── vendor_verification/manifest.json / pending-fixture.example.json / README.md
    ├── app/
    │   ├── __init__.py / main.py
    │   ├── api/__init__.py / parse.py / privacy.py / review.py / reports.py
    │   ├── domain/__init__.py / models.py
    │   ├── semantics/__init__.py / models.py / fixtures.py / registry.py / normalization.py
    │   ├── review/__init__.py / models.py / registry.py / service.py / templates.py / safeguards.py
    │   ├── reports/__init__.py / models.py / settings.py / groq_client.py / prompt.py / templates.py / validation.py / service.py
    │   └── parser/
    │       ├── __init__.py / service.py / tokenize.py / layouts.py
    │       ├── labels.py / values.py / teeth.py
    │       └── adapters/__init__.py / base.py / clincheck.py / suresmile.py
    └── tests/
        ├── test_health.py / test_parse_api.py / test_parser.py
        ├── test_semantics.py / semantic_helpers.py
        ├── test_review.py
        ├── test_reports.py
        └── fixtures/README.md / synthetic_vertical.tsv / synthetic_horizontal.txt
```

Generated virtual environments, node modules, build output, caches and local QA artifacts are ignored.

## Phase 1 verified results

Final Phase 1 checks on Windows with Python 3.12.10 and Node 24.12.0:

| Check | Result |
| --- | --- |
| pytest parser/API/contract suite | **120 passed** |
| Vitest / React Testing Library | **30 passed** |
| Playwright against the real API | **12 passed**, at 1440 / 1024 / 768 / 375 px |
| TypeScript and Vite production build | **Passed** |
| Backend dependency consistency | `pip check`: no broken requirements |
| Backend startup | Verified manually and through Playwright's automatic server startup |
| Visual review | Desktop/mobile synthetic results inspected; no horizontal page overflow |

Coverage includes irregular whitespace/blank lines, both orientations, explicit delimiters, Unicode and line endings, raw spans, exact Decimal strings, zero/missing distinctions, unsupported/ambiguous values/layouts, duplicates, notation/source/context conflicts, request size/validation privacy, explicit network action, loading/errors/timeouts, stale responses, and inert markup. Browser tests confirm no input-triggered request before Parse, only the intended parse request afterward, and no browser-storage writes.

One upstream Starlette TestClient warning remains about deprecated `httpx` integration. Playwright also reports an environment-only color-variable warning. Neither failed validation. This is synthetic-data technical validation, not authentic vendor verification, full accessibility certification, or clinical approval.

## Remaining review requirements

- Authentic, authorized ClinCheck and SureSmile clipboard oracles and exact source-version coverage; verify serialization and source-specific numbering, directions, reference basis, plan mode and stage scope against independently reviewed source UI.
- Review supported generic grammar and explicit engineering limits. The implementation deliberately rejects ambiguous alignment, CSV/quoted/multiline cells, multiple tables, unsupported units, scientific notation and unverified canonical mappings.
- Privacy/security and qualified clinical governance remain separate release requirements. The synthetic-data checkbox is an intake gate, not proof that text is free of patient information.
- The authentic-vendor release gate is still open. Phase 2A is limited to controlled infrastructure and TEST_ONLY descriptive development; Phase 2B requires review.

## Phase 1.5 offline verification gate

From the backend folder:

```powershell
.\.venv\Scripts\python.exe scripts\verify_vendor_fixtures.py
```

The shipped empty manifest intentionally returns exit code **2**, `NO_AUTHENTIC_ORACLES`, and leaves all vendor normalization disabled. This is not a passing vendor compatibility check. Local authorized captures can later be checked with `--manifest` and `--fixture-root`; the verifier reads but never acquires, writes, copies or transmits them. Passing artifact/oracle checks alone cannot register an approved release. No purported authentic capture, vendor gold output or real review has been added.

The semantic assessment remains an internal Python library; the Phase 2A endpoint recomputes it internally, rather than accepting supplied semantic models. The existing `/api/parse` gate, null canonical fields, false verification flags and health response remain unchanged. Test-only evidence stays TEST_ONLY and cannot enable a vendor.

Final Phase 1.5 validation: **192 backend tests passed** (all 120 existing tests plus 72 new verification/readiness tests), **30 frontend tests passed**, **12 browser tests passed**, and **TypeScript/production build passed**. Backend dependency consistency also passed. The original documents and both original JSON schemas retain their prior hashes. Frontend tests passed with normal worker-process access after sandbox worker startup timed out before collecting tests. The existing upstream Starlette TestClient deprecation warning remains; no failing checks remain. The Graphify AST refresh completed without LLM extraction.

## Phase 2A validation and review boundary

Final checks: **288 backend tests**, **55 frontend tests**, **16 browser tests** and **production TypeScript/Vite build** passed. `pip check` and `git diff --check` passed. Browser tests used fresh backend startup and all four existing viewport sizes. Sandboxed startup stalled for browser checks and one final backend invocation; approved normal local execution passed the final complete suites. Existing upstream deprecation/color warnings remain non-failing. AST-only Graphify refresh completed without LLM extraction.

The sole existing test scope change is expanding the exact route allowlist for the authorized observations endpoint. Parser and semantic algorithms, prior schema contracts and original documentation are unchanged. All 96 audit rule IDs are retained; clinical predicates are disabled, with R14 retained only as the audit-corrected abstention control. Reports are DRAFT only, with no sign-off action. Review has an explicit **512-position engineering limit** to bound output expansion; the parser's existing limits and full input retention remain unchanged. See [the complete implementation/disposition report](docs/ENGINE_PHASE2A.md) for exact active, disabled and deferred IDs, architecture, changed files, structured examples, limitations and authentic-sample requirements.

Vendor verification remains unavailable. No Phase 2B functionality has been started.

## Phase 3 backend configuration

Standard Templates work without a key. Optional wording uses Groq Cloud only, model `openai/gpt-oss-120b`, following [Groq's official structured-output documentation](https://console.groq.com/docs/structured-outputs). Settings are read from the **backend process environment**; `.env.example` is not automatically loaded. Never use a `VITE_` key variable or place a key in frontend code.

In the backend PowerShell terminal:

```powershell
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
```

Then start/restart the backend using the existing command. The key and server synthetic permission are both required, as is exact eligible TEST_ONLY evidence. Arbitrary pasted input currently has no released semantics, so no comment Groq call occurs even with a key. Phase 3 used mocked provider responses; the later parser-finalization task added the explicitly opted-in live probe below.

Retries default to zero. At most one optional retry honors a valid short `Retry-After` on 429/503; longer/unknown waits, timeouts, malformed/unsafe output or missing settings fall back to templates. Every accepted phrase must exactly match an approved alternative for its finding; measured values, original signs/directions, context, uncertainty and provenance are rendered locally. No unrestricted LLM comments are accepted.

**Real-patient transmission remains disabled with no environment/request override.** Vendor verification, approved privacy/data-handling controls and separately approved clinical policies remain open gates. No key setting activates them. Copy/download is local and explicit; Windows clipboard line endings may differ while TXT downloads preserve the server's UTF-8 text. See [REPORT_PHASE3.md](docs/REPORT_PHASE3.md) for all settings, safeguards, schema details and limitations.

## Historical Phase 3 final validation

**372 backend tests**, **86 frontend tests**, **20 browser tests** and **TypeScript/production build** passed. Dependency and formatting checks passed; desktop/mobile report screenshots were inspected. All prior tests remain, with the exact route allowlist extended for the authorized report endpoint. Original documents and existing parser schemas retain their hashes; clinical and vendor semantic policies remain unchanged. The required Graphify update completed using AST extraction only.

Provider responses were mocked throughout; **no live Groq call or other-provider test was performed**. The final complete backend suite used approved local process access after a sandboxed invocation stalled. Existing upstream/environment warnings remain non-failing. No additional phase has begun.

Examples: [Standard Templates TEST_ONLY report](examples/phase3-synthetic-template-report.txt), [mocked Groq TEST_ONLY report](examples/phase3-synthetic-groq-report.txt). Neither is vendor compatibility evidence or an actual clinical report.

## Historical parser finalization: optional synthetic development assistance

No secrets are required for normal parsing/review/templates. Keep `GROQ_API_KEY` for comment generation and `GROQ_API_KEY_2` for structural parsing. Neither key substitutes for the other. Secret files remain ignored and were not modified by this task. Never use a `VITE_` credential.

The parser's server defaults are `FINOVA_ENVIRONMENT=production` and `FINOVA_PARSER_GROQ_ENABLED=false`. Other defaults are `GROQ_PARSER_MODEL=openai/gpt-oss-120b`, `GROQ_PARSER_TIMEOUT_SECONDS=8` (0.1–30), `GROQ_PARSER_MAX_COMPLETION_TOKENS=2048` (256–8192), and `GROQ_PARSER_REASONING_EFFORT=low` (low/medium/high). A different configured model must actually support the strict schema; errors safely abstain. Parser retries are always zero. Comment configuration and its separate evidence gate are retained.

For an intentional development-only test, with keys already held in the ignored root `.env.local`, start the backend in its own terminal:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
$env:FINOVA_ENVIRONMENT = 'development'
$env:FINOVA_PARSER_GROQ_ENABLED = 'true'
.\.venv\Scripts\python.exe scripts\run_dev.py --env-file ..\.env.local
```

The explicit loader reads known settings only, supports plain or quoted single-line values, does no evaluation/interpolation, never prints values, and preserves existing process settings. Standard Uvicorn commands do not automatically load secret files. Do not create or overwrite an existing secret file from the template. Stop the old backend before starting another on port 8000.

Start the frontend with `npm run dev` in the frontend terminal. Choose **Load synthetic Markdown example**, confirm synthetic data and **Parse Table**. Only when all server gates are satisfied does the separate cloud consent and **Try AI-assisted parsing** action appear. The backend additionally requires byte-exact matching of one of the two shipped cloud-allowed synthetic examples. A synthetic prefix or checkbox alone is insufficient. Editing even one value disables cloud eligibility. There is no arbitrary-paste or real-patient cloud override. Disable the flag or return the environment to production and restart to remove the action.

Acceptance requires an independently proven complete Markdown outer-pipe grid with a separator row and exact original cell associations. This is a deliberately narrow development fallback, not general recovery of corrupted vendor exports. Ordinary tab/pipe/semicolon/multispace parsing retains its existing behavior. Draft reviews/reports independently reparse the original input; an assisted preview never supplies findings or semantic authorization.

The following CLI is a **live, potentially billable** check, separate from tests. Run it only when intentionally testing connectivity; it issues at most one fixed synthetic request per configured key, with no automatic retry or key failover:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe scripts\check_groq_connectivity.py --live --env-file ..\.env.local
# Optional: --service comments or --service parser
```

Without `--live`, nothing is transmitted. A missing key produces SKIPPED for that service. The CLI prints only static status, authentication/model checks, timing, token counts and validation; it never prints keys, model output or provider diagnostics. It explicitly opts in its own fixed synthetic probes without enabling the web feature. Normal pytest/Vitest/Playwright runs use mocked provider traffic.

Live results on 2026-11-13: comments **PASSED**, HTTP 200, **2.2139 s**, **531 tokens** (430 prompt / 101 completion); parser **PASSED**, HTTP 200, **2.0543 s**, **702 tokens** (522 / 180). Both returned the requested model and passed their independent validators. These are two small connectivity measurements, not latency benchmarks, vendor verification or clinical validation. See the finalization report for the initial restricted-network failures and complete verification results.

Final parser-finalization validation: **453 backend tests, 101 frontend tests, 32 browser tests and the TypeScript/production build passed**. Dependency/formatting checks passed; new desktop/mobile screens were inspected. The authentic-fixture verifier still returns `NO_AUTHENTIC_ORACLES` (Python exit 2). The graph was refreshed using AST extraction only. No clinical activation, vendor verification, deployment, commit or push was performed.

## Phase 4 parser development and verification

Normal installation and two-terminal startup commands above are unchanged. Cloud recovery defaults to disabled. To intentionally enable generated-synthetic development recovery, use the existing private parser key `GROQ_API_KEY_2` and start the backend as follows; do not overwrite `.env.local` or the separate comment key:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
$env:FINOVA_ENVIRONMENT = 'development'
$env:FINOVA_PARSER_GROQ_ENABLED = 'true'
.\.venv\Scripts\python.exe scripts\run_dev.py --env-file ..\.env.local
```

In the frontend, choose **Load generated recovery example**, confirm synthetic intake and **Parse Table**. Recovery runs automatically only when necessary and when the server can reproduce the entire controlled fixture. Loading/typing/checking confirmation makes no provider call. Editing the example clears its generator identity. A synthetic prefix/checkbox never authorizes arbitrary data transmission. Complete Markdown now parses deterministically. The original raw preview and all report/export controls remain.

Controlled fixtures can also be generated through `POST /api/v1/development/synthetic` with a closed recipe and bounded integer seed; no arbitrary text enrollment exists. Normal parsing accepts optional `synthetic_fixture: {recipe, seed}`. Review/report requests accept optional `recovery_receipt`, which the server verifies and re-proves against original raw text/context. Receipt expiry/restart/context mismatch returns HTTP 409 with reparse guidance. Use one backend process for this ephemeral development receipt design. No semantic/vendor release can be enabled by a receipt.

Rebuild/review the original synthetic corpus and run its deterministic oracle-mocked comparison without cloud calls:

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

Optional **live** evaluation uses at most three fixed generated synthetic requests and prints only aggregate status/timing/usage, never credentials or provider payloads:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe scripts\evaluate_phase4.py --live 3 --env-file ..\.env.local
# To limit further: --live 1 --live-recipes wrapped
```

The Phase 4 report records the initial rejected probes as well as the final 10/12 recovery result. The 240/240 deterministic test comparison uses independently declared gold proposals under mocked transport and is explicitly not live model accuracy. Vendor verification, real-input privacy authorization and clinical-rule activation remain separate, uncompleted release gates.

Phase 4 validation: **584 backend tests, 104 frontend tests, 40 browser tests, TypeScript and production build passed**. Dependency/formatting checks passed. The authentic-fixture gate still returns `NO_AUTHENTIC_ORACLES`; vendor mappings and clinical R predicates remain disabled. See the Phase 4 report for the supported formats, validation results and remaining requirements.

## Phase 5 rule review and verification

The UI now includes a collapsible 96-rule evaluation ledger, missing prerequisites, execution/implementation kind, approval status, literature IDs and field provenance. Descriptive programmed movements remain separate from unavailable clinical assessments. **DRAFT — Requires Orthodontist Review** and the absence of clinical approval remain visible. Copy Report and Download Report (TXT) are preserved.

The [Phase 5 report](RULE_ENGINE_PHASE5_REPORT.md) includes the complete implementation matrix, dependencies/priorities, schema changes, additional-input designs, changed files and precise remaining blockers. All 27 clinical predicates remain disabled. D16, N11 and N14 remain deferred. Tooth-group/status, pairing, expected-coverage and stage positive examples use private, exact-input-bound TEST_ONLY evidence; no public request, environment setting or Groq output can grant clinical or semantic authorization. A READY audit disposition or an ACTIVE engineering guard is not clinical approval. No thresholds were populated.

Rebuild documentation/schemas and run the complete checks in PowerShell:

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

Current validation: **781 backend tests, 112 frontend tests, 40 browser tests, TypeScript and production build passed**. `pip check` passed; npm audit reports **0 vulnerabilities** after patching Vite to 7.3.8 and Vitest to 4.1.12. The AST-only graph update performs no LLM extraction. Existing upstream Starlette/httpx and test color-environment warnings remain non-failing. No live Groq call was needed for Phase 5.

Inspect [the complete synthetic draft report](examples/phase5-synthetic-draft-report.txt) and [its finding JSON](examples/phase5-synthetic-finding.json). These are explicitly synthetic TEST_ONLY illustrations; they provide no vendor or clinical validation. Authentic captures/independent expected outputs, versioned vendor semantic releases, approved clinical policies and additional verified examination/geometry data remain required. Phase 5 stops here.
