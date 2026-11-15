# Finova AlignIQ — Generalized Planning Engine

Date: 2026-11-15. Independent PMCEASY-inspired software demonstration.

## Result and scope

The normal workflow now works with supported ordinary pasted tables:

**Paste TMT → Parse → Inspect → Choose Macro/Micro/Nano → Generate → Copy/Export.**

No predefined example or scenario ID is required. Macro produces evidence-linked
technician review requests; Micro produces tooth-wise profile-dependent
illustrative categories/alternatives; Nano produces movement-coordination review
priorities and an inspection outline, with actual stage processing only when
stage records are supplied. Numerical modification examples and geometry require
additional explicit context.

One discreet **Load synthetic example** control remains optional. The earlier
three scenario loaders are absent from the normal UI. The original 15-tooth
example can still carry explicitly authored context across all three tabs;
manually pasting its text does not load that context. Earlier module fixtures
remain for regression testing and backwards compatibility.

The parser, original numerical analyzer, source provenance, 96-rule registry and
27 disabled clinical predicates remain intact. Every new plan has
`clinical_authorized=false`, and underlying reviews remain `UNVERIFIED`. These
policies do not establish clinical suitability, actual treatment feasibility or
proprietary PMCEASY algorithm equivalence. No deployment, commit or push was
performed.

## Audit and root cause

Reviewed the PMCEASY functional research, gap matrix and roadmap, prior functional
and final analysis QA reports, current analysis/scenario/service contracts,
clinical rule restrictions and Groq integration. Graphify queries guided source
navigation. The research describes public interface/workflow observations, not
validated algorithms or clinically approved numerical parameters.

The scenario dependence was an explicit dispatch condition in
`backend/app/interactive/service.py`: only a non-null `planning_context` reached
the functional engine. Ordinary input without supplied records went directly to
the descriptive analyzer. The original Macro policies also required supplied
replacement targets; Micro used a combined-angular presence mapping; Nano's
functional pathway required authored stage records. This was a data/dispatch
limitation, rather than a parser failure or a need to recognize more fixtures.

## Architecture and reusable policies

```text
Existing parser + unchanged unverified 96-rule review
  → reusable planning options + actual source measurements
  → independent deterministic policy evaluation
  → source-linked structured decisions and immutable findings
  → automatic bounded Groq wording / validated standard fallback
  → UI, Copy, TXT and local PDF with complete evidence attachments
```

`backend/app/functional/generalized.py` reuses the existing functional contracts,
source helpers and supplied-stage validation. `PlanningOptions` is an optional
typed request/report contract. The normal frontend sends its defaults
automatically; API clients can request this behavior with `planning_options: {}`.
Older API callers omitting that field retain the previous analytical pathway.
Explicit scenario context remains separate and cannot be combined with options.

Evaluated context uses `origin=INPUT_DRIVEN_POLICY_REVIEW`, the actual source hash
and `scenario_id=null`. There is no fixture-ID lookup or source-hash allowlist in
the generalized engine. Hashes bind supplied context to its current table; they
never grant vendor or clinical authority. Original source cells are never changed
by proposals or context entry. Schemas were regenerated.

There are **19 new reusable policy IDs**, plus reused stage data/group/check/
support/scope policies. Their conditions, precedence, assumptions and output
limits are documented in
[`GENERALIZED_REVIEW_POLICIES.md`](docs/GENERALIZED_REVIEW_POLICIES.md).

| Module | Implemented behavior |
| --- | --- |
| Macro | Separate sagittal, transverse, vertical and angular review requests. Upper-half nonzero magnitude selection with every tie retained; exact recorded maxima/source-label counts; coupled-component evidence; retain-source/separate-component alternatives; missing-information and explicit-zero outcomes. |
| Micro | Complete angular profiles distinguish sole/unique dominant rotation, angulation, inclination and tied angular components. Complete seven-field evidence gates vertical-only and explicit-zero profiles. Specific category/alternative, no-candidate and insufficient-information outcomes are source-linked and reproducible. |
| Nano, TMT only | Existing arch/token-group counts and complete directional concentration groups, multi-component coordination priorities and separate inspection topics. No treatment stages, stage amounts, duration or forces are generated. |
| Nano, supplied stages | Existing ordered-stage/phase grouping, exact supplied amounts, compatible Decimal sums, field-total comparisons, missing/conflicting metadata checks and explicitly constrained fictional support review. |

