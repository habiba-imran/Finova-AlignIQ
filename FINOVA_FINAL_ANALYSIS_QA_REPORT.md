# Finova final analysis accuracy and output QA

15 November 2026, Asia/Karachi. Focused local audit. No deployment, commit or push.

## Findings and correction

**Confirmed: Tooth 24 was omitted by a display-group cap, not by the numerical cutoff or lexical parser.** Nano correctly selected all entries at or above the buccolingual upper-half cutoff, then sorted groups by size and kept only three with `[:3]`. Tooth 24 belonged to a fourth group and disappeared from the reported concentration results.

The 15-tooth source contains 15 buccolingual entries: 14 nonzero and one explicit zero. The descending nonzero cutoff is **0.40 mm**. Exactly seven entries qualify:

| Group, using unverified FDI-style token grouping | Teeth and original values |
| --- | --- |
| Upper anterior, L label | 11: 2.50 mm; 21: 2.50 mm; 22: 1.20 mm |
| Upper anterior, B label | 12: 0.40 mm; 13: 0.50 mm |
| Upper posterior, B label | 26: 0.40 mm |
| Upper posterior, L label | **24: 0.40 mm** |

Removed the three-group cap. Every qualifying measurement now belongs to exactly one primary concentration group, including every boundary tie. The upper-half selection formula, Decimal comparisons, grouping convention, source labels and all other deterministic ranking rules remain unchanged. Secondary run/shared-profile findings may reference those cells again for their separate pattern summaries; they do not alter or duplicate the primary grouping partition.

Regression checks independently calculate the expected set from source cells, compare exact membership/counts, reverse source rows, and exercise eight arch/label groups with all values tied, in both row and transposed inputs. A fourth or later group can no longer be silently discarded.

## Numerical audit

The independent oracle reads the original Markdown cells rather than deriving expected values from the analysis implementation. It verifies exact Decimal strings, units, direction labels, source spans, zeros, missing values, maxima, ranges, direction distributions, concentration partitions, Micro priorities, Nano component selection and group quantities.

Unchanged benchmark: **15 teeth, seven movement columns, 105 positions, 103 numeric entries, two missing values, six explicit zeros, zero invalid/ambiguous entries.** Both missing entries belong to Tooth 18's vertical and relative vertical fields. Original provenance and the underlying `PARTIAL` classification are preserved.

| Field | Available / missing | Largest magnitude | Source teeth / labels |
| --- | --- | --- | --- |
| Mesiodistal translation | 15 / 0 | 3.30 mm | 13, D |
| Buccolingual translation | 15 / 0 | 2.50 mm | 11 and 21, L |
| Vertical movement | 14 / 1 | 2.20 mm | 11, 21 and 22, I |
| Relative vertical movement | 14 / 1 | 1.50 mm | 12 and 22, I |
| Rotation | 15 / 0 | 18.90° | 11, D |
| Angulation | 15 / 0 | 28.80° | 11, D |
| Inclination | 15 / 0 | 7.20° | 12, B |

Arch/group quantities also match the cells: six upper anterior tokens with 42 numeric entries across 42 positions; nine upper posterior tokens with 61 numeric entries across 63 positions. No lower-arch findings are created for this input. Anatomy and direction conventions remain unverified.

Machine-readable source quantities and actual concentration groups are in `evidence/final-analysis-qa/numerical-audit.json`.

## Presentation corrections

- Equal endpoints now display once: **0.40 mm**, rather than **0.40–0.40 mm**. Genuine ranges such as 3.10–3.30 mm remain ranges. Decimal comparison/source precision is unchanged.
- Removed repeated anatomical-direction caveats from individual distribution lines. The report's source/scope uncertainty remains visible.
- Missing-data findings now name the actual reason, such as “missing”, rather than listing hypothetical ambiguity/invalid/unit problems for a cell known to be missing.
- Shortened Micro coverage/scope wording and Nano sequencing-review phrasing. Retained the illustrative-only distinction and the absence of established clinical need, geometry, placement, treatment schedule, forces or anchorage.
- Source disclosures render only when source rows contain measurements. Empty per-tooth Source values and empty Source movement values headings are suppressed. Existing source values remain available when present.
- No frontend redesign or new analysis engine was introduced. UI and PDF continue to consume the validated section text; Copy and TXT retain complete report text and provenance.

