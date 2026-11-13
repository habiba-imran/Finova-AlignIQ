# Phase 1 deterministic parser contract

This is an internal synthetic-data lexical parsing prototype. It recognizes explicit table structure and complete numeric tokens. It does not verify vendor semantics, produce clinical observations/recommendations, or satisfy the authentic-vendor-fixture release gate.

## Governing material reviewed

Before Phase 1 code changes, all contents and tables of these three files were read completely:

- `docs/FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md`
- `docs/Orthodontic_TMT_Independent_Critical_Audit(2).md`
- `docs/FINOVA_ARCHITECTURE_BLUEPRINT.md`

The audit and blueprint are now supplied as Markdown, rather than DOCX. No required document was unreadable or missing in this phase. These source documents were not modified. Authentic vendor clipboard fixtures remain absent. The current user authorization permits the Phase 1 synthetic parser; it does not authorize activating vendor semantic mappings or proceeding to Phase 2.

## Architecture

```text
Explicit Parse Table action + synthetic-data confirmation
    -> same-origin POST /api/parse via local Vite proxy
    -> byte limit + strict Pydantic submission contract
    -> raw logical text + SHA-256 of submitted UTF-8 text
    -> lossless cell/line spans
    -> exactly one explicit header, delimiter, and orientation
    -> complete-token Decimal parsing + label recognition
    -> source candidate / metadata contradiction checks
    -> raw tooth token + notation-claim syntax checks
    -> duplicate retention, coverage and clarification fields
    -> typed lexical result, with source semantics UNVERIFIED
    -> React raw/lexical preview, warnings, provenance and JSON
```

Responsibilities:

| Module | Responsibility |
| --- | --- |
| `backend/app/domain/models.py` | Strict versioned Pydantic contracts, field states and engineering limits |
| `backend/app/api/privacy.py` | Bound bodies before JSON decoding, no-store headers, sanitized validation errors |
| `backend/app/api/parse.py` | HTTP transport only |
| `backend/app/parser/tokenize.py` | Original line/cell tokens and code-point spans |
| `backend/app/parser/layouts.py` | Deterministic header/orientation/delimiter detection; no closest-match repair |
| `backend/app/parser/labels.py` | Explicit English label aliases and explicit unit suffixes; not canonical axes |
| `backend/app/parser/values.py` | Full-token decimal/unit/literal-direction extraction |
| `backend/app/parser/teeth.py` | Syntax under declared FDI/Universal notation; no conversion or anatomical mapping |
| `backend/app/parser/adapters/` | Separate versioned ClinCheck/SureSmile candidates and audited negative context checks |
| `backend/app/parser/service.py` | Composition, duplicate preservation, partial results, coverage and abstention |
| `frontend/src/api/parse.ts` | Same-origin explicit request and response-shape checks |
| `frontend/src/components/` | Optional context claims and structured lexical results |

Audited G/N input safeguards are applied as parser validation, without a rule-evaluation engine. No D/R observations, clinical policies, observations endpoint, report generation, LLM, ML, authentication, database or persistence is included.

## HTTP and JSON Schema

Routes are `GET /api/health` and **`POST /api/parse`**. The latter follows the user's requested path, replacing the blueprint's planned `/api/v1/tmt/parse` spelling. There is no `/analyze` endpoint or second parse alias. Public Swagger/OpenAPI/ReDoc routes remain disabled.

Machine-readable contracts generated directly from Pydantic:

- `schemas/parse-request.v1.json` — validation schema.
- `schemas/parse-result.v1.json` — serialization schema; Decimal fields are strings or null.
- `frontend/src/test/fixtures/synthetic-parse-result.json` — complete invented example response used by UI tests, not vendor evidence.

Request example (synthetic only):

```json
{
  "raw_text": "# SYNTHETIC\nTooth\tRotation (deg)\n13\t−1.2300 M\n",
  "source_claim": "Unknown",
  "context": {
    "notation": "UNKNOWN",
    "plan_mode": "UNKNOWN",
    "reference_basis": "UNKNOWN",
    "scope": "UNKNOWN",
    "decimal_separator": "DOT"
  },
  "synthetic_data_confirmed": true
}
```

`context` also accepts bounded source-version, coordinate-frame, pseudonymous case/plan claims, dentition, arch and a nonnegative stage index. Optional absent context stays unknown/null; no plan/case identities are invented. Client-provided verification flags and other extra fields are rejected. All context remains `USER_CLAIMS_UNVERIFIED` even when syntax is valid. All enum values are listed in the request schema.

