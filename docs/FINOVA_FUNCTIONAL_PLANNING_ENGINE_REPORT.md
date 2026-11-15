# Finova AlignIQ — Functional Planning Engine

Date: 2026-11-15. Scope: independently authored synthetic software demonstrations.

The subsequent generalized implementation makes ordinary pasted tables work
without an example ID. See
[`FINOVA_GENERALIZED_PLANNING_ENGINE_REPORT.md`](../FINOVA_GENERALIZED_PLANNING_ENGINE_REPORT.md)
and the reusable policy specification. The original phase evidence below remains
the record of the explicit-context implementation.

## Follow-up: one shared synthetic example

The normal interface now has one **Load synthetic example** button. The separate
optional-scenarios panel, three loader buttons and verbose context/count banner
were removed. Loading the existing 15-tooth table also loads separately authored
Macro objectives/targets, Micro catalog parameters and Nano stage/support records
from `examples/functional-all-in-one.json`. This preserves the original source
text, 105 positions, 103 numeric values and two missing values.

All three tabs share the same table, source hash and parse. Switching tabs selects
the appropriate supplied context and retains completed module reports. Editing
source/settings or clearing the input removes all example context and cached
reports, including when the edited text is subsequently pasted back unchanged.
Loading the example is local and causes no network/provider call. Ordinary pasted
tables continue without any silently attached context.

The shared preset contains six Macro targets, six Micro catalog concepts and
three Nano stages with 101 literal allocation records. All 97 compared source
fields match their supplied stage sums; three explicit phase-specific support
constraints pass the existing checks. Stage records are authored example data,
not a runtime-generated treatment schedule. The earlier three API fixtures remain
for regression coverage; the normal UI presents one case. The original phase
description and validation results below document the earlier implementation.
Follow-up verification evidence is in `evidence/unified-synthetic-example/`.

## Result

Implemented three distinct optional functional pathways alongside the existing
ordinary TMT analysis:

- **Macro:** objective-driven, source-bound modification proposals in Sagittal,
  Transverse, Vertical and Additional Considerations.
- **Micro:** deterministic tooth-wise attachment candidates, alternatives,
  supplied fictional dimensions/placement and explicit no-candidate outcomes.
- **Nano:** processing of actual supplied fictional stages, phase/group summaries,
  exact allocation checks and context-dependent fictional support strategies.

These are implemented decision/data-processing behaviors. They do not establish
clinical validity or proprietary PMCEASY algorithm equivalence. Every functional
plan has `clinical_authorized=false` and origin
`INDEPENDENT_SYNTHETIC_POLICIES`. The original 96-rule registry remains separate;
all 27 disabled predicates remain disabled. No deployment, commit or push was
performed.

## Inspection and architecture

Reviewed the existing PMCEASY functional research, gap matrix and roadmap, prior
`FINOVA_FINAL_ANALYSIS_QA_REPORT.md`, current module analysis, rule inventory,
clinical/semantic restrictions, supplied-detail contracts and Groq integration.
Graphify queries guided source navigation before implementation.

The parser and existing analytical ranking/grouping implementation are retained.
The new `backend/app/functional/` package contains typed scenario contracts,
independent deterministic policies, three scenario bundles and provider evidence
normalization. It reuses existing `Analysis` helpers, source references and
supplied stage/reference validation. It does not add a second parser, clinical
registry or semantic admission mechanism.

Pipeline:

```text
Original TMT -> existing parser + original unverified rule review
            -> optional explicit, source-hash-bound scenario context
            -> deterministic functional policies + immutable source-linked findings
            -> existing automatic constrained Groq wording / honest fallback
            -> FUNCTIONAL_DEMO_V1 report -> UI / Copy / TXT / local PDF
```

`InteractiveSubmission.planning_context` is optional. Reports add the complete
context and structured functional plan. JSON schemas were regenerated. The only
new API route is the read-only built-in scenario loader:
`GET /api/v1/interactive/scenarios/{scenario_id}`. Unknown scenarios return 404;
POST to that route remains disallowed. Existing ordinary and legacy supplied-detail
report pathways are retained.

