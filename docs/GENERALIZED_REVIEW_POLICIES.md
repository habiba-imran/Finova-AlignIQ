# Input-driven planning review policies — version 1.0.0

These independent engineering/simulation policies run on parsed supported tables;
they do not match fixture IDs, predefined answers or enrolled source hashes.
They are separate from the original 96-rule clinical registry. Their plans always
have `clinical_authorized=false`; vendor semantics and all 27 disabled predicates
remain unchanged. A source hash binds supplied context to its table; it does not
authorize clinical use or vendor semantics.

## Contracts and activation

The normal UI submits `planning_options` with default values automatically.
No optional form or example load is required. API callers can request this path
with `planning_options: {}`. Omitting that field retains the earlier API behavior
for compatibility. Explicit `planning_context` examples remain a separate path;
the two request fields cannot be combined.

The evaluated context has `origin=INPUT_DRIVEN_POLICY_REVIEW`, the actual parsed
source SHA-256 and `scenario_id=null`. It records the selected concept catalog,
objectives, supplied stage conventions and optional explicit targets. The
request's `planning_options` separately records user choices, including an
explicit arithmetic illustration method. No input-driven request needs a scenario
identifier. Clients cannot submit a derived context to the legacy scenario path.

Mode defaults to `SYNTHETIC_REVIEW` in this synthetic demonstration. The optional
`EVIDENCE_REVIEW` mode retains factual reviews and stage arithmetic but suppresses
toy attachment selections, numerical modification illustrations and fictional
support strategies. Neither mode can enable clinically authorized output.

Explicit targets/catalog specifications/stages/phases/support constraints or an
arithmetic example require `planning_options.source_sha256` to equal the current
table hash. Changing source/settings clears all module context and cached reports.
Each module keeps its own options for that same source. The single example loader
explicitly supplies its own case data; manually pasting identical text does not
load its geometry, objectives or stages.

## Macro: six new policy IDs

`DEMO-PLAN-INPUT-{SAGITTAL,TRANSVERSE,VERTICAL,ADDITIONAL}-v1`:

1. Compare only unambiguous parsed/explicit-zero cells with the recognized field's
   expected unit. Each lexical family is assessed separately; absolute/relative
   vertical values are never added or collapsed.
2. For nonzero magnitudes, sort descending and select the element at zero-based
   index `(n-1)//2` as the upper-half boundary. Keep **every** value at or above
   that boundary, including every tie. This is a within-table prominence criterion,
   not a clinical movement limit or severity threshold.
3. Report selected tooth tokens, exact boundary, recorded maxima and unchanged
   source-label counts. Identify nonzero coupled components at those teeth.
4. Produce a technician review request for that field/distribution, plus a
   retain-source or separate-component/source-convention review alternative.
   No numerical replacement is implied by a rank.
5. A family with no usable values gets a missing-information outcome. Comparable
   explicit zeros do not become nonzero flags; missing data remain separate.

`DEMO-PLAN-INPUT-TARGET-v1` supports either an explicitly supplied replacement or
an opt-in `HALF_MAGNITUDE` arithmetic illustration for a user-selected source cell.
A positive illustration requires synthetic mode, a matching objective, a declared
source-label convention, a distinct usable value and a compatible total-source
mode. Comparison-as-total data cannot authorize a replacement. The half method
divides the exact signed Decimal scalar by 2 and retains the opaque source label;
it is **not** a clinically justified target. Overlong values are withheld rather
than rounded or truncated. Missing/unusable source values never become quantities.

`DEMO-PLAN-INPUT-SCOPE-v1` records the limits of relative ranking and withholds
clinical IPR, extraction, surgery, auxiliaries and anchorage prescriptions.

## Micro: nine new policy IDs

All positive angular decisions require a compatible total-movement source and
exactly one unambiguous rotation, angulation and inclination value in degrees.
Known comparison values cannot establish no attachment, including when every
comparison cell is zero. For combined profiles, compare
absolute angular magnitudes **within that tooth**, not across the dataset.

| Policy suffix after `DEMO-ATT-INPUT-` | Condition | Illustrative category / alternative |
| --- | --- | --- |
| `ROTATION-v1` | Rotation is the sole or unique largest nonzero angular component. | Oval / vertical rectangular. |
| `ANGULATION-v1` | Angulation is the sole or unique largest nonzero angular component. | Horizontal rectangular / vertical rectangular. |
| `INCLINATION-v1` | Inclination is the sole or unique largest nonzero angular component. | Optimized-style category / generic rectangular. |
| `TIED-ANGULAR-v1` | Two or more nonzero angular components tie for largest magnitude. | Vertical rectangular / generic rectangular. |
| `VERTICAL-v1` | Complete seven-field profile, zero angular values and a nonzero vertical component. | Generic rectangular / oval. |
| `ZERO-v1` | All seven required source fields are usable and explicitly zero. | No attachment in this fictional screen only. |
| `TRANSLATION-ONLY-v1` | Complete profile, zero angular/vertical values and nonzero translation. | `NO_CANDIDATE`: no supported shape policy for that profile. |
| `INCOMPLETE-v1` | Required angular or seven-field evidence is incomplete/ambiguous. | `INSUFFICIENT_INFORMATION`, with required fields identified. |
| `SCOPE-v1` | All inputs. | Limits of the toy mappings and absent geometry/clinical suitability. |

