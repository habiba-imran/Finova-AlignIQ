"""Separate evidence contracts. No vendor direction, tooth, or axis maps are supplied."""

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import ConfigDict, Field, model_validator

from app.domain.models import Contract, LexicalInput, ParseResult, SourceSpan

Digest = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
Identifier = Annotated[str, Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_.:-]+$")]
ComponentName = Literal[
    "source_application", "source_version", "tooth_identifier", "notation", "dentition", "arch",
    "axis", "unit", "sign", "direction", "plan_mode", "reference_basis", "scope", "stage_index",
    "stage_kind", "coordinate_frame", "comparison_left_plan", "comparison_right_plan", "comparison_operation",
]
COMPONENTS: tuple[ComponentName, ...] = (
    "source_application", "source_version", "tooth_identifier", "notation", "dentition", "arch",
    "axis", "unit", "sign", "direction", "plan_mode", "reference_basis", "scope", "stage_index",
    "stage_kind", "coordinate_frame", "comparison_left_plan", "comparison_right_plan", "comparison_operation",
)
REQUIRED_COMPONENTS = frozenset({"source_application", "source_version", "tooth_identifier", "notation", "dentition", "arch",
                                 "axis", "unit", "sign", "direction", "plan_mode", "reference_basis", "scope", "coordinate_frame"})


def required_components(values: dict[str, str | None]) -> set[str]:
    required = set(REQUIRED_COMPONENTS)
    if values.get("scope") in {"CUMULATIVE", "INCREMENTAL", "STAGE_SPECIFIC"}:
        required.update({"stage_index", "stage_kind"})
    if values.get("plan_mode") == "COMPARISON":
        required.update({"comparison_left_plan", "comparison_right_plan", "comparison_operation"})
    return required


class EvidenceContract(Contract):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True, allow_inf_nan=False)


class Artifact(EvidenceContract):
    path: str = Field(min_length=1, max_length=256)
    sha256: Digest


class IndependentReview(EvidenceContract):
    reviewer_id: Identifier
    role: Literal["ORTHODONTIST", "INDEPENDENT_DATA_REVIEWER"]
    reviewed_at: datetime
    decision: Literal["APPROVE", "REJECT"]
    raw_sha256: Digest
    expected_sha256: Digest
    source_evidence_sha256: Digest

    @model_validator(mode="after")
    def timezone_required(self):
        if self.reviewed_at.utcoffset() is None:
            raise ValueError("Review timestamps must include a timezone")
        return self


class FixtureRecord(EvidenceContract):
    fixture_id: Identifier
    kind: Literal["AUTHENTIC", "SYNTHETIC"]
    application: Literal["ClinCheck", "SureSmile", "TEST_ONLY"]
    source_version: str | None = Field(default=None, max_length=64)
    status: Literal["PENDING", "REVIEWED", "REVOKED", "TEST_ONLY"] = "PENDING"
    captured_by: Identifier | None = None
    captured_at: datetime | None = None
    consent_ref: Identifier | None = None
    deidentification_ref: Identifier | None = None
    raw: Artifact | None = None
    expected: Artifact | None = None
    source_evidence: Artifact | None = None
    submission_context: LexicalInput | None = None
    reviews: tuple[IndependentReview, ...] = ()

    @model_validator(mode="after")
    def evidence_requirements(self):
        # Raw content belongs in the separately authorized read-only capture, not in this manifest.
        if self.submission_context is not None and self.submission_context.raw_text != "":
            raise ValueError("Manifest context must have empty raw_text; capture is read separately")
        if self.kind == "SYNTHETIC":
            if self.application != "TEST_ONLY" or self.status != "TEST_ONLY" or self.reviews:
                raise ValueError("Synthetic evidence must be TEST_ONLY, without fabricated reviews")
        elif self.application == "TEST_ONLY" or self.status == "TEST_ONLY":
            raise ValueError("Authentic evidence requires an actual vendor and review lifecycle")
        if self.status == "REVIEWED":
            required = (self.source_version, self.captured_by, self.captured_at, self.consent_ref,
                        self.deidentification_ref, self.raw, self.expected, self.source_evidence, self.submission_context)
            if not all(value is not None and value != "" for value in required):
                raise ValueError("Reviewed authentic evidence is incomplete")
            if self.captured_at.utcoffset() is None:
                raise ValueError("Capture timestamp must include timezone")
            if self.submission_context.source_claim not in {"Unknown", self.application}:
                raise ValueError("Capture source and submission source claim conflict")
            claimed_version = self.submission_context.context.source_version
            if claimed_version is not None and claimed_version != self.source_version:
                raise ValueError("Capture version and submission version claim conflict")
            reviewers = {review.reviewer_id for review in self.reviews}
            if len(reviewers) != len(self.reviews) or len(reviewers) < 2 or self.captured_by in reviewers:
                raise ValueError("Two distinct reviewers independent of the capture operator are required")
            if not any(review.role == "ORTHODONTIST" for review in self.reviews):
                raise ValueError("At least one qualified orthodontist review is required")
            for review in self.reviews:
                if review.decision != "APPROVE" or review.reviewed_at < self.captured_at:
                    raise ValueError("Review must approve the captured artifact after capture")
                if (review.raw_sha256, review.expected_sha256, review.source_evidence_sha256) != (
                    self.raw.sha256, self.expected.sha256, self.source_evidence.sha256,
                ):
                    raise ValueError("Review must bind all three exact artifact hashes")
        return self


