from typing import Literal

from app.domain.models import Contract, SourceContext
from app.parser.contracts import AutomaticParseResult
from app.reports.models import CommentMode, FinalDraftReport
from app.semantics.models import Digest

Dimension = Literal["SAGITTAL", "TRANSVERSE", "VERTICAL", "OTHER", "UNAVAILABLE"]


class PlanningSection(Contract):
    dimension: Dimension
    comment_ids: tuple[Digest, ...]
    explanation: str


class PlanningDraft(Contract):
    version: Literal["1.0.0"] = "1.0.0"
    report: FinalDraftReport
    sections: tuple[PlanningSection, ...]
    export_text: str


class DemoRequest(Contract):
    # No raw text, fixture IDs, paths, evidence, context or authority flags accepted.
    comment_mode: CommentMode = "AUTO"


class DemoInput(Contract):
    demo_id: Literal["FINOVA-SYNTHETIC-1"] = "FINOVA-SYNTHETIC-1"
    label: Literal["Finova Synthetic Demonstration — TEST_ONLY"] = "Finova Synthetic Demonstration — TEST_ONLY"
    convention: tuple[str, ...]
    context: SourceContext
    parsed: AutomaticParseResult
