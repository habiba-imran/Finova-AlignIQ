# Finova analysis pipeline fix

15 November 2026, Asia/Karachi. Local implementation and verification only. No deployment, commit or push.

## Result

Ordinary synthetic pasted tables now produce deterministic, distinct analytical reports before any AI wording runs:

`Parsed TMT → analytical findings and referenced evidence → optional automatic Groq wording → validated sections → UI / Copy / TXT / PDF`.

The lexical parser, semantic admission protections and clinical registry were preserved. The benchmark still has **15 tooth rows, seven movement columns, 105 positions, 103 numerical values, two intentional missing entries and zero invalid/ambiguous values**. All 96 rule evaluations remain present, with 27 clinical predicates disabled. This work does not establish clinical validation or proprietary PMCEASY algorithm parity.

## Reviewed context and root causes

Reviewed the current interactive service, narrative composer, module reports, source models, provider/client safeguards, frontend contract, report presentation and PDF renderer. Also reviewed the Phase 6A PMCEASY functional research, gap matrix and reconstruction roadmap; Phase 5 rule inventory; planning-wording implementation report; and existing final module report.

The public research supports dimension-organized planning comments, tooth-indexed attachment options and arch/segment sequencing text as output concepts. It does not establish authorized clinical triggers, attachment geometry, stage calculations or a proprietary algorithm that Finova may reproduce. Those boundaries remain intact.

Root causes:

1. Macro's narrative contract required every source cell exactly once per tooth. Groq could rearrange an inventory but could not select or compare meaningful findings.
2. The TMT-only Micro/Nano path grouped whole movement descriptions into long sections. The wording provider received section kinds and references without analytical results; changing prose could not create an analysis layer.
3. Existing supplied-detail reports correctly withheld unsupported attachment/staging decisions, but they did not supply a movement-based synthetic review demonstration for ordinary inputs.
4. The frontend contract assumed Macro had no sections and Micro/Nano always had four legacy sections. This needed an explicit analytical contract, not a frontend rewrite of existing strings.
5. Technical source inventories appeared again in the main TXT report before complete provenance. Partial-parse limitations also suggested unresolved parsing even when the only issue was intentionally missing cells.

## Implemented analysis

The complete independent policy is documented in `docs/SYNTHETIC_ANALYSIS_RULES.md`. It is separate from the clinical rule registry.

### Shared evidence handling

- Compare only recognized lexical families with explicit compatible units: mm for translation/vertical and deg for angular fields.
- Rank Decimal magnitudes, retaining ties and original signed scalar strings. No float rounding, missing-value filling, directional sign inference or cross-family sums.
- Exclude missing, invalid, ambiguous, duplicate-field and unknown-unit records from comparisons. Findings identify affected teeth and restrict rankings to available comparable entries.
- Retain original cell text, decimal precision, raw directions/signs, units and exact spans in the parsed report and complete provenance.
- Each analytical finding records its ID, kind, section, full comparison population, selected measurement references, origin and any independent demo-rule ID.
- FDI-style token grouping is explicitly unverified. Upper/lower and anterior/posterior groups require matching permanent-tooth token syntax; conflicting numbering claims and other tokens remain unassigned. Upper-only input produces no lower-arch findings.

### Macro

Five sections organize mesiodistal, buccolingual, vertical, angular and overall observations. They identify maxima, ranges, source-label distributions, repeated profiles and group coverage. Absolute and relative vertical fields remain separate. The overall summary points to the cross-tooth peaks. No clinical risk category is assigned.

The benchmark identifies:

- Tooth 13: largest mesiodistal translation magnitude, **3.30 mm, D-labelled**.
- Teeth 11/21: largest buccolingual translation magnitudes, **2.50 mm each, L-labelled**.
- Teeth 11/21/22: shared and maximal vertical entries, **2.20 mm each, I-labelled**.
- Tooth 11: largest rotation and angulation magnitudes, **18.90° and 28.80°**.
- Tooth 18's two missing vertical positions remain unknown and explicitly limit comparisons.

### Micro

Shortlist the two largest distinct nonzero magnitudes per angular family. Rank teeth by number of family maxima, then number of shortlisted components, then token for stable ties. Show at most five priority profiles with the exact movements causing selection.

`DEMO-ANGULAR-RANK-v1` supports illustrative family-control review candidates, combined-angular candidates and runner-up alternatives. `DEMO-ZERO-ANGULAR-v1` supports a no-candidate example only for a complete unambiguous three-family angular profile containing three explicit zeros. Unknown evidence never qualifies as zero or no candidate. These are review topics, not prescriptions or selected attachment shapes.