class FixtureManifest(EvidenceContract):
    schema_version: Literal["1.0.0"] = "1.0.0"
    fixtures: tuple[FixtureRecord, ...] = ()

    @model_validator(mode="after")
    def unique_ids(self):
        if len({record.fixture_id for record in self.fixtures}) != len(self.fixtures):
            raise ValueError("Fixture IDs must be unique")
        return self


class ExpectedComponent(EvidenceContract):
    name: ComponentName
    value: str | None = Field(default=None, min_length=1, max_length=256)
    evidence_locator: str | None = Field(default=None, min_length=1, max_length=256)

    @model_validator(mode="after")
    def explicit_evidence(self):
        if self.value is not None and self.value.strip().upper() in {"UNKNOWN", "UNVERIFIED", "UNSUPPORTED", "AMBIGUOUS", "N/A", "NULL", "NONE", "?", ""}:
            raise ValueError("Use null for unknown canonical values")
        if (self.value is None) != (self.evidence_locator is None):
            raise ValueError("Every supplied canonical value needs an exact evidence locator")
        return self


class ExpectedMeasurement(EvidenceContract):
    measurement_id: Identifier
    components: tuple[ExpectedComponent, ...] = ()

    @model_validator(mode="after")
    def unique_components(self):
        if len({component.name for component in self.components}) != len(self.components):
            raise ValueError("Component assertions must be unique")
        return self


class FixtureExpectedOutput(EvidenceContract):
    schema_version: Literal["1.0.0"] = "1.0.0"
    kind: Literal["AUTHENTIC", "SYNTHETIC"]
    lexical: ParseResult
    measurements: tuple[ExpectedMeasurement, ...] = ()

    @model_validator(mode="after")
    def valid_refs(self):
        refs = [m.measurement_id for m in self.measurements]
        if len(refs) != len(set(refs)) or not set(refs) <= {m.id for m in self.lexical.measurements}:
            raise ValueError("Expected measurement references must exist and be unique")
        return self


class EvidenceRef(EvidenceContract):
    fixture_id: Identifier
    release_digest: Digest
    raw_sha256: Digest
    expected_sha256: Digest
    source_evidence_sha256: Digest | None
    locator: str


class SemanticComponent(EvidenceContract):
    name: ComponentName
    status: Literal["UNKNOWN", "CONFLICT", "INVALID", "VERIFIED", "TEST_ONLY"] = "UNKNOWN"
    claim_value: str | None = None
    canonical_value: str | None = None
    evidence: tuple[EvidenceRef, ...] = ()
    abstain_reasons: tuple[str, ...] = ()
    input_refs: tuple[str, ...] = ()
    source_spans: tuple[SourceSpan, ...] = ()

    @model_validator(mode="after")
    def no_unproven_values(self):
        if self.status in {"VERIFIED", "TEST_ONLY"}:
            if self.canonical_value is None or not self.evidence or self.abstain_reasons:
                raise ValueError("Accepted components require a value, evidence, and no abstention")
            if self.canonical_value.strip().upper() in {"UNKNOWN", "UNVERIFIED", "UNSUPPORTED", "AMBIGUOUS", "N/A", "NULL", "NONE", "?", ""}:
                raise ValueError("Unknown markers cannot be accepted canonical values")
            if self.status == "VERIFIED" and any(ref.source_evidence_sha256 is None for ref in self.evidence):
                raise ValueError("Verified components require source-evidence hashes")
        elif self.canonical_value is not None or self.evidence:
            raise ValueError("Unverified components cannot carry canonical values or accepted evidence")
        return self