The frontend adds a collapsed **Optional fictional planning scenarios** control.
Nothing loads automatically. A loader explicitly installs its own table and
context. Source/settings edits or a module change clear that context and stale
results. Ordinary TMT pasting requires no new form fields. Custom structured
contexts are supported by the typed API; this phase does not provide a general
manual catalog/stage authoring UI.

## Inputs, applicability and provenance

| Input | Requirement / behavior |
| --- | --- |
| Original TMT | Existing parser input, exact raw hash, source cells, Decimal strings, units, labels and missing-data provenance retained. |
| Functional context | Explicit scenario ID, matching module, version 1.0.0, source SHA-256 and fictional origin. No context is inferred from table contents. |
| Notation | FDI is a declared fictional grouping assumption; otherwise groups remain unassigned. An explicit conflicting source notation or comparison-as-total source is rejected. |
| Macro objectives/targets | A supported objective plus exact source-field replacement targets and coupled movement evidence are necessary for a positive proposal. Targets retain the source unit/direction label. |
| Micro catalog | A supported movement profile and supplied primary concept are necessary. Geometry, orientation, surface and local placement appear only if supplied; unknown parameters remain unknown. |
| Nano stages | Explicit ordered stage records and stage-bound allocations use the existing `review_details` contract. Phase membership and support assumptions are additional supplied context. |
| Nano arithmetic convention | `INCREMENTS_MATCH_SOURCE_LABELS` is required for group sums and source-total comparisons. Without it, those calculations are unavailable. |
| Nano support strategy | Requires a phase, explicit support/active roles, stationary-support assumption, assigned active movements and complete non-conflicting stage checks. |

Stale hashes, module mismatch, unknown/duplicate target references, conflicting
units/labels, duplicate catalog concepts, invalid scalars/Unicode and inconsistent
catalog geometry/orientation are rejected. Stage/reference/phase conflicts produce
explicit conflict outcomes and withhold stage calculations rather than repairing
or inventing data. Missing amounts remain unknown; explicit zero remains zero.

Every decision includes policy/version, applicability status, original source
references, supplied-context references, rationale, proposal, alternatives and
missing information. Each decision is linked to one immutable analytical finding.
Original parsed values are never overwritten by proposed replacements.

## Independent synthetic policies

There are **19 policy identifiers**, including insufficiency and scope policies.
Their exact conditions, precedence and assumptions are documented in
[`docs/FUNCTIONAL_SYNTHETIC_POLICIES.md`](docs/FUNCTIONAL_SYNTHETIC_POLICIES.md).
They are not additions to the clinical 96-rule registry.

| Family | Policies and implemented behavior |
| --- | --- |
| Macro, 5 | `DEMO-PLAN-{SAGITTAL,TRANSVERSE,VERTICAL,ANGULAR,CONTEXT}-v1`: explicit objective and distinct supplied target plus coupled nonzero components; dimension-specific technician requests, retain-source alternatives, applicability/insufficiency outcomes and unevaluated clinical modifications. |
| Micro, 8 | `DEMO-ATT-{COMBINED,ROTATION,ANGULATION,INCLINATION,VERTICAL,ZERO,INCOMPLETE,SCOPE}-v1`: complete angular evidence selects an authored categorical mapping; combined rotation/angulation precedes rotation, angulation and inclination; complete seven-field evidence is required for vertical-only and explicit-zero profiles. |
| Nano, 6 | `DEMO-STAGE-{DATA,MOVEMENT-ONLY,GROUP,CHECKS,SUPPORT,SCOPE}-v1`: supplied-stage binding, existing movement-only analysis reuse, compatible grouping, exact consistency checks, explicit-context support review and unsupported clinical conclusions. |

Micro supports generic rectangular, vertical rectangular, horizontal rectangular,
ellipsoid/oval, optimized-style category and fictional no attachment. Selection
uses component presence and documented precedence, never dataset rank, alternating
rows or invented clinical magnitude thresholds. A missing primary catalog option
withholds the primary; the alternative is not silently promoted. Optimized-style
parameters are not invented.

