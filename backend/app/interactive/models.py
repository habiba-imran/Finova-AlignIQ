from typing import Literal
from pydantic import Field, field_validator

from app.domain.models import Contract, ParseResult, ParsedMeasurement
from app.review.models import DraftReview, ReviewSubmission
from app.reports.models import GenerationInfo
from app.semantics.models import Digest


class SuppliedContract(Contract):
    @field_validator("*", mode="before")
    @classmethod
    def valid_unicode(cls, value):
        if isinstance(value, str) and any(0xD800 <= ord(char) <= 0xDFFF for char in value):
            raise ValueError("Unpaired Unicode surrogates are unsupported")
        return value


class AttachmentDetail(SuppliedContract):
    tooth_ref: str = Field(min_length=1, max_length=80)
    choice: Literal["UNKNOWN", "ATTACHMENT", "NO_ATTACHMENT"] = "UNKNOWN"
    design: str | None = Field(default=None, max_length=80)
    width_mm: str | None = Field(default=None, pattern=r"^\+?(?:\d+(?:\.\d*)?|\.\d+)$", max_length=24)
    height_mm: str | None = Field(default=None, pattern=r"^\+?(?:\d+(?:\.\d*)?|\.\d+)$", max_length=24)
    depth_mm: str | None = Field(default=None, pattern=r"^\+?(?:\d+(?:\.\d*)?|\.\d+)$", max_length=24)
    surface: str | None = Field(default=None, max_length=80)
    orientation: str | None = Field(default=None, max_length=80)


class SuppliedStage(SuppliedContract):
    stage_id: str = Field(min_length=1, max_length=40)
    order: int = Field(ge=1, le=2_147_483_647)
    duration_days: int | None = Field(default=None, ge=1, le=2_147_483_647)


class SuppliedAllocation(SuppliedContract):
    stage_id: str = Field(min_length=1, max_length=40)
    tooth_ref: str = Field(min_length=1, max_length=80)
    measurement_ref: str = Field(min_length=1, max_length=80)
    amount: str | None = Field(default=None, pattern=r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$", max_length=24)
    unit: Literal["mm", "deg"] | None = None


class AnchorageNote(SuppliedContract):
    tooth_ref: str | None = Field(default=None, max_length=80)
    note: str = Field(min_length=1, max_length=240)


class ReviewDetails(Contract):
    attachments: list[AttachmentDetail] = Field(default_factory=list, max_length=32)
    stages: list[SuppliedStage] = Field(default_factory=list, max_length=64)
    allocations: list[SuppliedAllocation] = Field(default_factory=list, max_length=128)
    anchorage_notes: list[AnchorageNote] = Field(default_factory=list, max_length=32)


class InteractiveSubmission(ReviewSubmission):
    module: Literal["macro", "micro", "nano"] = "macro"
    raw_sha256: Digest
    review_details: ReviewDetails = Field(default_factory=ReviewDetails)


class ToothObservation(Contract):
    tooth_ref: str
    original_tooth: str
    text: str
    measurements: list[ParsedMeasurement]
    evidence_status: Literal["PARSED_SOURCE_ONLY"] = "PARSED_SOURCE_ONLY"


class Illustration(Contract):
    tooth_ref: str
    original_tooth: str
    label: Literal["Illustrative attachment example", "Illustrative sequencing example"]
    text: str
    origin: Literal["SIMULATED_DEMO"] = "SIMULATED_DEMO"
    clinical_status: Literal["NOT_EVALUATED"] = "NOT_EVALUATED"


class PlanningGenerationInfo(GenerationInfo):
    output_validation: Literal["GROUNDED_PLANNING_WORDING_V1"] = "GROUNDED_PLANNING_WORDING_V1"


class ModuleGenerationInfo(GenerationInfo):
    output_validation: Literal["GROUNDED_MODULE_WORDING_V1"] = "GROUNDED_MODULE_WORDING_V1"


class ModuleSection(Contract):
    section_id: str
    title: str
    status: Literal["SOURCE_REPORTED", "SUPPLIED_UNVERIFIED", "UNAVAILABLE"]
    text: str
    source_refs: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)


class InteractiveReport(Contract):
    schema_version: Literal["1.0.0"] = "1.0.0"
    module: Literal["macro", "micro", "nano"]
    report_id: Digest
    draft_status: Literal["Synthetic demonstration — not for clinical use"] = "Synthetic demonstration — not for clinical use"
    clinical_analysis_enabled: Literal[False] = False
    parsed: ParseResult
    engine_review: DraftReview
    generation: GenerationInfo | PlanningGenerationInfo | ModuleGenerationInfo
    wording_notice: str
    summary: str
    observations: list[ToothObservation]
    illustrations: list[Illustration]
    report_format: Literal["MOVEMENT_PROFILE_V1", "MODULE_SPECIFIC_V1"] = "MOVEMENT_PROFILE_V1"
    sections: list[ModuleSection] = Field(default_factory=list)
    review_details: ReviewDetails = Field(default_factory=ReviewDetails)
    limitations: list[str]
    export_text: str
