# Independent functional demonstration policies, version 1.0.0

The normal client workflow now uses the reusable input-driven policies in
[GENERALIZED_REVIEW_POLICIES.md](GENERALIZED_REVIEW_POLICIES.md), without loading
an example. The policies below describe the retained explicit-context/example
path and its regression fixtures.

These are original software demonstration policies, not validated orthodontic
rules or reconstructions of PMCEASY internals. Their results always have
`clinical_authorized=false`, origin `INDEPENDENT_SYNTHETIC_POLICIES` and an explicit
source-table SHA-256 binding. They never enter the 96-rule clinical registry or
authorize vendor semantics, TEST_ONLY admission or clinical approval.

## Required and optional inputs

Ordinary pasted synthetic TMTs require no new fields and retain their existing
Macro/Micro/Nano analytical behavior and numerical QA fixes. Functional behavior
requires an explicit optional `planning_context` on the interactive request:

- Required: scenario ID, policy version 1.0.0, source SHA-256 and matching module.
- Declared notation (`FDI` or `UNVERIFIED`) is an assumption, not verified anatomy.
- Macro: closed fictional objective(s) and exact source-bound replacement targets.
- Micro: explicitly supplied catalog options, including any fictional geometry,
  orientation, surface and local placement frame/coordinates.
- Nano: existing `review_details.stages` and `review_details.allocations`, optional
  phase membership and support constraints. Stage-to-total comparisons/group sums
  additionally require `INCREMENTS_MATCH_SOURCE_LABELS` as an explicit convention.

Targets bind measurement IDs and retain the source's explicit unit and direction
label. A missing source, conflicting unit/label, duplicate target/catalog entry,
module mismatch or stale source hash prevents a functional request. Invalid Unicode,
an explicit comparison-as-total request or a contradictory notation claim also
prevents scenario evaluation. The increment convention is an explicit fictional
assumption that stage amounts refer to each source-field total with its label
retained; it does not release vendor semantics. Non-decimal/non-finite scalar
strings, inconsistent orientation or geometry on a
no-attachment option are rejected. No user input can authorize clinical output.

The normal UI has one explicit **Load synthetic example** button. It loads the
existing 15-tooth table together with separately authored module contexts from
`examples/functional-all-in-one.json`. All three tabs share the same source and
parse; switching tabs selects only the corresponding supplied context. Editing
source/settings or clearing the table removes all example context and cached
reports. No scenario data are inferred or silently attached from a matching table alone.
Stage amounts/assignments are literal preset records in that asset; runtime never
constructs a sequence from total TMT values. The three earlier module-specific
fixtures remain available for API regression coverage, without extra normal-UI loaders.
Custom structured contexts use the same API contracts; no large intake form is
required for ordinary analysis. Legacy supplied-detail reports remain separate.

## Macro policies

| Policy | Deterministic applicability | Action / alternative |
| --- | --- | --- |
| DEMO-PLAN-SAGITTAL-v1 | REDISTRIBUTE_TRANSLATIONS objective; supplied mesiodistal target different from an unambiguous nonzero source value; another nonzero angular component at that tooth. | Propose the supplied target as an explicitly fictional technician request. Otherwise no proposal / state missing data. Retain original values as the alternative. |
| DEMO-PLAN-TRANSVERSE-v1 | Same objective/conditions for a buccolingual target. | Same source-bound target proposal, scoped to transverse fields. |
| DEMO-PLAN-VERTICAL-v1 | VERTICAL_REVIEW objective; distinct supplied target and nonzero absolute/relative vertical companion. | Change only the specified field to its supplied target; retain separate absolute/relative fields and request independent component review as the alternative. |
| DEMO-PLAN-ANGULAR-v1 | ANGULAR_CONTROL objective; distinct supplied angular target and another nonzero angular component. | Source-bound illustrative angular change; no independent target/limit calculation. |
| DEMO-PLAN-CONTEXT-v1 | Always reports the unsupported clinical domain. | Explicitly withhold IPR, extraction, surgery, auxiliaries and clinical anchorage modifications; require independent assessment, records and approved policy. |

Targets are supplied inputs, not calculated clinical limits. No magnitude cutoff,
risk class, overcorrection factor or clinical safety threshold is invented. Each
decision includes selected source evidence, coupled-component values, objective
and target references, applicability status, specific proposal and alternative.
The original parsed values are never overwritten by proposed changes.

## Micro policies and catalog

The catalog has six concepts: generic rectangular, vertical rectangular,
horizontal rectangular, ellipsoid/oval, optimized-style category, and fictional
no attachment. Alternatives refer to another supplied catalog concept. Catalog
geometry is parameter data only, not a fitted mesh, validated placement or a
proprietary optimized-attachment specification. Geometry never comes from Groq.

