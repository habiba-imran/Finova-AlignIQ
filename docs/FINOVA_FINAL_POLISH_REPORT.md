# Finova AlignIQ — final presentation polish

14 November 2026, Asia/Karachi. **Academic prototype — DRAFT, not clinical advice.**

This pass implements presentation changes only. The [enhancements report](FINOVA_FINAL_ENHANCEMENTS_REPORT.md), current UI, PDF renderer and report contracts were inspected first. Existing uncommitted enhancement work was preserved. Historical reports retain their original snapshots; this report supersedes their PDF presentation and test totals.

## Concise, auditable PDFs

The PDF now presents a review rather than printing the complete technical transcript:

1. Finova identity, module, full report ID, UTC export date, input hash and DRAFT status.
2. Executive summary showing TEST_ONLY or UNVERIFIED status, important supplied/descriptive results, unavailable counts and essential restrictions.
3. Module results: Macro dimensions/Other, Micro tooth-wise statuses/options/alternatives, and Nano upper/lower/segment/anchorage notes. Precise source values remain in readable tables with original labels, suffixes, scalar strings and source identifiers.
4. Unknown/withheld/disabled results, original clinical limitations, and all distinct missing requirements relevant to the displayed results.
5. Concise source/evidence keys, plus repeating identity/DRAFT/page-number footers.

The main pages exclude the 96-rule ledger, raw JSON and repeated component metadata. All original clinical limitations are retained verbatim, with exact duplicates shown once. Macro's 56 unavailable comments are grouped only when their outcome prose, evaluation statuses and evidence status match. Every original comment is still covered by explicit `C<n>` references/ranges; all distinct missing requirements and withholding reasons remain visible. No unavailable result becomes normal or approved.

Reference keys identify exact attachment records: `C<n>` → `/report/comments[n-1]` for Macro, `A<n>` → `/entries[n-1]` for Micro, `N<n>` → `/entries[n-1]` for Nano. The standalone descriptive report uses `/comments[n-1]`. These records retain full evidence/finding/measurement IDs and source spans. Main measurement tables also retain exact measurement identifiers and source coordinates where supplied. The reference guide explains the mapping and the existing TXT export.

The exact original UTF-8 **`report.txt`** and complete **`validated-report.json`** remain embedded. They are unchanged, not condensed, and include the complete technical audit. Normal copy, selected copy and TXT export behavior is unchanged. PDFs still use existing runtime validators, local bundled fonts and the cancellable inline worker; no network, provider call or persistence was added.

Short status/result paragraphs now stay together. Tables repeat headers on continuation pages; oversized rows continue with short identity/status context repeated when it fits. There is **no artificial page cap** and no text truncation.

| Fixed demonstration | Previous PDF | Current PDF |
| --- | ---: | ---: |
| Macro | 43 pages | **4 pages** |
| Micro | 28 pages | **3 pages** |
| Nano | 26 pages | **5 pages** |
| Ordinary unverified Micro | 23 pages | **3 pages** |
| Deliberately long visible-result stress case | Different previous stress input | **18 pages**, complete visible result and attachments |

These are measured fixture outputs, not imposed limits. Nano retains every original lexical position, including missing cells, and a separate source-reference section. The stress case includes an oversized explanation with long unbroken identifiers; independent extraction verifies its full explanation column and final sentinel across continuation pages. Technical-only diagnostic filler remains exact in the attachments without inflating the main pages.

Implementation: [presentation model](frontend/src/pdf/presentation.ts), [renderer](frontend/src/pdf/reportPdf.ts). No clinical ranking, threshold, treatment suggestion, source-axis conversion or numerical rounding is introduced. Existing computed coverage facts are displayed as supplied. Original JSON/TXT always remain the complete audit record.

## Minor UI refinements

- Shared report metrics use equal-height cards and a single aligned desktop row sized to the actual metric count. Tablet/mobile layouts retain readable two-column metrics.
- All three modules share a restrained “Review not started” state. It triggers no request or review automatically.
- Full-report actions appear in the same **copy → TXT → PDF** order. Macro's selection controls/selected-copy action remain together above them. Mobile export actions have consistent full-width touch targets.
- Input uses a slightly larger monospace size, deliberate tab stops and calm background. Table row spacing and attachment line height improve scanning; original characters are unchanged.
- Report section typography is more consistent. The extra Macro wording explanation moved into its existing disclosure; wording/provider status remains visible. Evidence, original limitations, provenance and the 96-rule ledger remain accessible through the existing expandable sections.
- Existing motion tokens and OpenCode transitions are preserved. Disclosure border feedback and non-shrinking button icons are small additions; native keyboard/focus behavior and reduced-motion overrides remain intact.

No navigation, component architecture, clinical text-generation behavior, parser or request lifecycle was redesigned. No new dependency was added.

## Visual evidence

All normal demo PDF pages were rendered and inspected for readable text/tables, precise values, missing/withheld labels, synthetic origin, embedded arrows, page breaks, repeated headers and footer separation. A preliminary browser run was stopped after visual review found an orphaned PDF result label; short-paragraph pagination was corrected and the final suite rerun without timeout or retry changes.

Representative saved samples:

