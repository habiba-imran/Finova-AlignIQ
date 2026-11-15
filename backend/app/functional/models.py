"""Optional, source-bound scenario inputs and reproducible demonstration outputs."""
from typing import Annotated, Literal
from decimal import Decimal
from pydantic import Field, field_validator, model_validator

from app.domain.models import Contract
from app.semantics.models import Digest

Scalar = Annotated[str, Field(pattern=r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$", max_length=24)]
Concept = Literal['RECTANGULAR', 'VERTICAL_RECTANGULAR', 'HORIZONTAL_RECTANGULAR', 'OVAL', 'OPTIMIZED_STYLE', 'NO_ATTACHMENT']


class ScenarioContract(Contract):
    @field_validator('*', mode='before')
    @classmethod
    def unicode_text(cls, value):
        def check(item, depth=0):
            if depth > 32:
                raise ValueError('Scenario input nesting limit')
            if isinstance(item,str) and any(0xD800 <= ord(c) <= 0xDFFF for c in item):
                raise ValueError('Invalid Unicode in scenario input')
            if isinstance(item,list):
                for child in item:
                    check(child,depth+1)
            if isinstance(item,dict):
                for key,child in item.items():
                    check(key,depth+1); check(child,depth+1)
        check(value)
        return value


class Geometry(ScenarioContract):
    width_mm: Scalar
    height_mm: Scalar
    depth_mm: Scalar

    @field_validator('width_mm', 'height_mm', 'depth_mm')
    @classmethod
    def positive(cls, value):
        if Decimal(value) <= 0:
            raise ValueError('Positive fictional geometry required')
        return value


class Placement(ScenarioContract):
    frame: Literal['FICTIONAL_TOOTH_LOCAL_MM']
    x_mm: Scalar
    y_mm: Scalar
    z_mm: Scalar


class AttachmentOption(ScenarioContract):
    concept: Concept
    geometry: Geometry | None = None
    orientation: Literal['VERTICAL', 'HORIZONTAL', 'UNSPECIFIED'] | None = None
    surface: Literal['BUCCAL', 'LINGUAL'] | None = None
    placement: Placement | None = None

    @model_validator(mode='after')
    def catalog_consistency(self):
        if self.concept == 'NO_ATTACHMENT' and any(v is not None for v in (self.geometry,self.orientation,self.surface,self.placement)):
            raise ValueError('No-attachment option cannot carry attachment geometry or placement')
        expected = {'VERTICAL_RECTANGULAR':'VERTICAL','HORIZONTAL_RECTANGULAR':'HORIZONTAL'}.get(self.concept)
        if expected and self.orientation not in {None,expected}:
            raise ValueError('Catalog orientation conflicts with its declared concept')
        return self


class MovementTarget(ScenarioContract):
    measurement_ref: str = Field(min_length=1, max_length=80)
    amount: Scalar
    unit: Literal['mm', 'deg']
    source_direction: str | None = Field(default=None, max_length=4)


class Phase(ScenarioContract):
    phase_id: str = Field(min_length=1, max_length=40)
    label: str = Field(min_length=1, max_length=80)
    stage_ids: list[str] = Field(min_length=1, max_length=64)


class SupportConstraint(ScenarioContract):
    phase_id: str = Field(min_length=1, max_length=40)
    support_tooth_refs: list[str] = Field(min_length=1, max_length=32)
    active_tooth_refs: list[str] = Field(min_length=1, max_length=32)
    assumption: Literal['STATIONARY_IN_FICTIONAL_SCENARIO']


class FunctionalContext(ScenarioContract):
    scenario_id: str = Field(pattern=r'^[a-zA-Z0-9_-]{1,60}$')
    policy_version: Literal['1.0.0'] = '1.0.0'
    source_sha256: Digest
    module: Literal['macro', 'micro', 'nano']
    origin: Literal['EXPLICIT_SYNTHETIC_SCENARIO'] = 'EXPLICIT_SYNTHETIC_SCENARIO'
    notation: Literal['FDI', 'UNVERIFIED'] = 'UNVERIFIED'
    objectives: list[Literal['REDISTRIBUTE_TRANSLATIONS', 'ANGULAR_CONTROL', 'VERTICAL_REVIEW', 'STAGE_REVIEW']] = Field(default_factory=list, max_length=4)
    targets: list[MovementTarget] = Field(default_factory=list, max_length=64)
    attachment_options: list[AttachmentOption] = Field(default_factory=list, max_length=6)
    phases: list[Phase] = Field(default_factory=list, max_length=16)
    stage_value_basis: Literal['UNSPECIFIED', 'INCREMENTS_MATCH_SOURCE_LABELS'] = 'UNSPECIFIED'
    support_constraints: list[SupportConstraint] = Field(default_factory=list, max_length=16)


class Decision(Contract):
    decision_id: str
    finding_id: str
    policy_id: str
    policy_version: Literal['1.0.0'] = '1.0.0'
    dimension: str
    status: Literal['ILLUSTRATIVE_PROPOSAL', 'INSUFFICIENT_INFORMATION', 'NOT_APPLICABLE', 'CONFLICT']
    tooth_refs: list[str]
    measurement_refs: list[str]
    context_refs: list[str]
    rationale: str
    proposal: str
    alternative: str | None = None
    missing_fields: list[str] = Field(default_factory=list)
    proposed_changes: list[MovementTarget] = Field(default_factory=list)
    attachment_primary: Concept | None = None
    attachment_alternative: Concept | None = None


class Candidate(Contract):
    tooth_ref: str
    decision_id: str
    movement_refs: list[str]
    primary: Concept | None
    alternative: Concept | None
    outcome: Literal['CANDIDATE', 'NO_ATTACHMENT', 'INSUFFICIENT_INFORMATION']
    missing_fields: list[str]


class StageMovement(Contract):
    tooth_ref: str
    measurement_ref: str
    amount: Scalar | None
    unit: Literal['mm', 'deg'] | None
    source_direction: str | None


class StageRow(Contract):
    stage_id: str
    order: int
    phase_id: str | None
    duration_days: int | None
    movements: list[StageMovement]
    decision_ids: list[str] = Field(default_factory=list)


class PlanCheck(Contract):
    code: str
    status: Literal['PASS', 'CONFLICT', 'UNAVAILABLE']
    message: str
    source_refs: list[str] = Field(default_factory=list)


class AllocationCheck(Contract):
    measurement_ref: str
    source_total: str | None
    allocated_total: str | None
    unit: Literal['mm', 'deg'] | None
    status: Literal['MATCH', 'MISMATCH', 'UNAVAILABLE', 'NOT_COMPARABLE']


class FunctionalPlan(Contract):
    policy_set_version: Literal['1.0.0'] = '1.0.0'
    origin: Literal['INDEPENDENT_SYNTHETIC_POLICIES'] = 'INDEPENDENT_SYNTHETIC_POLICIES'
    clinical_authorized: Literal[False] = False
    source_sha256: Digest
    decisions: list[Decision] = Field(default_factory=list)
    attachment_rows: list[Candidate] = Field(default_factory=list)
    stages: list[StageRow] = Field(default_factory=list)
    allocation_checks: list[AllocationCheck] = Field(default_factory=list)
    checks: list[PlanCheck] = Field(default_factory=list)
