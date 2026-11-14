# Finova AlignIQ — Phase 7: Attachment Interface

14 November 2026, Asia/Karachi. **Engineering prototype with supplied synthetic examples — not clinical validation.** Phase 7 stops at Micro attachment review; Nano/Sequencer remains unavailable.

## Delivered workflow and observed scope

**Micro → paste/inspect TMT → Run Attachment Review → tooth-indexed table → clinician review → DRAFT copy/TXT export.** The shared automatic parser, raw preview, exact lexical values, source indicators and missing/unsupported states remain available. Macro keeps its existing Planning Assistant, dimension organization, selection/export and fixed demo. Purpose changes retain text but cancel requests and invalidate prior results/authority. Review purposes are not aligner stage numbers.

Phase 6A public demonstration frames V01 210/220/240 seconds and V02 330 seconds support a paste/display step and textual tooth-indexed attachment output with candidates, alternatives and explicit no-attachment entries. GAP15 is reproduced as an independent **presentation and review workflow**, with an executable illustrative scenario. This is not a clone of protected graphics, exact UI, proprietary descriptions or an attachment library. Original Finova DEMO_TILE labels and invented toy shapes are used.

GAP16's observed dimension/orientation/location wording can be represented by the new typed contract, but **clinical geometry/placement remains blocked by independently verified data and validation**. The demonstration supplies labeled toy values; the application does not calculate them from movements. No dedicated PMCEASY 3D editor or automatic write-back was established by the public evidence, and none is implemented. No statement of current paid-product parity or clinical equivalence is made.

## Typed API and provenance

New owning modules:

- `backend/app/attachments/models.py`: strict frozen contracts, Decimal dimensions, supplied design/category IDs, optional shape/orientation/placement/surface/stage references, tooth-wise entries and complete DRAFT.
- `backend/app/attachments/service.py`: lexical projection, existing engine/safety integration, conservative unavailable rows, supplied-scenario binding and deterministic exact TXT assembly.
- `backend/app/attachments/demo.py` and `fixtures/`: read-only fixed demonstration input, scenario hash and semantic evidence validation.
- `backend/app/api/attachments.py`: normal intake and separately gated development routes.
- `frontend/src/api/attachments.ts` and `components/AttachmentWorkspace.tsx`: checked transport, tooth-indexed interface, evidence details, lifecycle/error handling and local export.

| Route | Input | Result and authority |
| --- | --- | --- |
| `POST /api/v1/attachments/draft` | AttachmentSubmission: original raw text, source/context claims, synthetic confirmation, optional Phase 4 recovery receipt | AttachmentDraft; normal semantic gates, only UNKNOWN/WITHHELD entries in the current unreleased vendor environment. |
| `POST /api/v1/development/attachment-demo/input` | Empty object | Fixed parsed AttachmentDemoInput; server-only synthetic table, no user text. |
| `POST /api/v1/development/attachment-demo/draft` | Empty object | Revalidated fixed synthetic scenario and engine-backed AttachmentDraft. |

Both development routes require **FINOVA_ENVIRONMENT=development** and **FINOVA_ATTACHMENT_DEMO_ENABLED=true**. The flag defaults false; production refuses it even when true. The Macro demo flag is independent. Neither body nor query/browser claims can enroll uploaded data. Unknown body fields are rejected by strict contracts and sanitized errors. Existing body limits, no-store/nosniff headers, in-memory processing and source/receipt binding remain. Invalid/expired receipts require reparsing; invalid fixed evidence produces a static 503 without disclosing paths or data.

The schema deliverables are `schemas/attachment-request.v1.json`, `attachment-draft.v1.json`, `attachment-demo-input.v1.json` and `attachment-demo-request.v1.json`. Existing public contracts and parser/rule policies are preserved.

Each review entry contains:

- Original token and internal tooth reference. `verified_tooth` is a reserved nullable field and is always null in this phase because no approved verified attachment path exists. A separate `synthetic_tooth` is permitted only with exact TEST_ONLY movement identity/evidence; it is never shown as verified clinical anatomy.
- CANDIDATE, ALTERNATIVE, NOT_INDICATED, UNKNOWN or WITHHELD, plus explicit SUPPLIED_SYNTHETIC versus WITHHOLDING_GUARD origin.
- Optional independently supplied design/category and geometry fields. Candidate/alternative/no-attachment decisions require synthetic evidence and authorized observation references. Unknown/withheld cannot carry a design, geometry, placement or alternative.
- Linked alternatives constrained to a candidate on the same original tooth. No superior option is chosen.
- Separate lexical measurement IDs, authorized observation IDs, scenario/semantic evidence locators and actual engine safeguard finding IDs. Safeguards are explicitly **not candidate-triggering predicates**.
- Explanation, missing prerequisites, NOT APPROVED and DRAFT status. No fake clinician signature, approval or policy ID is invented.

