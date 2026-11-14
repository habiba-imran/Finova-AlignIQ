# Finova interactive synthetic demonstration

Verified locally on 15 November 2026 (Asia/Karachi). No deployment, commit or push was performed.

## Delivered workflow

Paste synthetic TMT → Parse Table → inspect the formatted table → run Macro, Micro or Nano → generated report → Copy / TXT / PDF.

The normal workspace now uses `POST /api/v1/interactive/review`. Any supported table with parsed measurement positions can produce source-based observations; an exact Finova fixture match, vendor semantic release or fixed-demo permission is not needed. The optional fixed example loaders remain available. Switching modules preserves the parsed table and clears the previous generated report. Editing input or parsing context invalidates reports and exports; pending requests are aborted and late responses are suppressed.

Macro presents factual tooth-wise observations. Micro adds explicitly labelled illustrative attachment concepts. Nano adds explicitly labelled fictional sequencing groups and a sample narrative order. Examples alternate by input order, independently of movement values; they do not use treatment thresholds or clinical predicates. Attachment dimensions, placement, orientation and indications remain unspecified. Sequencing examples do not calculate stages, movement allocations, timing, forces or anchorage requirements.

The generated report is prominent and receives focus after completion. Copy, TXT and PDF controls appear at its top. The normal UI has no AI enable/disable selector, raw JSON, internal rule identifiers or unavailable-rule ledger. It retains clear parse errors, missing-value markers, a partial-parse notice when relevant, and one concise demonstration/not-for-clinical-use label. Existing engineering views and legacy workflows remain available through `?diagnostics=1`.

## Numerical and clinical boundaries

- Observations use the existing parser's exact Decimal strings and original cells, labels, direction suffixes, missing states and source spans. No rounding, numerical aggregation, direction inference, anatomy assignment or missing-value imputation is introduced.
- Explicit zero is described only where the source records zero. Missing, omitted, invalid and ambiguous cells produce no numerical observation.
- Factual observations are labelled `PARSED_SOURCE_ONLY`. This is lexical source evidence, not verification of a vendor convention, achieved tooth movement or a clinical prescription.
- Simulated content is separately typed as `SIMULATED_DEMO`, with `clinical_status=NOT_EVALUATED`, and appears in a distinct UI/PDF section. It is never promoted to a calculated finding.
- All 96 existing rule records are retained, including the 27 disabled records. The parser, semantic mappings, clinical review/rule engine and reference sources were not modified. Existing API contracts and endpoints retain their prior clinical authority boundaries. The new transport has separate exported request/report schemas.

## Automatic Groq wording and privacy

The new review automatically uses the backend's existing Groq key/model when configured. There is no extra UI permission or AI-selection step. Credentials remain backend-only, and the existing bounded Groq client retains its fixed HTTPS endpoint, timeouts, response-size limit, no redirect following and sanitized failure codes.

Every interactive wording request sends the **same constant approved phrase catalog**, independent of the input table and selected module. It sends no raw text, patient/case/plan identifiers, tooth tokens, measurements, directions, source labels, table dimensions, counts, hashes or source metadata. Tests compare provider payloads from different tables to verify that they are identical.

Groq may select only an exact approved phrase for each opaque reference. The response must have the complete unique reference set. Duplicate JSON keys, missing/duplicate references and altered prose are rejected. All numerical facts, observations and illustrative examples are inserted locally. There is no free-form provider-generated treatment advice. Rejected, unavailable, unconfigured, rate-limited or failed provider output yields deterministic wording with the visible notice: **“AI generation unavailable; deterministic wording used.”** Exports retain the sanitized reason and attempt count.

The legacy `FINOVA_GROQ_SYNTHETIC_ENABLED` switch continues to gate the unchanged legacy data-transmission paths. The new interactive endpoint sends only constant phrases and automatically uses a valid backend `GROQ_API_KEY`; it does not transmit source data even when that legacy switch is false. No environment file or stored credential was changed.

## Newly pasted synthetic tables

These original verification inputs are reproducible from `examples/interactive-synthetic-tmts.json`. They do not require the fixed Finova evidence loaders.

| Input | Tooth tokens | Positions | Numerical values | Missing/omitted | Modules verified |
| --- | ---: | ---: | ---: | ---: | --- |
| New tab-separated rows | 4 | 12 | 9 | 3 | Macro, Micro, Nano |
| New transposed columns | 3 | 6 | 5 | 1 | Macro, Micro, Nano |
| New Markdown table | 2 | 4 | 3 | 1 | Macro, Micro, Nano |
| New 16-tooth, seven-field table | 16 | 112 | 96 | 16 | Macro, Micro, Nano |

The newly authored 16-tooth/112-position example includes signed angular values, preserved trailing zeros, explicit zeros, literal directions and missing intrusion values. It produces 16 factual tooth-wise cards in each module, with 16 additional clearly simulated examples in Micro and Nano. All 112 positions are retained.

## Actual verification results