These categorical choices are independently authored simulations, not clinical
indications or comparative performance claims. A repeated category is appropriate
when the same documented profile condition repeats; types never alternate by row,
tooth number or dataset rank. Changing a tooth's dominant component can change its
selection without changing unrelated rows. Missing values cannot win a comparison
or qualify as zero.

Default catalog entries are **concepts only**: all dimensions, orientation,
surface and placement are null. User-supplied specifications overlay those concepts
unchanged. `SUPPLIED_OPTIONS_ONLY` can restrict selection to supplied entries;
missing primaries are withheld rather than replaced by arbitrary alternatives.
Optimized-style never implies an invented optimized design. Placement coordinates
use only the explicitly supplied fictional local frame; no fitted mesh or clinical
placement is computed.

## Nano: four new policy IDs and reused stage policies

- `DEMO-STAGE-INPUT-GROUPS-v1`: reuse the existing source-token group counts.
  FDI-style syntax is a grouping assumption; conflicting/other notation remains
  unassigned.
- `DEMO-STAGE-INPUT-COUPLING-v1`: group teeth with at least two usable nonzero
  components and issue a coordination-review priority. This does not assert
  simultaneous movement or a treatment order.
- `DEMO-STAGE-INPUT-OUTLINE-v1`: create inspection topics for available translation,
  angular and vertical patterns. Translation/vertical concentrations reuse the
  existing complete arch/source-label grouping, including all boundary ties and
  single-value range formatting. Angular comparisons use degrees and retain
  source-label counts. Unavailable topics are omitted.
- `DEMO-STAGE-INPUT-EMPTY-v1`: explicitly request missing comparable data where
  there is no supported review topic.

`functional_plan.review_outline` is separate from `functional_plan.stages`.
Each outline item has `origin=ILLUSTRATIVE_REVIEW_OUTLINE` and
`stage_allocations_generated=false`. There are no stage amounts, treatment-stage
counts, durations or force predictions in an outline. The topic order is for
inspection, not treatment delivery.

Actual supplied stages/allocations reuse the existing `DEMO-STAGE-{DATA,GROUP,
CHECKS,SUPPORT,SCOPE}-v1` processing and reference/unit/order/phase checks. Amounts
are never filled from source totals. Exact group sums and field-total comparisons
require `INCREMENTS_MATCH_SOURCE_LABELS`; otherwise they remain unavailable.
Unknown amounts stay unknown, explicit zeros remain zero, conflicting metadata
withholds calculations, and residuals are not repaired. All arithmetic uses
Decimal with locally sufficient precision.
Known comparison sources cannot be relabelled as totals by a user-selected
increment convention; their stage calculations and support strategies are withheld.

Support considerations require explicit phase/support/active roles and a fictional
stationary-support assumption, assigned active movements and complete consistent
stage checks. Missing/moving/conflicting support or evidence-only mode withholds
the strategy. Even a positive result is a tracking/review strategy, without a
clinical anchorage prescription or force estimate.

## Groq and complete output evidence

Deterministic decisions precede the existing automatic single-call wording path.
Only normalized fields, aliases, policy/status identifiers and approved finding
references are eligible for transmission. Raw text, free-form patient/case notes,
original tooth/stage/phase identifiers and credentials stay out of the payload.

Repeated source references use shared dictionaries. Stage datasets above 32
records use bounded stage metadata and allocation-status counts for wording;
complete allocations remain local. If the request still exceeds the unchanged
24,000-byte limit, a bounded summary of source counts and immutable finding
identifiers replaces duplicated numerical evidence. This is a transport budget,
not a clinical threshold. No additional provider call or retry is introduced.

The provider may arrange sealed finding references only. Each finding must occur
exactly once in its own section; invented prose/numbers/geometry/stages reject the
batch. Complete source values, uncertainty, decisions, optional inputs and policy
references remain in UI details, TXT and PDF attachments even in the bounded path.
Diagnostics accurately distinguish requested, attempted, validated and fallback
states, without logging prompts or secrets. Standard fallback is never labelled
AI-generated. The provider does not supply independent clinical reasoning.
