"""Separate rule, finding and report contracts; never an HTTP semantic trust input."""

from decimal import Decimal
from typing import Literal

from pydantic import Field, model_validator

from app.domain.models import AxisCoverage, RawTMTSubmission, SourceInfo, SourceSpan
from app.semantics.models import Digest, EvidenceContract, SemanticComponent

AssessmentQuestion = Literal[
    "SUITABILITY", "PERIODONTAL", "ROOT_BONE", "OCCLUSION", "IPR", "EXTRACTION_SURGERY",
    "PROGNOSIS", "ATTACHMENTS", "COLLISIONS", "COMPLEX_INTERVENTION",
]
Status = Literal["OBSERVED", "SEMANTICS_UNKNOWN", "CONTEXT_REQUIRED", "DISABLED", "SUPPRESSED", "NOT_APPLICABLE", "PARSE_INVALID"]
Category = Literal["TECHNICAL", "DESCRIPTIVE", "SAFETY", "OUTPUT", "CLINICAL", "STAGING", "ATTACHMENT", "PROTECTION"]


class ReviewSubmission(RawTMTSubmission):
    requested_assessments: list[AssessmentQuestion] = Field(default_factory=list, max_length=10)
    recovery_receipt: str | None = Field(default=None, max_length=100_000)

    @model_validator(mode="after")
    def distinct_questions(self):
        if len(set(self.requested_assessments)) != len(self.requested_assessments):
            raise ValueError("Repeated assessment questions are unsupported")
        return self


class RuleRef(EvidenceContract):
    rule_id: str
    version: Literal["2.0.0"] = "2.0.0"


class RuleDefinition(RuleRef):
    name: str
    category: Category
    disposition: Literal["READY", "REVISE", "VALIDATE", "MORE DATA", "ADDITIONAL"]
    execution: Literal["ACTIVE", "DISABLED", "DEFERRED"]
    required_fields: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    allowed_evidence: tuple[Literal["AUTHORIZED_VENDOR", "TEST_ONLY"], ...] = ()
    allowed_modes: tuple[str, ...] = ()
    allowed_scopes: tuple[str, ...] = ()
    basis_policy: str = "NO_CROSS_BASIS_OPERATIONS"
    source_policy: str = "EXACT_RELEASED_SOURCE_VERSION_MODE_BASIS_SCOPE_ONLY"
    reason: str
    policy_id: None = None
    clinical_approver: None = None
    threshold: None = None


class ObservedMeasurement(EvidenceContract):
    measurement_id: str
    tooth_ref: str
    raw_tooth_identifier: str
    raw_label: str
    raw_value: str
    raw_number: str
    raw_sign: str | None
    raw_direction: str | None
    signed_decimal: Decimal
    magnitude: Decimal = Field(ge=0)
    verification: Literal["VERIFIED", "TEST_ONLY"]
    components: tuple[SemanticComponent, ...]
    input_refs: tuple[str, ...]
    source_spans: tuple[SourceSpan, ...]


class Finding(EvidenceContract):
    finding_id: str
    rule_id: str
    rule_version: Literal["2.0.0"] = "2.0.0"
    triggering_rules: tuple[RuleRef, ...]
    tooth_id: str | None = None
    status: Status
    applicable: bool | None
    evaluated: bool
    finding_type: Literal["TECHNICAL", "DESCRIPTIVE", "SAFETY", "UNAVAILABLE", "OUTPUT"]
    template_id: str
    message: str
    input_refs: tuple[str, ...] = ()
    observed_measurements: tuple[ObservedMeasurement, ...] = ()
    missing_required_fields: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    abstain_reason: str | None = None
    review_status: Literal["DRAFT"] = "DRAFT"
    conflict_group: str | None = None
    summary_counts: dict[str, int] = Field(default_factory=dict)

    @model_validator(mode="after")
    def abstention_is_not_a_negative_finding(self):
        if self.status == "OBSERVED" and (not self.evaluated or self.applicable is not True):
            raise ValueError("Observed results must explicitly establish applicability and evaluation")
        if self.status == "NOT_APPLICABLE" and self.applicable is not False:
            raise ValueError("Not-applicable results require explicit inapplicability")
        if self.status != "OBSERVED" and (self.evaluated or self.observed_measurements or self.tooth_id):
            raise ValueError("Unavailable/suppressed results cannot claim evaluated movement facts")
        if self.status in {"SEMANTICS_UNKNOWN", "CONTEXT_REQUIRED", "DISABLED", "SUPPRESSED", "PARSE_INVALID"} and not self.abstain_reason:
            raise ValueError("Abstention requires an explicit reason")
        if self.finding_type == "DESCRIPTIVE" and self.status == "OBSERVED" and not self.observed_measurements:
            raise ValueError("Observed descriptions require source measurements")
        if not self.triggering_rules or self.rule_id not in {r.rule_id for r in self.triggering_rules}:
            raise ValueError("Findings must retain their triggering rule")
        return self


class RuleEvaluation(RuleRef):
    status: Status
    finding_ids: tuple[str, ...]
    missing_required_fields: tuple[str, ...] = ()
    abstain_reason: str | None = None


class ReviewCoverage(EvidenceContract):
    declared_positions: int
    eligible_positions: int
    unavailable_positions: int
    eligible_explicit_zero: int
    eligible_nonzero: int
    expected_axes: None = None
    lexical: AxisCoverage


class DraftReview(EvidenceContract):
    schema_version: Literal["1.0.0"] = "1.0.0"
    engine_version: Literal["0.2.0"] = "0.2.0"
    rule_set_version: Literal["2.0.0-phase2a"] = "2.0.0-phase2a"
    report_id: Digest
    review_status: Literal["DRAFT"] = "DRAFT"
    intended_for: Literal["CLINICIAN_REVIEW"] = "CLINICIAN_REVIEW"
    notice: Literal["Prototype — not for clinical use. DRAFT for clinician review. Descriptions concern programmed values, never achieved movement."] = "Prototype — not for clinical use. DRAFT for clinician review. Descriptions concern programmed values, never achieved movement."
    evidence_domain: Literal["UNVERIFIED", "AUTHORIZED_VENDOR", "TEST_ONLY"]
    clinical_analysis_enabled: Literal[False] = False
    raw_sha256: Digest
    parser_version: str
    normalization_version: str
    source: SourceInfo
    coverage: ReviewCoverage
    requested_assessments: tuple[AssessmentQuestion, ...]
    findings: tuple[Finding, ...]
    evaluations: tuple[RuleEvaluation, ...]
    limitations: tuple[str, ...]
