# Finova AlignIQ — clean UI final report

Session dates: 2026-11-14–2026-11-15 (Asia/Karachi). Project: `C:\Finova AlignIQ`.

## Scope

This task changed frontend presentation only. It did not edit backend parser, semantic admission, clinical predicates, rules, Groq integration, server authorization or report generation. No deployment, commit or push command was performed by this task.

The checkout already contained frontend changes when work began. During this session the Git reflog advanced externally to `642a3b4` (`Modify UI`), capturing some work already in progress. That commit was not created by this task; its contents were preserved. Later, concurrent changes appeared in `backend/app/main.py`, `backend/app/api/interactive.py` and `backend/app/interactive/`. This task left those files untouched and repeated backend verification against the current checkout. Those separate interactive-backend additions are outside the UI implementation scope and are not audited here. The current-tree backend suite is therefore not completely green; see the exact failure below.

## Workspace changes

- The normal workspace follows paste → formatted table → explicit review → results → export. Macro, Micro and Nano retain distinct modules, teal styling, keyboard focus, loading states and reduced-motion support.
- One editable original-text field remains visible. The duplicate raw preview is absent from the normal workspace.
- The formatted table uses actual validated parser measurements, source headings and tooth rows. Values retain precision and original direction tokens. Missing, explicit zero, ambiguous, invalid, unsupported and unknown-unit states remain distinct. Missing-cell unit omissions do not create duplicate columns. Separate source headings do not collapse solely because they name the same movement axis. All tooth rows remain available.
- Parsing feedback groups repeated issues into concise messages. Blocking error categories remain visible, including layout, row alignment, invalid numbers, conflicting values, decimal conventions and conflicting units. Vendor identity and movement conventions remain unverified for ordinary input.
- One visible top-level prototype / not-for-clinical-use notice remains. Reports retain DRAFT status and independent clinician-review restrictions. Checked fictional demonstrations are explicitly distinguished from unverified ordinary input; demonstration verification is not clinical or vendor validation.
- Normal screens omit raw JSON, complete rule ledgers, internal rule IDs, hashes, provider names, attempts/tokens and recovery configuration instructions. Complete technical evidence remains in exports. The explicit internal view at `/?diagnostics=1` retains the existing lexical/legacy diagnostics and related regression coverage; it does not authorize any backend route or promote input evidence.

## Demonstration behavior

The planning demo uses the existing fixed server input and draft endpoints. Server gates still require both `FINOVA_ENVIRONMENT=development` and `FINOVA_PLANNING_DEMO_ENABLED=true`. Micro/Nano retain their existing equivalent server flags. No production route was enabled and no authorization check was bypassed.

A disabled demo (404) or unavailable fixed artifact (503) disables the corresponding load button for the session and gives a short unavailable message. Network/invalid-response failures retain an explicit retry opportunity. Original text is preserved on failed loading. Editing text, changing context or switching modules discards demonstration authority and stale results.

The local browser harness runs a separate development backend with the existing three demo flags enabled and external wording/recovery disabled. All three fixed demos were exercised through their real local HTTP endpoints.

## Macro wording and exports

- **A. Standard Report — Template-Based:** displays the deterministic server report and eligible findings.
- **B. AI-Assisted Report — Enhanced Wording:** displays only eligible comments returned with approved AI provenance and accepted wording validation. It does not relabel template fallback as AI-generated.
- If the original response contains only template wording, it supplies the standard view and the enhanced view states unavailable. No comparison request is sent.
- If approved AI wording is returned, one additional `TEMPLATES` request retrieves the genuine deterministic comparison. This request makes no wording-provider call. The frontend requires the same complete engine review for comparison. No local clinical text is synthesized to stand in for a missing standard report.
- Partial AI availability is explicit: only approved enhanced comments are displayed in the enhanced view; complete enhanced-report exports retain and identify any template fallback. If the template comparison fails, the valid enhanced result stays available and the standard view reports unavailable.
- Switching wording views makes no HTTP/provider requests and clears comment selections. Copy, Export TXT and Export PDF use the active returned report. Source values, complete provenance, withheld findings and limitations remain in exports.
- Micro and Nano retain supplied fictional decisions/notes and deterministic wording. No AI variants, attachments, force choices or sequencing strategies were invented.
- The PDF generation pipeline was preserved: concise human-readable PDFs retain their complete technical TXT/JSON attachments. Export tests check exact complete report content and that exporting adds no HTTP calls.

