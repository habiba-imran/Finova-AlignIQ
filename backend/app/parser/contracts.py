"""Additive versioned intake contract; the Phase 1 lexical contract stays unchanged."""

from typing import Literal

from pydantic import Field, StrictBool, field_validator

from app.domain.models import Contract, ParseResult, RawCell, RawTMTSubmission


class SourceIndicator(Contract):
    candidate: Literal["ClinCheck", "SureSmile"]
    kind: Literal["EXPLICIT_BRAND", "DOCUMENTED_SIGNATURE"]
    evidence: list[RawCell]


class Detection(Contract):
    detected_source: Literal["Unknown", "ClinCheck", "SureSmile"] = "Unknown"
    verified_source: None = None
    status: Literal["UNKNOWN", "DETECTED_UNVERIFIED", "CONFLICT"] = "UNKNOWN"
    indicators: list[SourceIndicator] = Field(default_factory=list)
    notation_candidates: list[str] = Field(default_factory=list)
    layout_recognized: bool = False


class Clarification(Contract):
    code: str
    field: str
    measurement_ids: list[str] = Field(default_factory=list)
    message: str


class Assistance(Contract):
    available: bool = False
    status: Literal["NOT_REQUESTED", "BLOCKED", "FAILED", "REJECTED", "ACCEPTED"] = "NOT_REQUESTED"
    reason: str = "CLOUD_DISABLED"
    attempts: int = 0
    certificate: Literal["MARKDOWN_PIPE_V1", "SPAN_ASSOCIATIONS_V1"] | None = None
    origin: Literal["DETERMINISTIC", "GROQ_PROPOSAL_CERTIFIED"] = "DETERMINISTIC"
    real_patient_transmission_enabled: Literal[False] = False


class QualityAssessment(Contract):
    classification: Literal["NOT_TMT", "UNSUPPORTED_FORMAT", "AMBIGUOUS_STRUCTURE", "STRUCTURALLY_RECOGNIZED", "PARTIAL", "RECOVERABLE_STRUCTURE"]
    recoverable_associations: int = Field(ge=0, le=512)
    unresolved_lines: list[int]
    cloud_candidate: bool


class PipelineInfo(Contract):
    version: Literal["1.0.0"] = "1.0.0"
    detection: Detection
    assistance: Assistance
    clarifications: list[Clarification]
    quality: QualityAssessment | None = None
    recovery_receipt: str | None = None


class SyntheticFixture(Contract):
    recipe: Literal["clean", "irregular", "mixed_rows", "mixed_columns", "wrapped", "fragments", "header_mix", "partial", "ambiguous", "irrelevant", "adversarial", "unknown_vendor", "metadata"]
    seed: int = Field(ge=0, le=1_000_000)


class PipelineSubmission(RawTMTSubmission):
    synthetic_fixture: SyntheticFixture | None = None


class Association(Contract):
    tooth: str
    label: str
    value: str


class RecoveryProposal(Contract):
    associations: list[Association]


class AutomaticParseResult(ParseResult):
    pipeline: PipelineInfo


class AssistedSubmission(RawTMTSubmission):
    cloud_synthetic_consent: StrictBool

    @field_validator("cloud_synthetic_consent")
    @classmethod
    def affirmative_consent(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Affirmative synthetic cloud consent required")
        return value


class StructuralProposal(Contract):
    """IDs reference immutable original-text spans, not model-authored cell values.

    All properties required for strict provider structured outputs. Complete row
    order and column association are checked against an independently proven grid.
    """
    grammar: Literal["MARKDOWN_PIPE_V1"]
    orientation: Literal["TEETH_IN_ROWS", "TEETH_IN_COLUMNS"]
    rows: list[list[str]]
