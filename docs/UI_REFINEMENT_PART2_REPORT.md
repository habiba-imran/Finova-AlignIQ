# Finova AlignIQ — UI Refinement Part 2 of 3

**Clean parser presentation, progressive diagnostics and professional result reports**

14 November 2026 — frontend-only refinement. No backend service, parser algorithm, clinical calculation, rule predicate, semantic gate, Groq boundary, API contract or export byte was changed.

## Inspection performed

- Reviewed the Part 1 layout, all workspace components, parser result types, report schemas, existing Vitest suites and Playwright specs.
- Inspected the parser response fixtures to present real counts, statuses and evidence rather than invented summary values.
- Compared parser and result views before and after the changes at 1440, 1024, 768, 672 and 375 px.
- Preserved the existing distinction between structural parsing, source verification and clinical eligibility throughout.

## Files changed

| File | Change |
| --- | --- |
| `frontend/src/components/ReportPrimitives.tsx` | **New** shared presentation primitives: `ReportHeader`, `SummaryGrid`, `SummaryMetric`, `ReportSection`, `EvidenceDisclosure`, `ExportBar`. These carry presentation only; module schemas remain separate. |
| `frontend/src/components/ParserStatus.tsx` | Compact “Input assessment” with parse outcome, source-verification badges, actual tooth/measurement/missing/zero/issue clarification counts, visible blocking errors, and disclosures for parsing details and targeted clarification requirements. |
| `frontend/src/components/ParseResults.tsx` | Redesigned parsed-movement table with tooth token, movement label, original source cell, lexical value and unit, parse status and expandable row details. Added missing-versus-zero badges, source metadata disclosure, paged diagnostics, issue-clarification disclosures and full JSON. |
| `frontend/src/components/PlanningWorkspace.tsx` | Macro result now uses the shared report header, coverage summary, DRAFT status, dimension sections, withheld-assessment disclosure and consolidated export bar. Comment text, selection, copy, download and provenance are unchanged. |
| `frontend/src/components/AttachmentWorkspace.tsx` | Micro result now uses the shared report header and actual result-type counts. Tooth-indexed table gains explicit supplied/unknown/withheld states, mobile card stacking and row-level geometry/provenance disclosures. |
| `frontend/src/components/SequencingWorkspace.tsx` | Nano result now uses the shared report header, statement-count summary, six labelled region sections, stage-availability disclosure and consolidated export bar. All fictional/structural distinctions retained. |
| `frontend/src/App.tsx` | After a successful parse, the faithful raw preview collapses into a closed “Raw preview · original TMT text” disclosure and the editable input becomes full width. Parsed movements are the primary inspection view; the original text remains in the DOM and expandable. |
| `frontend/src/styles.css` | Added shared report, summary, movement-table, diagnostic-disclosure, export-bar, preview and mobile attachment-card styles. Removed vertical clipping from the attachment table on narrow screens. |
| `frontend/src/ParsePresentation.test.tsx` | **New** parser presentation regression tests: hidden raw preview, actual summary counts, visible blocking errors, expandable row evidence, explicit-zero versus missing values. |
| `frontend/src/ReportPresentation.test.tsx` | **New** shared report tests for Macro coverage/withheld sections, Micro result-type distinctions and Nano region/statement separation. |
| `frontend/e2e/presentation.spec.ts` | **New** browser presentation tests at four viewports: parser table/diagnostics/source disclosure, hidden raw preview, local table scrolling, Micro mobile cards and no page overflow. |

## Shared presentation primitives

`ReportPrimitives.tsx` now provides the common visual grammar used by Macro, Micro and Nano:

- **Report header** — module eyebrow, report title, DRAFT badges, explicit draft status and summary slot.
- **Summary grid/metrics** — consistent label, value and explanatory detail; notice tone for withheld or unavailable values.
- **Report section** — consistent section heading, description and optional action slot.
- **Evidence disclosure** — native `<details>` wrapper for provenance, rule IDs and source evidence.
- **Export bar** — step 04 treatment, description, actions and `role="status"` feedback.

The primitives do not merge clinical data models. Each module still renders its own schema, terminology, safety copy and export content.

## Parser presentation

### Input assessment

The former verbose detection block is now a compact outcome summary:

- Parse outcome and structure state remain explicit.
- Detected source, source-verification status and “not a clinical check” badges remain visible.
- Actual counts are derived from the parse response: tooth token positions, movement positions, missing values, explicit zeros, issues requiring attention and unresolved clarification fields.
- Blocking errors remain visible above the fold with code, message and source location.
- Numbering candidates and recovery notes remain visible.
- “Parsing details” and “Targeted clarification requirements” moved into native disclosures with all original content retained.

No count is inferred or fabricated, and no parser warning is removed.

### Parsed movement table

The movement table is now the primary inspection view:

| Column | Presentation |
| --- | --- |
| Tooth token | Original identifier in monospace plus identifier status. |
| Movement label | Original label plus recognized-label status. |
| Source cell | Original cell text, including explicit `(omitted cell)` and `(empty cell)` markers, plus line/column. |
| Lexical value & unit | Right-aligned signed decimal, unit, and magnitude at full source precision. |
| Parse status | Numeric status and field status badges; explicit zero and missing use distinct treatments. |
| Details | Expandable literal direction, semantic verification, clarification fields and measurement ID. |

Rows remain inside a labelled, keyboard-focusable scroll region with a sticky header. Pagination remains 25 positions per page. Missing values are never shown as zero and lexical precision is unchanged.

### Progressive diagnostics

Warnings, errors and informational issues remain in `Parsing warnings and errors`, with severity counts and a disclosure listing every issue. Long lists can be expanded 50 at a time. Unresolved fields remain in `Fields requiring clarification or verification`. Source evidence, parser metadata, candidate adapter and input SHA-256 remain available in a separate disclosure.

### Raw source

After a successful parse the raw preview is collapsed but not removed:

- The parsed table is promoted as the inspection view.
- “Raw preview · original TMT text” restores the exact original text with whitespace intact.
- Editable TMT input remains available above.
- The preview stays in the DOM, so existing tests and copy/inspection workflows continue to work.

## Module result presentation

### Macro — Planning

- Prominent DRAFT header with `DRAFT — Requires Orthodontist Review`, synthetic/unverified evidence badge and “Not approved” badge.
- Actual coverage summary: eligible, unavailable, authorized comments and withheld assessments.
- Sagittal, transverse and vertical sections retain their explanations and selectable comments.
- Withheld assessments remain in a separate notice section and keep the existing “Inspect withheld assessments” disclosure.
- Export bar keeps selection count, select-all/clear, copy-selected, copy-complete and TXT download behaviour.

### Micro — Attachment

- Prominent DRAFT header and actual counts for supplied candidates, alternatives, supplied no-attachment, unknown and withheld.
- The semantic table remains one table at every width. On screens below 1024 px each row stacks into a readable card with visible field labels.
- Candidate, alternative, supplied-none, unknown and withheld states remain visually and textually distinct.
- Each row retains “Details & provenance · row N” with supplied design, dimensions, placement, evidence references, safeguard findings and missing prerequisites.
- The earlier desktop-only height cap no longer clips tablet rows; wide desktop tables retain a generous local scroll area.

### Nano — Sequencing

- Prominent DRAFT header, synthetic demonstration notice and actual supplied/structural/unknown/stage-record counts.
- Stage availability remains an explicit notice section and never claims actual stage-bound movement data.
- All six regions retain dedicated sections: upper arch, lower arch, segments, right anchorage, left anchorage and unavailable assessments.
- Supplied fictional statements remain separate from structural metadata checks.
- Evidence disclosures retain stage windows, source references, movement scope, missing prerequisites and entry IDs.

## Safety, warnings and evidence preservation

- `Source verification: UNVERIFIED`, `DRAFT — Requires Orthodontist Review`, `Not approved`, `Synthetic · TEST_ONLY` and all existing source/semantic distinctions remain visible.
- Blocking parse errors remain visible; warnings and informational issues remain available in full.
- Withheld assessments remain separate from negative findings and are never hidden by the summary.
- Unknown and withheld attachment states are not presented as “no attachment”.
- Nano continues to state that actual stage movement data is unavailable.
- All clinical limitations, rule ledgers, provenance JSON and export previews remain in native disclosures.
- Export text, export button names, selection behaviour and clipboard/download actions are unchanged.

## Responsive behaviour

- Verified at 1440, 1024, 768, 672 and 375 px.
- No horizontal page overflow at any tested width.
- Parser table scrolls locally inside its labelled region rather than widening the page.
- Attachment rows become cards below 1024 px; the table fits its container at desktop widths without a forced minimum width.
- Macro dimension cards stack from three columns to one; summary metrics reflow from four to three to two columns.
- Nano region sections stack from two columns to one.
- Export actions wrap and retain 44 px minimum control height.
- Raw preview remains readable with wrapping long rows and local vertical scrolling.

## Test results

| Check | Result |
| --- | --- |
| Part 2 Vitest specs (`ParsePresentation`, `ReportPresentation`) | **6 tests passed** |
| Existing Vitest suite plus Part 2 specs | **Passed** |
| `npm run build` (`tsc --noEmit` + Vite) | **Passed** |
| New Playwright presentation scenarios | **8 passed** across desktop, laptop, tablet and mobile |
| Existing browser suite | **Passed** |
| Final combined suite after Part 3 | **13 Vitest files / 190 tests; 112 Playwright tests** |

The new browser test verifies the collapsed raw preview, visible parser summary, row-detail expansion, local table scrolling at 375 px, DRAFT/header presentation and Micro card stacking. No existing assertion was weakened and no safety or export assertion was removed.

## Intentionally deferred to Part 3

- Motion and interaction polish: tab and workflow transitions, result entrances, disclosure fades, button microinteractions and loading feedback.
- Final cross-module visual consistency and reduced-motion verification.
- Full cross-project regression, backend pytest and dependency/security checks.

Part 2 stops before Part 3.
