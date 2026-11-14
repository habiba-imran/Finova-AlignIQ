# Graph Report - Finova AlignIQ  (2026-11-14)

## Corpus Check
- 213 files · ~611,150 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 2, .sha256 2, .example 1)

## Summary
- 1181 nodes · 4167 edges · 56 communities (40 shown, 16 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 267 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bbda55e4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- package.json
- domain/models.py
- test_parser.py
- test_semantics.py
- planning/demo.py
- ContextFields.tsx
- compilerOptions
- test_review.py
- services
- manifest.json
- attachments.ts
- test_reports.py
- json
- test_phase4.py
- App.assisted.test.tsx
- parse.ts
- review_table
- capture-public.mjs
- test_parser_finalization.py
- resolve
- test_sequencing.py
- planning.ts
- test_attachments.py
- vercel.json
- review/service.py
- review.ts
- test_phase5.py
- reports/service.py
- App
- sequencing.ts
- build_phase5_artifacts.py
- sequencing/models.py
- attachments/service.py
- App.tsx
- sequencing/service.py
- groq_client.py
- test_planning.py
- test_parse_api.py
- load_development_env
- ReportSettings
- execution_order
- fixture
- build-evidence-index.py

## God Nodes (most connected - your core abstractions)
1. `synthetic_review()` - 60 edges
2. `review_table()` - 59 edges
3. `EvidenceContract` - 58 edges
4. `GroqClient` - 46 edges
5. `parse_table()` - 45 edges
6. `parse_pipeline()` - 44 edges
7. `SourceContext` - 42 edges
8. `resolve()` - 42 edges
9. `RawTMTSubmission` - 38 edges
10. `assess_semantics()` - 37 edges

## Surprising Connections (you probably didn't know these)
- `create_sequencing_draft()` --uses--> `SequencingSubmission`  [INFERRED]
  backend/app/api/sequencing.py → backend/app/sequencing/models.py
- `fixed_scenario()` --uses--> `SequencingScenario`  [INFERRED]
  backend/app/sequencing/demo.py → backend/app/sequencing/models.py
- `test_schema_files_and_invalid_stage_kind()` --uses--> `SequencingSubmission`  [INFERRED]
  backend/tests/test_sequencing.py → backend/app/sequencing/models.py
- `test_schema_files_and_invalid_stage_kind()` --uses--> `EmptyDemoRequest`  [INFERRED]
  backend/tests/test_sequencing.py → backend/app/sequencing/models.py
- `test_inconsistent_or_missing_stages_withhold_only_dependent_notes_and_do_not_sum_totals()` --uses--> `StageWindow`  [INFERRED]
  backend/tests/test_sequencing.py → backend/app/sequencing/models.py

## Import Cycles
- None detected.

## Communities (56 total, 16 thin omitted)

### Community 0 - "package.json"
Cohesion: 0.05
Nodes (38): devDependencies, autoprefixer@10.5.4, jsdom@29.1.1, @playwright/test@1.64.1, postcss@8.5.28, tailwindcss@3.4.19, @testing-library/jest-dom@7.0.1, @types/react@19.3.0 (+30 more)

### Community 1 - "domain/models.py"
Cohesion: 0.08
Nodes (51): parse_submission(), AdapterInfo, AxisCoverage, Contract, LayoutInfo, ParsedMeasurement, ParseIssue, ParseResult (+43 more)

### Community 2 - "test_parser.py"
Cohesion: 0.15
Nodes (31): codes(), parse(), sample(), test_arch_conflict_and_scope_do_not_trigger_arithmetic(), test_audited_source_context_mismatches_withhold_semantics(), test_blank_lines_do_not_consume_declared_grid_cells(), test_decimal_comma_requires_explicit_claim_and_does_not_modify_raw(), test_deterministic_no_logging_network_or_file_writes() (+23 more)

### Community 3 - "test_semantics.py"
Cohesion: 0.07
Nodes (57): LexicalInput, SourceContext, WordingChoice, assert_fixture_matches(), CheckedFixture, FixtureVerificationError, load_manifest(), _read_artifact() (+49 more)

### Community 4 - "planning/demo.py"
Cohesion: 0.07
Nodes (19): planning_demo_draft(), planning_demo_input(), planning_draft(), require_demo(), private_validation_error(), PrivateIntakeMiddleware, create_draft_report(), health() (+11 more)

### Community 5 - "ContextFields.tsx"
Cohesion: 0.50
Nodes (4): ContextFields(), humanize(), labels, options

### Community 6 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, esModuleInterop, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+8 more)

### Community 13 - "test_review.py"
Cohesion: 0.12
Nodes (40): test_forged_clinical_or_technical_finding_is_suppressed(), test_global_provenance_failure_blocks_all_movement_facts(), test_missing_group_does_not_invalidate_general_inventory(), test_rule_local_mode_and_scope_metadata(), test_report_endpoint_limits_and_unknown_input(), by_rule(), observed(), submission() (+32 more)

### Community 14 - "services"
Cohesion: 0.15
Nodes (12): key, value, services, buildCommand, envVars, healthCheckPath, name, plan (+4 more)

### Community 17 - "attachments.ts"
Cohesion: 0.12
Nodes (19): AttachmentDesign, AttachmentDraft, AttachmentEntry, dimension(), isAttachmentDraft(), obj(), optional(), post() (+11 more)

### Community 18 - "test_reports.py"
Cohesion: 0.15
Nodes (34): GroqClient, retry_delay(), _assemble(), suppress(), batch_from_request(), envelope(), settings(), successful_client() (+26 more)

### Community 19 - "json"
Cohesion: 0.19
Nodes (15): synthetic_examples(), WordingBatch, build_prompt(), response_format(), wording_options(), private_json(), _unique_object(), validate_wording() (+7 more)

### Community 20 - "test_phase4.py"
Cohesion: 0.10
Nodes (43): ParserSettings, Association, PipelineSubmission, SyntheticFixture, authorized(), generate(), Generated, deterministic() (+35 more)

### Community 21 - "App.assisted.test.tsx"
Cohesion: 0.13
Nodes (15): @testing-library/react@16.3.3, vitest@4.1.12, EMPTY_CONTEXT, Component, digest(), isDraftReview(), nullable(), obj() (+7 more)

### Community 22 - "parse.ts"
Cohesion: 0.41
Nodes (11): Adapter, adapter(), isAutomaticParseResult(), isParseResult(), Measurement, nullableString(), object(), Span (+3 more)

### Community 23 - "review_table"
Cohesion: 0.15
Nodes (9): review_submission(), RawTMTSubmission, provenance_errors(), TestRuleContext, review_table(), emit(), unavailable(), write_examples() (+1 more)

### Community 24 - "capture-public.mjs"
Cohesion: 0.19
Nodes (6): images, manifest, root, batches, records, root

### Community 26 - "test_parser_finalization.py"
Cohesion: 0.10
Nodes (44): development_synthetic(), parse_assisted(), parse_automatic(), structural_prompt(), validate_proposal(), load_parser_settings(), AssistedSubmission, AutomaticParseResult (+36 more)

### Community 27 - "resolve"
Cohesion: 0.44
Nodes (3): binding(), issue(), resolve()

### Community 28 - "test_sequencing.py"
Cohesion: 0.14
Nodes (24): demo_input(), fixed_input(), draft_demo(), fixed_scenario(), SequencingDraft, test_dev_gate_cannot_be_enabled_from_production_or_similar_flags(), test_typed_contract_refuses_unsafe_states(), test_demo_disabled_by_default_and_exact_server_permission_required() (+16 more)

### Community 29 - "planning.ts"
Cohesion: 0.13
Nodes (21): Dimension, DIMENSIONS, eligibleComment(), isPlanningDraft(), object(), PlanningDraft, post(), requestDemoInput() (+13 more)

### Community 30 - "test_attachments.py"
Cohesion: 0.14
Nodes (24): attachment_demo_draft(), attachment_demo_input(), create_attachment_draft(), require_attachment_demo(), draft_demo(), input_demo(), AttachmentDemoInput, AttachmentDesign (+16 more)

### Community 31 - "vercel.json"
Cohesion: 0.29
Nodes (6): buildCommand, framework, installCommand, outputDirectory, rewrites, $schema

### Community 32 - "review/service.py"
Cohesion: 0.15
Nodes (15): rule_eligibility(), ObservedMeasurement, ReviewCoverage, RuleDefinition, RuleEvaluation, RuleRef, _build_registry(), _complete() (+7 more)

### Community 33 - "review.ts"
Cohesion: 0.13
Nodes (20): SourceClaim, CommentMode, isFinalDraftReport(), obj(), ReportComment, requestReport(), str(), strings() (+12 more)

### Community 34 - "test_phase5.py"
Cohesion: 0.16
Nodes (26): admit_test_context(), ExpectedCoverage, input_digest(), PairedTeeth, stage_errors(), StageRecord, ToothContext, context_for() (+18 more)

### Community 35 - "reports/service.py"
Cohesion: 0.31
Nodes (11): FinalDraftReport, GenerationInfo, ReportComment, comment_units(), CommentUnit, _eligible(), _export_text(), literal() (+3 more)

### Community 36 - "App"
Cohesion: 0.13
Nodes (15): requestParse(), App(), clearText(), editContext(), editRawText(), invalidateParse(), loadAttachmentDemo(), loadExample() (+7 more)

### Community 37 - "sequencing.ts"
Cohesion: 0.09
Nodes (31): AttachmentDemoInput, AutomaticParseResult, ContextClaims, ParseResult, DemoInput, DraftReview, isSequencingDraft(), KINDS (+23 more)

### Community 38 - "build_phase5_artifacts.py"
Cohesion: 0.15
Nodes (16): CandidateInputReadiness, ClinicalPreparation, IllustrativePolicy, IllustrativeResult, inspect_candidate_inputs(), preparation(), simulate_test_only(), AdditionalInputRequirements (+8 more)

### Community 39 - "sequencing/models.py"
Cohesion: 0.26
Nodes (13): require_demo(), sequencing_demo_draft(), sequencing_demo_input(), input_demo(), EmptyDemoRequest, FictionalArch, FictionalSegment, ScenarioStatement (+5 more)

### Community 43 - "attachments/service.py"
Cohesion: 0.27
Nodes (9): AttachmentDraft, AttachmentEntry, assemble(), _entry(), _export(), _guards(), supplied_entries(), unavailable_entries() (+1 more)

### Community 44 - "App.tsx"
Cohesion: 0.14
Nodes (13): dependencies, lucide-react@1.48.0, react@19.3.0, react-dom@19.3.0, MAX_TEXT_CHARACTERS, SyntheticFixture, humanize(), ParseResults() (+5 more)

### Community 45 - "sequencing/service.py"
Cohesion: 0.18
Nodes (9): create_sequencing_draft(), SequencingEntry, StageInspection, assemble(), entry(), export_text(), inspect_stages(), refs() (+1 more)

### Community 47 - "test_planning.py"
Cohesion: 0.17
Nodes (8): finish(), GroqResult, generate_report(), status(), test_demo_groq_success_minimal_payload_and_failure_template_fallback(), generate(), test_empty_dimensions_explain_unavailability_without_success(), handler()

### Community 49 - "test_parse_api.py"
Cohesion: 0.19
Nodes (6): payload(), test_exported_schema_is_current_and_decimals_serialize_as_strings(), test_invalid_requests_are_sanitized(), test_parse_contract_exact_decimal_raw_and_no_cache(), test_unknown_extra_keys_and_invalid_json_are_not_echoed(), test_unsupported_input_is_a_structured_abstention_not_http_failure()

### Community 50 - "load_development_env"
Cohesion: 0.27
Nodes (3): load_development_env(), main(), test_explicit_env_loader_has_no_evaluation_no_secret_output_and_process_precedence()

### Community 51 - "ReportSettings"
Cohesion: 0.47
Nodes (4): load_settings(), ReportSettings, test_environment_config_is_centralized_server_only_and_redacted(), test_prompt_size_and_invalid_secret_never_make_requests()

### Community 52 - "execution_order"
Cohesion: 0.50
Nodes (3): execution_order(), test_priority_topology_is_stable_and_input_gates_precede_descriptions(), test_dependencies_stable_and_order_independent()

### Community 53 - "fixture"
Cohesion: 0.50
Nodes (3): no_llm(), development_environment(), forbid_provider()

## Knowledge Gaps
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SourceContext` connect `test_semantics.py` to `domain/models.py`, `test_parser.py`, `test_phase5.py`, `planning/demo.py`, `build_phase5_artifacts.py`, `sequencing/models.py`, `test_review.py`, `test_reports.py`, `test_phase4.py`, `review_table`, `test_parser_finalization.py`, `test_attachments.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `review_table()` (e.g. with `RawTMTSubmission` and `TestRuleContext`) actually correct?**
  _`review_table()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.050170068027210885 - nodes in this community are weakly interconnected._
- **Why does `review_table()` connect `review_table` to `review/service.py`, `test_phase5.py`, `reports/service.py`, `test_semantics.py`, `build_phase5_artifacts.py`, `sequencing/models.py`, `attachments/service.py`, `sequencing/service.py`, `test_review.py`, `test_planning.py`, `execution_order`, `test_phase4.py`, `test_parser_finalization.py`, `resolve`, `test_sequencing.py`, `test_attachments.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `GroqClient` (e.g. with `generate_report()` and `live()`) actually correct?**
  _`GroqClient` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Should `domain/models.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07517182130584192 - nodes in this community are weakly interconnected._
- **Why does `RawTMTSubmission` connect `review_table` to `review/service.py`, `domain/models.py`, `test_parser.py`, `test_semantics.py`, `planning/demo.py`, `reports/service.py`, `build_phase5_artifacts.py`, `sequencing/models.py`, `test_review.py`, `test_planning.py`, `test_parse_api.py`, `test_phase4.py`, `test_parser_finalization.py`, `test_sequencing.py`, `test_attachments.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._