Micro compares angular magnitudes **within each tooth**. It does not select a
vertical rectangle for every combined rotation/angulation profile, alternate types
by row, use dataset rank or invent a clinical magnitude threshold. Default catalog
entries are concepts only; every geometry/orientation/surface/placement field is
null until supplied. Optimized-style is a category, without an inferred optimized
design or fitted mesh.

Nano's `review_outline` is distinct from `stages`. Each inspection topic is marked
`ILLUSTRATIVE_REVIEW_OUTLINE` with `stage_allocations_generated=false`. Translation
and vertical concentration evidence reuses the existing analyzer, preserving
complete arch/directional grouping, ties and single-value range formatting.

Known comparison tables cannot authorize numerical replacements, turn comparison
zeros into no-attachment choices, or become stage totals through a user-selected
increment convention. They remain reviewable as recorded differences.

## Required versus optional data

| Output | Required data / limits |
| --- | --- |
| Default review | A supported parsed TMT. No example, target value or optional form is required. Unusable/missing cells remain unknown. |
| Profile-dependent illustrative categories | Complete relevant movement evidence and synthetic review mode. Evidence-only mode retains profile review while withholding toy choices. No clinical suitability is established. |
| Supplied replacement | Current source hash, comparable source field, matching explicit objective, unchanged unit/label convention, synthetic mode and distinct supplied target. Incompatible comparison sources are excluded. |
| Arithmetic illustration | The same applicability context plus explicit `HALF_MAGNITUDE` selection and a chosen source field. Exact signed Decimal ÷ 2, preserving its label. This is fictional arithmetic, not a justified clinical target; unsupported precision is withheld rather than rounded. |
| Geometry/placement | Explicit catalog specifications. Partial/invalid dimensions are rejected; no parameters are estimated from movement values. Placement uses only the explicitly supplied fictional local frame. |
| Actual stage calculations | Supplied stage records and allocations, source binding and compatible increment/source-label conventions. Missing amounts remain null; no total is divided into stages or residual repaired. |
| Support consideration | Explicit phase, support/active roles and stationary-support assumption, consistent assigned movements and complete stage checks. Incomplete/conflicting evidence or evidence-only mode withholds the strategy. |

The compact **Planning context · optional** panel appears after parsing. It offers
module-specific objectives/targets, catalog specifications or stage/support entry.
It is collapsed by default. Stage-entry amounts start blank, even after selecting
a source cell. Source edits/settings changes clear all options and cached results;
each module otherwise keeps its own source-bound options. Editing context clears
the dependent report while retaining the parsed table.

The existing input bounds remain explicit: up to 64 stages, 128 allocation
records, 16 phases and 16 support constraints. These are software contract limits,
not clinical staging limits.

## Client-style inputs and source accuracy

The tests paste ordinary input text and submit default options. They do not load
or recognize a scenario ID.

| Case | Source | Teeth | Positions | Numeric | Missing | Explicit zeros |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| A | Existing upper-arch Markdown benchmark | 15 | 105 | 103 | 2 | 6 |
| B | Independently authored lower-arch mixed-profile Markdown | 16 | 112 | 109 | 3 | 77 |
| C | New cross-arch TSV with different values/combinations | 8 | 56 | 56 | 0 | 37 |
| D | Sparse/incomplete TSV | 3 | 6 | 3 | 3 | 2 |

