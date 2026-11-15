# Synthetic analytical rules v1

These rules describe records in synthetic tables. They have no clinical validation,
vendor authority or relationship to proprietary PMCEASY algorithms. They do not
activate or replace any of the 96 registry rules or 27 disabled clinical predicates.

## Comparable evidence

Use recognized lexical movement families with an explicit matching unit (mm for
translation/vertical families; deg for angular families). Exclude missing, invalid,
ambiguous, duplicate-field and unknown-unit entries from comparisons. Preserve
Decimal strings, raw signs, directions, units and spans in the parsed record.
Rank absolute recorded magnitudes within each family only, retaining ties. Do not
convert M/D/B/L/E/I labels to signs or infer their anatomical interpretation.
Relative vertical and absolute vertical fields are never added together.

Maximum/range findings cite the complete comparable population and their selected
cells. Coverage findings identify unavailable cells and explicitly limit rankings
to available entries. Repeated profiles show up to two highest-magnitude sets of
three or more equal entries per family; they are descriptive patterns only.

FDI-style permanent token syntax (quadrants 1–4, positions 1–8) supports explicitly
unverified upper/lower and anterior/posterior grouping. A conflicting explicit
numbering claim or other token format stays unassigned. No lower-arch finding is
created unless lower-arch-style tokens actually occur. No group is a verified
anatomical assertion.

## Macro

Five sections: mesiodistal, buccolingual, vertical, angular and overall summary.
Compare maxima, ranges, source-label distributions and repeated profiles.
Show group coverage and available-data limitations; do not print every cell.

## Micro: independent illustrative rules

`DEMO-ANGULAR-RANK-v1`: shortlist the two largest distinct nonzero magnitudes in
each angular family. Rank teeth by number of dataset family maxima, then number
of shortlisted components, then lexical token for stable ties. Display at most
five profiles. A family maximum produces an illustrative family-control candidate;
two or more maxima produce a combined-angular candidate and the alternative of
reviewing components separately. Shortlisted runner-up-only teeth receive an
illustrative alternative. A candidate means a review topic, not an attachment
indication or selected shape. All facts causing the highlight are cited.

`DEMO-ZERO-ANGULAR-v1`: a complete unambiguous three-family angular profile with
three explicit zeros permits a **no candidate in the angular-only screen** example.
Show at most one such example. It never means no attachment is clinically needed.
Missing angular evidence never qualifies as zero or no candidate. Without usable
profiles the candidate remains unknown. Geometry, placement and orientation are
never calculated. Selection depends on evidence and is invariant to tooth row order.

## Nano

Show available arch/group coverage. For each translation or vertical family,
select the upper half of nonzero comparable position magnitudes with all boundary
ties retained; split these into disclosed token group/source-label concentrations,
showing up to three largest groups. Repeated profiles retain the original labels.

For multi-component review select the upper quarter of nonzero magnitudes in
each family, ties retained. Show at most four teeth with two or more selected
components, sorted by component count then lexical token. Half/quarter selection
uses index `(n-1)//2` / `(n-1)//4` in descending values. These ranks describe this
dataset; they are not clinical thresholds.

`DEMO-REVIEW-ORDER-v1`: illustrate reviewing translations, then vertical patterns,
then overlapping profiles. This is an order for inspecting information only, not
an order of delivering movements. No stages, durations, forces or anchorage are
calculated from totals.

## Wording and supplied records

Ordinary input follows parsed TMT → deterministic findings and evidence → one
automatic Groq wording call when configured → closed placeholder validation →
shared UI/PDF/TXT content. Findings contain complete immutable local sentences.
The provider can arrange those sentences within their sections. It receives
normalized measurement evidence and opaque references, never raw tables, arbitrary
tooth labels, patient notes or supplied free text. Any changed/missing/duplicate/
cross-section fact or extra model claim rejects the entire batch. One request,
no automatic repair call. Rate limits/errors preserve the complete deterministic
analysis and are honestly labelled standard wording. Logs contain event names,
module enums, fixed outcome codes and counts only.

Existing optional supplied attachment/stage detail reports keep their independent
source-bound review path and original validation. They do not become calculated
attachment or stage plans. The lexical parser and clinical registry are unchanged.
