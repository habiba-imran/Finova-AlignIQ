"""Closed wording alternatives and exact local fact rendering, never free-form advice."""

import json

from app.review.models import Finding, ObservedMeasurement
from app.review.safeguards import values
from app.review.templates import TEMPLATES

ALTERNATIVES = {
    'group_rotation': 'Programmed rotation is described with independent tooth-group evidence. No clinical risk or failure prediction is provided.',
    'group_extrusion': 'Programmed extrusion is described with independent tooth-group evidence. No treatment auxiliary or outcome is inferred.',
    'group_intrusion': 'Programmed intrusion is described with independent tooth-group evidence. Group membership is not a danger classification.',
    'molar_md': 'Programmed molar mesial/distal displacement is described using independent group and direction evidence. Sequence and treatment outcome remain unassessed.',
    'paired_difference': 'Programmed magnitudes differ between independently paired positions in equivalent context. No pathology, subtraction or treatment conclusion is asserted.',
    "inventory": "The source-reported programmed value is listed in its stated mode, basis and scope. Achieved movement is not assessed.",
    "co_programmed": "These distinct axes are co-programmed within the same total plan scope. Their temporal overlap is unknown.",
    "angular": "The source reports programmed inclination or angulation. This does not establish achieved root movement or torque control.",
    "bl": "The source reports programmed buccolingual displacement. Expansion and bodily movement are not assessed.",
    "md": "The source reports programmed mesiodistal displacement. Anchorage, space closure and root movement are not assessed.",
    "zero": "Each supported, observed axis is explicitly zero in this scope. Unlisted axes remain unknown.",
    "distribution": "This capture's eligible nonzero positions and distinct axes, teeth and arches are counted within compatible context. Magnitudes are not added.",
}


def wording_options(finding: Finding) -> tuple[str, str]:
    return TEMPLATES[finding.template_id], ALTERNATIVES[finding.template_id]


def literal(value: str | None) -> str:
    # Quote untrusted data; line breaks/control characters cannot impersonate report headings.
    return "UNKNOWN" if value is None else json.dumps(value, ensure_ascii=False)


def measurement_text(o: ObservedMeasurement) -> str:
    v = values(o)
    fields = ("tooth_identifier", "notation", "dentition", "arch", "axis", "unit", "sign", "direction",
              "source_application", "source_version", "plan_mode", "reference_basis", "scope", "stage_index", "stage_kind", "coordinate_frame")
    canonical = "; ".join(f"{name}: {literal(v.get(name))}" for name in fields)
    extra=(f" Independent group: {literal(o.tooth_group)}; additional evidence: {literal(', '.join(o.additional_evidence_refs))}." if o.tooth_group else '')
    return (f"Programmed magnitude: {str(o.magnitude)}; lexical signed scalar: {str(o.signed_decimal)}. "
            f"Evidence: {o.verification}. {canonical}. "
            f"Original tooth: {literal(o.raw_tooth_identifier)}; original label: {literal(o.raw_label)}; "
            f"original cell: {literal(o.raw_value)}; original number: {literal(o.raw_number)}; "
            f"original sign: {literal(o.raw_sign)}; original direction: {literal(o.raw_direction)}. "
            f"Source position: {o.measurement_id}; "
            + ", ".join(f"L{s.line}:C{s.column_start}-C{s.column_end} [offsets {s.start}:{s.end}]" for s in o.source_spans) + extra)


def render_comment(finding: Finding, *, wording: str | None = None) -> str:
    # Reuse audit-approved abstention/safety templates, not arbitrary Finding.message input.
    text = wording if wording is not None else TEMPLATES[finding.template_id]
    if finding.summary_counts:
        text += "\nCoverage counts: " + "; ".join(f"{key}={value}" for key, value in sorted(finding.summary_counts.items())) + "."
    for o in finding.observed_measurements:
        text += "\n" + measurement_text(o)
    if finding.missing_required_fields:
        text += "\nRequired information: " + ", ".join(finding.missing_required_fields) + "."
    if finding.abstain_reason:
        text += "\nAssessment withheld: " + finding.abstain_reason + "."
    return text