Full inputs, offline/mock reports, TXT exports and metrics are retained in
[`evidence/generalized-planning/`](evidence/generalized-planning/), including
`inputs.json` and `case-metrics.json`. Original raw text, spans, signs, labels,
Decimal strings, missing classifications and the full rule ledger remain in the
structured reports and PDF attachments.

### A: upper-arch before/after

Previously, ordinary Macro/Micro/Nano supplied descriptive distributions, priority
teeth and concentrations; concrete choices or stage processing required example
context. Now Macro produces eight source-linked findings, Micro has 15 tooth rows
plus scope, and Nano adds coordination review and three inspection topics with
zero generated stages.

Macro identifies Tooth 13's recorded `3.30 mm` D-labelled mesiodistal value and
the relevant distribution/coupled components before issuing a technician review
request. It does not choose a new numerical target by itself. Micro reads Tooth
11's `18.90°` rotation, `28.80°` angulation and `0.70°` inclination: angulation is
the largest within-tooth angular component, producing the illustrative horizontal
rectangular category with vertical rectangular alternative, without dimensions.

Nano retains every buccolingual upper-half token exactly once:
`{11,12,13,21,22,24,26}`. Tooth 24 appears in the posterior L-labelled group at
`0.40 mm`; equal endpoints are not printed as `0.40–0.40 mm`. Source grouping
keeps all arch/label partitions. The successful-parse presentation still states
two missing values while retaining the underlying `PARTIAL`/missing provenance.

### B: lower-arch before/after

The new table is processed without loading an example. Micro distinguishes all
six concept categories: Tooth 37 rotation → oval; Tooth 36 inclination →
optimized-style category; Tooth 35 vertical-only → generic rectangular; Tooth
34 angulation-dominant → horizontal rectangular; Tooth 31 tied angular values →
vertical rectangular; complete-zero Teeth 38/48 → fictional no attachment.
Tooth 44's complete translation-only profile has no supported category, while
45/46/47 have insufficient required data. In particular, Tooth 46 has explicit
zero angular values with a missing vertical field; that missing field is not
called an incomplete angular value or treated as zero.

Macro produces dimension-specific review requests from the lower-arch values;
Nano groups lower-arch source patterns, overlapping components and three review
topics. Neither module supplies automatic replacement values or invented stages.

### C: completely new input

The independent table combines upper and lower tokens with new decimals and
profiles. Examples: Tooth 14's equal `7.250°` rotation/angulation selects the tied
angular category; Tooth 22's `12.345°` inclination selects an optimized-style
category without geometry; Tooth 33's `-4.125°` M-labelled rotation retains its
negative scalar/opaque label and selects the rotation category. Tooth 38 is an
explicit-zero profile; Tooth 46 is a complete translation-only no-candidate case.

Its ordinary outputs contain eight Macro, nine Micro and sixteen Nano findings,
with three Nano inspection topics and no stages. This input is not a built-in
scenario or exact-match rule trigger.

### D: sparse input

All three Micro rows remain insufficient for attachment selection. Macro can
review the recorded `2.750°` rotation while identifying unavailable dimensions.
Nano produces the supported angular inspection topic and missing stage/context
requirements. Three missing values stay missing; the two explicit zeros do not
complete missing profiles or authorize no-attachment choices.

## Counterfactual and explicit-context behavior

- Changing only Tooth 34 rotation from `1.20` to `5.40°` changes its primary
  category from horizontal rectangular to oval. Other tooth choices/alternatives
  remain unchanged.
- Changing Tooth 24 buccolingual `0.40` to `0.10 mm` changes the relevant Macro
  transverse finding while unrelated dimensions remain unchanged.
- Explicitly requesting a half-source illustration for `-4.125°` produces
  `-2.0625 deg`, preserving the M label. Removing the matching objective,
  convention, method or illustration mode suppresses the dependent proposal.
  Stale source hashes and incompatible source/unit/label references are rejected.
- Supplying `1.234 × 2.345 × 0.456 mm` oval geometry displays those exact strings.
  Removing the specification returns geometry to null; no placement is invented.