Nano sorts supplied orders and groups only compatible arch/tooth group, movement
family, unit and unchanged source label. Decimal sums use locally sufficient
precision, including under a deliberately reduced ambient Decimal precision in
tests. No total is divided into invented stages, no residual is filled and no
clinical limit or duration is calculated. Invalid phase overlap/reference/order/
unit metadata withholds the stage plan. Missing assignments, null amounts and
sum mismatches are reported explicitly. Incomplete/conflicting checks withhold
support proposals.

## Reproducible scenarios and before/after examples

### Macro: `macro-distribution`

The built-in scenario contains a complete 16-tooth upper-arch table: 112 positions
and 112 numeric values. Its separate context supplies three fictional objectives
and six replacement targets.

Previously, Macro could describe cross-tooth maxima and distributions. With this
explicit scenario, four positive policy decisions generate six concrete changes,
plus one clinical-context insufficiency decision. For example, Teeth 16 and 17
each have source mesiodistal `2.00 mm (D-labelled)` and nonzero angular companions.
The sagittal policy selects the supplied fictional `1.00 mm (D-labelled)` targets
and produces a technician request to replace those two fields. The alternative
retains source values and requests coupled-component review.

The other dimensions select supplied buccolingual targets for Teeth 11/21
(`1.60 -> 1.20 mm`, L-labelled), Tooth 12 vertical (`1.00 -> 0.80 mm`, I-labelled,
with separate `0.50 mm` relative-vertical evidence), and Tooth 11 rotation
(`2.00 -> 1.50 deg`, D-labelled). These targets are scenario inputs, not clinical
optimizations calculated from the TMT. IPR, extraction, surgery, auxiliaries and
clinical anchorage modifications remain unevaluated.

### Micro: `micro-catalog`

The scenario has eight teeth, 56 positions, 55 numeric values and one explicitly
missing value. Previously, Micro identified noteworthy teeth without selecting
specific options. It now produces these reproducible catalog outcomes:

| Tooth | Primary | Alternative / result |
| --- | --- | --- |
| 11 | Vertical rectangular | Horizontal rectangular; combined rotation/angulation policy. |
| 12 | Ellipsoid / oval | Generic rectangular; nonzero rotation policy. |
| 13 | Horizontal rectangular | Vertical rectangular; nonzero angulation policy. |
| 14 | Optimized-style category | Generic rectangular; geometry/orientation/surface/placement explicitly unknown. |
| 15 | Generic rectangular | Oval; complete zero-angular/nonzero-vertical profile. |
| 16 | No attachment in the fictional scenario | All seven source fields explicitly zero. |
| 17 | No supported candidate | Rotation missing; cannot treat it as zero. |
| 18 | No supported candidate | No supplied toy policy for its translation-only profile. |

For Tooth 11 the catalog explicitly supplies `2.000 x 3.000 x 1.000 mm`, vertical
orientation, buccal surface and `(0.000, 0.000, 0.000) mm` in an explicitly fictional
tooth-local frame. Those values are displayed unchanged. They are parameters,
not a fitted mesh or a validated placement. Eight tooth decisions plus one scope
decision are retained. The UI provides the requested five-column table and
expandable complete per-tooth findings.

### Nano: `nano-phases`

The scenario contains eight upper/lower teeth, 56 numeric source positions,
three supplied ordered stages/phases and 12 explicit allocation records. There
are nine source-field allocation comparisons; all nine match, including four
explicit-zero support fields. No duration is supplied or invented.

Previously, Nano described concentration and multi-component movement profiles.
With explicit stage context, Tooth 11's `1.00 mm` L-labelled buccolingual source
total is bound to supplied S1 `0.40 mm` and S2 `0.60 mm`. Tooth 31's `1.20 mm`
D-labelled mesiodistal total is bound to S1 `0.50 mm` and S2 `0.70 mm`. S3 contains
supplied Tooth 11 rotation `2.00 deg` and Tooth 41 angulation `1.00 deg`. Group
summaries and checks preserve those assignments and source labels.

