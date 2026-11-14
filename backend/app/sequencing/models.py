from typing import Literal

from pydantic import Field, model_validator

from app.domain.models import ParseResult, RawTMTSubmission, SourceContext
from app.parser.contracts import AutomaticParseResult
from app.review.context import StageRecord, stage_errors
from app.review.models import DraftReview
from app.semantics.models import Digest, EvidenceContract

Section = Literal["UPPER_ARCH", "LOWER_ARCH", "SEGMENTS", "RIGHT_ANCHORAGE", "LEFT_ANCHORAGE", "UNAVAILABLE"]
Result = Literal["VERIFIED_OBSERVATION", "STRUCTURAL_OBSERVATION", "SUPPLIED_SYNTHETIC", "UNKNOWN", "WITHHELD", "DISABLED"]


class SequencingSubmission(RawTMTSubmission):
    recovery_receipt: str | None = Field(default=None, max_length=100_000)


class EmptyDemoRequest(EvidenceContract):
    """No input, stage records, decisions, fixture paths or authority switches."""


class StageWindow(EvidenceContract):
    start_id: str
    end_id: str


class FictionalArch(EvidenceContract):
    arch_id: str
    label: str
    role: Literal["UPPER", "LOWER"]


class FictionalSegment(EvidenceContract):
    segment_id: str
    label: str
    arch_id: str
    side: Literal["RIGHT", "LEFT"]
    tooth_refs: tuple[str, ...] = Field(min_length=1)


class ScenarioStatement(EvidenceContract):
    key: str
    section: Section
    text: str = Field(min_length=1, max_length=800)
    arch_id: str | None = None
    segment_id: str | None = None
    side: Literal["RIGHT", "LEFT", "UNKNOWN"] = "UNKNOWN"
    stage_window: StageWindow | None = None


class SequencingScenario(EvidenceContract):
    scenario_id: Literal["FINOVA-NANO-1"] = "FINOVA-NANO-1"
    kind: Literal["TEST_ONLY"] = "TEST_ONLY"
    input_sha256: Digest
    arches: tuple[FictionalArch, ...] = Field(min_length=2, max_length=2)
    segments: tuple[FictionalSegment, ...] = Field(min_length=1, max_length=16)
    stages: tuple[StageRecord, ...] = Field(max_length=32)
    statements: tuple[ScenarioStatement, ...] = Field(min_length=1, max_length=20)

    @model_validator(mode="after")
    def references(self):
        arches = {a.arch_id: a for a in self.arches}
        segments = {s.segment_id: s for s in self.segments}
        if len(arches) != len(self.arches) or {a.role for a in self.arches} != {"UPPER", "LOWER"} or len(segments) != len(self.segments):
            raise ValueError("Invalid fictional arch/segment identities")
        if len({s.key for s in self.statements}) != len(self.statements):
            raise ValueError("Duplicate scenario statement")
        if any(s.arch_id not in arches for s in self.segments) or any(s.arch not in arches for s in self.stages):
            raise ValueError("Unknown fictional arch")
        for s in self.statements:
            if s.arch_id and s.arch_id not in arches or s.segment_id and s.segment_id not in segments:
                raise ValueError("Unknown fictional reference")
            if s.segment_id and (segments[s.segment_id].arch_id != s.arch_id or segments[s.segment_id].side != s.side):
                raise ValueError("Incompatible segment identity")
            if s.section in {"UPPER_ARCH", "LOWER_ARCH"} and (not s.arch_id or arches[s.arch_id].role != s.section.removesuffix("_ARCH")):
                raise ValueError("Incorrect arch section")
            if s.section in {"RIGHT_ANCHORAGE", "LEFT_ANCHORAGE"} and s.side != s.section.removesuffix("_ANCHORAGE"):
                raise ValueError("Incorrect anchorage side")
        return self


class StageInspection(EvidenceContract):
    status: Literal["MISSING", "SUPPLIED_SYNTHETIC_METADATA", "INVALID"]
    records: tuple[StageRecord, ...] = ()
    issues: tuple[str, ...] = ()
    evidence_ref: str | None = None
    movement_binding: Literal["NO_STAGE_MOVEMENT_BINDING"] = "NO_STAGE_MOVEMENT_BINDING"
    explanation: str

    @model_validator(mode="after")
    def honest_stage_status(self):
        if self.status == "MISSING" and (self.records or self.issues or self.evidence_ref):
            raise ValueError("Missing stage data cannot claim supplied records/evidence")
        if self.status == "SUPPLIED_SYNTHETIC_METADATA" and (not self.records or not self.evidence_ref or self.issues
            or stage_errors(self.records) or len({s.stage_id for s in self.records}) != len(self.records)):
            raise ValueError("Supplied stage check requires consistent actual records")
        if self.status == "INVALID" and not self.issues:
            raise ValueError("Invalid stage data requires explicit issues")
        return self