The benchmark prioritizes Tooth 11 because it leads both rotation and angulation. Tooth 12 is a separate inclination candidate; Teeth 15/21/23 supply ranked alternatives. Tooth 18 has no candidate in this explicitly angular-only demonstration. No arbitrary oval/rectangular alternation, attachment dimensions, orientations or placement coordinates are generated.

### Nano

Report available arch/tooth-group coverage, translation and vertical concentrations, repeated profiles, consecutive source-token runs and teeth with multiple notable components.

Concentrations select the upper half of nonzero magnitudes in each family, keeping boundary ties, then group by available token group and source label. Multi-component review selects the upper quarter within each family, keeps ties and shows at most four teeth with two or more selected components. These are dataset ranks, not clinical thresholds.

The benchmark identifies the D-labelled **12–17 token run at 3.10–3.30 mm**, the **11/21/22 vertical cluster at 2.20 mm, I-labelled**, and overlapping components at teeth including 11/12/13/21. `DEMO-REVIEW-ORDER-v1` illustrates inspecting translations, then vertical patterns, then overlapping profiles. It is an information-review order, not a movement-delivery sequence. No stage count, timing, force or anchorage prescription is inferred.

## Before / after examples

| Module | Before | After, representative excerpt |
| --- | --- | --- |
| Macro | Each tooth's rotation, angulation, inclination, vertical, relative vertical and two translation cells became a paragraph. | “Tooth 13: largest recorded mesiodistal translation magnitude, 3.30 mm (D-labelled), among 15 comparable entries.” Separate transverse/vertical sections identify the 11/21 and 11/21/22 ties. |
| Micro | Rotation and angulation/inclination became broad movement inventories. Older illustrations used tooth-order choices. | “Tooth 11: rotation 18.90° (D-labelled) (dataset maximum); angulation 28.80° (D-labelled) (dataset maximum).” A separate labelled illustrative combined-angular candidate follows from those ranks. |
| Nano | Almost every translation/vertical measurement was transcribed. | “Teeth 12, 13, 14, 15, 16, 17 form a consecutive FDI-style token run among the upper-half mesiodistal translation entries: D source label, magnitudes 3.10–3.30 mm.” The vertical cluster and multi-component teeth have distinct sections. |

Complete before evidence remains in the existing historical reports. Current deterministic snapshots are `evidence/analysis-pipeline/{macro,micro,nano}.json` and `.txt`.

## Groq architecture, privacy and execution evidence

The existing configured server key automatically enables the ordinary analytical path; there is no separate AI selection. The existing fixed-demo, lexical-parser, legacy rule-report and supplied-detail protections remain separate.

Groq receives normalized evidence arrays, opaque tooth/measurement references, finding kinds, comparison sets, selected references and explicit demo origins. Raw tables, arbitrary tooth identifiers, patient/context notes and supplied free text are excluded. Shared comparison sets keep prompts below the existing 24,000-byte bound. Current mocked benchmark prompts are 18,694 bytes (Macro), 11,277 (Micro), 17,778 (Nano).

Provider wording is deliberately bounded: it arranges complete approved-finding placeholders within their own sections. Every factual sentence is substituted locally. Added claims/numbers, omitted or duplicate findings, cross-section references and malformed envelopes reject the whole batch. This is AI-assisted arrangement of analytical wording, not unrestricted model clinical reasoning. There is one provider request per ordinary analysis, no automatic repair/retry call. Module navigation caches unchanged results; Copy/TXT/PDF exports make no provider request.

Safe `finova.analysis` events record AI requested, provider attempts/response result, validation outcome, fixed reason code and fallback use. They do not log credentials, raw input or measurements. Fallback is always `STANDARD_TEMPLATES`, never successful AI generation.

Actual configured live check, one bounded attempt per module:

| Module | Observed result |
| --- | --- |
| Macro | **GROQ_VALIDATED**, 5/5 sections accepted, one attempt. |
| Micro | **GROQ_RATE_LIMIT**, one attempt; complete deterministic fallback, zero accepted AI sections. |
| Nano | **GROQ_RATE_LIMIT**, one attempt; complete deterministic fallback, zero accepted AI sections. |

All three separately passed actual `GroqClient` HTTP transport tests using `httpx.MockTransport`: **one request each**, 5/4/5 accepted sections. See `mock-summary.json`, `live-summary.json`, sanitized diagnostic logs and `*-mock` / `*-live` reports under `evidence/analysis-pipeline/`. The initial sandboxed live attempt could not connect; the bounded network-enabled check established the results above. No successful live Micro/Nano wording is claimed. Live snapshots precede the final removal of repeated explanatory sentences; current final behavior is verified with the mocked transport and browser checks.

## Presentation and compatibility