The response preserves `raw_text`, `raw_sha256`, `source`, `layout`, `teeth`, `measurements`, `coverage`, `issues`, `clarification_fields`, and `unparsed_lines`. Each measurement retains raw label/value/number/sign/unit/direction/suffix, signed Decimal, nonnegative magnitude Decimal, explicit unit claims, field statuses, provenance and duplicate membership. `source.context` retains the submitted plan mode, basis, scope and stage. Explicit source-line claims retain raw/span evidence in `source.claim_evidence`; supplied metadata is separately marked as unverified user claims.

Example measurement excerpt, not the complete response schema:

```json
{
  "raw_value": "−1.2300 M",
  "raw_number": "−1.2300",
  "signed_decimal": "-1.2300",
  "magnitude_decimal": "1.2300",
  "raw_sign": "−",
  "raw_direction": "M",
  "header_unit": "deg",
  "unit": "deg",
  "numeric_status": "PARSED",
  "field_status": "SEMANTICS_UNKNOWN",
  "semantics_verified": false,
  "canonical_axis": null,
  "canonical_direction": null,
  "mapping_id": null
}
```

Decisions and limitations:

- `signed_decimal` is a lexical scalar, not a signed physical direction. `magnitude_decimal` uses `Decimal.copy_abs()` without context-dependent rounding. All trailing numerical precision survives JSON as a string. Original spelling remains in the raw tokens.
- `recognized_label` is an English lexical label family. It never populates `canonical_axis`. In particular, torque is not silently equated with inclination, nor crown inclination with root movement.
- Normalized tooth IDs, canonical axes/directions and mapping IDs are always null in this implementation. `semantics_verified` and adapter `verified` remain false. There are no verified vendor versions.
- Positions in `SourceSpan` use **zero-based Unicode code-point offsets**, end exclusive. Physical line and column numbers are **one-based**, with column end exclusive. These are not UTF-16 indexes. Every present cell span slices the unmodified submitted text exactly. Omitted trailing cells have null raw values/spans; empty cells have a present empty token/span.
- The hash covers submitted logical text encoded as UTF-8, not clipboard-original bytes. Browser textarea newline canonicalization still applies before submission. API submissions otherwise retain CR, LF and CRLF exactly.
- No arithmetic between measurements, coordinates, plans, totals, cumulative values or stage counts occurs.

## States and coverage

Overall statuses: `PARSED_UNVERIFIED` (recognized structure and lexical values, never source verification), `PARTIAL`, `UNSUPPORTED`, `INVALID`.

Numeric statuses: `PARSED`, `EXPLICIT_ZERO`, `MISSING`, `NOT_PRESENT`, `INVALID`, `AMBIGUOUS`. Field states separately retain `SEMANTICS_UNKNOWN`, `EXPLICIT_ZERO`, `NOT_PRESENT`, `PARSE_INVALID`, `UNSUPPORTED`, `AMBIGUOUS`. These do not represent rule evaluation or clinician report approval states. An explicit zero with unknown semantics remains numerically zero and semantically unverified.

Missing kinds preserve blank, dash, not-reported, literal N/A token, and omitted trailing cell separately. N/A is only a token category; it does not prove an axis/tooth is clinically inapplicable. No missing token becomes zero; a missing tooth column proves no tooth status.

Coverage counts refer only to declared table positions. Counts can overlap (an unsupported label may also have an explicit numerical zero). `expected_axes` is null because no verified vendor coverage profile exists. Measurements and issues identify individual clarification needs; a failed field does not remove unrelated parsed fields.

Duplicate keys use current context claims (case, plan, basis, scope, stage), raw tooth token and lexical label family. Repeated positions/aliases are retained, assigned a duplicate group, and marked ambiguous. Differing lexical values raise a parsing conflict. Identical values are also retained; repeated columns could represent unconfirmed plan comparisons. No merging, summation or last-value-wins behavior is used.

## Supported structural variations