class SequencingEntry(EvidenceContract):
    entry_id: Digest
    section: Section
    result_type: Result
    origin: Literal["SUPPLIED_SCENARIO", "ENGINE_GUARD"]
    text: str
    original_tooth_refs: tuple[str, ...] = ()
    original_tooth_tokens: tuple[str, ...] = ()
    verified_tooth_refs: tuple[str, ...] = ()
    verified_arch: None = None
    verified_segment: None = None
    synthetic_arch_id: str | None = None
    synthetic_segment_id: str | None = None
    side: Literal["RIGHT", "LEFT", "UNKNOWN"] = "UNKNOWN"
    evidence_status: Literal["UNVERIFIED", "TEST_ONLY"]
    movement_scope: Literal["TOTAL", "CUMULATIVE", "INCREMENTAL", "UNKNOWN"]
    stage_window: StageWindow | None = None
    stage_kinds: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    measurement_refs: tuple[str, ...] = ()
    finding_refs: tuple[str, ...] = Field(min_length=1)
    missing_prerequisites: tuple[str, ...] = Field(min_length=1)
    policy_id: None = None
    approval_status: Literal["NOT APPROVED"] = "NOT APPROVED"
    clinical_predicate_evaluated: Literal[False] = False
    review_status: Literal["DRAFT"] = "DRAFT"

    @model_validator(mode="after")
    def no_authority_promotion(self):
        if self.result_type == "VERIFIED_OBSERVATION" or self.verified_tooth_refs:
            raise ValueError("No released verified sequencing evidence path in this phase")
        if len(self.original_tooth_refs) != len(self.original_tooth_tokens):
            raise ValueError("Original references must preserve paired tokens")
        if self.result_type == "SUPPLIED_SYNTHETIC":
            if self.origin != "SUPPLIED_SCENARIO" or self.evidence_status != "TEST_ONLY" or not self.evidence_refs:
                raise ValueError("Supplied statements require fixed scenario provenance")
        elif self.origin != "ENGINE_GUARD":
            raise ValueError("Withholding and observations are engine guards")
        if self.result_type in {"UNKNOWN", "WITHHELD", "DISABLED"} and (self.stage_window or self.stage_kinds):
            raise ValueError("Unavailable entries cannot claim a stage window")
        if self.evidence_status == "UNVERIFIED" and (self.synthetic_arch_id or self.synthetic_segment_id or self.stage_window):
            raise ValueError("Unverified input cannot supply synthetic identities or windows")
        if self.section in {"RIGHT_ANCHORAGE", "LEFT_ANCHORAGE"} and self.side != self.section.removesuffix("_ANCHORAGE"):
            raise ValueError("Anchorage sides must remain separate")
        return self


