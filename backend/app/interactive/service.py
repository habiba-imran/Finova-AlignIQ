"""Analytical synthetic reports and separate supplied-record reviews.

Deterministic cross-tooth findings precede bounded provider wording. Complete
facts and provenance remain local; source claims never grant clinical authority.
"""
import json

from app.interactive.models import InteractiveReport, ToothObservation
from app.interactive.module_reports import module_sections, validate_details
from app.interactive.analysis import analyze
from app.interactive.analytical_wording import analytical_wording
from app.parser.receipts import resolve
from app.reports.groq_client import GroqClient
from app.reports.models import GenerationInfo, WordingBatch
from app.reports.settings import load_settings
from app.reports.validation import private_json
from app.review.service import review_table
from app.semantics.fixtures import digest_json
from app.functional.engine import functional_review
from app.functional.provider import provider_evidence
from app.functional.generalized import generalized_review

WORDINGS = {
    "F0001": ("The parsed source values are described below.", "The following observations summarize the values recorded in the synthetic table."),
    "F0002": ("Recorded values", "Source-reported movement observations"),
    "F0003": ("Illustrative attachment examples", "Simulated attachment examples for demonstration"),
    "F0004": ("Illustrative sequencing examples", "Simulated sequencing examples for demonstration"),
}
LIMITATIONS = [
    "Values describe the parsed source only. Tooth tokens, axes, directions, units and source conventions are not independently clinically verified.",
    "Missing, omitted, invalid and ambiguous values remain unknown; explicit zero applies only to its recorded cell. No achieved movement, suitability or safety conclusion is inferred.",
    "Clinical attachment, staging, anchorage, force, timing, diagnosis and treatment predicates remain unevaluated. No clinical approval is recorded.",
]


def load_wording_settings():
    # This endpoint transmits only the same constant phrase catalog for every run.
    # The legacy synthetic-data transmission switch still gates the unchanged
    # parser/report endpoints. No input data are transmitted by this endpoint.
    return load_settings().model_copy(update={"synthetic_transmission_enabled": True})


def wording(settings=None, client=None):
    selected = {ref: options[0] for ref, options in WORDINGS.items()}
    reason, attempts, accepted = "GROQ_NOT_CONFIGURED", 0, 0
    try:
        settings = settings or load_wording_settings()
    except ValueError:
        reason = "GROQ_CONFIGURATION_INVALID"
    else:
        if settings.configured:
            messages = [
                {"role": "system", "content": "Select professional wording from the supplied approved alternatives. Return exactly one comment for each finding_ids reference. Copy one approved wording exactly. Do not add facts, numbers, instructions or clinical decisions. All measurements will be inserted locally. Return JSON only."},
                {"role": "user", "content": json.dumps({"authorized_findings": [
                    {"finding_ids": [ref], "approved_wordings": list(options)} for ref, options in WORDINGS.items()
                ]}, separators=(",", ":"))},
            ]
            result = (client or GroqClient(settings)).generate(messages)
            attempts, reason = result.attempts, result.code
            if result.content is not None:
                try:
                    batch = WordingBatch.model_validate_json(json.dumps(private_json(result.content), allow_nan=False))
                    choices = {c.finding_ids[0]: c.text for c in batch.comments}
                    if len(batch.comments) != len(WORDINGS) or set(choices) != set(WORDINGS):
                        raise ValueError()
                    if any(text not in WORDINGS[ref] for ref, text in choices.items()):
                        raise ValueError()
                    selected, accepted, reason = choices, len(choices), "GROQ_VALIDATED"
                except (ValueError, TypeError, RecursionError):
                    reason = "GROQ_UNSUPPORTED_WORDING"
    info = GenerationInfo(requested_mode="AUTO", used_mode="GROQ_AI" if accepted else "STANDARD_TEMPLATES",
        reason=reason, attempts=attempts, provider="GROQ" if attempts else None,
        model="openai/gpt-oss-120b" if attempts else None, eligible_wording_findings=len(WORDINGS), accepted_comments=accepted)
    return selected, info


def quoted(value):
    return json.dumps(value, ensure_ascii=False)