| Variation | Behavior |
| --- | --- |
| Teeth in rows | Explicit Tooth/Teeth/Tooth ID/Tooth Identifier corner and at least one recognized movement header |
| Teeth in columns | Movement/Movements/Axis/Measurement, Tooth, or empty corner, with tooth header tokens and a recognized movement row |
| Delimiters | Tabs, semicolons, pipes, or runs of two or more ordinary spaces/NBSP; one delimiter per table |
| Spacing | Uneven run widths and outer indentation retained; cell-local whitespace interpreted only in derived tokens |
| Blank lines | Retained in raw text and provenance; skipped structurally |
| Newlines | LF, CRLF and CR; API raw string is not normalized |
| Units | Explicit degree/deg/degree/degrees/° or mm/millimeter/millimetre variants in a cell or suffix header; conflicts are flagged |
| Numbers | ASCII digits, optional +/ASCII minus/Unicode minus, decimal dot; comma decimal only with explicit COMMA claim |
| Labels | Rotation/rot/rotate, inclination/incl, angulation/ang, intrusion/intrude, extrusion/extrude, explicit buccolingual/B-L and mesiodistal/M-D label variants, vertical and translation/displacement; exact alias list is in `labels.py` |
| Missing values | Empty, whitespace-only, dash variants, N/A/NA, ? and omitted trailing explicit-delimiter cells retain distinct missing kinds |
| Partial label recognition | Unknown labels remain unsupported positions alongside independent recognizable positions |
| Source text | Exact standalone `Source: ClinCheck` or `Source: SureSmile` is a claim/candidate signal only |

## Unsupported or withheld variations

- Single-space column guessing, fixed-width reconstruction, arbitrary OCR/prose, long-form Tooth/Movement/Value tables, CSV/quoted fields, multiline cells, Markdown outer-pipe/separator rows, implicit merged cells, and multiple tables/cases per submission.
- Ragged multi-space rows: positions cannot be recovered reliably after empty columns collapse. Entire affected rows are retained unassigned. Extra-column or mixed-delimiter rows are also unassigned. Explicit-delimiter short rows can retain known positions and mark absent trailing cells, but separators never reconstruct an unknown omitted middle cell.
- Missing units are not inferred from movement type. Unsupported units are not converted. Unknown suffixes, grouping separators, scientific notation, NaN/Infinity, formulas and embedded markup are not accepted as numeric values.
- Missing/unverified notation is not inferred from numeric ranges or platform selection. FDI/Universal syntax checks under an explicit claim do not verify source notation or tooth anatomy. Palmer normalization, supernumerary identifiers and externally meaningful tooth-status tokens are not supported.
- Every ClinCheck and SureSmile **semantic adapter remains unverified**, including apparently familiar layouts and plausible version strings. Generic lexical structure recognition is not manufacturer compatibility.

## Engineering limits and privacy

These are resource limits, not clinical thresholds: 1 MiB HTTP request body, 100,000 Unicode code points of raw text, 2,000 physical lines, 128 columns, 10,000 possible grid cells, 2,000 characters per cell/header, 128 characters per numeric token, and a stage-index claim in 0–2,147,483,647. They are explicit initial defaults for review. The frontend never truncates raw input; it disables Parse above its text limit. Backend limits return validation errors or typed structural issues without truncation. The UI uses a 20-second request timeout, paginates measurements by 25 positions, and expands issue visibility in batches of 50; the full response remains in memory.

Only the user's checked synthetic-data confirmation and explicit Parse Table action transmit content. The API independently requires a strict true confirmation value. Editing raw text revokes confirmation; editing text/source/context or Clear/demo revokes any result and aborts stale requests. No retries happen automatically.

No raw input/metadata is stored, logged by application code, placed in browser storage, or sent to third parties. The backend handles requests in memory. Validation errors deliberately omit input values, unknown field names and malformed JSON excerpts. Responses use `Cache-Control: no-store`. Uvicorn runs with access logging disabled in documented commands. Do not put patient data in URLs, terminals or configuration. Infrastructure/browser/OS handling is outside this development prototype; synthetic confirmation is not PHI detection or a production privacy certification.

## Vendor verification requirements

1. Obtain authorized, consented/de-identified **verbatim** clipboard captures for exact target product versions. Screenshots alone and these synthetic fixtures do not verify serialization.
2. Independently double-review captures against source UI: numbering/dentition/arch, raw movement labels, units/precision, sign/direction for each tooth/arch/axis, source version, plan/comparison mode and operands, reference basis, stage/scope, missing/excluded/zero variants and coverage.
3. Create version-specific oracle records and unsupported/version-drift fixtures. Include transposes, reordering, both arches, mirror signs, crown/root/cusp differences, locale and comparison/staged variants.
4. Approve exact mappings and provenance, register supported versions explicitly, and require zero silent reinterpretations on supported oracles. User claims must never bypass source validation.
5. Review local consent/PHI handling and technical resource limits before broadening data use. Vendor verification is separate from clinical approval. Clinical logic remains outside Phase 1.

The authentic-vendor Phase 1 exit gate remains open. No Phase 2 implementation has begun.

Implementation references: [Pydantic decimal serialization](https://docs.pydantic.dev/latest/api/standard_library_types/#decimals), [FastAPI validation-error handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/), and [Vite server proxy](https://vite.dev/config/server-options.html#server-proxy).
