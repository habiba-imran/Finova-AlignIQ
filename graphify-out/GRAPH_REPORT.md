# Graph Report - Finova AlignIQ  (2026-11-13)

## Corpus Check
- 125 files · ~148,056 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 2, .example 1, .ini 1)

## Summary
- 832 nodes · 2792 edges · 40 communities (24 shown, 16 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 150 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5e5615e5`
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
- reports/service.py
- services
- manifest.json
- test_reports.py
- review.ts
- test_phase4.py
- App.assisted.test.tsx
- parse.ts
- load_development_env
- ContextClaims
- test_parser_finalization.py
- ChatSettings
- @playwright/test
- scripts
- vercel.json
- FinalReport.test.tsx
- devDependencies
- dependencies
- ParseResults.tsx
- tailwindcss
- setup.ts
- @vitejs/plugin-react

## God Nodes (most connected - your core abstractions)
1. `synthetic_review()` - 50 edges
2. `GroqClient` - 42 edges
3. `parse_pipeline()` - 42 edges
4. `parse_table()` - 41 edges
5. `assess_semantics()` - 37 edges
6. `review_table()` - 36 edges
7. `automatic_parse()` - 35 edges
8. `write_synthetic_fixture()` - 35 edges
9. `_assemble()` - 32 edges
10. `SourceContext` - 31 edges

## Surprising Connections (you probably didn't know these)
- `App()` --calls--> `ParserStatus()`  [EXTRACTED]
  frontend/src/App.tsx → frontend/src/components/ParserStatus.tsx
- `setup()` --calls--> `App()`  [EXTRACTED]
  frontend/src/App.assisted.test.tsx → frontend/src/App.tsx
- `FixtureExpectedOutput` --uses--> `ParseResult`  [INFERRED]
  backend/app/semantics/models.py → backend/app/domain/models.py
- `SemanticAssessment` --uses--> `ParseResult`  [INFERRED]
  backend/app/semantics/models.py → backend/app/domain/models.py
- `assess_semantics()` --uses--> `ParseResult`  [INFERRED]
  backend/app/semantics/normalization.py → backend/app/domain/models.py

## Import Cycles
- None detected.

## Communities (40 total, 16 thin omitted)

### Community 0 - "package.json"
Cohesion: 0.18
Nodes (10): jsdom@29.1.1, @types/react@19.3.0, engines, node, name, private, type, version (+2 more)

### Community 1 - "domain/models.py"
Cohesion: 0.08
Nodes (45): parse_submission(), AdapterInfo, AxisCoverage, Contract, LayoutInfo, ParsedMeasurement, ParseIssue, ParseResult (+37 more)

### Community 2 - "test_parser.py"
Cohesion: 0.15
Nodes (31): codes(), parse(), sample(), test_arch_conflict_and_scope_do_not_trigger_arithmetic(), test_audited_source_context_mismatches_withhold_semantics(), test_blank_lines_do_not_consume_declared_grid_cells(), test_decimal_comma_requires_explicit_claim_and_does_not_modify_raw(), test_deterministic_no_logging_network_or_file_writes() (+23 more)

### Community 3 - "test_semantics.py"
Cohesion: 0.07
Nodes (53): LexicalInput, WordingChoice, assert_fixture_matches(), CheckedFixture, FixtureVerificationError, load_manifest(), _read_artifact(), verify_fixture() (+45 more)

### Community 4 - "main.py"
Cohesion: 0.06
Nodes (11): private_validation_error(), PrivateIntakeMiddleware, create_draft_report(), health(), HealthResponse, ReportSubmission, payload(), test_invalid_requests_are_sanitized() (+3 more)

### Community 5 - "App.tsx"
Cohesion: 0.12
Nodes (19): @testing-library/react@16.3.3, vitest@4.1.11, EMPTY_CONTEXT, MAX_TEXT_CHARACTERS, requestParse(), SyntheticFixture, App(), clearText() (+11 more)

### Community 6 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, esModuleInterop, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+8 more)

### Community 13 - "reports/service.py"
Cohesion: 0.08
Nodes (42): RawTMTSubmission, GenerationInfo, ReportComment, WordingBatch, build_prompt(), comment_units(), CommentUnit, _eligible() (+34 more)

### Community 14 - "services"
Cohesion: 0.15
Nodes (12): key, value, services, buildCommand, envVars, healthCheckPath, name, plan (+4 more)

### Community 18 - "test_reports.py"
Cohesion: 0.06
Nodes (81): SourceContext, GroqClient, finish(), GroqResult, retry_delay(), FinalDraftReport, response_format(), _assemble() (+73 more)

### Community 19 - "review.ts"
Cohesion: 0.16
Nodes (23): ContextClaims, SourceClaim, CommentMode, FinalDraftReport, ReportComment, str(), strings(), ASSESSMENT_OPTIONS (+15 more)

### Community 20 - "test_phase4.py"
Cohesion: 0.08
Nodes (51): development_synthetic(), parse_automatic(), review_submission(), Association, PipelineSubmission, SyntheticFixture, authorized(), generate() (+43 more)

### Community 21 - "App.assisted.test.tsx"
Cohesion: 0.18
Nodes (5): requestReview(), setup(), DraftReviewPanel(), review(), FindingCard()

### Community 22 - "parse.ts"
Cohesion: 0.28
Nodes (14): Adapter, adapter(), AutomaticParseResult, isAutomaticParseResult(), isParseResult(), Measurement, nullableString(), object() (+6 more)

### Community 23 - "load_development_env"
Cohesion: 0.27
Nodes (3): load_development_env(), main(), test_explicit_env_loader_has_no_evaluation_no_secret_output_and_process_precedence()

### Community 24 - "ContextClaims"
Cohesion: 0.50
Nodes (4): ContextFields(), humanize(), labels, options

### Community 26 - "test_parser_finalization.py"
Cohesion: 0.09
Nodes (48): parse_assisted(), Certificate, certify_markdown(), structural_prompt(), validate_proposal(), load_parser_settings(), ParserSettings, AssistedSubmission (+40 more)

### Community 29 - "@playwright/test"
Cohesion: 0.22
Nodes (4): @playwright/test@1.64.1, backend, python, @playwright/test

### Community 30 - "scripts"
Cohesion: 0.29
Nodes (7): scripts, build, dev, preview, test, test:e2e, test:watch

### Community 31 - "vercel.json"
Cohesion: 0.29
Nodes (6): buildCommand, framework, installCommand, outputDirectory, rewrites, $schema

### Community 33 - "FinalReport.test.tsx"
Cohesion: 0.18
Nodes (7): isFinalDraftReport(), obj(), requestReport(), CommentCard(), FinalReportPanel(), generate(), panel()

### Community 34 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, autoprefixer@10.5.4, postcss@8.5.28, @types/react-dom@19.3.0, typescript@6.0.3, vite@7.3.6, autoprefixer, postcss (+3 more)

### Community 35 - "dependencies"
Cohesion: 0.33
Nodes (6): dependencies, lucide-react@1.48.0, react@19.3.0, react-dom@19.3.0, lucide-react, react-dom

### Community 36 - "ParseResults.tsx"
Cohesion: 0.67
Nodes (3): humanize(), ParseResults(), titles

## Knowledge Gaps
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `parse_table()` connect `domain/models.py` to `test_parser.py`, `test_semantics.py`, `test_reports.py`, `test_phase4.py`, `test_parser_finalization.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `GroqClient` (e.g. with `generate_report()` and `test_malformed_truncated_refused_and_oversized_responses_fallback()`) actually correct?**
  _`GroqClient` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `domain/models.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07711950970377937 - nodes in this community are weakly interconnected._
- **Why does `SourceContext` connect `test_reports.py` to `domain/models.py`, `test_parser.py`, `test_semantics.py`, `test_phase4.py`, `test_parser_finalization.py`, `field_validator`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `assess_semantics()` (e.g. with `ParseResult` and `CheckedFixture`) actually correct?**
  _`assess_semantics()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_semantics.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06606942889137737 - nodes in this community are weakly interconnected._
- **Why does `GroqClient` connect `test_reports.py` to `domain/models.py`, `reports/service.py`, `test_phase4.py`, `test_parser_finalization.py`, `ChatSettings`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._