Both backend and frontend reject malformed identity/evidence, contradictory result/geometry combinations, missing references, cross-tooth alternatives, unknown references, duplicate entries and approval/provider promotion. The report retains the full immutable engine review and all 96 evaluations. Report IDs hash validated content excluding self-referential IDs/export text. Exact Decimal spelling and evidence locators are preserved in serialized output and TXT.

## Existing engine and safeguards

Normal attachment review recomputes the original table through the existing receipt resolver/parser and **review_table(... requested_assessments=(ATTACHMENTS,))**. This activates the existing requested-assessment withholding report, not an attachment clinical predicate. The public contract has no supplied findings, decisions, policy or test-only fields.

The 96-rule registry and semantic release registry are unchanged: **66 engineering handlers/guards, 27 disabled clinical predicates, 3 deferred controls**. A01–A04 and R15 remain DISABLED / NOT APPROVED; A05 continues the exact-placement withholding guard, A06 blocks universal superiority and H08 reports missing plan/policy/geometry. G16/G17 and N08/N09/N10/N13 provenance, locality, coordinate and eligibility protections are retained. Raw parsing never creates attachment necessity, omission or geometry. An explicit zero or a large rotation is not a decision trigger.

For ordinary data, rows with lexical numeric information are UNKNOWN; missing/unsupported measurement rows are WITHHELD. Both retain null design/geometry/placement/verified identity. Unsupported/empty tables produce a systemic WITHHELD entry rather than invented teeth. More than 256 tooth tokens or 512 movement positions produces an explicit engineering-limit withholding entry rather than silently dropping teeth. No-attachment is never the fallback for absent information.

## Reproducible supplied demonstration

`scripts/build_attachment_demo.py` authors a fixed `SyntheticScenario` under `backend/app/attachments/fixtures/`. The scenario JSON has an independently stored SHA-256 and binds to the exact raw digest of the existing Phase 6B synthetic table. Runtime uses the same checked raw/expected fixture, read-only verifier, semantic assessor and real rule engine. It validates scenario schema/hash/input identity, authorized observation IDs and alternative relationships before producing a response. No runtime fixture writing, persistence or arbitrary scenario upload exists.

| Original opaque token | Result | Supplied demonstration content |
| --- | --- | --- |
| 11 / DEMO_11 | CANDIDATE | DEMO_TILE_A, original toy prism label, dimensions **2.000 × 1.250 × 0.500 mm**, DEMO_LONG_AXIS orientation, DEMO_SURFACE_A / DEMO_SCHEMATIC_V1, optional DEMO_WINDOW_A reference. |
| 11 / DEMO_11 | ALTERNATIVE | DEMO_TILE_B, toy oval label, linked to the same-tooth candidate; unspecified dimensions/placement stay null. |
| 12 / DEMO_12 | CANDIDATE | DEMO_TILE_C category/design example; unspecified geometry stays null. |
| 13 / DEMO_13 | NOT_INDICATED | Explicit supplied fictional no-attachment decision, with its own scenario locator. Never inferred by the engine. |
| 14 / DEMO_14 | UNKNOWN | Authorized synthetic movement identity exists; it does not determine attachment need. No design or placement. |
| 15 | WITHHELD | No authorized synthetic movement identity; original token retained, no canonical clinical identity or attachment choice. |

These are **independently authored demonstration inputs, not approved orthodontic policies**. The existing tokens are opaque identifiers, not FDI/Universal anatomical mappings. The toy surface/window labels establish no dental surface, clinical placement feasibility, stage kind, timing or schedule. No true stage dataset, tooth mesh or attachment library is supplied. The existing four eligible TEST_ONLY movement positions and field-specific abstention remain intact. Supplying a candidate does not override A05/H08; engine findings still withhold real clinical geometry and decisions.

The demonstration uses actual HTTP routes and validation, not a screenshot or client-only mock. Replaying even the exact table through normal intake yields UNVERIFIED and no candidate/no-attachment result. Editing text/context, clearing input, revoking confirmation or switching purpose removes the loaded demo state and results. Pending operations are aborted and revision-checked; late responses cannot reinstate authority or exports.

