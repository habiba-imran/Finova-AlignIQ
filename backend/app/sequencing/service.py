"""Existing evidence gates plus scoped presentation; no order/force/amount calculator."""
from app.parser.receipts import resolve
from app.review.context import stage_errors
from app.review.service import review_table
from app.semantics.fixtures import digest_json
from app.sequencing.models import SequencingDraft, SequencingEntry, StageInspection

SECTIONS = ("UPPER_ARCH", "LOWER_ARCH", "SEGMENTS", "RIGHT_ANCHORAGE", "LEFT_ANCHORAGE", "UNAVAILABLE")
GUARDS = {"G15", "N07", "N08", "N09", "N10", "N12", "N13", "R13", "R14", "H09", "H11", *(f"T{i:02}" for i in range(1, 9))}
MISSING = ("verified_source_and_arch_segment_identity", "actual_stage_bound_movement_dataset", "verified_scope_kind_and_coordinate_operations", "clinical_objectives_geometry_and_anchorage_context", "independently_approved_sequencing_policy")
LIMITATIONS = (
    "DRAFT — Requires Orthodontist Review. Prototype — not for clinical use. No clinician approval or sign-off is recorded.",
    "Supplied synthetic order and anchorage notes are fictional authored inputs, never recommendations calculated by the rule engine or an LLM.",
    "TOTAL movement values do not establish a movement order, simultaneous movement, stage allocations, stage ceilings, achieved movement or wear/treatment duration.",
    "Missing stage/anchorage data are unknown, never an indication for simultaneous movement or a conclusion that anchorage is not needed.",
    "Stage-record checks validate identifiers, ordering and kinds only. No stage-to-movement binding, movement composition, summation, subtraction or collision/force optimization is performed.",
    "Fictional upper/lower, segment and side identities are supplied scenario metadata, not anatomical interpretations of opaque tooth tokens or released vendor mappings.",
    "R13 and T01–T08 remain disabled. No clinical sequencing, anchorage, auxiliary, force, safety or suitability predicate is activated.",
    "Synthetic input only; runtime processing stays in memory. This module makes no LLM call and performs no persistence, CAD write-back or clinical approval.",
)


def entry(**data):
    value = SequencingEntry(entry_id="0" * 64, **data)
    return value.model_copy(update={"entry_id": digest_json(value.model_dump(mode="json", exclude={"entry_id"}))})


def refs(review):
    return tuple(f.finding_id for f in review.findings if f.rule_id in GUARDS)


def inspect_stages(scenario, evidence_ref):
    if not scenario or not scenario.stages:
        return StageInspection(status="MISSING", explanation="Actual stage records are unavailable. Neither total movements nor a claimed stage index reconstruct an ordered dataset.")
    issues = list(stage_errors(scenario.stages))
    stages = {s.stage_id: s for s in scenario.stages}
    if len(stages) != len(scenario.stages):
        issues.append("AMBIGUOUS_STAGE_IDENTIFIER")
    for statement in scenario.statements:
        window = statement.stage_window
        if not window:
            continue
        start, end = stages.get(window.start_id), stages.get(window.end_id)
        if not start or not end:
            issues.append("WINDOW_REFERENCE_MISSING")
        elif start.arch != end.arch or start.arch != statement.arch_id:
            issues.append("WINDOW_ARCH_MISMATCH")
        elif start.index > end.index:
            issues.append("WINDOW_ORDER_INVALID")
    return StageInspection(status="INVALID" if issues else "SUPPLIED_SYNTHETIC_METADATA", records=scenario.stages,
        issues=tuple(sorted(set(issues))), evidence_ref=evidence_ref,
        explanation="Supplied fictional stage identifiers/order/kinds failed structural checks; dependent windows/statements are withheld." if issues else
            "Supplied fictional stage identifiers, ordering and kinds passed structural checks only. TOTAL measurements are not stage-bound; no schedule or clinical sequence was computed.")