- A separately entered two-tooth context has two stages, four allocations and
  four matching field-total checks. Explicit support roles can produce two
  fictional support-review strategies. Removing the second stage leaves missing
  assignments/conflicting constraints and withholds dependent strategies.
- Invalid stage references, orders, duplicate/overlapping phase metadata, units,
  null amounts and mismatched sums are detected without repairing records.
- A 32-tooth/224-position ordinary table exercises bounded provider summaries.
  Unmapped columns do not trigger known movement policies; overlong calculated
  replacement values are withheld without rounding.

## Groq execution and integrity

Groq remains automatic when configured and eligible; there is no main-UI AI enable
button. Deterministic analysis and policy choices precede provider wording.
Provider output can arrange sealed finding references only; every reference must
appear once in its own section. Additional clinical prose, altered numbers,
geometry or schedules reject the batch. This is constrained wording assembly,
not unrestricted paraphrasing or independent clinical reasoning.

The unchanged 24,000-byte prompt bound is met using shared references, compact
stage tables/status counts and, where needed, a bounded immutable-finding summary.
Complete numerical evidence stays local in the report. No retry or extra API call
is added. The 32-tooth test confirms an actual mocked transport request rather
than silently skipping the provider for size.

All twelve case/module mock calls used one request and passed grounding validation.
Live execution used the independently authored ordinary Test C, once per module,
with `openai/gpt-oss-120b`:

| Module | HTTP/provider result | Attempts | Final status |
| --- | --- | ---: | --- |
| Macro | 200; grounding validated | 1 | `GROQ_AI` / `GROQ_VALIDATED`, 4 accepted sections |
| Micro | 200; response failed grounding validation | 1 | `STANDARD_TEMPLATES` / `GROQ_UNSUPPORTED_WORDING`, 0 accepted sections |
| Nano | 429 rate limit | 1 | `STANDARD_TEMPLATES` / `GROQ_RATE_LIMIT`, 0 accepted sections |

Thus live Macro succeeded; live Micro/Nano success is not claimed. Nano's request
reached Groq, demonstrating that it was not blocked locally by the earlier prompt
size failure. No quota retries were made. Safe diagnostics record requested,
attempted, responded, validated/succeeded and fallback states. Fallback is never
labelled AI-generated. Source aliases and normalized enums/scalars exclude raw
tables, free-form notes, original identifiers and credentials from provider input.
`real_patient_transmission_enabled=false` in all live records.

Evidence: `live-summary.json`, `live-diagnostics.txt`, `live-plan-integrity.json`,
`mock-summary.json` and full `C-*-live.json`/TXT reports in the evidence folder.
Live probes preserved their deterministic source data and plans; final mock
verification covers the complete four-case matrix.

## Presentation and complete output consistency

The normal pasted-table reports use review headings. Macro separates sagittal,
transverse, vertical and additional/angular findings. TMT-only Nano uses
**Movement patterns and review outline**; **Ordered phases and movements** is
reserved for actual supplied stage records. Invalid or withheld stage records use
**Supplied stage review**. Micro distinguishes **Insufficient information** from
**No supported candidate** in both the UI and PDF.

The default Micro table keeps candidate, alternative, movement profile and
source-linked rationale together. Supplied geometry appears only when present.
Repeated per-row illustration badges and duplicated Nano outline text were
removed from the visible report. Full immutable findings and essential limits
remain available. Missing cells stay missing, explicit zeros stay zero, and
single-valued ranges use one value. No empty source-value sections are added.

Copy and TXT preserve the complete report text. PDF provides a concise visible
presentation and embeds the exact full TXT and validated JSON. The PDF audit
compares these attachments byte-for-byte with the corresponding report and
checks every immutable finding against extracted visible text. Original source
spans, labels, Decimal strings, options, decisions, policies and the complete
96-rule ledger remain in the structured exports. Browser checks also confirm
that export actions do not trigger another backend/provider request.

