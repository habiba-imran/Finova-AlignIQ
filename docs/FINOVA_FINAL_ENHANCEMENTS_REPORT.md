# Finova AlignIQ — final PDF and lexical-label enhancements

14 November 2026, Asia/Karachi. Scope: two requested improvements to the existing local academic prototype. **DRAFT / NOT CLINICAL ADVICE. No vendor certification or clinical authorization.**

The [final integration report](docs/FINOVA_FINAL_INTEGRATION_REPORT.md), [public TMT evaluation](docs/FINOVA_PUBLIC_TMT_REFERENCE_EVALUATION.md) and current source were inspected before implementation. The repository was clean at the start. Historical reports and source reference files are preserved. This report supersedes their test totals and unsupported-label count for this enhancement snapshot.

## PDF export

Macro, Micro and Nano now offer **Export PDF** beside their existing copy/TXT controls. The existing standalone descriptive-report panel uses the same exporter. Existing copy, selection and TXT code paths are unchanged. A PDF always exports the complete validated draft, including content hidden by UI disclosures or pagination, independently of selected comments.

The shared renderer uses the same runtime report validators as the existing frontend and takes a snapshot before asynchronous generation. It adds presentation only:

- A4 pages, Finova teal, consistent typography, repeating module/DRAFT headers, footer warnings and `Page n of total`.
- An opening scope/limitations section with **SYNTHETIC EXAMPLE — NOT CLINICAL ADVICE** for TEST_ONLY examples; ordinary input is explicitly UNVERIFIED.
- Readable exact-measurement tables. Nano includes its parsed positions, including missing values; Macro/Micro include the report's admitted observations. Original labels/unit text, literal values and Decimal strings remain distinct from lexical status. No numeric rounding, direction conversion or new clinical interpretation occurs.
- Tables wrap long tokens, repeat column headers across pages and can split an oversized row. The complete original report text follows, retaining every finding, source/evidence reference, missing prerequisite, rule-ledger entry, clinical limitation and DRAFT label from the original export.
- Embedded **`report.txt`**, the exact original UTF-8 export, and **`validated-report.json`**, the complete validated report object, preserve all original content and structured evidence, including fields not expanded in the visible UI. Use a reader with attachment support to extract them. Visible page wrapping changes layout whitespace; embedded TXT is byte-exact.

Rendering runs in a **bundled inline Web Worker**. PDF code, Noto Sans and a small arrow/math subset of Noto Sans Symbols are bundled; no CDN, font, API or provider request occurs on export. The main UI thread remains available. Changing the source/draft/purpose or unmounting cancels and terminates pending work; completed workers terminate too. A stale job cannot download a previous draft. Failures offer explicit retry and existing TXT/copy fallback; unsupported glyphs fail rather than silently substituting lost source text.

No report endpoint, clinical rule, vendor registry, provider configuration, database or persistence was added. Explicit local PDF downloads contain the same synthetic/unverified information already available through TXT/copy. PDF text remains inert; no HTML rendering, active scripts or automatic CAD write-back is introduced.

