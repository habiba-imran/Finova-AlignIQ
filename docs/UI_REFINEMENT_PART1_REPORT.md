# Finova AlignIQ — UI Refinement Part 1 of 3

**Professional layout, navigation and visual hierarchy**

14 November 2026 — frontend-only refinement. No backend, API contract, parser, clinical rule, Groq integration or report data model was changed.

## Inspection performed

- Reviewed the current React/Tailwind implementation in `frontend/src`, including `App.tsx`, all workspace components, shared styles and design tokens.
- Read the Phase 6B, Phase 7 and Phase 8 implementation reports to preserve module behaviour, fixed demonstrations, safety wording and export guarantees.
- Reviewed the existing Vitest and Playwright suites. No separate frontend Phase 9 UI audit artifact was found; existing Phase 9 backend audit files and unrelated local work were left untouched.
- Captured and inspected the interface at 1440, 1024, 768, 672 and 375 px before and after the changes.

## Files changed

| File | Change |
| --- | --- |
| `frontend/src/App.tsx` | Context-sensitive page header, compact module tabs, four-area page structure, workflow progress logic, consolidated safety/processing copy, unified buttons and consistent max-width shell. |
| `frontend/src/styles.css` | Refined component classes for panels, section headings, module tabs, workflow steps, buttons and form controls. Reduced panel-heading height and standardized radii, borders and spacing. |
| `frontend/tailwind.config.ts` | Added restrained supporting tokens (`brand-deep`, `brand-line`, danger tones), a subtle panel shadow, slightly stronger muted text and a 1200 px-friendly neutral canvas. Existing teal identity retained. |
| `frontend/src/components/ParserStatus.tsx` | Applied the shared panel typography and heading hierarchy. No detection or clarification logic changed. |
| `frontend/src/components/ParseResults.tsx` | Applied the shared panel header/heading system. Parser diagnostics content and tables were not redesigned. |
| `frontend/src/components/PlanningWorkspace.tsx` | Grouped heading treatment, unified primary action styling, labelled the export area as step 04 and aligned export button styles. Review content, selection and exports unchanged. |
| `frontend/src/components/AttachmentWorkspace.tsx` | Same heading/action/export-area treatment. Attachment table and review content unchanged. |
| `frontend/src/components/SequencingWorkspace.tsx` | Same heading/action/export-area treatment. Sequencing sections and evidence content unchanged. |
| `frontend/src/Workflow.test.tsx` | **New** unit regression for workflow progression and module-switch invalidation. |
| `frontend/e2e/responsive.spec.ts` | **New** browser regression for contextual headings, compact tabs, five viewport widths, overflow checks and workflow states. |

Generated `test-results/` screenshots and the production `dist/` build are local verification artifacts; no test was altered to hide a failure.

## Header and context

The generic headline “A clearer view of the plan.” is removed. The page header now derives from the selected module:

| Module | Heading | Supporting text |
| --- | --- | --- |
| Macro | **Planning Assistant** | Review programmed movements and prepare structured draft comments. |
| Micro | **Attachment Review** | Inspect tooth-wise attachment information and supporting evidence. |
| Nano | **Sequencing Review** | Review sequencing information, segment notes and anchorage context. |

A small module kicker (`Macro · Planning`, etc.) identifies the module family. The app title is also updated in the document title. The app bar keeps the Finova identity, a compact synthetic-prototype badge, no-persistence status and the teal palette.

## Module navigation

The three large purpose cards were replaced with a compact segmented tab control:

- **MACRO / Planning**
- **MICRO / Attachments**
- **NANO / Sequencing**

Each tab keeps an explicit uppercase module code for existing accessible-name and keyboard behaviour, with the review purpose below it. The active tab uses a soft teal background, restrained teal border and teal text. Inactive tabs stay neutral with a subtle hover surface.

Navigation remains real buttons inside `nav aria-label="Review purpose"` with `aria-pressed`. Keyboard activation and focus visibility are preserved. The existing invalidation path is unchanged: switching modules aborts pending work and clears parse results, module drafts, demo authority and export availability while retaining raw text. A visible caption states that review modules are planning contexts, not aligner stages.

## Page structure and hierarchy

The interface is now organized around four labelled areas:

1. **01 Input** — compact demonstration action, paste/preview panels and parse controls.
2. **02 Movement inspection** — automatic detection and structured lexical preview, both still conditionally rendered after parsing.
3. **03 Review results** — the selected module’s review workspace.
4. **04 Export** — labelled inside each workspace above the copy/download controls.

Area numbers are presentation-only; they are not aligner stages. Section headings use a restrained 17–18 px scale. The main content is capped at 1200 px, with 20 px mobile and 32 px desktop gutters.

## Workflow progress indicator

The old indicator marked a step active from module selection alone. It now derives directly from actual workflow evidence:

- **Input** is active until synthetic text exists and the synthetic-data confirmation is checked.
- **Inspection** becomes active after input readiness and remains active until a valid parse result exists.
- **Planning / Attachment / Sequencing review** becomes active after parsing and remains active until the workspace reports a completed draft.
- **Export** becomes active only when the module review has completed. It reads “Available”; it is not marked as a completed export.