## Verification

| Check | Result |
| --- | --- |
| Backend: `.\.venv\Scripts\python.exe -m pytest -q` in `backend` | **Initial baseline: 1,006 passed. Current checkout rerun: 1,005 passed, 1 failed** because a concurrent backend addition introduced `/api/v1/interactive/review`, which the existing authorized-route allowlist rejects. One existing Starlette/httpx deprecation warning. |
| Frontend: `.\node_modules\.bin\vitest.cmd run --maxWorkers=2 --reporter=dot` in `frontend` | **230 passed across 20 files** |
| Production: `npm run build` in `frontend` | **Passed** (TypeScript and Vite); existing large-chunk advisory remains |
| Browser: production-bundle Playwright final configuration | 175 passed / 5 stale-selector failures in the full run; corrected rerun passed 4 widths, then the concurrently replaced main workspace failed the compact-width case. Final acceptance is blocked by workspace drift. |
| `graphify update .` | Completed, AST-only: 1,652 nodes / 5,109 edges / 90 communities; no LLM call |
| `git diff --check` | Passed |

Frontend regressions cover original-text fidelity, inert markup, validation boundaries, request cancellation/timeouts, stale-result invalidation, demonstration authority, supplied Micro/Nano behavior, exact TXT/copy exports and PDF evidence attachments. New clean-UI coverage adds absent normal-screen diagnostics, unavailable demos, genuine template/approved-AI separation, mixed fallback, comparison failure, comparison cancellation, conflicting/unknown units and missing-cell column alignment.

The browser configuration targets 1440, 1024, 768, 672 and 375 pixel widths, plus existing landscape and reduced-motion checks. Browser tests initially encountered sandbox localhost `EACCES`; they were rerun with local networking permitted. Test servers bind to loopback and are owned by the regression harness.

## Validation limits

No live Groq request was made. Approved enhanced-wording paths were tested using simulated approved synthetic responses and existing backend mocked-provider tests. Real local demonstration tests intentionally used template output. These checks establish UI presentation and existing contract behavior, not clinical validity, released vendor semantics, caller/patient outcomes or live provider availability.

## Concurrent backend verification failure

`backend/tests/test_health.py::test_only_authorized_routes_exist` fails because the current OpenAPI path set contains the additional `/api/v1/interactive/review` route. The concurrent diff adds an interactive-router import and registration in `backend/app/main.py`; this UI task did not make those edits. The earlier unchanged-backend run passed all 1,006 tests. The later current-checkout rerun passed 1,005 and failed this one route-contract assertion. No backend code or safety test was reverted, weakened or changed to hide the failure.

## Final browser evidence

The full production-bundle browser run completed 180 cases: 175 passed and five copies of one outdated Copy-button selector failed. That selector was corrected to use an exact accessible name. The explicit five-width rerun then passed desktop, laptop, tablet and mobile. Its compact-width case failed because another task replaced the main workflow with `InteractiveWorkspace` and rebuilt the shared `frontend/dist` during the run; the expected Wording preference selector was no longer present.

The current `App.tsx` now places the clean Macro/Micro/Nano workspaces behind diagnostics and mounts the concurrent interactive workspace on normal screens. It also changes module-switch invalidation and the top-level notice. Concurrent edits additionally affect `frontend/src/pdf/presentation.ts`, `frontend/src/pdf/reportPdf.ts`, a new interactive frontend API/component and demo documentation. This task did not make those changes. The earlier 230-test frontend result and passing build apply to the tested clean-UI source/bundle before those later concurrent changes; they do not validate the current combined tree.

No green final acceptance is claimed for the combined checkout. A reviewable clean-UI App candidate is saved at `evidence/clean-ui-final/App.clean-ui.tsx`; it is not installed over the concurrent integration. The prior PDF sources are preserved alongside it as `presentation.clean-ui.ts` and `reportPdf.clean-ui.ts`. These are review snapshots, not a separately runnable checkout. Choosing which main workflow should take priority is required before further integration or a reliable final verification run.

Reviewed screenshots are saved in `evidence/clean-ui-final/`: `macro-1440.png`, `micro-1440.png`, `nano-1440.png`, `macro-375.png`, `micro-375.png`, `nano-375.png`. The original browser failure ID summary is preserved as `browser-full-run.json`.
