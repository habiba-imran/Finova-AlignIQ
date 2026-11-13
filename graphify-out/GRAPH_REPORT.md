# Graph Report - Finova AlignIQ  (2026-11-14)

## Corpus Check
- 141 files · ~240,458 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 2, .example 1, .ini 1)

## Summary
- 909 nodes · 3165 edges · 30 communities (21 shown, 9 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 227 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3e877d17`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- package.json
- domain/models.py
- test_parser.py
- test_semantics.py
- main.py
- App.tsx
- compilerOptions
- test_review.py
- services
- manifest.json
- test_reports.py
- review.ts
- test_phase4.py
- App.assisted.test.tsx
- parse.ts
- test_parser_finalization.py
- @playwright/test
- scripts
- vercel.json
- reports/service.py
- FinalReport.test.tsx
- dependencies

## God Nodes (most connected - your core abstractions)
1. `synthetic_review()` - 60 edges
2. `review_table()` - 47 edges
3. `parse_table()` - 43 edges
4. `GroqClient` - 43 edges
5. `parse_pipeline()` - 42 edges
6. `SourceContext` - 37 edges
7. `EvidenceContract` - 37 edges
8. `assess_semantics()` - 37 edges
9. `automatic_parse()` - 35 edges
10. `write_synthetic_fixture()` - 35 edges

## Surprising Connections (you probably didn't know these)
- `parse_automatic()` --uses--> `PipelineSubmission`  [INFERRED]
  backend/app/api/automatic_parse.py → backend/app/parser/contracts.py
- `parse_submission()` --uses--> `ParseResult`  [INFERRED]
  backend/app/api/parse.py → backend/app/domain/models.py
- `parse_submission()` --uses--> `RawTMTSubmission`  [INFERRED]
  backend/app/api/parse.py → backend/app/domain/models.py
- `review_submission()` --uses--> `DraftReview`  [INFERRED]
  backend/app/api/review.py → backend/app/review/models.py
- `SourceAdapter` --uses--> `SourceContext`  [INFERRED]
  backend/app/parser/adapters/base.py → backend/app/domain/models.py

## Import Cycles
- None detected.

## Communities (30 total, 9 thin omitted)

### Community 0 - "package.json"
Cohesion: 0.09
Nodes (29): devDependencies, autoprefixer@10.5.4, jsdom@29.1.1, postcss@8.5.28, tailwindcss@3.4.19, @testing-library/jest-dom@7.0.1, @types/react@19.3.0, @types/react-dom@19.3.0 (+21 more)

### Community 1 - "domain/models.py"
Cohesion: 0.09
Nodes (38): parse_submission(), AdapterInfo, AxisCoverage, LayoutInfo, ParsedMeasurement, ParseIssue, RawCell, SourceInfo (+30 more)

### Community 2 - "test_parser.py"
Cohesion: 0.15
Nodes (31): codes(), parse(), sample(), test_arch_conflict_and_scope_do_not_trigger_arithmetic(), test_audited_source_context_mismatches_withhold_semantics(), test_blank_lines_do_not_consume_declared_grid_cells(), test_decimal_comma_requires_explicit_claim_and_does_not_modify_raw(), test_deterministic_no_logging_network_or_file_writes() (+23 more)

### Community 3 - "test_semantics.py"
Cohesion: 0.07
Nodes (51): LexicalInput, assert_fixture_matches(), CheckedFixture, FixtureVerificationError, load_manifest(), _read_artifact(), verify_fixture(), Artifact (+43 more)

### Community 4 - "main.py"
Cohesion: 0.07
Nodes (9): private_validation_error(), PrivateIntakeMiddleware, health(), HealthResponse, payload(), test_invalid_requests_are_sanitized(), test_parse_contract_exact_decimal_raw_and_no_cache(), test_unknown_extra_keys_and_invalid_json_are_not_echoed() (+1 more)

### Community 5 - "App.tsx"
Cohesion: 0.12
Nodes (23): AutomaticParseResult, ContextClaims, MAX_TEXT_CHARACTERS, ParseResult, requestParse(), SyntheticFixture, App(), clearText() (+15 more)

### Community 6 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, esModuleInterop, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+8 more)

### Community 13 - "test_review.py"
Cohesion: 0.05
Nodes (87): SourceContext, CandidateInputReadiness, ClinicalPreparation, IllustrativePolicy, IllustrativeResult, inspect_candidate_inputs(), preparation(), simulate_test_only() (+79 more)

### Community 14 - "services"
Cohesion: 0.15
Nodes (12): key, value, services, buildCommand, envVars, healthCheckPath, name, plan (+4 more)

### Community 18 - "test_reports.py"
Cohesion: 0.08
Nodes (46): create_draft_report(), ChatSettings, GroqClient, finish(), GroqResult, retry_delay(), FinalDraftReport, ReportSubmission (+38 more)

### Community 19 - "review.ts"
Cohesion: 0.19
Nodes (15): ASSESSMENT_OPTIONS, Component, digest(), isDraftReview(), nullable(), obj(), Observation, requestReview() (+7 more)

### Community 20 - "test_phase4.py"
Cohesion: 0.10
Nodes (42): review_submission(), Association, PipelineSubmission, authorized(), generate(), Generated, deterministic(), parse_pipeline() (+34 more)

### Community 21 - "App.assisted.test.tsx"
Cohesion: 0.14
Nodes (6): @testing-library/react@16.3.3, EMPTY_CONTEXT, setup(), setup(), parsed(), @testing-library/react

### Community 22 - "parse.ts"
Cohesion: 0.41
Nodes (11): Adapter, adapter(), isAutomaticParseResult(), isParseResult(), Measurement, nullableString(), object(), Span (+3 more)

### Community 26 - "test_parser_finalization.py"
Cohesion: 0.05
Nodes (68): development_synthetic(), parse_assisted(), parse_automatic(), load_development_env(), Contract, ParseResult, RawTMTSubmission, Certificate (+60 more)

### Community 29 - "@playwright/test"
Cohesion: 0.22
Nodes (4): @playwright/test@1.64.1, backend, python, @playwright/test

### Community 30 - "scripts"
Cohesion: 0.29
Nodes (7): scripts, build, dev, preview, test, test:e2e, test:watch

### Community 31 - "vercel.json"
Cohesion: 0.29
Nodes (6): buildCommand, framework, installCommand, outputDirectory, rewrites, $schema

### Community 32 - "reports/service.py"
Cohesion: 0.07
Nodes (50): synthetic_examples(), GenerationInfo, ReportComment, WordingBatch, WordingChoice, build_prompt(), response_format(), comment_units() (+42 more)

### Community 33 - "FinalReport.test.tsx"
Cohesion: 0.13
Nodes (17): SourceClaim, CommentMode, FinalDraftReport, isFinalDraftReport(), obj(), ReportComment, requestReport(), str() (+9 more)

### Community 35 - "dependencies"
Cohesion: 0.25
Nodes (7): dependencies, lucide-react@1.48.0, react@19.3.0, react-dom@19.3.0, lucide-react, react, react-dom

## Knowledge Gaps
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SourceContext` connect `test_review.py` to `domain/models.py`, `test_parser.py`, `test_semantics.py`, `test_reports.py`, `test_phase4.py`, `test_parser_finalization.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `review_table()` (e.g. with `RawTMTSubmission` and `TestRuleContext`) actually correct?**
  _`review_table()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.08522727272727272 - nodes in this community are weakly interconnected._
- **Why does `parse_table()` connect `domain/models.py` to `test_parser.py`, `test_semantics.py`, `test_review.py`, `test_phase4.py`, `test_parser_finalization.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `parse_table()` (e.g. with `LexicalInput` and `Layout`) actually correct?**
  _`parse_table()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `domain/models.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08503732554365466 - nodes in this community are weakly interconnected._
- **Why does `RawTMTSubmission` connect `test_parser_finalization.py` to `reports/service.py`, `domain/models.py`, `test_parser.py`, `test_semantics.py`, `main.py`, `test_review.py`, `test_reports.py`, `test_phase4.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._