## Parse-status wording

The structurally valid benchmark now says **“Successfully parsed with 2 missing values”** in the intake heading, diagnostic lexical preview, generated report summary and export text. Missing cells remain unknown, not zero. The original parse result still records `PARTIAL`, two missing cells, the original source spans and all parser issues.

The wording helper is presentation-only. Errors, ambiguous measurements, unsupported input and unrecognized fields continue to show correction/clarification wording. An explicit regression checks that adding a blocking issue prevents a successful-parse label. The lexical parser architecture and contracts were not changed.

## Groq execution and diagnostics

The configured path still requests wording automatically, without a main-UI AI selector. It sends the existing normalized evidence/findings, never raw tables, arbitrary identifiers or notes. One provider attempt per ordinary analysis remains the limit; no new retry/repair loop was added.

Backend diagnostic events now explicitly distinguish:

- `requested=True`: automatic wording was requested.
- `analysis_groq_attempt ... attempted=True`: the provider client is being invoked.
- `provider_responded` / `http_status`: whether an HTTP response arrived, independently of accepted report wording.
- `succeeded` / `validated`: whether the response passed the closed finding-reference validation.
- `fallback`: whether deterministic report wording was used.

These INFO events contain fixed event/outcome codes, module names, booleans, HTTP statuses and attempt counts. They contain no credentials, source cells, raw input or hashes. The verification script enables INFO logging and retains only these safe diagnostics. Normal deployment logging must also enable this logger at INFO to collect these events.

### Actual configured live verification

One bounded synthetic request per module was made through the existing Groq client/configuration:

| Module | Requested / attempted | Provider result | Accepted AI report | Fallback |
| --- | --- | --- | --- | --- |
| Macro | Yes / yes, one attempt | HTTP 200; wording rejected by validation (`GROQ_UNSUPPORTED_WORDING`) | No | Yes |
| Micro | Yes / yes, one attempt | HTTP 429 (`GROQ_RATE_LIMIT`) | No | Yes |
| Nano | Yes / yes, one attempt | HTTP 429 (`GROQ_RATE_LIMIT`) | No | Yes |

HTTP 200 is deliberately not reported as successful AI generation when report validation fails. All three live reports correctly use `STANDARD_TEMPLATES` with zero accepted AI sections. No successful live AI wording is claimed for this audit, and no additional quota-consuming retries were made.

Mocked HTTP transport checks separately verify automatic success for all three modules: **5/5 Macro, 4/4 Micro and 5/5 Nano sections**, one request each. Additional tests cover missing configuration, connection failure, rate limits and rejected provider wording, with the expected requested/attempted/succeeded/fallback flags and no private log content. Evidence: `live-summary.json`, `live-diagnostics.txt`, `mock-summary.json`, `mock-diagnostics.txt` and complete synthetic report snapshots under `evidence/final-analysis-qa/`.

## Module differentiation

| Module | Preserved purpose and checked behavior |
| --- | --- |
| Macro | Cross-tooth overview in five dimension/summary sections. Correct maxima, ranges, directions and missing-data qualifiers; no cell-by-cell narrative inventory. |
| Micro | Tooth-focused angular shortlist and explicitly illustrative attachment considerations. Independent source ranks yield priorities **11, 12, 15, 21, 23**. Candidate/alternative states follow those ranks; the complete zero-angular profile at 18 remains an illustrative no-candidate example. No arbitrary shape alternation or calculated geometry. |
| Nano | Arch/group distributions, complete upper-half concentrations, repeated/run patterns and multiple-component review. Independent upper-quarter selection gives displayed multi-component order **12, 11, 13, 21**. The illustration is an order for reviewing information, not a treatment schedule. |

