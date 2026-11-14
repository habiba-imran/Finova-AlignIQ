from typing import Literal

from app.domain.models import Contract, ParseResult, ParsedMeasurement
from app.review.models import DraftReview, ReviewSubmission
from app.reports.models import GenerationInfo
from app.semantics.models import Digest


class InteractiveSubmission(ReviewSubmission):
    module: Literal["macro", "micro", "nano"] = "macro"
    raw_sha256: Digest


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


class InteractiveReport(Contract):
    schema_version: Literal["1.0.0"] = "1.0.0"
    module: Literal["macro", "micro", "nano"]
    report_id: Digest
    draft_status: Literal["Synthetic demonstration — not for clinical use"] = "Synthetic demonstration — not for clinical use"
    clinical_analysis_enabled: Literal[False] = False
    parsed: ParseResult
    engine_review: DraftReview
    generation: GenerationInfo
    wording_notice: str
    summary: str
    observations: list[ToothObservation]
    illustrations: list[Illustration]
    limitations: list[str]
    export_text: str