Three supplied phase-specific support constraints produce fictional tracking/
review strategies: P1 support Teeth 16/36, P2 Tooth 26, P3 Tooth 46. Their roles
and stationary assumption come from explicit context, not an inference that
unassigned teeth are stationary. The engine checks roles against assigned active
movements and withholds inconsistent cases. No biological force, anchorage
prescription or treatment schedule is produced.

Without stages, ordinary Nano retains the previous movement-pattern analysis;
the explicit functional no-stage path also reuses that analyzer and reports the
missing stage/context requirements.

## Groq execution and privacy evidence

The automatic existing wording path receives deterministic decisions before
provider execution. Its additional payload contains aliased tooth/cell/stage/
phase references, fixed policy/status enums, exact supplied numeric parameters,
allocation checks and supplied support roles. Raw tables, free-text notes,
original identifiers, source hashes and credentials are not transmitted by this
normalizer. Existing synthetic-only transmission restrictions remain in force.

Groq performs constrained assembly/ordering of approved finding placeholders.
Every finding must occur exactly once in its own section; added prose, altered
numbers, invented geometry or schedules reject the batch. This is not independent
clinical reasoning or unrestricted paraphrasing. Deterministic policies and
arithmetic remain authoritative whether wording succeeds or falls back.

Actual configured live execution was performed once per scenario, model
`openai/gpt-oss-120b`, requested mode `AUTO`:

| Module | Attempts | Result | Accepted section comments |
| --- | --- | --- | --- |
| Macro | 1 | `GROQ_VALIDATED`, `GROQ_AI` | 4 / 4 |
| Micro | 1 | `GROQ_VALIDATED`, `GROQ_AI` | 2 / 2 |
| Nano | 1 | Provider HTTP 429, `GROQ_RATE_LIMIT`, `STANDARD_TEMPLATES` | 0 / 4; full deterministic plan retained |

Nano therefore proves an actual attempted request and honest rate-limit fallback,
not a live successful Nano response. No quota retries were made. Mocked successful
automatic calls pass for all three modules; mocked provider failures and invented
content also exercise deterministic fallback. Requested/attempted/validated/
fallback diagnostics preserve the prior safe backend fields without prompt or
credential logging. Fallback reports are labelled standard wording, never AI
generated. `real_patient_transmission_enabled=false` in all live records.

Evidence: [`live-summary.json`](evidence/functional-planning/live-summary.json),
[`live-diagnostics.txt`](evidence/functional-planning/live-diagnostics.txt),
[`mock-summary.json`](evidence/functional-planning/mock-summary.json) and complete
module `*-live.json` / `*-mock.json` snapshots in the same folder.

## Verification and export consistency

| Check | Observed result |
| --- | --- |
| Complete backend suite | **1,170 passed**; existing Starlette/httpx deprecation warning. |
| Final backend functional + route checks | **51 passed** after adding the last two comparison/notation guard tests. This focused run includes those additions; the earlier full-suite count does not. |
| Complete frontend suite | **290 passed**, 25 files. |
| Production TypeScript / Vite build | **Passed**; existing large-bundle size advisory remains. |
| Complete desktop/mobile browser suite | **112 passed**, including the previous analysis QA and six new scenario checks. |
| Functional browser export recheck | **6 passed** after the final Micro PDF header spacing adjustment; result recorded in `browser-focused-final.txt`. |
| PDF verification | Six PDFs, 2/3/3 pages for Macro/Micro/Nano on each viewport; exact embedded TXT/JSON, false clinical authority, source binding, original 96/27 ledger and every immutable finding visible in extracted text. |