| Check | Actual result |
| --- | --- |
| Complete backend suite | **1,035 passed**, one existing Starlette/httpx deprecation warning; 86.33 seconds |
| Complete frontend suite | **252 passed**, 21 test files |
| Frontend typecheck and production build | **Passed**; existing large-bundle warning remains |
| Targeted desktop interactive browser checks | **8 passed**, including newly pasted tables, all modules, automatic-AI UI status, fallback, invalid input, Copy/TXT/PDF |
| Complete five-viewport browser suite | **205 passed**, zero failures, skips or flaky tests; 14.1 minutes; widths 1440, 1024, 768, 672 and 375 pixels |
| Focused checks after final wording polish | **29 backend and 31 frontend/export tests passed** |
| Live Groq, 16-tooth/112-position input | **Macro, Micro and Nano all succeeded**; one call each, four approved phrase selections accepted per call |
| Mocked provider failures | 401, 429, 500 and 503 returned honest deterministic fallback |
| Adversarial provider wording | Invented numerical facts, extraction advice, safety claims, arbitrary markup and incomplete/duplicate reference sets rejected |
| Provenance and API security | Source measurements/spans preserved; stale hash rejected with 409; unsupported input and forged authority/credential fields rejected; responses remain `no-store` |
| Export fidelity | Clipboard and downloaded TXT match the complete report text; PDF embedded TXT and validated JSON match the accepted report, including all 96 rule outcomes |
| Knowledge graph | `graphify update .` succeeded using AST extraction without an LLM |

Browser acceptance runs against fresh owned local backend and production-preview servers. The regression suite covers the normal interactive workspace and the preserved diagnostic workflows, including keyboard use, reduced motion, responsive layout and invalidation. Provider access is explicitly disabled in these repeatable browser runs; live provider success is recorded separately, rather than claimed from mocked browser responses.

PDF verification includes visible text extraction and page rendering, as well as byte-equivalent embedded report checks. The small-table Macro PDF has two pages; Micro and Nano have three pages each. All eight rendered pages were visually inspected, with no observed clipping, overlap or lost measurement/simulation labels. Rendering tools are isolated under `.qa`; app dependency manifests were not changed.

### Reproduction commands

From `backend`:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts/export_schemas.py
.\.venv\Scripts\python.exe scripts/verify_interactive_demo.py
.\.venv\Scripts\python.exe scripts/verify_interactive_demo.py --live
```

The live command reads the existing root `.env.local` only through the backend allowlisted loader and emits sanitized generation metadata. It sends the constant phrase catalog, not the table.

From `frontend`:

```powershell
npm.cmd test -- --maxWorkers=2 --reporter=json --outputFile=../evidence/interactive-demo/frontend-tests.json
npm.cmd run build
$env:PLAYWRIGHT_JSON_OUTPUT_FILE = 'C:\Finova AlignIQ\evidence\interactive-demo\browser-tests.json'
npm.cmd run test:e2e -- --config=playwright.final.config.ts --reporter=line,json
```

### Evidence

- `evidence/interactive-demo/verification-summary.json`: consolidated verified results.
- `evidence/interactive-demo/frontend-tests.json`: complete frontend results.
- `evidence/interactive-demo/browser-tests.json`: complete browser results, including per-test outcomes and zero unexpected/flaky results.
- `evidence/interactive-demo/frontend-final-wording-tests.json`: final focused report/export results.
- `evidence/interactive-demo/live-groq.json`: actual configured-provider results for all three modules.
- `evidence/interactive-demo/synthetic-summary.json`: results for the four original inputs in all modules.
- `evidence/interactive-demo/*-112.json` and `*-112.txt`: complete 112-position report snapshots and text exports.
- `evidence/interactive-demo/macro.pdf`, `micro.pdf`, `nano.pdf`: generated small-table PDF exports.
- `evidence/interactive-demo/pdf-visual/`: rendered pages and visible-text verification.
- `frontend/test-results/interactive-large-*/`: downloaded 112-position TXT/PDF files and browser screenshots from the acceptance run.

## Remaining limitations

1. This is a synthetic descriptive demonstration. Source syntax can be parsed without establishing tooth identity, vendor semantics, clinical suitability, achieved movement or patient safety.
2. Micro attachment concepts and Nano group/order examples are deliberately arbitrary simulations. They are not treatment calculations, validated attachment prescriptions or executable staging plans.
3. Supported parser formats and engineering limits still apply. Unresolved content in partially parsed tables is not reconstructed or guessed; unsupported input cannot generate a report.
4. Groq selects from a closed phrase catalog. Professional wording is intentionally constrained to prevent invented facts and unsupported clinical choices. Network availability and provider credentials/quota can change after these live checks.
5. A synthetic-data declaration is not PHI detection. Use synthetic input only. The interactive provider boundary prevents source-data transmission, but the browser must send the pasted table to the local/configured backend for parsing and review.
6. PDF generation remains local and preserves complete TXT/JSON attachments. Unsupported display glyphs cause a visible refusal rather than a corrupt PDF; the lossless TXT option remains available. Large inputs produce longer reports.
7. Browser automation uses Chromium. No human clinical validation or human screen-reader certification is claimed. Existing build-size and dependency-deprecation warnings are not resolved by this scoped change.

Existing unrelated working-tree edits and documentation changes were preserved. No unrelated component redesign, deployment, commit or push was performed.