`ANALYTICAL_V1` adds a strict report contract alongside older formats. All sections and immutable findings are checked on the frontend; forged status, evidence references, modified text and missing sections are rejected. Older saved reports and optional supplied attachment/stage records retain their existing handling.

The UI and PDF consume the same validated section text. Copy and TXT use the exact complete `export_text`. Main results no longer repeat every tooth's source cells; source values remain in a disclosure and the complete technical record. TXT retains source values/provenance once, plus structured analytical provenance, original input and the full rule ledger. PDFs retain exact TXT and JSON attachments. Numeric precision remains unchanged.

Successful parsing with missing values is explicitly distinguished from unreliable/invalid entries in both the visible report and exported limitations. Existing responsive layout and export controls were reused; no application redesign was performed.

## Modified files

| Area | Files added or changed by this task |
| --- | --- |
| Backend analysis | `backend/app/interactive/analysis.py`, `analytical_wording.py`, `models.py`, `service.py`; `backend/app/api/interactive.py` |
| Frontend contract/rendering | `frontend/src/api/interactive.ts`, `components/InteractiveWorkspace.tsx`, `reviewPresentation.ts` |
| Tests | `backend/tests/test_analytical_pipeline.py`, `test_interactive.py`, `test_module_reports.py`, `fixtures/analysis_15_tooth.md`; `frontend/src/AnalyticalPipeline.test.tsx`; `frontend/e2e/analysis-pipeline.spec.ts`, `interactive.spec.ts`, `module-final.spec.ts` |
| Verification/contracts | `backend/scripts/verify_analysis_pipeline.py`, `verify_analysis_pdfs.py`; `schemas/interactive-report.v1.json` |
| Documentation/evidence | This report, `docs/SYNTHETIC_ANALYSIS_RULES.md`, `evidence/analysis-pipeline/`, refreshed local Graphify output |

Pre-existing dirty presentation/report files were preserved. Clean historical PDFs regenerated by browser tests are restored to their original bytes; this task's PDF evidence is kept separately.

## Tests and results

- Complete backend suite: **1,109 passed**. Final focused report/parser/privacy/provider regressions after report compaction: **78 passed**.
- Complete frontend suite: **274 passed**; final outcome is recorded in `frontend-tests.txt`.
- Production TypeScript/Vite build passed. The existing large-bundle advisory remains.
- Full production-bundle browser run covers **106 desktop/mobile cases**. Its 104 passes and two stale Micro inventory expectations are followed by **12/12 passing final analytical/module/PDF checks** in `browser-final-focused.txt`, including both previously failing cases. The expectation now verifies the actual highest-ranked angular value instead of demanding an omitted low-ranked cell. All 106 unique cases are covered by passing results across these runs.
- The six primary 15-tooth browser cases verify numeric counts, successfully parsed missing values, all displayed sections, exact Copy/TXT, exact embedded PDF attachments, responsive width, cached navigation and zero export API/provider calls.
- All **six primary PDFs passed** text/provenance checks: Macro three pages, Micro two pages, Nano three pages at both desktop and mobile. Verification checks all visible finding text, headings, exact attached TXT/JSON, original input hash and unchanged clinical rule ledger. All pages were rendered; the complete desktop page sets were visually inspected for clipping, legibility and section transitions. See `pdf-verification.json` and `renders/`.
- Independent Markdown, TSV, transposed, incomplete and supported messy synthetic inputs pass. Adversarial provider changes, duplicates, omissions, cross-section references, unsupported geometry/advice, HTTP failures, missing keys and honest fallback are covered.
- The 15-row fixture is taken from the archived user synthetic table with its wholly missing Tooth 28 row excluded. The attachment for this task contains the requested counts/examples rather than a second full table; this derivation exactly matches the stated 105/103/two-missing benchmark. Original source precision and direction labels were retained.
- Graphify AST update completed without model/API extraction. Its existing environment lacks `pypdf` for graph PDF extraction; source/code graph refresh completed. No clinical rule, parser or provider configuration was changed to bypass a safeguard.

## Remaining limitations

The configured Groq account rate-limited live Micro/Nano checks. Upstream quota availability is outside this local change; standard analytical reports still work. AI wording arranges approved immutable analytical sentences rather than generating arbitrary clinical prose.

Token groups and source direction conventions remain unverified. Comparisons describe available source data, not achieved outcomes, clinical difficulty, treatment suitability or risk. Rank-based demonstrations are relative to the supplied dataset and are bounded shortlists, not exhaustive attachment or sequencing decisions. Total TMT data cannot supply validated geometry, actual movement staging, collisions, timing, forces or anchorage requirements.

Optional supplied-detail reports preserve their separate unverified-record workflow; they do not become calculated treatment plans. Unsupported messy layouts continue to abstain rather than invent associations. No deployment, commit or push was performed.