Policies are evaluated by component presence (nonzero/zero), with combined
rotation/angulation taking precedence, then rotation, angulation and inclination.
The ordering is an explicitly authored toy mapping, not a clinical preference.

| Policy | Condition | Primary / alternative |
| --- | --- | --- |
| DEMO-ATT-COMBINED-v1 | Complete three-field angular profile; rotation and angulation both nonzero. | Vertical rectangular / horizontal rectangular. |
| DEMO-ATT-ROTATION-v1 | Nonzero rotation without angulation. | Oval / generic rectangular. |
| DEMO-ATT-ANGULATION-v1 | Nonzero angulation without rotation. | Horizontal rectangular / vertical rectangular. |
| DEMO-ATT-INCLINATION-v1 | Rotation and angulation zero; inclination nonzero. | Optimized-style category / generic rectangular; missing geometry remains explicit. |
| DEMO-ATT-VERTICAL-v1 | Complete seven-field profile; all angular fields zero and a vertical component nonzero. | Generic rectangular / oval. |
| DEMO-ATT-ZERO-v1 | Complete seven-field profile; every entry explicitly zero. | No attachment **within this fictional scenario only**; no clinical absence claim. |
| DEMO-ATT-INCOMPLETE-v1 | Angular evidence incomplete or no supported categorical profile. | No supported candidate; identify missing evidence or policy. |
| DEMO-ATT-SCOPE-v1 | All scenarios. | Scope/clinical-suitability limitation. |

A missing primary catalog option withholds that primary; an alternative remains
an alternative, not an automatic substitute. Shape selection never uses tooth
index, alternating rows, dataset maximum/runner-up rank or an undocumented clinical
threshold. Reordering rows or changing nonzero magnitudes cannot change selections
unless component presence changes. Unknown evidence never qualifies as zero.

Only supplied parameters are shown. Built-in shapes have clearly fictional
dimensions/placement; optimized-style geometry and orientation remain unknown.
No attachment option can imply validated retention, root control or suitability.

## Nano policies

| Policy | Processing |
| --- | --- |
| DEMO-STAGE-DATA-v1 | Require explicit stages/amount records. Reuse legacy reference/order/unit/duplicate guards. Conflicting metadata withholds all stage calculations. |
| DEMO-STAGE-MOVEMENT-ONLY-v1 | Without stage records, reuse existing movement distributions/concentrations/multi-component analysis. Do not create stages. |
| DEMO-STAGE-GROUP-v1 | Sort supplied stage order; bind supplied phase; group records by arch/tooth group, family, unit and unchanged source label. Preserve amounts, including explicit zero and unknown. Sum complete compatible records only under the declared convention. |
| DEMO-STAGE-CHECKS-v1 | Detect conflicting/overlapping phase metadata, unknown references, duplicate stages/orders/allocations, missing amounts, missing nonzero assignments and stage-total mismatches. Report exact sums without filling residuals or changing records. |
| DEMO-STAGE-SUPPORT-v1 | Require a named phase, explicit support/active groups, stationary-support assumption, actual nonzero active assignments, no moving support-group member, and complete non-conflicting stage checks. Generate only a fictional tracking/review strategy. Withhold conflicting/incomplete cases. |
| DEMO-STAGE-SCOPE-v1 | No stage count, timing, biological force, clinical staging limit or anchorage prescription inferred from totals. |

All sums use Decimal arithmetic with locally sufficient precision. Amounts are
never obtained by dividing total TMT values. Different families/directions/units
are not merged. Source-total comparison is conditional on explicit compatible
increment conventions; it never proves treatment feasibility. Stage durations are
shown only if supplied. Absent support assignments do not prove stationary teeth;
stationarity is an explicit fictional assumption, not a computed clinical fact.

## Groq and output contract

The existing automatic one-call wording path receives normalized source evidence
and approved deterministic decisions, exact targets/catalog parameters, supplied
stage amounts, allocation checks and aliased support roles. Free text, original
tooth/stage/phase identifiers, patient notes, raw input and credentials stay local.

Groq can arrange immutable approved-finding placeholders within sections. Every
reference must occur exactly once in its own section; additional language,
altered numbers, geometry or schedules reject the whole batch. Policy choices and
arithmetic are never delegated to the provider. Honest deterministic fallback
retains every plan fact. Existing requested/attempted/validated/fallback diagnostics
and no-retry behavior are preserved.

`FUNCTIONAL_DEMO_V1` reports retain the original parse, unverified 96-rule review,
explicit context, structured decisions, catalog choices, ordered stages, exact
allocation checks and every source reference. UI tables/details and PDF consume
the same immutable findings; Copy/TXT and PDF attachments retain full provenance.