- PDF first pages: [Macro](evidence/polish/screenshots/pdf-macro-page1.png), [Micro](evidence/polish/screenshots/pdf-micro-page1.png), [Nano](evidence/polish/screenshots/pdf-nano-page1.png).
- Report hierarchy and metric alignment: [desktop](evidence/polish/screenshots/review-headers-desktop.png), [mobile](evidence/polish/screenshots/review-headers-mobile.png).
- Consistent export controls: [1440](evidence/polish/screenshots/exports-desktop.png), [1024](evidence/polish/screenshots/exports-laptop.png), [768](evidence/polish/screenshots/exports-tablet.png), [672](evidence/polish/screenshots/exports-compact.png), [375](evidence/polish/screenshots/exports-mobile.png).

These are synthetic-demo screenshots. Overview sheets crop report headers/export regions for comparison; complete journeys and source renders remain local ignored QA artifacts. No publisher figure or patient capture was used in the website.

| Width | Acceptance observations |
| --- | --- |
| 1440 | Balanced report headers and metrics; clear results/table hierarchy; evidence disclosures and copy/TXT/PDF order retained. |
| 1024 | Metrics remain aligned; long labels wrap within cards; export controls fit without page overflow. |
| 768 | Two-column metrics, stacked intake, tooth cards and wrapped result sections remain readable. |
| 672 | Compact workflow/header layout retains source inspection, evidence controls and all export actions. |
| 375 | Full-width export buttons, readable input, two-column metrics and stacked attachment cards; no page-level overflow. Wide lexical tables intentionally scroll locally. |

## Verification

| Check | Actual result |
| --- | --- |
| Complete backend | **1,006 passed**, 45.40 seconds; existing upstream Starlette/httpx deprecation warning only. |
| Complete frontend | **214 passed / 17 files**, 70.08 seconds, two workers. Previous 208 plus six PDF-presentation cases. |
| Complete Chromium suite / built bundle / real API | **165 passed in 12.1 minutes**, no failures, skips or retries. Previous 160 plus one cross-module polish scenario at each of five widths. |
| TypeScript/build | **Passed**, 1,918 main modules, 14.87 seconds. Existing bundle-size warning retained: JS 2,321.31 kB / 989.31 kB gzip, CSS 38.33 kB. |
| Independent PDF verification | **Passed**: exact complete TXT/JSON attachments; all displayed statement/warning/missing-requirement/source checks; all-page headers/footers; full ledger excluded from visible pages; long visible text preserved without a page cap. |
| Protected implementation | **99 files unchanged** against the start-of-polish snapshot: backend/parser/rules/Groq/semantic and vendor gates, frontend API validators and original public TMT references. |
| API schemas | **32 regenerated identically**. |
| Public reference regression | **196/196 exact positions and recognized labels**, source agreement remains 195/196 with the separate known correction; semantic authorization remains **0/196**, provider calls/releases zero. No parser changes. |
| Vendor verifier | **Exit 2, NO_AUTHENTIC_ORACLES** — expected open release gate, not a compatibility pass. |
| Dependency checks | `pip check` and npm resolution passed; npm audit **0 vulnerabilities**; pinned Python requirements **no known vulnerabilities** at audit time. Existing unhashed-requirements advisory remains. |
| Graphify | AST update passed: **1,504 nodes / 4,851 edges**; no semantic document indexing or provider call. |
| Whitespace, links and key-pattern checks | Final handoff record supplied under `evidence/polish/handoff-checks.json`; no source/bundle key-pattern match, whitespace error or broken current handoff link. This is not exhaustive secret detection or remote-link uptime certification. |

Tests intentionally validate the new concise contract instead of requiring every technical TXT line to appear on the main pages. Exact attachment equality, validation/refusal, all clinical limitations, missing requirements, unknown/withheld states, source associations, precise values, stale cancellation, request restrictions and all 96 rule IDs remain asserted. A technical-only unsupported glyph is preserved in UTF-8 attachments; an unsupported glyph in visible results still refuses PDF output rather than corrupting it.

Evidence: [PDF verification](evidence/polish/pdf-verification.json), [protected-source/schema/gate checks](evidence/polish/integrity-checks.json), [reference benchmark](evidence/polish/public-reference-evaluation.json), [final verification summary](evidence/polish/verification-summary.json) and [handoff checks](evidence/polish/handoff-checks.json). Complete run logs are retained under `evidence/polish/`.

## Reproduction and limits

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
Set-Location 'C:\Finova AlignIQ\frontend'
npm test -- --maxWorkers=2
npm run build
npx playwright test --config playwright.final.config.ts --output ../evidence/polish/browser-results
npm audit
```

Load the existing dedicated synthetic examples, run each module and choose Export PDF. Inspect status, exact values, unknown/withheld results, source keys and limitations, then extract the attachments with a PDF reader that exposes embedded files. Copy/TXT remain beside PDF. Editing input/purpose/draft still invalidates results and cancels pending PDF work.

PDF font coverage remains bounded; PDFs are not certified PDF/A or tagged-accessible documents. Local Blob workers/downloads must be allowed. The UI is regression- and keyboard-tested, not independently certified for every assistive technology. Clinical approval, authentic vendor semantics and production release remain absent. These boundaries are unchanged.

**Presentation polish is complete and final acceptance passes.** No parser, backend clinical logic, Groq integration, rule engine, authorization safeguard, patient processing or dependency change was introduced. No commit, push or deployment is performed. The work stops here.