def cell_text(m):
    label = quoted(m.raw_label)
    if m.numeric_status in {"PARSED", "EXPLICIT_ZERO"}:
        # Decimal -> str only; never round, sum, infer sign/direction or fill cells.
        text = f"{label}: {str(m.signed_decimal)}"
        text += f" {m.unit}" if m.unit else " (unit not reported)"
        if m.raw_direction is not None:
            text += f"; direction label {quoted(m.raw_direction)}"
        if m.numeric_status == "EXPLICIT_ZERO":
            text += "; explicitly recorded zero"
        return text + f". Original cell: {quoted(m.raw_value)}."
    status = {"MISSING": "missing", "NOT_PRESENT": "omitted", "INVALID": "invalid", "AMBIGUOUS": "ambiguous"}.get(m.numeric_status, "unrecognized")
    return f"{label}: {status}; no numerical observation (unknown, not zero). Original cell: {quoted(m.raw_value)}."


def generate_interactive(submission, *, settings=None, client=None):
    parsed = resolve(submission)
    if submission.raw_sha256 != parsed.raw_sha256 or any(i.code == "RECOVERY_RECEIPT_INVALID" for i in parsed.issues):
        raise ValueError("REPARSE_REQUIRED")
    if parsed.status in {"INVALID", "UNSUPPORTED"} or not parsed.measurements:
        raise ValueError("PARSE_REQUIRED")
    review = review_table(submission)
    if submission.planning_context is None and submission.planning_options is None:
        validate_details(parsed, submission)
    has_details = any((submission.review_details.attachments, submission.review_details.stages,
                       submission.review_details.allocations, submission.review_details.anchorage_notes))
    findings = []
    functional_plan = None
    policy_context = submission.planning_context
    if submission.planning_options is not None:
        if submission.planning_context is not None:
            raise ValueError('FUNCTIONAL_CONTEXT_INVALID')
        sections,findings,functional_plan,policy_context = generalized_review(parsed,submission)
        sections,generation = analytical_wording(parsed,submission.module,sections,findings,settings=settings,client=client,
            functional_evidence=provider_evidence(parsed,policy_context,functional_plan))
    elif submission.planning_context is not None:
        sections, findings, functional_plan = functional_review(parsed,submission)
        sections, generation = analytical_wording(parsed,submission.module,sections,findings,settings=settings,client=client,
            functional_evidence=provider_evidence(parsed,submission.planning_context,functional_plan))
    elif has_details:
        sections, generation = module_sections(parsed, submission, settings=settings, client=client)
    else:
        sections, findings = analyze(parsed, submission.module)
        sections, generation = analytical_wording(parsed, submission.module, sections, findings, settings=settings, client=client)
    narratives = None
    phrases = {ref: options[0] for ref, options in WORDINGS.items()}
    observations, illustrations = [], []
    by_tooth = {}
    for m in parsed.measurements:
        by_tooth.setdefault(m.tooth_ref, []).append(m)
    for tooth in parsed.teeth:
        cells = by_tooth.get(tooth.id, [])
        if not cells:
            continue
        observations.append(ToothObservation(tooth_ref=tooth.id, original_tooth=tooth.raw_identifier,
            text=narratives[tooth.id] if narratives is not None else phrases["F0002"] + ":\n" + "\n".join(cell_text(m) for m in cells), measurements=cells))
    numeric = sum(m.numeric_status in {"PARSED", "EXPLICIT_ZERO"} for m in parsed.measurements)
    missing = sum(m.numeric_status in {"MISSING", "NOT_PRESENT"} for m in parsed.measurements)
    other = len(parsed.measurements) - numeric - missing
    unresolved = any(i.severity == "ERROR" for i in parsed.issues) or any(
        m.field_status == "AMBIGUOUS" or m.numeric_status not in {"PARSED", "EXPLICIT_ZERO", "MISSING", "NOT_PRESENT"}
        for m in parsed.measurements)
    parse_note = f"Successfully parsed with {missing} missing value{'s' if missing != 1 else ''}." if not unresolved and all(m.recognized_label for m in parsed.measurements) else "Review the marked source entries for parsing limitations."
    lead = {"macro": "Programmed movement profile.", "micro": "TMT-based attachment review: rotation, angulation and inclination observations.", "nano": "TMT-based sequencing review: movement context, translations and vertical movements."}[submission.module]
    if submission.planning_options is not None:
        lead = {'macro':'Input-driven planning review.','micro':'Tooth-wise movement-profile attachment review.','nano':'Movement coordination and sequencing review.'}[submission.module]
    summary = f"{lead} {parse_note} {len(observations)} teeth; {len(parsed.measurements)} measurement positions; {numeric} recorded numerical values; {missing} missing or omitted; {other} invalid or ambiguous."
    if submission.planning_options is not None and parsed.source.context.plan_mode == 'COMPARISON':
        summary = 'Comparison source: these are recorded differences, not verified total movements. '+summary
    notice = "AI-assisted report wording." if generation.used_mode == "GROQ_AI" else "Standard report wording."
    limitations = (["Source values, units, direction labels and FDI-style token grouping remain unverified. Missing values remain unknown, not zero.",
        "Independent illustration policies do not establish clinical suitability, safe movement limits, forces or a treatment prescription."]
        if submission.planning_options is not None else list(LIMITATIONS))
    if parsed.status == "PARTIAL" and submission.planning_options is None:
        limitations.insert(0, "Some entries could not be parsed reliably. Unresolved values remain unknown; inspect the marked source table."
            if unresolved else parse_note + " Missing values remain unknown, not zero.")
    body = dict(module=submission.module, parsed=parsed, engine_review=review, generation=generation,
        wording_notice=notice, summary=summary, observations=observations, illustrations=illustrations, limitations=limitations,
        report_format="FUNCTIONAL_DEMO_V1" if functional_plan else "MODULE_SPECIFIC_V1" if has_details else "ANALYTICAL_V1", analytical_findings=findings,
        planning_context=policy_context,functional_plan=functional_plan,planning_options=submission.planning_options,
        sections=sections, review_details=submission.review_details)
    report_id = digest_json({k: v.model_dump(mode="json") if hasattr(v, "model_dump") else
        [x.model_dump(mode="json") if hasattr(x, "model_dump") else x for x in v] if isinstance(v, list) else v for k, v in body.items()})
    lines = ["FINOVA ALIGNIQ", f"{submission.module.upper()} — Generated synthetic review", "Synthetic demonstration — not for clinical use", "", notice, summary,
        ""]
    if sections:
        lines += ["MODULE REVIEW COMMENTS"]
        for section in sections:
            lines += ["", section.title.upper(), f"Status: {section.status}", section.text]
            if section.missing_fields:
                lines += ["Information needed: " + "; ".join(section.missing_fields)]
        # Complete cells are already retained once in SOURCE AND PROVENANCE.
    else:
        lines += ["TOOTH-WISE MOVEMENT COMMENTS"]
    if not sections:
        for o in observations:
            lines += ["", f"Tooth {o.original_tooth.strip()}", o.text]
    lines += ["", "LIMITATIONS", *limitations, "", "SOURCE AND PROVENANCE", f"Report ID: {report_id}", f"Input SHA-256: {parsed.raw_sha256}",
        f"Parser: {parsed.parser_version}; engine: {review.engine_version}; rules: {review.rule_set_version}",
        f"Wording: {generation.used_mode}; status: {generation.reason}; provider attempts: {generation.attempts}"]
    for o in observations:
        for m in o.measurements:
            location = f"L{m.span.line}:C{m.span.column_start}-C{m.span.column_end}; offsets {m.span.start}:{m.span.end}" if m.span else "omitted cell; no source span"
            lines += [f"{m.id}; tooth_ref {o.tooth_ref}; {location}; {m.numeric_status}; raw sign {quoted(m.raw_sign)}; raw direction {quoted(m.raw_direction)}; magnitude {m.magnitude_decimal}", cell_text(m)]
    lines += ["", "RULE EVALUATION LEDGER — CLINICAL AUTHORITY UNCHANGED"]
    lines += [f"{e.rule_id} v{e.version}: {e.status}; execution {e.execution}; approval {e.approval_status}" for e in review.evaluations]
    if findings:
        lines += ["", "ANALYTICAL FINDING PROVENANCE", json.dumps([f.model_dump(mode="json") for f in findings], ensure_ascii=False, indent=2)]
    if functional_plan is not None:
        lines += ['', 'INPUT-DRIVEN POLICY CONTEXT — NOT TMT FACTS' if submission.planning_options is not None else 'EXPLICIT FICTIONAL SCENARIO CONTEXT — NOT TMT FACTS', policy_context.model_dump_json(indent=2),
            '', 'SYNTHETIC POLICY DECISIONS — NO CLINICAL AUTHORIZATION', functional_plan.model_dump_json(indent=2)]
    if submission.planning_options is not None:
        lines += ['', 'USER REVIEW OPTIONS — SOURCE-BOUND, NO CLINICAL AUTHORITY',submission.planning_options.model_dump_json(indent=2)]
    lines += ["", "SUPPLIED REVIEW DETAILS — UNVERIFIED", submission.review_details.model_dump_json(indent=2),
        "", "ORIGINAL INPUT — VERBATIM", parsed.raw_text, "", "Synthetic demonstration — not for clinical use"]
    return InteractiveReport(report_id=report_id, export_text="\n".join(lines) + "\n", **body)
