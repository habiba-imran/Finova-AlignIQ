"""Deterministic review: derive trust internally, then observe only eligible fields."""

from collections import defaultdict

from app.domain.models import ParseResult, RawTMTSubmission
from app.parser.receipts import resolve
from app.review.models import (
    AssessmentQuestion, DraftReview, Finding, ObservedMeasurement, ReviewCoverage, RuleEvaluation, RuleRef,
)
from app.review.registry import RULES, execution_order
from app.review.safeguards import apply_output_safeguards, context_key, values
from app.review.templates import CONTEXT_MATRIX, LIMITATIONS, TEMPLATES
from app.semantics.fixtures import CheckedFixture, digest_json
from app.semantics.models import required_components
from app.semantics.normalization import assess_semantics

# Engineering output-size bound, not a clinical threshold. Lexical parsing limits are unchanged.
MAX_REVIEW_POSITIONS = 512


def _finding(rid, status, template, *, refs=(), observations=(), missing=(), reason=None, counts=None):
    refs = tuple(sorted(set(refs)))
    observations = tuple(sorted(observations, key=lambda o: o.measurement_id))
    tooth_ids = {values(o)["tooth_identifier"] for o in observations if o.verification == "VERIFIED"}
    kind = "DESCRIPTIVE" if observations else "TECHNICAL" if rid.startswith("G") else "OUTPUT" if rid.startswith("L") else "SAFETY"
    if status not in {"OBSERVED", "NOT_APPLICABLE"}:
        kind = "UNAVAILABLE"
    evidence = tuple(sorted({f"{e.fixture_id}:{e.release_digest}:{e.locator}" for o in observations for c in o.components for e in c.evidence}))
    body = dict(rule_id=rid, rule_version="2.0.0", triggering_rules=(RuleRef(rule_id=rid),),
                tooth_id=next(iter(tooth_ids)) if len(tooth_ids) == 1 else None,
                status=status, applicable=False if status == "NOT_APPLICABLE" else True if status == "OBSERVED" else None,
                evaluated=status == "OBSERVED", finding_type=kind, template_id=template, message=TEMPLATES[template],
                input_refs=refs, observed_measurements=observations, missing_required_fields=tuple(sorted(set(missing))),
                evidence_refs=evidence, abstain_reason=reason, summary_counts=counts or {})
    fid = digest_json({**body, "triggering_rules": [r.model_dump(mode="json") for r in body['triggering_rules']],
                       "observed_measurements": [o.model_dump(mode="json") for o in observations]})
    return Finding(finding_id=fid, **body)


