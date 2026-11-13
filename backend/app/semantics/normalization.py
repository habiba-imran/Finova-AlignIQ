"""Field-level evidence projection. No general vendor maps or arithmetic are implemented."""

from app.domain.models import ParseResult
from app.semantics.fixtures import CheckedFixture
from app.semantics.models import (
    COMPONENTS, EvidenceRef, FixtureExpectedOutput, FixtureRecord, SemanticAssessment,
    SemanticComponent, SemanticMeasurement, required_components,
)
from app.semantics.registry import DEFAULT_REGISTRY, EvidenceRegistry

VALUE_COMPONENTS = frozenset({"sign", "direction"})
DEPENDENT_ON_BASIS = frozenset({"axis", "sign", "direction"})


def assess_semantics(lexical: ParseResult, checked: CheckedFixture | None = None, *,
                     registry: EvidenceRegistry = DEFAULT_REGISTRY, allow_test_only: bool = False) -> SemanticAssessment:
    # Clone and validate; the original lexical result, including its always-null canonical fields, is untouched.
    snapshot = ParseResult.model_validate_json(lexical.model_dump_json())
    authority = None
    expected = None
    record = None
    reason = "NO_VERIFIED_VENDOR_MAPPING"
    if checked:
        try:
            authority = registry.authority(checked, allow_test_only=allow_test_only)
            expected = FixtureExpectedOutput.model_validate_json(checked.expected_json)
            record = FixtureRecord.model_validate_json(checked.record_json)
            # Bind raw bytes, all context claims, parser/adapter versions, cells, spans, and field states.
            if snapshot.model_dump(mode="json") != expected.lexical.model_dump(mode="json") or checked.lexical_json != expected.lexical.model_dump_json():
                authority = None
                reason = "EVIDENCE_INPUT_OR_CONTEXT_MISMATCH"
            elif authority is None:
                reason = "EVIDENCE_NOT_RELEASED_OR_REVOKED"
        except ValueError:
            authority = None
            reason = "EVIDENCE_INVALID"
    expected_by_id = {m.measurement_id: m for m in expected.measurements} if authority and expected else {}
    teeth = {tooth.id: tooth for tooth in snapshot.teeth}
    measurements = []
    for measurement in snapshot.measurements:
        tooth = teeth[measurement.tooth_ref]
        context = snapshot.source.context
        claims = {name: getattr(context, name, None) for name in COMPONENTS}
        claims.update(source_application=snapshot.source.source_claim, tooth_identifier=tooth.raw_identifier,
                      axis=measurement.recognized_label, unit=measurement.unit, sign=measurement.raw_sign,
                      direction=measurement.raw_direction)
        assertions = {c.name: c for c in expected_by_id[measurement.id].components} if measurement.id in expected_by_id else {}
        conflicts = {name for name, assertion in assertions.items()
                     if name in {"source_application", "source_version", "notation", "dentition", "arch", "plan_mode", "reference_basis", "scope", "stage_index", "coordinate_frame"}
                     and assertion.value is not None and claims.get(name) not in {None, "UNKNOWN", "Unknown"}
                     and str(claims[name]) != assertion.value}
        if any(issue.code == "SOURCE_CLAIM_CONFLICT" for issue in snapshot.issues):
            conflicts.add("source_application")
        conflicts.update(issue.field for issue in snapshot.issues
                         if issue.code == "SOURCE_CONTEXT_CONFLICT" and issue.field in COMPONENTS)
        components = []
        for name in COMPONENTS:
            assertion = assertions.get(name)
            claim = claims.get(name)
            reasons = []
            status = "UNKNOWN"
            value = None
            evidence = ()
            if not authority:
                reasons.append(reason)
            elif name in conflicts or "source_application" in conflicts or "source_version" in conflicts:
                reasons.append("SOURCE_OR_CONTEXT_CONFLICT")
                status = "CONFLICT"
            elif "reference_basis" in conflicts and name in DEPENDENT_ON_BASIS:
                reasons.append("INCOMPATIBLE_REFERENCE_BASIS")
                status = "CONFLICT"
            elif name in VALUE_COMPONENTS and measurement.numeric_status not in {"PARSED", "EXPLICIT_ZERO"}:
                reasons.append("VALUE_NOT_PRESENT_OR_INVALID")
                status = "INVALID" if measurement.numeric_status in {"INVALID", "AMBIGUOUS"} else "UNKNOWN"
            elif measurement.duplicate_group and name in {"tooth_identifier", "axis", "sign", "direction"}:
                reasons.append("DUPLICATE_POSITION_UNRESOLVED")
                status = "CONFLICT"
            elif name in {"tooth_identifier", "notation", "dentition", "arch"} and tooth.identifier_status == "INVALID":
                reasons.append("TOOTH_SYNTAX_OR_ARCH_CONFLICT")
                status = "CONFLICT"
            elif name == "unit" and any(i.code in {"UNIT_CONFLICT", "UNSUPPORTED_HEADER_UNIT"} and measurement.id in i.measurement_ids for i in snapshot.issues):
                reasons.append("UNIT_CONFLICT")
                status = "CONFLICT"
            elif name == "unit" and assertion and assertion.value is not None and (
                assertion.value not in {"mm", "deg"} or measurement.unit is not None and assertion.value != measurement.unit
            ):
                reasons.append("UNIT_CONVERSION_NOT_IMPLEMENTED")
                status = "CONFLICT"
            elif assertion and assertion.value is not None:
                value = assertion.value
                status = authority
                evidence = (EvidenceRef(fixture_id=record.fixture_id, release_digest=checked.release_digest,
                                        raw_sha256=record.raw.sha256, expected_sha256=record.expected.sha256,
                                        source_evidence_sha256=record.source_evidence.sha256 if record.source_evidence else None,
                                        locator=assertion.evidence_locator),)
            else:
                reasons.append("FIELD_EVIDENCE_MISSING")
            if not authority:
                if name == "notation" and context.notation == "UNKNOWN":
                    reasons.append("NUMBERING_AMBIGUOUS")
                if name == "source_version":
                    reasons.append("SOURCE_VERSION_UNVERIFIED")
            spans = tuple(s for s in (measurement.span, measurement.header_span, tooth.span)
                          if s is not None) if name in {"tooth_identifier", "axis", "unit", "sign", "direction"} else ()
            components.append(SemanticComponent(name=name, status=status, claim_value=str(claim) if claim is not None else None,
                                                canonical_value=value, evidence=evidence, abstain_reasons=tuple(reasons),
                                                input_refs=(f"measurements/{measurement.id}", f"teeth/{tooth.id}", f"source/context/{name}"),
                                                source_spans=spans))
        by_name = {component.name: component for component in components}
        required = required_components({name: c.canonical_value for name, c in by_name.items()})
        scope = by_name["scope"].canonical_value
        mode = by_name["plan_mode"].canonical_value
        abstentions = [f"{name}:UNVERIFIED" for name in sorted(required) if authority is None or by_name[name].status != authority]
        if scope not in {"TOTAL", "CUMULATIVE", "INCREMENTAL", "STAGE_SPECIFIC"}:
            abstentions.append("MOVEMENT_SCOPE_UNKNOWN_OR_UNSUPPORTED")
        if mode not in {"ALIGN_FINAL", "DOCTOR_FINAL", "COMPARISON"} and not (authority == "TEST_ONLY" and mode == "TEST_PLAN_MODE"):
            abstentions.append("PLAN_MODE_UNKNOWN_OR_UNSUPPORTED")
        if mode == "COMPARISON":
            operands = [by_name[name].canonical_value for name in ("comparison_left_plan", "comparison_right_plan")]
            if None in operands or operands[0] == operands[1]:
                abstentions.append("COMPARISON_OPERANDS_REQUIRED")
        if measurement.numeric_status not in {"PARSED", "EXPLICIT_ZERO"} or measurement.field_status in {"PARSE_INVALID", "UNSUPPORTED", "AMBIGUOUS"}:
            abstentions.append("LEXICAL_FIELD_INELIGIBLE")
        complete_for_test = not abstentions and authority == "TEST_ONLY"
        if authority == "TEST_ONLY":
            abstentions.append("TEST_ONLY_NOT_VENDOR_EVIDENCE")
        ready = not abstentions and authority == "VERIFIED"
        measurements.append(SemanticMeasurement(
            measurement_id=measurement.id, components=tuple(components), canonical_measurement_ready=ready,
            evidence_complete_for_test=complete_for_test,
            canonical_magnitude=measurement.magnitude_decimal if ready else None,
            value_kind=("SOURCE_REPORTED_COMPARISON" if mode == "COMPARISON" else "SOURCE_REPORTED_MOVEMENT") if ready else "UNKNOWN",
            abstain_reasons=tuple(abstentions),
        ))
    if not authority:
        status = "DISABLED"
    elif authority == "TEST_ONLY":
        status = "TEST_ONLY"
    elif measurements and all(m.canonical_measurement_ready for m in measurements) and snapshot.status == "PARSED_UNVERIFIED":
        status = "VERIFIED"
    elif any(c.status == "VERIFIED" for m in measurements for c in m.components):
        status = "PARTIAL"
    else:
        status = "ABSTAINED"
    return SemanticAssessment(status=status, lexical=snapshot, measurements=tuple(measurements),
                              reasons=(reason,) if not authority else ("TEST_ONLY_NOT_VENDOR_EVIDENCE",) if authority == "TEST_ONLY" else ())
