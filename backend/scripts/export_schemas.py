"""Export JSON Schema from the API contracts. Does not read any submitted data."""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.models import ParseResult, RawTMTSubmission  # noqa: E402
from app.semantics.models import FixtureExpectedOutput, FixtureManifest, SemanticAssessment  # noqa: E402
from app.review.models import DraftReview, ReviewSubmission, RuleDefinition  # noqa: E402
from app.reports.models import FinalDraftReport, ReportSubmission, WordingBatch  # noqa: E402
from app.parser.contracts import AssistedSubmission, AutomaticParseResult, StructuralProposal, PipelineSubmission, RecoveryProposal, SyntheticFixture  # noqa: E402

output = Path(__file__).resolve().parents[2] / "schemas"
output.mkdir(exist_ok=True)
for name, model, mode in [
    ("parse-request.v1.json", RawTMTSubmission, "validation"),
    ("parse-result.v1.json", ParseResult, "serialization"),
    ("vendor-fixture-manifest.v1.json", FixtureManifest, "validation"),
    ("vendor-fixture-expected.v1.json", FixtureExpectedOutput, "serialization"),
    ("semantic-assessment.v1.json", SemanticAssessment, "serialization"),
    ("review-request.v1.json", ReviewSubmission, "validation"),
    ("draft-review.v1.json", DraftReview, "serialization"),
    ("rule-definition.v1.json", RuleDefinition, "serialization"),
    ("report-request.v1.json", ReportSubmission, "validation"),
    ("final-draft-report.v1.json", FinalDraftReport, "serialization"),
    ("groq-wording.v1.json", WordingBatch, "validation"),
    ("automatic-parse-result.v1.json", AutomaticParseResult, "serialization"),
    ("assisted-parse-request.v1.json", AssistedSubmission, "validation"),
    ("groq-structure.v1.json", StructuralProposal, "validation"),
    ("pipeline-parse-request.v1.json", PipelineSubmission, "validation"),
    ("groq-recovery.v1.json", RecoveryProposal, "validation"),
    ("synthetic-generator-request.v1.json", SyntheticFixture, "validation"),
]:
    (output / name).write_text(json.dumps(model.model_json_schema(mode=mode), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
