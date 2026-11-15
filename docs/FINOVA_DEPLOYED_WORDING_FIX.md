# Deployed attachment wording — diagnosis and correction

15 November 2026. Site: https://frontend-lr7x.vercel.app/

## Observed cause

The initial production Micro probe returned HTTP 200 but `generation.used_mode=STANDARD_TEMPLATES`, `reason=GROQ_UNSUPPORTED_WORDING`, `attempts=1`, and `accepted_comments=0` for the supplied synthetic 16-tooth, 112-position table. This proves the configured backend reached the provider and received content, then rejected it under the local wording contract. It was not a missing API key or a missing Micro integration. The public response does not identify the individual failed wording check; no specific rejected clinical statement or word is claimed here.

The frontend was serving `index-BDTjrmf6.js` at that initial probe. An existing displayed fallback report is a snapshot and does not automatically regenerate after a backend change.

## Backend correction

- Send compact normalized movement facts with immutable references. The model arranges prose around references; exact values, labels, units, directions and missing/zero clauses are supplied locally rather than retyped by the model.
- Use the simple structured response contract. Complex word/enum/regex constraints were not reliable in diagnostic provider calls and are not part of the final patch.
- When a successful provider response fails the unchanged local fact/prose checks, permit one focused correction using only tooth aliases and fact references. Do not resend rejected recommendations, arbitrary text or patient notes.
- Keep both attempts inside the original total timeout. No correction call is made after a missing key, transport failure, rate limit, upstream HTTP error or exhausted deadline. A second rejection still produces honestly labeled standard wording. Export makes no provider call.
- Keep the 96-rule engine, clinical restrictions, parsing, API/report shape, frontend application code and PDF renderer unchanged in this fix.

## Verification

| Check | Result |
| --- | --- |
| Backend suite | **1,060 passed**, including bounded correction, remaining-deadline handling, refusal, exact source facts and clinical safeguards |
| Real local Macro request | 16/16 comments accepted, 1 attempt |
| Real local Micro request | 16/16 comments accepted, 2 bounded attempts |
| Real local Nano request | 16/16 comments accepted, 1 attempt |
| Desktop/mobile UI and PDF regression | **6 passed**, using those actual captured reports, including Micro's two-attempt provenance, every visible paragraph, exact PDF attachments and no export API calls |
| Production build | **Passed**, with the existing bundled PDF/font chunk advisory |
| Full frontend run during concurrent UI work | 254 passed, 4 failed around parse/cache/loading assertions; not represented as a green full frontend suite |

Concurrent UI changes were preserved. Another actor committed workspace changes during verification (`380365f`); this assistant did not perform a commit, push or deployment.

## Final production recheck

A subsequent request to the same deployed URL served `index-C6IMVhrP.js` and returned **GROQ_AI / GROQ_VALIDATED, 16 accepted comments out of 16, one attempt** for Micro. Thus the deployed attachment endpoint was producing accepted AI wording at the final check. No further environment-variable change is indicated by this successful probe. This is one successful synthetic request, not an unconditional availability or clinical-validation claim.

Evidence: `evidence/deployed-wording-diagnosis/deployed-micro.json` (initial failure), `deployed-micro-recheck.json` (final production success), and `local-fixed-{macro,micro,nano}.json` (real local provider results). The browser tests replay those local results; they make no additional live provider calls.

To view a new result in an already open tab, copy the TMT before refreshing, then paste, parse and run the review again. The old standard-wording snapshot will not turn into a new AI report automatically.
