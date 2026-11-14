# Planning wording implementation — 2026-11-15

## Result

Macro now produces readable, tooth-specific descriptive planning paragraphs under **Planning comments** in the normal UI. The identical paragraphs appear in PDF and TXT exports. Provider names, transmission details, token counts and internal diagnostics are absent from the normal report view. Source cells remain available in a closed Source values disclosure and complete technical exports.

Previously, the interactive endpoint asked Groq to choose four short fixed phrases; it never generated tooth-wise prose. The new Macro path passes minimized structured movement records to Groq and validates the resulting narrative arrangement. Micro/Nano retain their existing constant-phrase and supplied-example behavior; no AI treatment choices were added.

## Facts, safeguards and transmission

The user explicitly authorized sharing movement data for wording. Macro sends normalized movement families, exact numeric strings, units, supplied direction labels and missing/zero states with temporary per-request tooth references. Raw tables, arbitrary/free-text labels, original tooth identifiers, patient/context notes and input hashes are excluded. Credentials remain server-only.

The provider writes connective prose around complete fact references. Every source cell must occur exactly once for its correct tooth. All complete movement clauses, labels, exact values, units, directions and unknown/zero states are inserted locally after validation. Unrecognized references, altered/extra numbers, missing/duplicate/cross-tooth facts, unsupported clinical advice, invented risk/severity or achieved-movement claims reject the whole generated batch. Model-authored vocabulary is limited to connective descriptive language; clinical facts and recommendations cannot be introduced through that channel.

Unverified anatomy and movement conventions remain unverified. All 96 existing rules and clinical restrictions remain unchanged. No diagnosis, attachment indication, staging, force or anchorage recommendation is invented. Missing values are never replaced by zero. Micro/Nano illustrations remain supplied/table-order simulations.

If generation is unavailable or rejected, the complete source still receives readable standard paragraphs. The UI identifies standard wording rather than mislabeling it AI-generated. No automatic request, retry, extra view-switch call or export-time provider call was introduced.

## Configuration

The existing backend `GROQ_API_KEY` is sufficient for this interactive Macro path. The parser's independent key and development-only recovery gates are unchanged. Production does not need development demo routes enabled.

Macro uses its own 25-second default provider timeout, optionally configured with `FINOVA_PLANNING_TIMEOUT_SECONDS` (1–45 seconds), 4,096 completion-token allowance and no automatic retry. The browser timeout is 55 seconds to allow a complete response/fallback. Legacy rule-report and parser timeouts remain unchanged. The optional setting is documented in `.env.example`; no Render variables or production service settings were modified.

## Verification

- Full backend suite: **1,049 passed**, one existing Starlette/httpx deprecation warning.
- Full frontend suite: **252 passed**, followed by **33 focused UI/PDF tests passed**, including two additional acceptance tests.
- Browser regression: **10 passed** across desktop and 375-pixel phone views, exercising rows, columns, Markdown and 112-cell tables in all three modules, unsupported input, exact TXT/copy, PDF attachments, stale-output invalidation and absence of provider/transmission details.
- Approved-wording browser acceptance: **2 passed**, desktop and phone. These use the saved actual successful synthetic response to verify that its tooth-specific paragraphs appear in the UI and exact PDF attachments without additional live calls.
- Production build: **passed** (TypeScript and Vite). Existing large-bundle advisory remains.
- `git diff --check`: passed. AST-only `graphify update .` completed; no LLM graph extraction.

The accepted four-page PDF was rendered and visually reviewed on all four pages. Comments are readable and not clipped, and all 16 tooth entries remain visible. Its embedded TXT and validated JSON match the source report exactly. Legacy saved report contracts remain readable alongside the new `GROUNDED_PLANNING_WORDING_V1` provenance.

## Live synthetic evidence

The supplied synthetic Markdown table was used: **16 tooth rows, 112 measurement positions, 103 numeric values, nine missing values and six explicit zeros**. An initial live request returned a bounded HTTP-error fallback; a separate explicit diagnostic retry returned HTTP 200 and **16 of 16 accepted comments**, with one provider attempt for that successful review. The successful provider response took approximately **3.85 seconds**; this is provider-request timing, not a browser end-to-end latency measurement.

Evidence is under `evidence/planning-wording/`:

- `user-synthetic-live-report.json` and `.txt`: actual validated output and complete source evidence.
- `planning-comments-approved.pdf`: four-page app-exported PDF using the accepted comments.
- `planning-comments-desktop.png` / `planning-comments-mobile.png`: main-UI screenshots.

No real patient data were used in validation. The browser tests use mocked transport for the saved approved response; they make no additional live Groq calls. No deployment, commit or push was performed. Both backend and frontend must be redeployed before the deployed URL can show this implementation.