def assemble(parsed, review, *, scenario=None, evidence_ref=None):
    supplied = scenario is not None
    if supplied and (review.evidence_domain != "TEST_ONLY" or parsed.raw_sha256 != scenario.input_sha256 or not evidence_ref):
        raise ValueError("SCENARIO_AUTHORITY_OR_INPUT_MISMATCH")
    inspection = inspect_stages(scenario, evidence_ref)
    authorized_scopes = {c.canonical_value for f in review.findings for o in f.observed_measurements for c in o.components if c.name == "scope"}
    scope = "TOTAL" if supplied and authorized_scopes == {"TOTAL"} else parsed.source.context.scope
    shared = dict(finding_refs=refs(review), movement_scope=scope, missing_prerequisites=MISSING)
    entries = []
    if supplied:
        teeth = {t.id: t for t in parsed.teeth}
        if any(t not in teeth for segment in scenario.segments for t in segment.tooth_refs):
            raise ValueError("SCENARIO_TOOTH_REFERENCE_INVALID")
        segments = {s.segment_id: s for s in scenario.segments}
        stages = {s.stage_id: s for s in inspection.records}
        for statement in scenario.statements:
            segment = segments.get(statement.segment_id)
            tooth_refs = segment.tooth_refs if segment else tuple(dict.fromkeys(t for s in scenario.segments if s.arch_id == statement.arch_id and (statement.side == "UNKNOWN" or s.side == statement.side) for t in s.tooth_refs))
            failed = statement.stage_window is not None and inspection.status != "SUPPLIED_SYNTHETIC_METADATA"
            kinds = tuple(dict.fromkeys((stages[statement.stage_window.start_id].kind, stages[statement.stage_window.end_id].kind))) if statement.stage_window and not failed else ()
            entries.append(entry(section=statement.section, result_type="WITHHELD" if failed else "SUPPLIED_SYNTHETIC",
                origin="ENGINE_GUARD" if failed else "SUPPLIED_SCENARIO", evidence_status="TEST_ONLY",
                text="Supplied stage-dependent statement withheld because its stage records/window are missing or inconsistent. No replacement order is inferred." if failed else statement.text,
                original_tooth_refs=tooth_refs, original_tooth_tokens=tuple(teeth[t].raw_identifier for t in tooth_refs),
                synthetic_arch_id=statement.arch_id, synthetic_segment_id=statement.segment_id, side=statement.side,
                stage_window=None if failed else statement.stage_window, stage_kinds=kinds,
                evidence_refs=(f"{evidence_ref}:statements/{statement.key}",),
                measurement_refs=tuple(m.id for m in parsed.measurements if m.tooth_ref in tooth_refs), **shared))
        entries.append(entry(section="UNAVAILABLE", result_type="STRUCTURAL_OBSERVATION" if inspection.status == "SUPPLIED_SYNTHETIC_METADATA" else "WITHHELD",
            origin="ENGINE_GUARD", evidence_status="TEST_ONLY", text=inspection.explanation, evidence_refs=(evidence_ref,), **shared))
        # Token 15 has deliberately unverified movement identity in the fixed source.
        entries.append(entry(section="SEGMENTS", result_type="WITHHELD", origin="ENGINE_GUARD", evidence_status="UNVERIFIED",
            text="An anatomical segment for the unresolved source token is unavailable. Opaque numbering and missing semantic evidence cannot establish a segment or movement order.",
            original_tooth_refs=("tooth-5",), original_tooth_tokens=(teeth["tooth-5"].raw_identifier,),
            measurement_refs=tuple(m.id for m in parsed.measurements if m.tooth_ref == "tooth-5"), **{**shared, "movement_scope": parsed.source.context.scope}))
    else:
        messages = {
            "UPPER_ARCH": "Upper-arch sequencing is unavailable: no verified upper-arch identity, actual stage-bound movement dataset or approved sequencing policy is available.",
            "LOWER_ARCH": "Lower-arch sequencing is unavailable: no verified lower-arch identity, actual stage-bound movement dataset or approved sequencing policy is available.",
            "SEGMENTS": "Tooth-group and segment sequencing are unknown. Original tooth tokens and parsed magnitudes do not establish anatomical segments or movement order.",
            "RIGHT_ANCHORAGE": "Right-side anchorage information is unknown. Missing clinical and force-strategy context does not mean anchorage is unnecessary.",
            "LEFT_ANCHORAGE": "Left-side anchorage information is unknown. No anchorage requirement or absence is inferred from movement totals.",
        }
        for section, text in messages.items():
            entries.append(entry(section=section, result_type="WITHHELD" if section.endswith("_ARCH") else "UNKNOWN", origin="ENGINE_GUARD", evidence_status="UNVERIFIED", text=text,
                side=section.removesuffix("_ANCHORAGE") if section.endswith("_ANCHORAGE") else "UNKNOWN", **shared))
    entries.append(entry(section="UNAVAILABLE", result_type="DISABLED", origin="ENGINE_GUARD", evidence_status="UNVERIFIED",
        text="R13 and T01–T08 clinical decisions remain disabled. No stage ceiling, sequence, force, auxiliary, duration, collision-free result or anchorage prescription was evaluated.", **shared))
    body = dict(evidence_domain=review.evidence_domain, synthetic_notice="SYNTHETIC DEMONSTRATION — NOT CLINICAL ADVICE" if supplied else None,
        parsed=parsed, engine_review=review, stage_inspection=inspection,
        fictional_arches=scenario.arches if supplied else (), fictional_segments=scenario.segments if supplied else (), entries=tuple(entries),
        limitations=tuple(dict.fromkeys(LIMITATIONS + review.limitations)))
    provisional = SequencingDraft(report_id="0" * 64, export_text="", **body)
    report = SequencingDraft(report_id=digest_json(provisional.model_dump(mode="json", exclude={"report_id", "export_text"})), export_text="", **body)
    return report.model_copy(update={"export_text": export_text(report)})