class SemanticMeasurement(EvidenceContract):
    measurement_id: str
    components: tuple[SemanticComponent, ...]
    canonical_measurement_ready: bool = False
    evidence_complete_for_test: bool = False
    canonical_magnitude: Decimal | None = None
    value_kind: Literal["UNKNOWN", "SOURCE_REPORTED_MOVEMENT", "SOURCE_REPORTED_COMPARISON"] = "UNKNOWN"
    abstain_reasons: tuple[str, ...] = ()

    @model_validator(mode="after")
    def readiness_requires_evidence(self):
        by_name = {c.name: c for c in self.components}
        if len(by_name) != len(self.components) or set(by_name) != set(COMPONENTS):
            raise ValueError("Each semantic component must be represented exactly once")
        values = {name: c.canonical_value for name, c in by_name.items()}
        if self.canonical_measurement_ready:
            if self.canonical_magnitude is None or self.canonical_magnitude < 0 or self.abstain_reasons:
                raise ValueError("Ready measurements require a nonnegative value and no abstention")
            if any(by_name[name].status != "VERIFIED" for name in required_components(values)):
                raise ValueError("Ready measurements require independently verified components")
            if values['scope'] not in {"TOTAL", "CUMULATIVE", "INCREMENTAL", "STAGE_SPECIFIC"}:
                raise ValueError("Unknown scope is not ready")
            if values['plan_mode'] not in {"ALIGN_FINAL", "DOCTOR_FINAL", "COMPARISON"}:
                raise ValueError("Unclassified plan modes are not ready")
            expected_kind = "SOURCE_REPORTED_COMPARISON" if values['plan_mode'] == "COMPARISON" else "SOURCE_REPORTED_MOVEMENT"
            if self.value_kind != expected_kind:
                raise ValueError("Comparison and movement values cannot be conflated")
            if values['plan_mode'] == "COMPARISON" and values['comparison_left_plan'] == values['comparison_right_plan']:
                raise ValueError("Comparison operands must be distinct")
        elif self.canonical_magnitude is not None or self.value_kind != "UNKNOWN":
            raise ValueError("Abstained measurements cannot carry a canonical number or value kind")
        return self


class SemanticAssessment(EvidenceContract):
    schema_version: Literal["1.0.0"] = "1.0.0"
    normalization_version: Literal["0.1.0-disabled"] = "0.1.0-disabled"
    status: Literal["DISABLED", "ABSTAINED", "PARTIAL", "VERIFIED", "TEST_ONLY"]
    lexical: ParseResult
    measurements: tuple[SemanticMeasurement, ...]
    reasons: tuple[str, ...]

    @model_validator(mode="after")
    def assessment_status_is_consistent(self):
        if [m.measurement_id for m in self.measurements] != [m.id for m in self.lexical.measurements]:
            raise ValueError("Semantic assessment must retain each lexical measurement position")
        components = [c for m in self.measurements for c in m.components]
        if self.status == "DISABLED" and any(c.canonical_value is not None for c in components):
            raise ValueError("Disabled assessments cannot contain canonical values")
        if self.status == "TEST_ONLY" and any(c.status == "VERIFIED" for c in components):
            raise ValueError("Synthetic assessments cannot contain vendor verification")
        if self.status != "TEST_ONLY" and any(c.status == "TEST_ONLY" for c in components):
            raise ValueError("Test-only evidence cannot enter a vendor assessment")
        if self.status == "VERIFIED" and (not self.measurements or not all(m.canonical_measurement_ready for m in self.measurements)):
            raise ValueError("Verified assessments require ready measurements")
        return self
