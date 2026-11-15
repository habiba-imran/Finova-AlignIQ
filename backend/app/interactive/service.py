"""Descriptive review without promoting source claims to clinical authority.

Macro uses minimized movement records; Micro/Nano use purpose-specific supplied
records and explicit unavailable findings. Complete facts are inserted locally
after validation, without promoting supplied details to clinical decisions.
"""
import json

from app.interactive.models import InteractiveReport, ToothObservation
from app.interactive.module_reports import module_sections, validate_details
from app.interactive.narrative import planning_wording
from app.parser.receipts import resolve
from app.reports.groq_client import GroqClient
from app.reports.models import GenerationInfo, WordingBatch
from app.reports.settings import load_settings
from app.reports.validation import private_json
from app.review.service import review_table
from app.semantics.fixtures import digest_json

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
    validate_details(parsed, submission)
    sections = []
    if submission.module == "macro":
        narratives, generation = planning_wording(parsed, module=submission.module, settings=settings, client=client)
    else:
        sections, generation = module_sections(parsed, submission, settings=settings, client=client)
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
    lead = {"macro": "Programmed movement profile.", "micro": "TMT-based attachment review: rotation, angulation and inclination observations.", "nano": "TMT-based sequencing review: movement context, translations and vertical movements."}[submission.module]
    summary = f"{lead} {len(observations)} tooth tokens; {len(parsed.measurements)} measurement positions; {numeric} recorded numerical values; {missing} missing or omitted; {other} invalid or ambiguous."
    notice = "AI-assisted report wording." if generation.used_mode == "GROQ_AI" else "Standard report wording."
    limitations = list(LIMITATIONS)
    if parsed.status == "PARTIAL":
        limitations.insert(0, "This table was partially parsed. Unresolved content remains in the original input and is not interpreted; inspect the marked table before using these observations.")
    body = dict(module=submission.module, parsed=parsed, engine_review=review, generation=generation,
        wording_notice=notice, summary=summary, observations=observations, illustrations=illustrations, limitations=limitations,
        report_format="MODULE_SPECIFIC_V1", sections=sections, review_details=submission.review_details)
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
        lines += ["", "SOURCE MOVEMENT VALUES — NOT ATTACHMENT OR STAGE DECISIONS"]
    else:
        lines += ["TOOTH-WISE MOVEMENT COMMENTS"]
    for o in observations:
        lines += ["", f"Tooth token {quoted(o.original_tooth)}", o.text]
    lines += ["", "LIMITATIONS", *limitations, "", "SOURCE AND PROVENANCE", f"Report ID: {report_id}", f"Input SHA-256: {parsed.raw_sha256}",
        f"Parser: {parsed.parser_version}; engine: {review.engine_version}; rules: {review.rule_set_version}",
        f"Wording: {generation.used_mode}; status: {generation.reason}; provider attempts: {generation.attempts}"]
    for o in observations:
        for m in o.measurements:
            location = f"L{m.span.line}:C{m.span.column_start}-C{m.span.column_end}; offsets {m.span.start}:{m.span.end}" if m.span else "omitted cell; no source span"
            lines += [f"{m.id}; tooth_ref {o.tooth_ref}; {location}; {m.numeric_status}; raw sign {quoted(m.raw_sign)}; raw direction {quoted(m.raw_direction)}; magnitude {m.magnitude_decimal}", cell_text(m)]
    lines += ["", "RULE EVALUATION LEDGER — CLINICAL AUTHORITY UNCHANGED"]
    lines += [f"{e.rule_id} v{e.version}: {e.status}; execution {e.execution}; approval {e.approval_status}" for e in review.evaluations]
    lines += ["", "SUPPLIED REVIEW DETAILS — UNVERIFIED", submission.review_details.model_dump_json(indent=2),
        "", "ORIGINAL INPUT — VERBATIM", parsed.raw_text, "", "Synthetic demonstration — not for clinical use"]
    return InteractiveReport(report_id=report_id, export_text="\n".join(lines) + "\n", **body)