The PDF matrix includes A/B/C/D across all three modules plus one explicit-context
case per module, each at desktop and mobile sizes. All desktop pages were rendered
and inspected for clipped text, table wrapping, continuation headers and footer
overlap. The final rerender specifically checks the corrected TMT-only Nano
heading and Micro insufficient-data labels.

## Verification results

| Check | Result | Evidence |
| --- | --- | --- |
| Full backend suite, final code | **1,236 passed** | `backend-tests.txt` |
| Full frontend suite, final code | **322 passed**, 26 files | `frontend-tests.txt` |
| Full desktop/mobile browser regression suite before final heading/label cleanup | **144 passed** | `browser-tests.txt` |
| Final affected desktop/mobile browser paths after that cleanup | **66 passed** | `browser-final-tests.txt` |
| TypeScript check and production Vite build | **Passed** | `build.txt` |
| Final PDF verification | **30 PDFs / 88 pages; every visible finding and exact embedded TXT/JSON verified; 44 desktop pages rendered** | `pdf-verification.json`, `pdf-checks.txt`, `renders/` |
| Four-case offline reports and actual mocked provider transport | **12 module reports each; all 12 mock calls validated** | `offline-summary.json`, `mock-summary.json` |
| Live Groq | **3 attempts**, Macro validated, Micro grounding fallback, Nano rate-limit fallback | `live-summary.json`, `live-diagnostics.txt` |

All evidence filenames above are relative to `evidence/generalized-planning/`.
The final browser run covers all 30 generalized input/context/viewport cases plus
36 affected existing analysis, functional-example, ordinary-input and export
regressions. It uses fresh owned backend/preview servers and the production build.
The earlier 144-test run also includes the remaining existing desktop/mobile
regressions. No test substitutes fixture-specific answers for ordinary requests.

One additional frontend run under concurrent unrestricted worker load had four
five-second timeouts (318 passed). The complete final rerun used `--maxWorkers=2`
and passed all 322 tests without changing assertions or timeout settings; the
initial log is retained as `frontend-concurrent-timeouts.txt`.

Backend tests cover exact source counts/labels, zero versus missing, every
qualifying tie once, source-bound targets/catalog/stages, independent comparison
sources, unknown fields, overlong decimals, mode restrictions, stale/forged
contexts, context removal, module isolation, deterministic counterfactuals,
bounded provider requests and preserved 96/27 rule restrictions. Frontend/browser
tests cover the corresponding strict contracts, ordinary pasted workflows,
optional-context editing, cache invalidation, responsive overflow and exact
Copy/TXT/PDF data. Existing explicit scenarios remain compatible.

The build retains the existing large-bundle advisory. Backend tests emit the
existing Starlette/httpx deprecation warning. Graphify's separate environment
does not have the PDF text-extraction extra; PDF verification uses the bundled
Python environment with pypdf and Poppler instead. AST-only `graphify update .`
completed with **2,193 nodes, 6,912 edges and 108 communities**; its log is
`graphify-update.txt`. No LLM labeling or dependency installation was needed.
Final `git diff --check` passed. Historical generated PDFs/snapshots overwritten
by regression tests were restored; this phase's output is retained separately in
`evidence/generalized-planning/`.

## Remaining clinical and product gaps

These are independently authored simulation/review policies. No clinical outcome
validation, approved movement limits, patient-specific diagnosis, treatment
prescription or proprietary PMCEASY equivalence has been established. Source
notation/axes/conventions remain unverified assumptions. No clinical registry
predicate or vendor evidence-admission route was enabled.

Macro does not calculate clinically optimal replacement targets. Attachment
categories do not establish retention, root control, physical fit or optimized
geometry. Nano does not optimize biological staging, predict duration/forces or
prescribe anchorage. No CAD write-back or clinical sign-off workflow was added.
Provider quota/grounding failures can still require standard wording; all
deterministic review content remains available.