Completed steps use a teal check and explicit screen-reader completion text. The active step alone receives `aria-current="step"` and the soft teal surface. Selecting another module does not advance progress; it invalidates the prior result and returns the user to the inspection task.

The status captions also distinguish “Add synthetic text”, “Confirm synthetic data”, “Parse text”, “Retry parse”, “Run review” and “After review”.

## Typography and visual system

- Page title: 28 px mobile / 32 px desktop.
- Section heading: 17–18 px.
- Panel heading: 17 px.
- Body copy: 14–15 px.
- Supporting captions: 12–13 px; decorative module codes/area numbers may use 11 px.
- Technical identifiers continue to use the existing Cascadia Code/Consolas monospace stack.
- Existing Segoe UI/system font stack retained. No font package added.

Panels use consistent 12 px radii, one-pixel neutral borders, reduced 56 px minimum header height and a faint panel shadow. Primary actions use teal; secondary actions use white/neutral surfaces; clear is a restrained dark-red outline; amber is reserved for limitations, unverified status and withheld clinical information. No gradients or decorative oversized headings were introduced.

## Reduced visual noise with safety preserved

- The prototype notice is now a compact two-line amber banner that keeps the visible statement **“Prototype — not for clinical use”**, the synthetic-only instruction and the structure-versus-clinical-verification limitation.
- The former large demonstration banner was replaced by a compact demonstration action and one-line scope note. Fixed conventions remain available in expandable details.
- The “Choose a review purpose” heading and long explanatory paragraph were replaced by the tab control and a one-line caption.
- The long parse-processing paragraph was reduced to the visible privacy summary (“No input is saved”), with Groq recovery/processing detail moved into an expandable disclosure.
- Redundant marketing-style hero copy was removed. Verification status, parser warnings, clinical withholding, DRAFT status and all export limitations remain unchanged.
- No critical warning was removed from results or exports, and no unverified input is presented as approved.

## Buttons and controls

A shared button system now covers:

- **Primary** — Parse Table and each module’s explicit run action.
- **Secondary** — example loaders, export copy/download and neutral navigation actions.
- **Accent** — fixed demonstration and selected-comment copy actions.
- **Destructive/clear** — the Clear input action.
- **Disabled** — neutral surface, muted text and reduced opacity.
- **Tabs and disclosures** — consistent focus rings, hover states and 44 px touch targets.

Existing button names and action handlers were preserved so behavioural tests continue to target the same operations.

## Preserved interactions

- All module requests, abort controllers, revision checks, timeouts and error/retry handling are unchanged.
- Demo loading, demo authority boundaries, parse confirmation, context claims and synthetic fixture handling are unchanged.
- Module switching still clears results and exports while retaining raw text.
- Review selection, copy, download, export previews and provenance disclosures are unchanged.
- Parser diagnostics, issue lists, result tables, rule ledgers, DRAFT wording and clinical withholding are unchanged in content.
- Existing accessible names, skip link, nav label, focus movement and keyboard operation are intact.

## Responsive behaviour

Verified with Playwright at 1440, 1024, 768, 672 and 375 px:

- No horizontal page overflow at any tested width.
- Module tabs remain a three-column control with 44 px minimum height and 11 px/13 px labels; no tab clips or becomes unreadable at 375 px.
- Input and preview panels remain side by side at 1024+ and stack at 768 px and below, avoiding squeezed textareas and previews.
- The workflow stepper is four columns on desktop, two columns on laptop/tablet/mobile, and keeps readable 13 px titles plus 12 px status captions.
- The mobile app bar uses a shorter “Prototype” badge so the full Finova AlignIQ wordmark remains visible.
- Export controls wrap instead of overflowing; result tables retain their existing local scroll/stacking behaviour.
- Section headings, demonstration content and export labels wrap cleanly at 672 px and 375 px.

## Test results

| Check | Result |
| --- | --- |
| `npm test` (Vitest) | **10 files, 182 tests passed** |
| `npm run build` (`tsc --noEmit` + Vite) | **Passed** |
| `npx playwright test` (desktop 1440, laptop 1024, tablet 768, mobile 375) | **92 tests passed** |
| New responsive browser checks | **Passed**, including the additional 672 px width and no-overflow assertions |

No failing or skipped checks. No existing test assertion was weakened, and no safety/behavioural assertion was removed.

The new `Workflow.test.tsx` verifies that typing alone does not advance progress, confirmation moves to inspection, parsing moves to the module review, and switching modules invalidates the parse without falsely marking review complete. The new `responsive.spec.ts` verifies contextual headings, tab sizing/legibility, no overflow at all five widths, and the input → inspection → review → export progress states.

## Intentionally deferred to Part 2

- Visual refinement of parser diagnostics, warning lists and clarification panels.
- Module-specific result table/card redesign, including denser evidence presentation and mobile table treatment.
- Further consolidation of module-specific clinical limitation copy inside Planning, Attachment and Sequencing results.
- Any motion or transition polish beyond the existing reduced-motion-safe colour transitions. No animation library was added.

Part 1 stops here.
