# Phase 1.5 semantic verification and normalization readiness

Status: infrastructure implemented; **vendor mappings disabled**. Authentic captures: **0**. Independently reviewed vendor gold outputs: **0**. Approved vendor releases: **0**. No clinical rule engine or Phase 2 work is included.

All three complete documents in `docs/`, `PARSER_PHASE1.md`, both existing JSON schemas and the complete parser were reviewed before implementation. Those documents and the Phase 1 wire contracts remain unchanged. No missing vendor semantics were replaced by assumptions.

## Contract review: lexical versus semantic

| Existing data | What Phase 1 establishes | What it does not establish |
| --- | --- | --- |
| Raw text, SHA-256, cell/header/tooth spans | Exact submitted logical text and code-point provenance | Original clipboard-internal bytes, authenticity or patient identity |
| Decimal, raw sign, magnitude | Complete-token scalar syntax and precision, including explicit zero | Physical direction, motion, biological meaning or achieved movement |
| Unit and recognized label | Explicit unit spelling/alias and English label family | Source-specific axis equivalence, implicit units, coordinate transforms or root torque |
| Tooth token, notation/dentition/arch claims | Raw identifier and syntax under a declared convention | Verified notation, anatomical identity, tooth status or a numbering conversion |
| Source/version and adapter candidate | Selected/explicit textual claims, not a verified signature | Vendor compatibility or support for an unknown version |
| Plan mode, basis, scope, stage/frame claims | User-supplied metadata retained independently | Source-confirmed reference basis, stage timing, total/cumulative equivalence or valid plan arithmetic |
| Coverage and field states | Declared positions and lexical zero/missing/invalid/ambiguous distinctions | Full vendor axis coverage, no-movement conclusions or clinical review outcomes |
| Existing canonical fields | Intentionally null/false | Any clinically meaningful canonical normalization |

## Architecture

```text
LexicalInput -> deterministic parser -> existing ParseResult v1 (unchanged)
                                         |
Authorized offline manifest + exact capture/expected/source-evidence artifacts
  -> strict contracts, path/size/hash checks, independent review metadata checks
  -> exact lexical oracle comparison -> immutable CheckedFixture snapshot
                                         |
Code-reviewed release registry (EMPTY) ----+
                                         v
Separate assess_semantics() -> per-component verification / partial abstention
  -> SemanticAssessment, retaining the entire original lexical snapshot
```

New package: `backend/app/semantics/`.

- `models.py`: strict immutable evidence/manifest/oracle/assessment contracts and readiness invariants.
- `fixtures.py`: read-only artifact checking and a pytest helper with static, non-content-bearing failures.
- `registry.py`: empty code-controlled approved/revoked release digests. No manifest field, metadata claim, environment flag or source dropdown enables a release.
- `normalization.py`: evidence-scoped field projection, dependency/context gates and partial abstention. No vendor maps are defined here or in the source-adapter candidates.

The first provider is an **exact curated-fixture oracle**, not a general vendor adapter: it can project only independently reviewed component assertions for the identical raw text, full context, parser/adapter/schema versions and lexical result of a released fixture. It does not extrapolate to a new input, a similar label, a different tooth, a new version or another basis/mode/stage. A future generalizing adapter needs actual source fixtures, explicit mappings, independently reviewed oracles and a separate code-reviewed release. The existing ClinCheck/SureSmile candidates remain lexical/negative-check extension points with no verified versions.

`LexicalInput` now holds the parser's internal data contract. `RawTMTSubmission` inherits it and retains the same strict true synthetic-data confirmation requirement for HTTP requests. This small internal separation lets an authorized future offline capture be checked without falsely calling authentic evidence synthetic.

## Field verification and abstention

Each measurement has explicit components for source application/version, tooth identity/notation/dentition/arch, axis/unit/sign/direction, mode/basis/scope, stage index/kind, coordinate frame and comparison operands/operation. Every component records its original claim, canonical value or null, verification status, evidence locator/hash/release references, input references, source spans and abstention reasons.

- No accepted proof: `UNKNOWN`, null canonical value, explicit reason. Nothing is filled from a user claim.
- Contradictory source/context, incompatible basis, unit conflict, invalid tooth claim or unresolved duplicate: affected dependencies abstain; independently evidenced fields are retained.
- A missing/invalid number never gains a direction or canonical magnitude. Explicit zero stays distinct in the lexical snapshot; zero is not permission to invent a physical direction.
- `VERIFIED` requires real reviewed artifacts **and** a code-approved release digest. Review metadata alone is not release authority. Revocation overrides approval.
- Neutral synthetic tests use only `TEST_ONLY` application/opaque test identities/axes/directions. These cannot become vendor VERIFIED or canonical-measurement-ready, even when placed in an approval set. `evidence_complete_for_test` tests dependency wiring only.
- Complete canonical measurements require all relevant components verified. Stage-specific/cumulative/incremental scopes additionally require stage index and kind, including an explicitly evidenced zero stage. Comparison requires distinct operand plans and a source-reported operation, and retains a comparison value kind rather than an absolute prescription.
- Unknown scope cannot be complete. Unsupported/incomplete lexical measurements cannot yield a canonical magnitude. Overall verification cannot hide unresolved partial lexical input.
- New/unclassified plan modes cannot default to absolute movement. The initial readiness vocabulary classifies only the documented Align Final, Doctor Final and Comparison canonical modes; other source modes are retained but need an explicitly reviewed classification/extension before readiness. The opaque TEST_PLAN_MODE exists only in neutral plumbing tests.