Automated coverage includes policy applicability, missing objectives/targets,
unchanged targets, source/hash/module/notation mismatches, source units/directions,
all six catalog concepts, missing catalog/geometry, no-candidate cases, row-order
and nonzero-magnitude invariance, stage order/reference/unit/duplicate/phase
conflicts, missing/null allocation values, exact sums, sum mismatches, unknown
conventions and support conflicts. Provider tests reject added clinical prose,
geometry and timing, and verify privacy-normalized payloads and one-call behavior.
Frontend tests reject forged authority, source links, choices, targets, stage
amounts and accepted finding text, as well as functional metadata on legacy
report formats.

The original 15-tooth regression remains **105 positions, 103 numeric values,
two missing values and six explicit zeros**. Nano's BL upper-half qualifying
tokens remain exactly `{11,12,13,21,22,24,26}` at the `0.40 mm` boundary, each once.
The previous tie/group fix, equal-endpoint range formatting and successful-parse
wording with retained underlying missing-data classification remain intact.
No parser architecture or original analytical ranking code was changed here.

Browser checks use the real local API, all three explicit scenario loaders and
mobile/desktop viewports. They verify clinical isolation, expected visible
decisions, exact clipboard and TXT text, exact PDF embedded report/TXT, no API
calls during export, no horizontal page overflow and context clearing on source
edits. PDFs and JSON are saved under `evidence/functional-planning/pdfs/`.
Standalone PDF checks render every page and check all accepted findings, while
contact sheets support visual inspection. Micro header spacing was corrected
during this visual review. Complete source context, rules and provenance stay in
the attached JSON/TXT; the main UI shows human-readable tables and stage cards.

`graphify update .` completed its AST-only refresh (2,107 nodes, 6,594 edges).
Its environment reported that PDF text extraction was unavailable because its
own Python lacks pypdf; the separate bundled-Python PDF verification above passed.
`git diff --check` passed. Historical PDF fixtures rewritten by the broad browser
suite were restored to their pre-phase committed bytes; new functional evidence
is retained. No clinical registry, parser or environment/credential configuration
was changed.

Reproduction commands (from the repository root unless noted):

```powershell
backend/.venv/Scripts/python.exe -m pytest backend/tests -q
backend/.venv/Scripts/python.exe -m pytest backend/tests/test_functional_planning.py backend/tests/test_health.py -q
backend/.venv/Scripts/python.exe backend/scripts/verify_functional_planning.py
backend/.venv/Scripts/python.exe backend/scripts/verify_functional_planning.py --mock
# frontend working directory:
npm run test -- --run --maxWorkers=2
npm run build
npm run test:e2e -- --config=playwright.audit.config.ts --project=desktop --project=mobile --workers=2
```

`backend/scripts/verify_functional_pdfs.py` uses Python with pypdf/Pillow and
`pdftoppm`; the bundled Codex Python was used for the recorded verification.
`--live` on the scenario evidence script explicitly performs provider requests;
it is not required for offline regression checks.

## Remaining gaps and limits

- The 19 independent policies are authored fictional mappings, without clinical
  validation, patient-outcome evidence or proprietary PMCEASY equivalence.
- Macro applies supplied fictional targets under defined combined-evidence
  conditions; it does not discover a clinically optimal replacement plan.
- Attachment geometry is parameter display only. No CAD mesh, crown/root fit,
  retention validation, optimized-attachment specification or clinically suitable
  placement is calculated.
- Nano processes supplied stages and checks internal consistency. It does not
  optimize biological staging, calculate forces/timing, prescribe anchorage or
  establish treatment feasibility. Its support strategy is an explicit fictional
  review of supplied roles.
- Source notation/directions and increment semantics remain declared assumptions;
  the vendor verification/admission and clinical approval mechanisms are unchanged.
- Custom context authoring currently uses the structured API. The simple UI offers
  three complete built-ins and inspection, without a general scenario editor.
- Groq cannot introduce new facts or freely rewrite policy findings. Live Nano
  success was not demonstrated because the provider rate-limited its one request.

The implementation advances the functional demonstration while retaining the
existing distinction between source facts, supplied fictional assumptions,
independent simulated decisions and clinically authorized logic.