Implementation: [renderer](frontend/src/pdf/reportPdf.ts), [inline worker](frontend/src/pdf/pdfWorker.ts), [shared export control](frontend/src/components/PdfExportButton.tsx). Pinned frontend additions: `pdf-lib` 1.17.1 and `@pdf-lib/fontkit` 1.1.1; Node 22 type definitions are a development dependency for verification. PDF generation uses the documented [PDF-LIB custom-font/attachment APIs](https://pdf-lib.js.org/docs/api/classes/pdfdocument). [Font provenance and license](frontend/src/pdf/assets/README.md) and the bundled OFL are retained. FontTools was used only as a development tool to produce the arrow/math subset; it is not an application dependency.

## Deterministic lexical recognition

Only [parser/labels.py](backend/app/parser/labels.py) changes backend application behavior.

| Original label family | Lexical recognition tag | Boundary |
| --- | --- | --- |
| `Extrusion / Intrusion` | `vertical` | Existing combined-label family; no signed axis/direction mapping. |
| `Relative Ext / Int` | `relative_vertical` | Distinct from absolute vertical; no reference basis inferred. Full `Relative Extrusion / Intrusion` is an explicit alias. |
| `Translation B / L` | `buccolingual` | Existing lexical tag only; B/L anatomy and suffix directions remain unverified. |
| `Translation M / D` | `mesiodistal` | Existing lexical tag only; M/D anatomy and suffix directions remain unverified. |

Safe matching variations are case differences, whitespace/NBSP normalization and optional whitespace around the ASCII slash, with the existing explicit suffix-unit grammar. No fuzzy matching, substring matching, spelling guessing, inferred unit or vendor-specific map was added. Ambiguous composite labels such as `Translation B / L / M / D` remain unsupported. A normalized alias assigned to multiple families is withheld, not resolved by declaration order. Synonymous repeated columns are retained and marked ambiguous rather than merged.

Raw labels, cell values, unit tokens, signs, suffixes, Decimal precision, zero/missing states and exact header/value spans follow the existing parsing path unchanged. Recognition does not populate `canonical_axis`, `canonical_direction`, `mapping_id` or `semantics_verified`. The empty vendor release registry and existing evidence gates remain authoritative. Existing table-layout ambiguity is still refused; normalizing a label does not repair a damaged grid.

## Published-reference benchmark

The same offline evaluator was rerun against all 196 cells, both table orientations and the separately documented correction overlay. Published case-derived references were not sent to the synthetic-only website or any provider.

| Check | Historical snapshot | Current result |
| --- | --- | --- |
| Exact original positions/values/spans | 196/196 | **196/196** |
| Recognized lexical movement-label positions | 84/196 | **196/196** |
| Unsupported-label positions | 112/196 | **0/196** |
| Numeric positions, including 8 explicit zeros | 182/182 | **182/182** |
| Missing dash positions | 14/14 retained | **14/14 retained** |
| Incorrect associations/extra positions | 0 | **0** |
| CSV agreement with independently reviewed original figures | 195/196 | **195/196** |
| Explicit correction overlay: source-reviewed compact values | 196/196 | **196/196** |
| Transposed control: same original cells | 196/196 | **196/196** |
| Semantic authorization | 0/196, DISABLED | **0/196, DISABLED** |
| Approved vendor releases / provider calls | 0 / 0 | **0 / 0** |

The preserved conflict is Mamani Figure 2, tooth 25 angulation, CSV line 94: supplied **`24D`**, original figure **`2.4 D`**. The parser retains `24D` in the primary run and `2.4D` only in the explicitly corrected derived control. No source CSV/PDF or prior review-grid value was silently edited. The one-agent visual review and re-typeset TSV scope remain unchanged; these are not native clipboard or clinical gold data. Controls reuse the same cells and do not increase the denominator.

Evidence: [per-cell evaluation](evidence/enhancements/public-reference-evaluation.json) and [integrity/gate results](evidence/enhancements/integrity-checks.json). Original input hashes still match the historical evaluation. Lexical recognition is reported separately from semantic authorization throughout.

## Verification

| Check | Result |
| --- | --- |
| Complete backend suite | **1,006 passed**, 43.11 seconds; one existing upstream Starlette/httpx deprecation warning. Prior 970 + 36 new alias/precision/span/ambiguity/safeguard cases. |
| Complete frontend suite | **208 passed / 16 files**, 77.81 seconds, using two workers. Prior 190 + 18 PDF/content/lifecycle/worker tests. |
| TypeScript and production build | **Passed**, 2,100 modules. No schema or backend dependency changes. |
| Complete browser suite, real API and built bundle | **160 passed in 9.8 minutes**, 32 scenarios × 5 widths (1440/1024/768/672/375); no failures, retries or skips. Includes all original 140 cases plus 15 real module-PDF downloads and 5 generic-label/semantic-refusal cases. |
| PDF content verification | **Passed** for Macro, Micro, Nano, ordinary unverified and long reports: exact embedded TXT/JSON, complete visible original report text, headers/footers on every page and body baselines within margins. |
| PDF visual checks | **Passed**: opening scope, exact tables, original-report pages, embedded arrows, final limitations and stress-report ending reviewed. No clipping, overlap, missing glyph or footer collision observed. Export controls/status inspected at desktop/mobile widths, with overflow and real export checks at all five widths. |
| Schemas / vendor gate | **32 regenerated identically**. Vendor verifier exits **2, NO_AUTHENTIC_ORACLES**, expected open release gate; not a vendor-compatibility pass. |
| Dependencies | `pip check` and npm resolution passed; npm audit **0 vulnerabilities**; pinned Python requirements **no known vulnerabilities** at audit time. Python audit retains its existing unhashed-requirements warning. |
| Graphify / whitespace / links | **Passed**: AST update exit 0, 1,391 nodes / 4,699 edges; no semantic-document re-indexing/API call. Whitespace check clean; 53 current handoff links resolve; 66 frontend source/bundle files scanned with no Groq-key pattern matches; backend `.env.local` ignored. Pattern scan is not exhaustive secret detection. |

The final frontend command limits concurrent test workers to two. An earlier unconstrained run passed 202 tests but exceeded the unchanged 30-second Macro PDF test limit under CPU contention; the complete constrained run passes without timeout changes, skips or weakened assertions. Earlier PDF development checks exposed long-token wrapping cost and an unavailable arrow glyph; wrapping was optimized and the final arrow font is embedded. A preliminary browser run was stopped for the font/worker update; it is not the final acceptance run.

Independent PDF checks use pypdf to compare embedded files exactly and compare all visible original report text after whitespace/Unicode compatibility normalization. This verifies actual page content independently of attachments. Final fixture page counts: **Macro 43, Micro 28, Nano 26, ordinary 23, stress report 45**. The stress report includes repeated long unbroken tokens and a final sentinel; no source content is truncated. Complete safeguarding and provenance intentionally make reports long. Test PDFs/renders are ignored local QA artifacts under `evidence/enhancements/qa/`, not patient persistence or vendor fixtures.

Remaining presentation limits: fonts have bounded Unicode coverage (unsupported glyphs cause explicit refusal); PDFs are not PDF/A or certified tagged accessible documents; browser support for local Blob workers/downloads is required. The all-local renderer/fonts increase the initial JS bundle to **2,312.02 kB / 986.56 kB gzip**, with Vite's normal chunk-size warning retained. CSS remains approximately 37.34 kB. No runtime network-loading workaround or warning suppression was introduced. Export generation takes several seconds for these long reports; worker cancellation prevents stale downloads.

## Reproduction

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check

Set-Location 'C:\Finova AlignIQ'
.\backend\.venv\Scripts\python.exe backend/scripts/evaluate_public_tmt.py --output evidence/enhancements/public-reference-evaluation.json

Set-Location 'C:\Finova AlignIQ\frontend'
npm ci
npm test -- --maxWorkers=2
npm run build
npx playwright test --config playwright.final.config.ts --output ../evidence/enhancements/browser-results
npm audit
```

For presentation, follow the existing [local demo guide](backend/FINOVA_FINAL_DEMO_GUIDE.md) with all three development demo flags enabled and both Groq flags disabled. Load each dedicated fixed demo, run its review, then choose Export PDF. Inspect its DRAFT/origin warnings, exact table, complete text and evidence. TXT/copy remain beside PDF. Editing the input/purpose invalidates the draft/export. The published benchmark stays a terminal-only reference test.

**Both requested improvements are implemented and final regression acceptance passes.** All **96 rules**, including **27 disabled clinical predicates** and **3 deferred controls**, remain intact. Groq integrations and existing UI/motion are preserved. No new clinical recommendation, vendor certification, patient persistence, database, deployment, Git commit or push is performed. The work stops here. A machine-readable [verification summary](evidence/enhancements/verification-summary.json), [independent PDF checks](evidence/enhancements/pdf-verification.json) and [handoff checks](evidence/enhancements/handoff-checks.json) retain the final evidence.
