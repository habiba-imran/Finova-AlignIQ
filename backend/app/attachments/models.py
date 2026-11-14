from decimal import Decimal
from typing import Literal

from pydantic import Field, model_validator

from app.domain.models import RawTMTSubmission, SourceContext
from app.parser.contracts import AutomaticParseResult
from app.review.models import DraftReview
from app.semantics.models import Digest, EvidenceContract

ResultType = Literal["CANDIDATE", "ALTERNATIVE", "NOT_INDICATED", "UNKNOWN", "WITHHELD"]


class AttachmentSubmission(RawTMTSubmission):
    recovery_receipt: str | None = Field(default=None, max_length=100_000)


class EmptyDemoRequest(EvidenceContract):
    """No uploaded text, decisions, geometry, paths, provider or authority switches."""


class Dimensions(EvidenceContract):
    x: Decimal = Field(gt=0)
    y: Decimal = Field(gt=0)
    z: Decimal = Field(gt=0)
    unit: Literal["mm"] = "mm"


class AttachmentDesign(EvidenceContract):
    design_id: str = Field(min_length=1, max_length=80)
    category_id: str = Field(min_length=1, max_length=80)
    label: str = Field(min_length=1, max_length=160)
    shape: str | None = Field(default=None, max_length=80)
    dimensions: Dimensions | None = None
    orientation: str | None = Field(default=None, max_length=80)


class Placement(EvidenceContract):
    surface_id: str = Field(min_length=1, max_length=80)
    frame_id: str = Field(min_length=1, max_length=80)
    stage_ref: str | None = Field(default=None, max_length=80)


class AttachmentEntry(EvidenceContract):
    entry_id: Digest
    tooth_ref: str | None
    original_tooth: str | None
    verified_tooth: str | None = None
    synthetic_tooth: str | None = None
    result_type: ResultType
    decision_origin: Literal["SUPPLIED_SYNTHETIC", "WITHHOLDING_GUARD"]
    evidence_status: Literal["UNVERIFIED", "TEST_ONLY"]
    design: AttachmentDesign | None = None
    placement: Placement | None = None
    alternative_for: Digest | None = None
    explanation: str
    measurement_refs: tuple[str, ...]
    observation_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    finding_refs: tuple[str, ...]
    missing_prerequisites: tuple[str, ...]
    approval_status: Literal["NOT APPROVED"] = "NOT APPROVED"
    review_status: Literal["DRAFT"] = "DRAFT"

    @model_validator(mode="after")
    def no_unapproved_prescription(self):
        # There is no approved vendor attachment path in this phase.
        if self.verified_tooth is not None:
            raise ValueError("No approved verified attachment identity path")
        if not self.finding_refs:
            raise ValueError("Attachment entries require safeguard finding references")
        if self.evidence_status == "TEST_ONLY" and (not self.synthetic_tooth or not self.observation_refs or not self.evidence_refs):
            raise ValueError("Synthetic identity requires authorized observations and evidence")
        supplied = self.result_type in {"CANDIDATE", "ALTERNATIVE", "NOT_INDICATED"}
        if supplied and (self.decision_origin != "SUPPLIED_SYNTHETIC" or self.evidence_status != "TEST_ONLY"
                         or not self.synthetic_tooth or not self.evidence_refs or not self.observation_refs):
            raise ValueError("Attachment decisions require fixed synthetic evidence")
        if not supplied and (self.design or self.placement or self.alternative_for or not self.missing_prerequisites
                             or self.decision_origin != "WITHHOLDING_GUARD"):
            raise ValueError("Unknown/withheld cannot carry attachment decisions")
        if self.result_type == "NOT_INDICATED" and (self.design or self.placement or self.alternative_for):
            raise ValueError("No-attachment decision cannot carry geometry")
        if self.result_type in {"CANDIDATE", "ALTERNATIVE"} and not self.design:
            raise ValueError("Supplied candidate needs a design reference")
        if (self.result_type == "ALTERNATIVE") != (self.alternative_for is not None):
            raise ValueError("Alternative must link to its candidate")
        if self.evidence_status == "UNVERIFIED" and (self.synthetic_tooth or self.observation_refs):
            raise ValueError("Unverified entries cannot claim semantic observations")
        return self


class AttachmentDraft(EvidenceContract):
    schema_version: Literal["1.0.0"] = "1.0.0"
    report_id: Digest
    title: Literal["Finova AlignIQ — Attachment Review"] = "Finova AlignIQ — Attachment Review"
    draft_status: Literal["DRAFT — Requires Orthodontist Review"] = "DRAFT — Requires Orthodontist Review"
    clinical_analysis_enabled: Literal[False] = False
    evidence_domain: Literal["UNVERIFIED", "TEST_ONLY"]
    engine_review: DraftReview
    entries: tuple[AttachmentEntry, ...] = Field(max_length=512)
    wording_source: Literal["DETERMINISTIC_TEMPLATES"] = "DETERMINISTIC_TEMPLATES"
    provider: None = None
    provider_attempts: Literal[0] = 0
    limitations: tuple[str, ...]
    export_format: Literal["text/plain;charset=utf-8"] = "text/plain;charset=utf-8"
    export_text: str

    @model_validator(mode="after")
    def bound_entries(self):
        if self.evidence_domain != self.engine_review.evidence_domain:
            raise ValueError("Attachment evidence must match engine evidence")
        ids = {e.entry_id: e for e in self.entries}
        if len(ids) != len(self.entries):
            raise ValueError("Duplicate attachment entry")
        for e in self.entries:
            if self.evidence_domain == "UNVERIFIED" and e.evidence_status != "UNVERIFIED":
                raise ValueError("Unverified report cannot carry synthetic evidence")
            if not set(e.finding_refs) <= {f.finding_id for f in self.engine_review.findings}:
                raise ValueError("Missing safeguard references")
            observations = {o.measurement_id: o for f in self.engine_review.findings for o in f.observed_measurements}
            for mid in e.observation_refs:
                observation = observations.get(mid)
                if (not observation or observation.verification != "TEST_ONLY" or observation.tooth_ref != e.tooth_ref
                    or not any(c.name == "tooth_identifier" and c.status == "TEST_ONLY" and c.canonical_value == e.synthetic_tooth for c in observation.components)):
                    raise ValueError("Attachment observation/identity binding invalid")
            if e.alternative_for:
                candidate = ids.get(e.alternative_for)
                if not candidate or candidate.result_type != "CANDIDATE" or candidate.tooth_ref != e.tooth_ref:
                    raise ValueError("Alternative must belong to the same tooth")
        return self


class AttachmentDemoInput(EvidenceContract):
    demo_id: Literal["FINOVA-ATTACHMENTS-1"] = "FINOVA-ATTACHMENTS-1"
    label: Literal["Finova Synthetic Attachment Demonstration — TEST_ONLY"] = "Finova Synthetic Attachment Demonstration — TEST_ONLY"
    convention: tuple[str, ...]
    context: SourceContext
    parsed: AutomaticParseResult


class ScenarioRow(EvidenceContract):
    key: str
    tooth_ref: str
    synthetic_tooth: str | None
    result_type: ResultType
    design: AttachmentDesign | None = None
    placement: Placement | None = None
    alternative_key: str | None = None


class SyntheticScenario(EvidenceContract):
    scenario_id: Literal["FINOVA-ATTACHMENTS-1"] = "FINOVA-ATTACHMENTS-1"
    kind: Literal["TEST_ONLY"] = "TEST_ONLY"
    input_sha256: Digest
    rows: tuple[ScenarioRow, ...] = Field(min_length=1, max_length=20)