No unit conversion, basis transform, sign inversion, rotation composition, stage summation, total/stage-count division, plan subtraction, treatment observation or clinical recommendation is implemented. Even a source-reported comparison value is never computed by this layer.

## Fixture framework and schemas

The authoritative empty catalog is `backend/vendor_verification/manifest.json`. The adjacent PENDING example is a template with no capture, reviews, hashes, mappings or expected clinical values. There is deliberately no purported authentic gold-output file. Expected-output contracts/helpers are ready; real gold must be independently authored and reviewed after actual captures exist.

Full workflow and exact sample/metadata checklist: [vendor verification README](backend/vendor_verification/README.md).

New generated schemas:

- `schemas/vendor-fixture-manifest.v1.json`
- `schemas/vendor-fixture-expected.v1.json`
- `schemas/semantic-assessment.v1.json`

These describe structure. Pydantic cross-field validators, artifact checking and the release registry enforce additional invariants; JSON Schema alone does not authenticate evidence or approve normalization.

The manifest requires real capture/source version and operator metadata, consent/de-identification references, exact raw/expected/source-evidence hashes, and two distinct approving reviewers independent of the capture operator, including an orthodontist. Each review binds all three hashes and real timezone-aware dates. Software checks integrity and declared review consistency; the responsible organization must authenticate reviewer identities, qualifications, capture authenticity and authorization. This is technical evidence governance, not clinical approval or a regulatory workflow.

The CLI reads an explicitly authorized local artifact root, preserves UTF-8 bytes and newlines, checks bounded sizes, refuses path traversal/absolute/URL/escaping-symlink paths, and prints only static codes/counts. It never creates, copies, logs or transmits captures. Temporary test assets are invented text created by test helpers only. No new application persistence or external service is introduced.

## API and frontend compatibility decision

No new HTTP routes, request options, response fields, frontend controls or canonical-display claims are necessary while no vendor release exists. `/api/parse`, `ParseResult.schema_version=1.0.0`, both original JSON schemas, synthetic-data confirmation, safe raw rendering, and the existing frontend response validator are preserved. The health response remains `phase: 1`, its existing public contract.

The semantic layer is offline/library-only and is **not invoked by `/api/parse`**. This preserves the distinction between a lexical result and a semantically verified one. Future online normalization should use an explicit versioned/opt-in contract after evidence exists, rather than reinterpreting existing null/false fields or widening the UI's verification claims silently.

## Commands

Existing install/run/build commands remain in [README](README.md). From `C:\Finova AlignIQ\backend`:

```powershell
.\.venv\Scripts\python.exe scripts\export_schemas.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\verify_vendor_fixtures.py
```

The last command intentionally exits **2**, `NO_AUTHENTIC_ORACLES`, with the shipped catalog. That is an open verification gate, not vendor verification success. Future local read-only fixture checks use `--manifest` and `--fixture-root` as documented in the verification README. A successful check still does not activate mappings.

From `C:\Finova AlignIQ\frontend`:

```powershell
npm test
npm run build
npm run test:e2e
```

## Remaining verification work

For each exact supported version/copy surface/locale, obtain actual ClinCheck Align Final/Doctor Final/Comparison and crown/root views; actual SureSmile crown-center/cusp-tip and incremental/cumulative/stage views; all intended notation/dentition/arch/axis/sign/direction/missing/zero variants; raw serialization plus independently checked source UI, context, per-field gold values and review records. Capture stage-zero/passive/overcorrection states and comparison operands where available. Never manufacture a vendor variant that does not exist. The detailed matrix specifies required metadata and how to mark unsupported variants.

Then validate exact oracles, resolve uncertainty per field, define actual versioned mappings without cross-vendor assumptions, and approve the scoped release digest through code review. Authentic compatibility remains **unverified** until that work is completed. No Phase 2 work has begun.

## Final validation

- Backend: **192 passed**, preserving all 120 Phase 1 tests and adding 72 evidence/readiness tests.
- Frontend: **30 passed**; production TypeScript/Vite build passed with unchanged frontend source.
- Browser integration: **12 passed** at 1440, 1024, 768 and 375 px, using a freshly started backend.
- `pip check`: no broken requirements. Original documents and both Phase 1 schema files retained their hashes.
- Default fixture CLI: intentionally `NO_AUTHENTIC_ORACLES`, exit 2; zero reviewed captures and zero vendor releases. This is an unmet evidence gate, not compatibility validation.
- The frontend suite needed normal process access after sandbox workers timed out before collecting tests; the rerun passed. One existing upstream Starlette TestClient deprecation warning remains. No product tests are failing.

Tests use neutral synthetic semantics. No authentic vendor oracle or clinically meaningful vendor normalization was claimed or tested. The separate approved-release path still requires real independently reviewed evidence; all production mappings remain disabled.