def export_text(report):
    review = report.engine_review
    lines = ["FINOVA ALIGNIQ — SEQUENCER / NANO REVIEW", report.draft_status, "Prototype — not for clinical use",
        report.synthetic_notice or "UNVERIFIED INPUT — sequencing and anchorage advice withheld.",
        f"Report: {report.report_id}", f"Input SHA-256: {review.raw_sha256}", f"Engine report: {review.report_id}",
        f"Source claim: {review.source.source_claim}; version claim: {review.source.context.source_version or 'UNKNOWN'}; source movement scope claim: {review.source.context.scope}",
        f"Source stage index claim (unverified): {review.source.context.stage_index if review.source.context.stage_index is not None else 'UNKNOWN'}; plan mode claim: {review.source.context.plan_mode}; basis claim: {review.source.context.reference_basis}; coordinate frame claim: {review.source.context.coordinate_frame or 'UNKNOWN'}",
        f"Versions: parser {review.parser_version}; semantics {review.normalization_version}; engine {review.engine_version}; rules {review.rule_set_version}",
        "Wording: DETERMINISTIC_TEMPLATES; provider attempts: 0", "No clinical approval or sign-off is recorded."]
    for section in SECTIONS:
        lines.extend(("", section))
        for e in (e for e in report.entries if e.section == section):
            lines.extend((f"{e.result_type}; origin {e.origin}; evidence {e.evidence_status}; side {e.side}", e.text,
                f"Entry: {e.entry_id}; approval {e.approval_status}; policy UNKNOWN; {e.review_status}",
                f"Original tooth tokens: {', '.join(e.original_tooth_tokens) or 'UNKNOWN'}; references {', '.join(e.original_tooth_refs) or 'None assigned'}",
                f"Verified arch/segment/tooth: UNKNOWN; fictional arch {e.synthetic_arch_id or 'None'}; fictional segment {e.synthetic_segment_id or 'None'}",
                f"Movement scope claim: {e.movement_scope}; supplied stage kinds: {', '.join(e.stage_kinds) or 'UNKNOWN'}",
                f"Supplied stage window IDs: {e.stage_window.start_id} → {e.stage_window.end_id}; no movement allocation" if e.stage_window else "Stage window: UNAVAILABLE; no order inferred.",
                "Evidence references: " + (", ".join(e.evidence_refs) or "No accepted sequencing evidence"),
                "Lexical measurement refs: " + (", ".join(e.measurement_refs) or "No arch/segment assignment"),
                "Safeguard finding refs (not strategy triggers): " + ", ".join(e.finding_refs),
                "Missing prerequisites: " + ", ".join(e.missing_prerequisites), ""))
    lines += ["SUPPLIED FICTIONAL IDENTITIES (not anatomical inference)"]
    lines += [f"{a.arch_id}: {a.label}; role {a.role}" for a in report.fictional_arches]
    lines += [f"{s.segment_id}: {s.label}; arch {s.arch_id}; side {s.side}; original references {', '.join(s.tooth_refs)}" for s in report.fictional_segments]
    lines += ["", f"STAGE METADATA: {report.stage_inspection.status}", report.stage_inspection.explanation,
        "Movement binding: " + report.stage_inspection.movement_binding,
        "Stage issues: " + (", ".join(report.stage_inspection.issues) or "None recorded; this is not clinical approval"),
        "Stage source: " + (report.stage_inspection.evidence_ref or "Unavailable")]
    lines += [f"{s.stage_id}; index {s.index}; arch {s.arch}; kind {s.kind}; supplied evidence {s.evidence_ref}" for s in report.stage_inspection.records]
    lines += ["", "ORIGINAL LEXICAL VALUES — UNVERIFIED; NOT STAGE ALLOCATIONS"]
    teeth = {t.id: t.raw_identifier for t in report.parsed.teeth}
    lines += [f"{m.id}: original tooth {teeth[m.tooth_ref]}; {m.raw_label}; raw cell {repr(m.raw_value)}; scalar {m.signed_decimal}; magnitude {m.magnitude_decimal}; literal direction {m.raw_direction}; unit {m.unit}; {m.numeric_status}; source L{m.span.line}:C{m.span.column_start}" if m.span else f"{m.id}: cell not present; not zero" for m in report.parsed.measurements]
    lines += ["", "RULE EVALUATION LEDGER"] + [f"{e.rule_id} v{e.version}: {e.status}; {e.execution}; approval {e.approval_status}; findings {', '.join(e.finding_ids)}; missing {', '.join(e.missing_required_fields)}; reason {e.abstain_reason or 'See finding'}" for e in review.evaluations]
    lines += ["", "LIMITATIONS"] + list(report.limitations) + [report.draft_status, ""]
    return "\n".join(lines)


def sequencing_review(submission):
    parsed = resolve(submission)
    review = review_table(submission, requested_assessments=("COLLISIONS", "COMPLEX_INTERVENTION"))
    return assemble(parsed, review)
