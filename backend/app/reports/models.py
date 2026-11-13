"""Versioned report contracts, independent of the unchanged review endpoint."""

from typing import Literal

from pydantic import Field

from app.review.models import DraftReview, ObservedMeasurement, ReviewSubmission, RuleRef
from app.semantics.models import Digest, EvidenceContract

CommentMode = Literal["AUTO", "GROQ", "TEMPLATES"]


class ReportSubmission(ReviewSubmission):
    comment_mode: CommentMode = "AUTO"


class WordingChoice(EvidenceContract):
    finding_ids: list[str] = Field(min_length=1, max_length=1)
    text: str = Field(min_length=1, max_length=1000)


class WordingBatch(EvidenceContract):
    comments: list[WordingChoice] = Field(min_length=1, max_length=24)


class ReportComment(EvidenceContract):
    comment_id: Digest
    finding_ids: tuple[str, ...]
    rules: tuple[RuleRef, ...]
    section: Literal["TOOTH", "SUMMARY", "UNAVAILABLE"]
    tooth_id: str | None = None
    evidence_status: Literal["VERIFIED", "TEST_ONLY", "UNVERIFIED"]
    text: str
    wording_source: Literal["STANDARD_TEMPLATE", "GROQ_VALIDATED"] = "STANDARD_TEMPLATE"
    wording_validation: Literal["NOT_REQUESTED", "ACCEPTED", "FALLBACK"] = "NOT_REQUESTED"
    fallback_reason: str | None = None
    measurements: tuple[ObservedMeasurement, ...] = ()
    input_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    missing_required_fields: tuple[str, ...]
    abstain_reasons: tuple[str, ...]
    evaluation_statuses: tuple[str, ...]


class GenerationInfo(EvidenceContract):
    requested_mode: CommentMode
    used_mode: Literal["STANDARD_TEMPLATES", "GROQ_AI", "MIXED"]
    reason: str
    provider: Literal["GROQ"] | None = None
    model: Literal["openai/gpt-oss-120b"] | None = None
    attempts: int = Field(ge=0, le=2)
    eligible_wording_findings: int = Field(ge=0)
    accepted_comments: int = Field(ge=0)
    real_patient_transmission_enabled: Literal[False] = False
    output_validation: Literal["CLOSED_WORDING_AND_LOCAL_FACTS_V1"] = "CLOSED_WORDING_AND_LOCAL_FACTS_V1"


class FinalDraftReport(EvidenceContract):
    schema_version: Literal["1.0.0"] = "1.0.0"
    report_version: Literal["0.3.0"] = "0.3.0"
    report_id: Digest
    title: Literal["Finova AlignIQ — Descriptive Planning Report"] = "Finova AlignIQ — Descriptive Planning Report"
    draft_status: Literal["DRAFT — Requires Orthodontist Review"] = "DRAFT — Requires Orthodontist Review"
    clinical_analysis_enabled: Literal[False] = False
    engine_review: DraftReview
    generation: GenerationInfo
    comments: tuple[ReportComment, ...]
    limitations: tuple[str, ...]
    export_format: Literal["text/plain;charset=utf-8"] = "text/plain;charset=utf-8"
    export_text: str