All 96 rule evaluations and all 27 disabled clinical predicates are preserved. No clinical policy, validated attachment recommendation or proprietary PMCEASY algorithm was introduced.

## Verification record

| Check | Final result |
| --- | --- |
| Complete backend suite | **1,124 passed**; existing Starlette/httpx deprecation warning only. |
| Complete frontend suite | **277 passed**, 24 files, with two workers. |
| Complete production-bundle desktop/mobile browser suite | **106 passed** in the final clean run. |
| TypeScript / Vite production build | **Passed**; existing bundle-size advisory remains. |
| Primary benchmark PDF content and provenance | **Six passed**; every section/finding present and exact embedded TXT/JSON. Macro 3 pages, Micro 2 pages, Nano 3 pages at each width. |
| Visual PDF review | All 16 pages rendered; all eight desktop pages visually inspected for legibility, clipping and section transitions. |
| Source accuracy | All 105 source positions, 103 numbers, six zeros, two missing cells; independent maxima, direction counts, Micro/Nano ranks and complete concentration partitions passed. |
| Diff and knowledge graph | `git diff --check` passed; AST-only `graphify update .` completed without model/API extraction. Graphify reported two test files with no extracted symbols and skipped PDF text extraction because its own environment lacks `pypdf`; bundled PDF verification ran successfully separately. |

Evidence files are `backend-tests.txt`, `frontend-tests.txt`, `build.txt`, `browser-tests.txt`, `pdf-verification.json` and `graphify-update.txt` in `evidence/final-analysis-qa/`.

The primary browser cases check actual parsed counts, all section paragraphs, the corrected parse heading, Tooth 24's exact L-labelled value, all seven buccolingual qualifying teeth exactly once, absence of single-value ranges, 105 source cells, exact Copy/TXT contents, exact embedded PDF TXT/JSON, responsive layout and cached navigation with no export/provider requests. The rest of the existing desktop/mobile suite covers routing, earlier reports, errors, semantic protections and other exports.

Earlier status-label assertions were updated to the newly requested visible wording. An initial unrelated legacy frontend test timed out under heavy concurrent execution; the full suite was rerun with two workers. No timeout or assertion was relaxed to hide a data or report defect.

## Files changed and preserved scope

- Analysis/presentation: `backend/app/interactive/analysis.py`, `service.py`; `frontend/src/api/parse.ts`; `frontend/src/components/InteractiveWorkspace.tsx`, `ParserStatus.tsx`, `ParseResults.tsx`.
- Provider diagnostics: `backend/app/interactive/analytical_wording.py`.
- Independent numerical/provider tests: `backend/tests/test_final_analysis_qa.py`; updated expectation in `test_analytical_pipeline.py`.
- Frontend/browser checks: `frontend/src/AnalyticalPipeline.test.tsx`, `App.assisted.test.tsx`; `frontend/e2e/analysis-pipeline.spec.ts`, `automatic.spec.ts`, `parse.spec.ts`.
- Reusable verification output location: `backend/scripts/verify_analysis_pipeline.py`, `verify_analysis_pdfs.py` accept an optional project-contained output directory, leaving earlier evidence untouched by these scripts.
- Documentation/evidence: this report, `docs/SYNTHETIC_ANALYSIS_RULES.md`, `evidence/final-analysis-qa/`, local Graphify refresh.

Test-generated changes to older tracked PDFs are restored from their original bytes after verification; final audit PDF evidence is retained separately. No parser implementation, source-value contract, rule registry, credential or deployment setting was changed.

## Remaining limits

The live provider returned rejected wording/rate limits, so successful live AI phrasing remains unverified in this audit; complete deterministic reports remain available. The source labels and FDI-style grouping are descriptive assumptions, not verified anatomy. Illustrative attachment/sequence review remains unvalidated and does not establish clinical need or a treatment prescription. Existing provider-size bounds still fall back honestly when exceeded; they do not truncate findings to fit a prompt.

No deployment, commit or push was performed.
