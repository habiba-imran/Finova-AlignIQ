# Finova AlignIQ — final module reports

15 November 2026. This report supersedes the earlier movement-only Micro/Nano wording descriptions.

## Implemented behavior

| Module | Main comments | Required source information |
| --- | --- | --- |
| Macro | Tooth-wise programmed movement descriptions | Actual parsed TMT values, directions, units and missing/zero states |
| Micro | Supplied attachment choices; design/dimensions; placement; independent-assessment limits | Optional attachment records tied to existing parsed tooth rows |
| Nano | Supplied stages; explicit movement allocations; supplied anchorage notes; independent-assessment limits | Optional stage IDs/order/durations, source movement references, separately supplied stage amounts and notes |

Micro and Nano no longer repeat Macro movement paragraphs as their main comments. Their source movements remain accessible in a disclosure and complete exports. A TMT alone does not establish an attachment indication or a treatment sequence: missing findings are explicitly unavailable. Supplied choices, dimensions, order and notes remain **supplied and unverified**. No clinical recommendations, attachment geometry, optimized sequence, force, timing or anchorage requirement is invented.

The fictional illustrative attachment/sequence section has been removed from the ordinary interactive UI, visible PDF and TXT. The response retains an empty `illustrations` field for compatibility. Existing fixed, evidence-controlled development demonstrations retain their server authorization; production development-route restrictions are unchanged.

## Wording and source preservation

- All three modules use the existing Groq integration. Only locally accepted provider output is labeled **AI-assisted wording**. A provider failure, quota limit or rejected output remains **Standard wording · AI-assisted wording unavailable**.
- Macro sends minimized movement facts and temporary references. Micro/Nano send closed section kinds/statuses and temporary references. Their supplied free-text designs, stage IDs, notes, tooth labels and geometry values are inserted locally; those free-text inputs are not sent to the provider.
- Immutable facts retain exact decimal strings, source units/directions and explicit unknown/zero states. Local validation prevents missing/cross-record references, altered values and additional clinical assertions. The existing repetition checks remain.
- One successful but rejected response can receive one correction within the original total timeout. No correction follows a provider error, rate limit or exhausted deadline. Completion reservations are bounded to the actual report size.
- Switching back to an unchanged module reuses its in-memory result. Edits invalidate the affected result; raw/context changes invalidate all results. No report is persisted in browser storage. Copy/TXT/PDF exports do not call Groq.

Supplementary inputs are optional, bounded and validated. Tooth/movement references must exist; stage IDs/orders must be unique; allocations must refer to the selected tooth and an existing stage; supplied amount units must match known source units. A stage amount starts blank and is never copied or divided from TMT values. Invalid entries produce concise, focused errors before a provider call where possible.

## PDF and UI

The visible PDF contains the same accepted comment paragraphs as the UI, module statuses, missing information and clinical restrictions. The exact complete UTF-8 `report.txt` and `validated-report.json` remain embedded attachments, including raw input, source spans, supplementary records and the complete 96-rule ledger. The bundled PDF worker/fonts remain local. Technical details and provider names stay out of normal report screens.

The prototype notice and unverified-source distinction remain visible. Partial parses with blocking issues are not described as completely successful. All 96 rules remain present, with all 27 clinical predicates disabled; no parser, clinical policy, vendor authorization or rule thresholds were redesigned.

## Verification record

| Check | Observed result |
| --- | --- |
| Complete backend suite | **1,074 passed** |
| Complete frontend suite | **266 passed** |
| Production TypeScript/build | **Passed**; existing PDF/font bundle-size advisory remains |
| Desktop/mobile browser regression | **104 passed** against the production bundle, including five new module/PDF cases at both widths, fixed-demo availability/errors and clinical safeguards |
| Five local PDF cases | **Passed**: all visible comments present; exact TXT/JSON attachments; all 12 pages rendered and visually inspected (Macro 4 pages; each Micro/Nano case 2 pages) |
| Real local Micro, supplied details | **4/4 AI comments accepted**, one attempt |
| Real local Nano, supplied details | **4/4 AI comments accepted**, one attempt |
| Real local large Macro | Reached Groq; first response required correction, then Groq returned a daily-quota rate limit. No false AI status was shown |
| Production Macro | **16/16 AI comments accepted**, one attempt, with the user's 16-tooth/112-position synthetic table |
| Production Micro/Nano | Distinct supplied-detail reports and PDFs passed; Groq returned `GROQ_RATE_LIMIT`. A spaced Micro recheck was also rate-limited. Production AI availability for these two modules is **not claimed** |
| Production PDFs | All three downloads passed: Macro **4 pages**, Micro **2 pages**, Nano **2 pages**; all eight pages rendered and visually inspected; exact TXT/JSON attachments and matching UI comments; zero export API/provider calls |
| Production layout | All three reports checked at **1440px and 375px**, without viewport overflow |

## Published revision and remaining external limit

Implementation commit `81b132d` was pushed to the existing `main` branch. Vercel served `/assets/index-CngGCJaA.js`, matching the verified local production bundle. After Render's rollout, the deployed capabilities endpoint returned HTTP 200 with revision `module-reviews-2026-11-15-v1`. No environment values, credentials, security controls or production development-route settings were changed.

The production checks used the user's supplied synthetic table: 16 tooth rows, 112 positions, 103 recorded numerical values and nine unknown/missing positions. They preserved all 96 rules and 27 disabled clinical predicates. Macro used actual accepted provider wording. Micro/Nano generated their correct purpose-specific standard reports while the provider was rate-limited; both separately passed real local AI checks with four accepted comments each. There is no evidence that another environment-variable change is required, and no unconditional provider-availability claim is made.

The persistent upstream rate limit is outside the report/PDF implementation. It must clear, or the configured account's capacity must be addressed, before Micro/Nano AI wording can be verified on production. The UI keeps the concise unavailable state, and **Re-run Review** permits a new explicit attempt later. No automatic rate-limit retry loop or key rotation was added.

Evidence is stored in `evidence/module-final/`, including `deployed/summary.json` and the initial `deployed/first-pass-summary.json`. `backend/scripts/verify_final_modules.py` generates offline fixtures and supports explicitly requested live synthetic checks. `frontend/scripts/verify-module-deployment.mjs --run-live` performs three bounded production synthetic reviews, desktop/mobile checks and downloads each PDF; optional `--module micro` limits a subsequent check to one module. `backend/scripts/verify_module_pdfs.py` verifies visible comments and exact attachments and renders all PDF pages with Poppler for visual review.

AI availability depends on the configured account's upstream quota and service availability. These engineering checks do not establish clinical validation, vendor compatibility or suitability for patient care.
