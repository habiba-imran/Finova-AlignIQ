"""Conservative presentation assignment. A dimension is not a clinical assessment."""

from app.planning.models import PlanningDraft, PlanningSection
from app.reports.models import FinalDraftReport, ReportComment
from app.review.safeguards import context_key, values
from app.semantics.models import required_components

EXPLANATIONS = {
    "SAGITTAL": "Authorized mesiodistal movement descriptions only; sagittal relationships and correction strategies are unavailable.",
    "TRANSVERSE": "Authorized buccolingual movement descriptions only; arch expansion, skeletal relationships and bone limits are unavailable.",
    "VERTICAL": "Authorized vertical movement descriptions only; bite, occlusal contacts and clinical adequacy are unavailable.",
    "OTHER": "Cross-dimension summaries, rotations and observations without an approved dimension convention remain here without reinterpretation.",
    "UNAVAILABLE": "Withheld assessments and missing information. Unavailable does not mean normal or no concern.",
}


def dimension(comment: ReportComment) -> str:
    if comment.section == "UNAVAILABLE":
        return "UNAVAILABLE"
    if not comment.measurements or comment.evidence_status != "TEST_ONLY":
        # No production vendor dimension mappings have been approved.
        return "OTHER"
    assigned = set()
    contexts = set()
    for observation in comment.measurements:
        v = values(observation)
        components = {c.name: c for c in observation.components}
        if (observation.verification != "TEST_ONLY"
            or any(components.get(k) is None or components[k].status != "TEST_ONLY" for k in required_components(v))
            or any(not c.evidence for k, c in components.items() if k in required_components(v))
            or any(v.get(k) != value for k, value in {
                "source_application": "TEST_ONLY", "source_version": "FINOVA-DEMO-1",
                "notation": "FINOVA_OPAQUE", "dentition": "SYNTHETIC", "arch": "DEMO_ARCH",
                "plan_mode": "TEST_PLAN_MODE", "reference_basis": "DEMO_CROWN_POINT",
                "scope": "TOTAL", "coordinate_frame": "FINOVA_LOCAL_AXES_V1",
            }.items())):
            return "OTHER"
        axis, direction = v.get("axis"), v.get("direction")
        if v.get("unit") != "mm":
            return "OTHER"
        if axis == "MESIODISTAL" and direction in {"MESIAL", "DISTAL"}:
            assigned.add("SAGITTAL")
        elif axis == "BUCCOLINGUAL" and direction in {"BUCCAL", "LINGUAL"}:
            assigned.add("TRANSVERSE")
        elif axis == "EXTRUSION" and direction == "EXTRUSION":
            assigned.add("VERTICAL")
        else:
            return "OTHER"
        contexts.add(context_key(observation))
    # Do not slice or duplicate a compound comment to make it appear dimension-specific.
    return assigned.pop() if len(assigned) == 1 and len(contexts) == 1 else "OTHER"


def organize(report: FinalDraftReport) -> PlanningDraft:
    groups = {key: [] for key in EXPLANATIONS}
    for comment in report.comments:
        groups[dimension(comment)].append(comment.comment_id)
    sections = tuple(PlanningSection(dimension=key, comment_ids=tuple(ids),
        explanation=("No sufficiently authorized descriptions for this dimension. " if not ids and key in {"SAGITTAL", "TRANSVERSE", "VERTICAL"} else "") + EXPLANATIONS[key])
        for key, ids in groups.items())
    index = ["FINOVA ALIGNIQ — PLANNING ASSISTANT / MACRO REVIEW", report.draft_status,
        "FINOVA SYNTHETIC DEMONSTRATION — TEST_ONLY; no patient or vendor validation." if report.engine_review.evidence_domain == "TEST_ONLY" else "Vendor semantics unverified; unavailable does not mean normal.",
        "DIMENSION PRESENTATION INDEX — descriptive grouping only, no complete clinical assessment."]
    for section in sections:
        index.extend((section.dimension, section.explanation, "Comment IDs: " + (", ".join(section.comment_ids) or "None authorized")))
    return PlanningDraft(report=report, sections=sections, export_text="\n".join(index) + "\n\n" + report.export_text)