def review_table(submission: RawTMTSubmission, *, requested_assessments: tuple[AssessmentQuestion, ...] = (),
                 checked: CheckedFixture | None = None, test_only: bool = False) -> DraftReview:
    """HTTP supplies raw submission only. Evidence/test switches are library-only, never request fields.

    No release lookup/generalizing adapter is implemented: production has no approved vendor mappings.
    Internal callers may supply an exact checked oracle; the existing registry is always rechecked.
    """
    if len(set(requested_assessments)) != len(requested_assessments) or any(q not in CONTEXT_MATRIX for q in requested_assessments):
        raise ValueError("INVALID_REVIEW_QUESTION")
    lexical = resolve(submission)
    if len(lexical.measurements) > MAX_REVIEW_POSITIONS:
        limited = []
        for rule in RULES:
            if rule.execution == "DISABLED":
                limited.append(_finding(rule.rule_id, "DISABLED", "disabled", reason=rule.reason, missing=rule.required_fields))
            elif rule.rule_id in {"H10", "L06", "H12", "A05", "A06"}:
                template = {"H10": "draft", "L06": "draft", "H12": "privacy", "A05": "placement", "A06": "superiority"}[rule.rule_id]
                limited.append(_finding(rule.rule_id, "OBSERVED", template))
            else:
                limited.append(_finding(rule.rule_id, "CONTEXT_REQUIRED", "context", refs=("coverage/declared_positions",),
                                        missing=("capture_with_at_most_512_measurement_positions",), reason="REVIEW_POSITION_ENGINEERING_LIMIT"))
        return _finish(lexical, "0.1.0-disabled", "UNVERIFIED", {}, apply_output_safeguards(limited, {}), requested_assessments)
    assessment = assess_semantics(lexical, checked, allow_test_only=test_only)
    domain = "TEST_ONLY" if assessment.status == "TEST_ONLY" else "AUTHORIZED_VENDOR" if any(m.canonical_measurement_ready for m in assessment.measurements) else "UNVERIFIED"
    raw_measurements = {m.id: m for m in lexical.measurements}
    teeth = {t.id: t for t in lexical.teeth}
    semantics = {m.measurement_id: m for m in assessment.measurements}
    eligible = {}
    missing_by_id = {}
    reasons_by_id = {}
    for sm in assessment.measurements:
        m = raw_measurements[sm.measurement_id]
        component = {c.name: c for c in sm.components}
        v = {name: c.canonical_value for name, c in component.items()}
        authority = "TEST_ONLY" if domain == "TEST_ONLY" else "VERIFIED"
        missing = {name for name in required_components(v) if component[name].status != authority}
        reasons = []
        if domain == "TEST_ONLY" and (not test_only or lexical.source.source_claim != "Unknown" or lexical.source.detected_claims or v.get("source_application") != "TEST_ONLY"):
            reasons.append("SYNTHETIC_VENDOR_BOUNDARY")
        ready = sm.evidence_complete_for_test if domain == "TEST_ONLY" else sm.canonical_measurement_ready
        if not ready:
            reasons.append("SEMANTICS_NOT_AUTHORIZED")
        if v.get("plan_mode") == "COMPARISON" or sm.value_kind == "SOURCE_REPORTED_COMPARISON":
            reasons.append("COMPARISON_NOT_ABSOLUTE")
            missing.add("absolute_programmed_plan")
        if m.numeric_status not in {"PARSED", "EXPLICIT_ZERO"}:
            missing.add("numeric_value")
        if missing or reasons:
            missing_by_id[m.id] = tuple(sorted(missing))
            reasons_by_id[m.id] = "COMPARISON_NOT_ABSOLUTE" if "COMPARISON_NOT_ABSOLUTE" in reasons else reasons[0] if reasons else "REQUIRED_FIELDS_UNVERIFIED"
            continue
        tooth = teeth[m.tooth_ref]
        spans = tuple(s for s in (tooth.span, m.header_span, m.span) if s is not None)
        refs = (f"measurements/{m.id}", f"teeth/{tooth.id}", "source/context")
        eligible[m.id] = ObservedMeasurement(
            measurement_id=m.id, tooth_ref=m.tooth_ref, raw_tooth_identifier=tooth.raw_identifier,
            raw_label=m.raw_label, raw_value=m.raw_value, raw_number=m.raw_number, raw_sign=m.raw_sign,
            raw_direction=m.raw_direction, signed_decimal=m.signed_decimal,
            magnitude=m.magnitude_decimal, verification=authority, components=sm.components,
            input_refs=refs, source_spans=spans,
        )

    findings = []

    def emit(rid, status, template, **kwargs):
        f = _finding(rid, status, template, **kwargs)
        findings.append(f)
        return f

    def unavailable(rid, ids, *, reason=None, missing=()):
        ids = tuple(sorted(ids))
        fields = set(missing)
        for mid in ids:
            fields.update(missing_by_id.get(mid, ()))
        why = reason or next((reasons_by_id[mid] for mid in ids if mid in reasons_by_id), "REQUIRED_CONTEXT_UNAVAILABLE")
        status = "SEMANTICS_UNKNOWN" if fields.intersection({"source_application", "source_version", "notation", "axis", "sign", "direction"}) else "CONTEXT_REQUIRED"
        return emit(rid, status, "unknown" if status == "SEMANTICS_UNKNOWN" else "context",
                    refs=tuple(f"measurements/{mid}" for mid in ids), missing=fields, reason=why)

    # G rules delegate to existing parser/semantic results. No second numerical/tooth parser.
    component_gates = {"G02": ("source_application", "source_version"), "G03": ("notation", "dentition", "arch"),
                       "G04": ("tooth_identifier", "notation", "dentition"), "G05": ("arch",), "G07": ("axis",),
                       "G09": ("sign", "direction"), "G11": ("reference_basis",), "G12": ("scope",), "G13": ("plan_mode",)}
    for rule in execution_order():
        rid = rule.rule_id
        if rid == "G15" and lexical.source.context.scope not in {"CUMULATIVE", "INCREMENTAL"} and lexical.source.context.stage_index is None:
            emit(rid, "NOT_APPLICABLE", "not_applicable")
            continue
        if rule.execution != "ACTIVE":
            emit(rid, "DISABLED" if rule.execution == "DISABLED" else "CONTEXT_REQUIRED", "disabled" if rule.execution == "DISABLED" else "context",
                 missing=rule.required_fields, reason=rule.reason)
            continue
        if rid == "G01":
            valid = bool(lexical.measurements) and lexical.status not in {"INVALID", "UNSUPPORTED"}
            emit(rid, "OBSERVED" if valid else "PARSE_INVALID", "gate" if valid else "context", refs=("layout",),
                 missing=() if valid else ("lexical_structure",), reason=None if valid else "LEXICAL_STRUCTURE_UNAVAILABLE")
        elif rid.startswith("G"):
            for m in lexical.measurements:
                fields = ()
                if rid in component_gates:
                    components = {c.name: c for c in semantics[m.id].components}
                    names = list(component_gates[rid])
                    if rid == "G12" and components['scope'].canonical_value in {"CUMULATIVE", "INCREMENTAL", "STAGE_SPECIFIC"}:
                        names.extend(("stage_index", "stage_kind"))
                    if rid == "G13" and components['plan_mode'].canonical_value == "COMPARISON":
                        names.extend(("comparison_left_plan", "comparison_right_plan", "comparison_operation"))
                    fields = tuple(n for n in names if components[n].status not in {"VERIFIED", "TEST_ONLY"})
                elif rid == "G06":
                    fields = ("duplicate_scope",) if m.duplicate_group else ()
                elif rid in {"G08", "G10"}:
                    fields = ("numeric_value",) if m.numeric_status not in {"PARSED", "EXPLICIT_ZERO"} else ()
                    if rid == "G08" and m.unit is None:
                        fields += ("unit",)
                elif rid == "G16":
                    fields = ("source_provenance",) if m.span is None or not lexical.raw_sha256 else ()
                elif rid == "G17":
                    fields = missing_by_id.get(m.id, ()) or (("field_semantic_eligibility",) if m.id not in eligible else ())
                emit(rid, "SEMANTICS_UNKNOWN" if fields else "OBSERVED", "unknown" if fields else "gate",
                     refs=(f"measurements/{m.id}",), missing=fields, reason="EXISTING_GATE_NOT_SATISFIED" if fields else None)
            if not lexical.measurements:
                emit(rid, "CONTEXT_REQUIRED", "context", refs=("layout",), missing=rule.required_fields, reason="NO_MEASUREMENT_POSITIONS")
        elif rid == "D01":
            for m in lexical.measurements:
                if m.id not in eligible:
                    unavailable(rid, (m.id,))
                elif eligible[m.id].magnitude.is_zero():
                    emit(rid, "NOT_APPLICABLE", "not_applicable", refs=eligible[m.id].input_refs)
                else:
                    o = eligible[m.id]
                    emit(rid, "OBSERVED", "inventory", refs=o.input_refs, observations=(o,))
            if not lexical.measurements:
                unavailable(rid, (), missing=("measurement_positions",))
        elif rid in {"D06", "D07", "D08"}:
            target = {"D06": {"INCLINATION", "ANGULATION"}, "D07": {"BUCCOLINGUAL"}, "D08": {"MESIODISTAL"}}[rid]
            matches = [o for o in eligible.values() if values(o)['axis'] in target and not o.magnitude.is_zero()]
            for o in matches:
                emit(rid, "OBSERVED", {"D06": "angular", "D07": "bl", "D08": "md"}[rid], refs=o.input_refs, observations=(o,))
            if not matches:
                if missing_by_id:
                    unavailable(rid, missing_by_id)
                else:
                    emit(rid, "NOT_APPLICABLE", "not_applicable")
        elif rid in {"D02", "D10", "D11", "D12", "D15"}:
            # Capture-local context keys include source/version, tooth, mode, basis, scope, stage and frame.
            groups = defaultdict(list)
            for o in eligible.values():
                key = context_key(o)
                if rid == "D12":
                    # Distribution spans teeth/arches but never spans basis/mode/scope/frame.
                    key = tuple(v for i, v in enumerate(key) if i not in {2, 5})
                groups[key].append(o)
            produced = False
            for group in groups.values():
                nonzero = [o for o in group if not o.magnitude.is_zero()]
                axes = {values(o)['axis'] for o in nonzero}
                if rid in {"D02", "D10", "D11"}:
                    if values(group[0])['scope'] != "TOTAL":
                        unavailable(rid, (o.measurement_id for o in group), reason="TOTAL_CO_PROGRAMMING_ONLY", missing=("total_plan_scope",))
                        produced = True
                        continue
                    matches = len(axes) >= 2
                    if rid == "D10":
                        matches = matches and "ROTATION" in axes and bool(axes & {"VERTICAL", "INTRUSION", "EXTRUSION"})
                    if rid == "D11":
                        matches = matches and bool(axes & {"INCLINATION", "ANGULATION"}) and bool(axes & {"MESIODISTAL", "BUCCOLINGUAL"})
                    if matches:
                        emit(rid, "OBSERVED", "co_programmed", refs=tuple(r for o in nonzero for r in o.input_refs), observations=nonzero)
                        produced = True
                elif rid == "D12" and nonzero:
                    emit(rid, "OBSERVED", "distribution", refs=tuple(r for o in nonzero for r in o.input_refs), observations=nonzero,
                         counts={"nonzero_positions": len(nonzero), "distinct_axes": len(axes),
                                 "distinct_teeth": len({values(o)['tooth_identifier'] for o in nonzero}),
                                 "distinct_arches": len({values(o)['arch'] for o in nonzero}),
                                 "eligible_positions_in_context": len(group)})
                    produced = True
                elif rid == "D15" and not nonzero:
                    # Missing/unverified sibling positions prohibit a categorical zero observation for that tooth.
                    tooth_refs = {o.tooth_ref for o in group}
                    siblings = [m.id for m in lexical.measurements if m.tooth_ref in tooth_refs and m.id not in eligible]
                    if siblings or any(i.code=='ASSOCIATION_UNRESOLVED' for i in lexical.issues):
                        unavailable(rid, siblings, reason="UNOBSERVED_AXES_PREVENT_ZERO_INVENTORY")
                    else:
                        emit(rid, "OBSERVED", "zero", refs=tuple(r for o in group for r in o.input_refs), observations=group)
                    produced = True
            if missing_by_id:
                unavailable(rid, missing_by_id)
                produced = True
            if not produced:
                emit(rid, "NOT_APPLICABLE", "not_applicable")
        elif rid in {"D14", "R14"}:
            if not requested_assessments:
                emit(rid, "NOT_APPLICABLE", "not_applicable")
            for question in sorted(requested_assessments):
                _, _, fields = CONTEXT_MATRIX[question]
                emit(rid, "CONTEXT_REQUIRED", "context", refs=(f"requested_assessments/{question}",), missing=fields,
                     reason="REQUESTED_ASSESSMENT_CONTEXT_UNAVAILABLE")
        elif rid in {entry[0] for entry in CONTEXT_MATRIX.values()}:
            entries = [(q, template, fields) for q, (code, template, fields) in CONTEXT_MATRIX.items() if code == rid and q in requested_assessments]
            for question, template, fields in entries:
                emit(rid, "CONTEXT_REQUIRED", template, refs=(f"requested_assessments/{question}",), missing=fields, reason="TMT_CANNOT_SUPPORT_REQUESTED_CONCLUSION")
            if not entries:
                emit(rid, "NOT_APPLICABLE", "not_applicable")
        elif rid in {"H10", "L06"}:
            emit(rid, "OBSERVED", "draft", refs=("report/review_status",))
        elif rid == "H12":
            emit(rid, "OBSERVED", "privacy", refs=("intake/synthetic_data_confirmed",))
        elif rid in {"A05", "A06"}:
            emit(rid, "OBSERVED", "placement" if rid == "A05" else "superiority")
        elif rid.startswith("L"):
            # These success records are appended only after the actual output validator below succeeds.
            continue
        elif rid.startswith("N"):
            if rid in {"N05", "N07"} and missing_by_id:
                unavailable(rid, missing_by_id)
            elif rid == "N06":
                emit(rid, "CONTEXT_REQUIRED", "context", missing=("verified_external_tooth_status",), reason="TOOTH_STATUS_NOT_INFERRED")
            else:
                emit(rid, "OBSERVED", "gate", refs=("report/limitations",))

    safe = apply_output_safeguards(findings, eligible)
    for rid in ("L01", "L02", "L03", "L04", "L05"):
        safe += (_finding(rid, "OBSERVED", "gate", refs=("report/findings",)),)
    safe = tuple(sorted(safe, key=lambda f: (f.rule_id, f.finding_id)))
    return _finish(lexical, assessment.normalization_version, domain, eligible, safe, requested_assessments)


