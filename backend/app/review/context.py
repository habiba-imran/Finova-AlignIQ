"""Additional-input contracts, not public intake or a vendor/clinical trust switch."""

from typing import Literal
from pydantic import Field, model_validator

from app.semantics.models import Digest, EvidenceContract
from app.semantics.fixtures import digest_json

ToothGroup = Literal["INCISOR", "CANINE", "PREMOLAR", "MOLAR", "PRIMARY", "SUPERNUMERARY", "NON_TOOTH"]


class ToothContext(EvidenceContract):
    canonical_tooth_id: str
    group: ToothGroup | None = None
    status: Literal["PRESENT", "PONTIC", "UNERUPTED", "IMPACTED", "EXTRACTED", "EXCLUDED", "FIXED", "UNKNOWN"] = "UNKNOWN"
    movement_permitted: bool | None = None
    evidence_ref: str = Field(min_length=1)


class StageRecord(EvidenceContract):
    stage_id: str = Field(min_length=1)
    index: int = Field(ge=0)
    arch: str = Field(min_length=1)
    kind: Literal["BASELINE", "ACTIVE", "ACCOMMODATION", "CORRECTION", "OVERCORRECTION", "PASSIVE"]
    evidence_ref: str = Field(min_length=1)


class PairedTeeth(EvidenceContract):
    left_id: str
    right_id: str
    axis: str
    left_direction: str
    right_direction: str
    equivalent_plan_basis_scope_frame: Literal[True]
    equivalent_direction_meaning: Literal[True]
    evidence_ref: str = Field(min_length=1)


class ExpectedCoverage(EvidenceContract):
    canonical_tooth_id: str
    expected_axes: tuple[str, ...] = Field(min_length=1)
    evidence_ref: str = Field(min_length=1)


class AdditionalInputRequirements(EvidenceContract):
    """Prerequisite design only; none of these fields is exposed on HTTP submissions."""
    source_and_version: bool = True
    patient_and_plan_binding: bool = True
    stage_sequence: bool = False
    attachment_tooth_surface_stage_map: bool = False
    initial_final_crown_root_geometry: bool = False
    coordinate_frame_and_validated_operations: bool = False
    interproximal_contact_and_enamel_assessment: bool = False
    approved_ipr_plan: bool = False
    verified_occlusal_examination: bool = False
    periodontal_and_root_assessment: bool = False
    patient_objectives_and_exclusions: bool = False
    device_profile_and_config_history: bool = False
    orthodontist_approved_policy: bool = True


class TestRuleContext(EvidenceContract):
    """Explicit illustrative evidence. Cannot represent VERIFIED or clinical approval.

    Admission additionally requires the private test_only switch, TEST_ONLY
    semantic domain, exact input/context binding and an unknown source claim.
    """
    __test__ = False
    kind: Literal["TEST_ONLY"] = "TEST_ONLY"
    input_digest: Digest
    teeth: tuple[ToothContext, ...] = ()
    stages: tuple[StageRecord, ...] = ()
    pairs: tuple[PairedTeeth, ...] = ()
    coverage: tuple[ExpectedCoverage, ...] = ()

    @model_validator(mode="after")
    def unique_records(self):
        ids=[t.canonical_tooth_id for t in self.teeth]
        if len(ids)!=len(set(ids)): raise ValueError("DUPLICATE_TOOTH_CONTEXT")
        if any(p.left_id==p.right_id for p in self.pairs): raise ValueError("PAIR_REQUIRES_DISTINCT_TEETH")
        participants=[(tooth,p.axis) for p in self.pairs for tooth in (p.left_id,p.right_id)]
        if len(participants)!=len(set(participants)): raise ValueError("CONFLICTING_PAIR_CONTEXT")
        coverage=[(c.canonical_tooth_id,axis) for c in self.coverage for axis in c.expected_axes]
        if len(coverage)!=len(set(coverage)): raise ValueError("DUPLICATE_COVERAGE_CONTEXT")
        return self


def input_digest(submission) -> str:
    return digest_json({'raw_text':submission.raw_text,'source_claim':submission.source_claim,'context':submission.context.model_dump(mode='json')})


def admit_test_context(context, submission, *, test_only: bool, domain: str):
    if context is None or not test_only or domain!='TEST_ONLY' or submission.source_claim!='Unknown': return None
    checked=TestRuleContext.model_validate_json(context.model_dump_json())
    return checked if checked.input_digest==input_digest(submission) else None


def stage_errors(stages: tuple[StageRecord, ...]) -> tuple[str, ...]:
    errors=[]
    for arch in sorted({s.arch for s in stages}):
        group=[s for s in stages if s.arch==arch]
        if len({s.stage_id for s in group})!=len(group): errors.append('DUPLICATE_STAGE_ID')
        if len({s.index for s in group})!=len(group): errors.append('DUPLICATE_STAGE_INDEX')
        if [s.index for s in group]!=sorted(s.index for s in group): errors.append('STAGE_ORDER_INVALID')
        if any(s.index==0 and s.kind!='BASELINE' for s in group): errors.append('STAGE_ZERO_KIND_UNRESOLVED')
    # Gaps are allowed; no missing stages or arch correspondence is invented.
    return tuple(sorted(set(errors)))