Rebuild with `backend/.venv/Scripts/python.exe backend/scripts/build_attachment_demo.py --frontend-fixtures` from the repository root, or follow [README startup/rebuild commands](README.md#attachment-interface--micro-review). This regenerates only invented repository assets and actual deterministic frontend response fixtures. No provider key is required.

## Interface, wording and export

Micro shares Finova's existing React/Tailwind design, teal palette, typography, Lucide icons, raw input and parser preview. The new table has original-tooth headers, explicit result badges, candidate/alternative links, supplied no-attachment labels and expandable geometry/evidence/missing-prerequisite details. Desktop/tablet tables scroll locally with sticky headings; narrow screens stack each tooth's cells into labeled blocks while preserving table semantics. Keyboard users can focus the region and disclosure controls. Loading, empty, disabled-demo, error and explicit retry paths are present. The result heading receives focus after rendering. Macro remains independently usable; Nano remains an unavailable informational module.

The clinician-review section explains missing clinical indication/actual plan/geometry and states that no sign-off is recorded. It is not an approval control. Entries are immutable and not editable. Neither copy nor download constitutes approval.

This module deliberately uses **deterministic templates only**, with provider=null and attempts=0, including the demonstration. The existing Groq approved-wording vocabulary concerns descriptive movement findings; it is not repurposed as authority for attachment decisions. No Groq/other-provider path is introduced, and there is no LLM output that can create a design, geometry, necessity or superiority claim. Existing Macro wording and structural fallback services/keys/gates remain unchanged. No live Groq call is made in verification.

Copy and TXT download preserve the server's exact complete UTF-8 export: DRAFT/prototype labels, explicit synthetic or unverified domain, report/input hashes, original/synthetic/unknown identity, every result and origin, exact supplied geometry, alternative links, evidence/measurement/finding refs, missing prerequisites, authorized movement evidence, all 96 rule evaluations and all limitations. Blob URLs are revoked and filenames contain a nonpatient report digest only. Clipboard errors leave a usable report/export preview. Exports trigger no backend/provider/CAD request. Windows clipboard newline serialization is handled in tests; downloaded content is compared exactly.

## Verification and remaining limitations

| Check | Result |
| --- | --- |
| Complete backend pytest | **882 passed**: 828 retained + 54 new attachment cases. |
| Complete frontend tests | **154 passed**: 132 retained + 22 new attachment cases, including the final narrow-screen layout. |
| Playwright Chromium / real API | **68 passed**, including the final standalone run after the narrow-screen layout improvement. 56 retained journeys and 12 new Micro journeys at desktop/laptop/tablet/mobile widths. |
| TypeScript / production build | Passed (`tsc --noEmit && vite build`). |
| JSON schemas | All four match owning Pydantic contracts in automated tests. |
| Dependency consistency | `pip check` clean; all direct npm dependencies resolve. |
| Advisory checks | npm: **0 vulnerabilities**. Pinned Python requirements: **no known vulnerabilities** via isolated pip-audit; no project dependencies added or changed in Phase 7. |
| Graphify / diff / visual QA | Final `graphify update .` completed AST-only/no LLM: **1090 nodes, 3817 edges, 49 communities**. `git diff --check` passed. Desktop and final mobile screenshots inspected; small-screen tooth blocks are readable without sideways clipping. |

Coverage includes complete real demo flow, supplied candidates/alternatives/no-attachment distinction, unknown/withheld normal data, missing values/unsupported vendors, zero/large magnitudes, exact geometry/provenance/export, all 96 rule states and disabled attachment predicates, no provider calls, strict body/test-only/geometry injection refusal, production demo refusal, corrupted scenario and wrong input binding, stale receipts/results, copy/download failures, local export privacy, purpose switching, Macro regression and Nano exclusion. Existing tests are retained; only prior expectations that Micro was unavailable were intentionally updated for the now-functional interface. A broad evidence-text selector initially matched several rows and was corrected to identify the candidate evidence being asserted; validation assertions were not weakened.

Initial schema comparison needed explicit UTF-8 file decoding on Windows. The synthetic generator constructs Decimal instances explicitly under the existing strict models. No clinical guard was relaxed for either correction. A later responsive verification run passed 67 browser tests but timed out once before a laptop page's navigation rendered, while a build/test command was running concurrently; the full browser suite was rerun on its own without increasing timeouts or enabling retries. Upstream Starlette/httpx deprecation and NO_COLOR/FORCE_COLOR warnings are non-failing. Python audit is bounded to the fully pinned requirements file and warns that hashes are absent. Graphify skipped unsupported extensions (including CSS and scenario.sha256) and noted no modeled symbols in two browser test files during the initial refresh; this is a code AST refresh, not semantic-document extraction.

No authentic vendor capture, production attachment mapper, approved clinical indication/omission/alternative policy, validated geometry/contact engine, actual attachment plan importer, 3D editor, real-patient cloud handling, authentication/persistence, CAD integration or Sequencer is delivered. GAP15's illustrative workflow is usable; real clinical content remains data/policy blocked. GAP16 remains clinically and geometrically unvalidated. The Phase 6A observation limits and corrected clinical audit continue to govern. No phase after 7 is started.
