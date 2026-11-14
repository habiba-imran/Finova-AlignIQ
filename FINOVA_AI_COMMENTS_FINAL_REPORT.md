# Finova AlignIQ — AI comments across Macro, Micro and Nano

Date: 15 November 2026. Local implementation only; no deployment, commit or push.

## Result

The normal planning, attachment and sequencing reports now use the same grounded narrative composer. Micro and Nano no longer call a four-label phrase selector while displaying unchanged local value lists as AI wording. Each module receives actual tooth-wise provider prose derived from its parsed movement facts. The UI and PDF use the same `observations[].text`; the complete TXT and embedded JSON retain those paragraphs and all technical evidence.

The main report uses **Planning comments**, **Attachment review comments** or **Sequencing review comments**. Source cells remain available in collapsed per-tooth details. Copy, Export TXT and Export PDF remain visible. Provider names, transmission details, tokens and diagnostics are absent from normal results. Fallback says **Standard wording · AI-assisted wording unavailable** and is never presented as accepted AI output.

## Repetition correction and factual boundaries

The previous Macro prompt supplied a single introductory formula and mostly allowed its repetition. The new prompt requests short paragraphs with different openings and sentence groupings, with no single worked paragraph to imitate. Validation rejects batches with insufficient opening variety for differing source profiles. It does not manufacture variation by rotating local prefixes.

Complete fact clauses are checked individually, then restored from local source facts. Every source movement stays associated with its tooth; signs, decimal strings, units, supplied direction labels, missing entries and explicit zeros are retained. Numeric changes, omitted/duplicated/cross-tooth facts, extra numerical claims, clinical judgments, recommendations and negation are rejected. A bounded neutral vocabulary permits editorial grammar only. Ordinary inflections such as `comprise` and `featuring` were added after observing unnecessarily rejected, otherwise fact-exact responses. An `unknown` summary is permitted only when every fact for that tooth is unknown.

This produces descriptive comments, not a clinically validated treatment plan. Micro attachment indication, geometry and placement, and Nano stage order, timing and anchorage remain unevaluated. Existing table-order illustrations stay separately labeled as fictional simulations. No attachment or sequence is invented from movement magnitude. All 96 rules, including the 27 disabled clinical predicates, remain intact; source semantics remain UNVERIFIED.

## Integration and privacy

An explicit review sends minimized parsed movement facts under temporary tooth references through the existing Groq client. Raw input, patient/context notes, original tooth identifiers, arbitrary labels and secrets are excluded. No provider call occurs on export or merely switching wording presentation. Request, response and prompt bounds, server-only credentials, timeout and safe deterministic fallback remain in place. The existing frontend prevents repeat review calls for an unchanged completed run. Legacy fixed-demo authorization, structural recovery and rule-report routes remain unchanged. No development route was enabled in production.

## Provider evidence

The user's synthetic upper-arch table has 16 tooth tokens and 112 measurement positions: 103 numerical and 9 missing. Real provider responses were captured using this table; no real patient data were used.

| Module | Accepted comments on current validation | Distinct first three words | Evidence |
| --- | ---: | ---: | --- |
| Macro | 16 | 14 | `evidence/unified-wording/approved-macro.json` |
| Micro | 16 | 10 | `evidence/unified-wording/approved-micro.json` |
| Nano | 16 | 13 | `evidence/unified-wording/approved-nano.json` |

Macro and Micro passed the final live request validation directly. Nano returned fact-exact prose but was initially rejected for neutral connective words. Its unchanged captured response was accepted by an offline replay after the grammar correction. All three captured responses were replayed through the current complete report-generation path. These are real provider responses, not hand-written expected paragraphs; the replay makes zero network calls. Capture hashes and the distinction are recorded in `approved-summary.json`. Earlier prompt experiments also encountered safe rejection and rate-limit fallback; this is not a claim of universal model acceptance or provider availability.

Reproduce the acceptance without credentials:

```powershell
.\backend\.venv\Scripts\python.exe backend/scripts/verify_interactive_wording_replay.py
```

## Verification

- Backend: **1,056 passed**. Fact preservation, all modules, omissions, duplicates, cross-tooth references, invented attachment/sequence plans, unknown-unit/value distinctions, unknown/zero states, repetitive output, provider failures, rule gates and schemas covered. Existing Starlette/httpx deprecation warning remains.
- Frontend: **258 passed**. All-module AI status, source details, inconsistent provenance refusal, exports, cancellation and stale-result handling covered. Stale tests were aligned with the existing diagnostics-only fixed-demo controls and disabled repeat-parse behavior; those application changes were preserved.
- TypeScript and production build: **passed**. Existing large bundled PDF/font chunk advisory remains.
- PDF verification: **48/48 comments visible** across the three exports. Macro has 4 pages, Micro 6 and Nano 6; all 16 pages rendered and visually inspected. TXT is exact and embedded JSON equals the complete approved report in each PDF. Visible paragraphs match the UI; no provider details appear in the visible PDF. Evidence is in `evidence/unified-wording/pdf-verification.json` and `visual-review/`.
- Browser: **88 cases covered and passing** across desktop and mobile against a production bundle and fresh local backend: 82 passed in the full run, then all six affected cases passed after correcting a stale presentation fixture and adding the missing parse-completion wait. The module-switch cancellation behavior was preserved. Coverage includes all module/source-format combinations, formatted tables, legitimate errors, fixed-demo availability and refusal, source preservation, AI/fallback distinctions, UI/PDF parity, exact attachments, no export-time API calls, keyboard access and viewport overflow.
- `git diff --check`: **passed**. AST-only `graphify update .`: **completed**, with no LLM/API extraction. Rule engine, parser, legacy report integration and demo authorization files were not changed by this follow-up.

The machine-readable final outcomes are in `evidence/unified-wording/verification-summary.json`. Normal browser cases use real local deterministic parsing/review endpoints with the key disabled; approved AI cases replay the captured provider reports. No deployed-URL or clinical validation is claimed.

No local change can update the already deployed URL. Both backend and frontend must be deployed together through the project's usual process to publish this implementation. This task performs no deployment.