class SequencingDraft(EvidenceContract):
    schema_version: Literal["1.0.0"] = "1.0.0"
    report_id: Digest
    title: Literal["Finova AlignIQ — Sequencing Review"] = "Finova AlignIQ — Sequencing Review"
    draft_status: Literal["DRAFT — Requires Orthodontist Review"] = "DRAFT — Requires Orthodontist Review"
    synthetic_notice: Literal["SYNTHETIC DEMONSTRATION — NOT CLINICAL ADVICE"] | None = None
    evidence_domain: Literal["UNVERIFIED", "TEST_ONLY"]
    clinical_analysis_enabled: Literal[False] = False
    parsed: ParseResult
    engine_review: DraftReview
    stage_inspection: StageInspection
    fictional_arches: tuple[FictionalArch, ...] = ()
    fictional_segments: tuple[FictionalSegment, ...] = ()
    entries: tuple[SequencingEntry, ...] = Field(min_length=6, max_length=32)
    wording_source: Literal["DETERMINISTIC_TEMPLATES"] = "DETERMINISTIC_TEMPLATES"
    provider: None = None
    provider_attempts: Literal[0] = 0
    limitations: tuple[str, ...]
    export_format: Literal["text/plain;charset=utf-8"] = "text/plain;charset=utf-8"
    export_text: str

    @model_validator(mode="after")
    def bind_report(self):
        if self.evidence_domain != self.engine_review.evidence_domain or self.parsed.raw_sha256 != self.engine_review.raw_sha256:
            raise ValueError("Sequencing source binding invalid")
        if (self.synthetic_notice is not None) != (self.evidence_domain == "TEST_ONLY"):
            raise ValueError("Synthetic notice required only for fixed demonstration")
        if self.evidence_domain == "UNVERIFIED" and (self.stage_inspection.records or self.fictional_arches or self.fictional_segments):
            raise ValueError("No supplied staged evidence in normal requests")
        if {e.section for e in self.entries} != {"UPPER_ARCH", "LOWER_ARCH", "SEGMENTS", "RIGHT_ANCHORAGE", "LEFT_ANCHORAGE", "UNAVAILABLE"}:
            raise ValueError("All sequencing sections required")
        if len({e.entry_id for e in self.entries}) != len(self.entries):
            raise ValueError("Duplicate sequencing entry")
        teeth = {t.id: t.raw_identifier for t in self.parsed.teeth}
        findings = {f.finding_id for f in self.engine_review.findings}
        measurements = {m.id for m in self.parsed.measurements}
        arches = {a.arch_id: a for a in self.fictional_arches}
        segments = {s.segment_id: s for s in self.fictional_segments}
        stages = {s.stage_id: s for s in self.stage_inspection.records}
        source_scopes = {c.canonical_value for f in self.engine_review.findings for o in f.observed_measurements for c in o.components if c.name == "scope"}
        expected_scope = "TOTAL" if self.evidence_domain == "TEST_ONLY" and source_scopes == {"TOTAL"} else self.parsed.source.context.scope
        for e in self.entries:
            if e.result_type == "STRUCTURAL_OBSERVATION" and (self.stage_inspection.status != "SUPPLIED_SYNTHETIC_METADATA" or e.evidence_status != "TEST_ONLY"):
                raise ValueError("Structural observation requires checked supplied stage metadata")
            if not set(e.finding_refs) <= findings or not set(e.measurement_refs) <= measurements:
                raise ValueError("Unknown source/finding references")
            if any(teeth.get(ref) != token for ref, token in zip(e.original_tooth_refs, e.original_tooth_tokens)):
                raise ValueError("Original tooth token altered")
            if e.synthetic_arch_id and e.synthetic_arch_id not in arches or e.synthetic_segment_id and e.synthetic_segment_id not in segments:
                raise ValueError("Unknown fictional identity")
            entry_scope = self.parsed.source.context.scope if e.evidence_status == "UNVERIFIED" and e.original_tooth_refs else expected_scope
            if e.movement_scope != entry_scope:
                raise ValueError("Movement scope must preserve source evidence/claim status")
            if e.synthetic_arch_id:
                if e.section in {"UPPER_ARCH", "LOWER_ARCH"} and arches[e.synthetic_arch_id].role != e.section.removesuffix("_ARCH"):
                    raise ValueError("Fictional arch role mismatches report section")
                allowed_refs = {ref for s in segments.values() if s.arch_id == e.synthetic_arch_id and (e.side == "UNKNOWN" or s.side == e.side) for ref in s.tooth_refs}
                if not set(e.original_tooth_refs) <= allowed_refs:
                    raise ValueError("Fictional arch/side source references mismatch")
            if e.synthetic_segment_id:
                segment = segments[e.synthetic_segment_id]
                if segment.arch_id != e.synthetic_arch_id or segment.side != e.side or not set(e.original_tooth_refs) <= set(segment.tooth_refs):
                    raise ValueError("Fictional segment/side binding mismatch")
            if self.evidence_domain == "UNVERIFIED" and (e.result_type in {"SUPPLIED_SYNTHETIC", "STRUCTURAL_OBSERVATION"} or e.evidence_status != "UNVERIFIED"):
                raise ValueError("Normal input cannot gain supplied strategy authority")
            if e.stage_window:
                start, end = stages.get(e.stage_window.start_id), stages.get(e.stage_window.end_id)
                if (self.stage_inspection.status != "SUPPLIED_SYNTHETIC_METADATA" or not start or not end
                    or start.arch != end.arch or start.arch != e.synthetic_arch_id or start.index > end.index):
                    raise ValueError("Invalid supplied stage window")
                if e.stage_kinds != tuple(dict.fromkeys((start.kind, end.kind))):
                    raise ValueError("Stage kinds must match supplied records")
        return self


class SequencingDemoInput(EvidenceContract):
    demo_id: Literal["FINOVA-NANO-1"] = "FINOVA-NANO-1"
    label: Literal["Finova Synthetic Sequencer Demonstration — TEST_ONLY"] = "Finova Synthetic Sequencer Demonstration — TEST_ONLY"
    convention: tuple[str, ...]
    context: SourceContext
    parsed: AutomaticParseResult