def _finish(lexical: ParseResult, normalization_version: str, domain: str,
            eligible: dict[str, ObservedMeasurement], safe: tuple[Finding, ...],
            requested_assessments: tuple[AssessmentQuestion, ...]) -> DraftReview:
    evaluations = []
    for rule in RULES:
        fs = [f for f in safe if rule.rule_id in {r.rule_id for r in f.triggering_rules}]
        # Mixed field results retain their individual statuses; the aggregate reports the limiting state.
        priority = ("SUPPRESSED", "PARSE_INVALID", "SEMANTICS_UNKNOWN", "CONTEXT_REQUIRED", "DISABLED", "OBSERVED", "NOT_APPLICABLE")
        status = next(s for s in priority if any(f.status == s for f in fs))
        evaluations.append(RuleEvaluation(rule_id=rule.rule_id, status=status, finding_ids=tuple(f.finding_id for f in fs),
                                          missing_required_fields=tuple(sorted({n for f in fs for n in f.missing_required_fields})),
                                          abstain_reason=next((f.abstain_reason for f in fs if f.status == status and f.abstain_reason), None)))
    coverage = ReviewCoverage(declared_positions=len(lexical.measurements), eligible_positions=len(eligible),
                              unavailable_positions=len(lexical.measurements) - len(eligible),
                              eligible_explicit_zero=sum(o.magnitude.is_zero() for o in eligible.values()),
                              eligible_nonzero=sum(not o.magnitude.is_zero() for o in eligible.values()), lexical=lexical.coverage)
    report_body = dict(evidence_domain=domain, raw_sha256=lexical.raw_sha256, parser_version=lexical.parser_version,
                       normalization_version=normalization_version, source=lexical.source, coverage=coverage,
                       requested_assessments=tuple(sorted(requested_assessments)), findings=safe, evaluations=tuple(evaluations), limitations=LIMITATIONS)
    provisional = DraftReview(report_id="0" * 64, **report_body)
    content = provisional.model_dump(mode="json", exclude={"report_id"})
    return DraftReview(report_id=digest_json(content), **report_body)
