"""Descriptive review without promoting source claims to clinical authority.

Macro uses minimized parsed movement records for grounded narrative wording;
complete facts are inserted locally after validation. Micro/Nano retain their
constant phrase catalog and table-order illustrations, never clinical choices.
"""
import json

from app.interactive.models import Illustration, InteractiveReport, ToothObservation
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
    "Attachment and sequencing examples are arbitrary simulations based on table order, independent of movement magnitude. They are not calculated treatment choices or prescriptions.",
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
    return f"{label}: {status}; no numerical observation. Original cell: {quoted(m.raw_value)}."


def generate_interactive(submission, *, settings=None, client=None):
    parsed = resolve(submission)
    if submission.raw_sha256 != parsed.raw_sha256 or any(i.code == "RECOVERY_RECEIPT_INVALID" for i in parsed.issues):
        raise ValueError("REPARSE_REQUIRED")
    if parsed.status in {"INVALID", "UNSUPPORTED"} or not parsed.measurements:
        raise ValueError("PARSE_REQUIRED")
    review = review_table(submission)
    if submission.module == "macro":
        narratives, generation = planning_wording(parsed, settings=settings, client=client)
        phrases = {ref: options[0] for ref, options in WORDINGS.items()}
    else:
        phrases, generation = wording(settings, client)
        narratives = None
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
        index = len(observations) - 1
        if submission.module == "micro":
            shape = ("oval", "rectangular")[index % 2]
            text = f"Illustration only: a simulated {shape} attachment concept is displayed for this source token. The shape alternates by table order, regardless of recorded movement. Dimensions, orientation, surface, position and clinical indication are unspecified. No attachment is recommended."
            illustrations.append(Illustration(tooth_ref=tooth.id, original_tooth=tooth.raw_identifier,
                label="Illustrative attachment example", text=text))
        elif submission.module == "nano":
            group = ("A", "B")[index % 2]
            text = f"Illustration only: this source token is assigned to fictional demonstration group {group} by table order. A sample display places group A before group B, then reassessment. This is an arbitrary narrative, not a movement schedule; no stage allocation, duration or anchorage need is calculated."
            illustrations.append(Illustration(tooth_ref=tooth.id, original_tooth=tooth.raw_identifier,
                label="Illustrative sequencing example", text=text))
    numeric = sum(m.numeric_status in {"PARSED", "EXPLICIT_ZERO"} for m in parsed.measurements)
    missing = sum(m.numeric_status in {"MISSING", "NOT_PRESENT"} for m in parsed.measurements)
    other = len(parsed.measurements) - numeric - missing
    summary = f"{phrases['F0001']} {len(observations)} tooth tokens; {len(parsed.measurements)} measurement positions; {numeric} recorded numerical values; {missing} missing or omitted; {other} invalid or ambiguous."
    notice = "AI-assisted planning wording." if generation.used_mode == "GROQ_AI" else "Standard planning wording."
    limitations = list(LIMITATIONS)
    if parsed.status == "PARTIAL":
        limitations.insert(0, "This table was partially parsed. Unresolved content remains in the original input and is not interpreted; inspect the marked table before using these observations.")
    body = dict(module=submission.module, parsed=parsed, engine_review=review, generation=generation,
        wording_notice=notice, summary=summary, observations=observations, illustrations=illustrations, limitations=limitations)
    report_id = digest_json({k: v.model_dump(mode="json") if hasattr(v, "model_dump") else
        [x.model_dump(mode="json") if hasattr(x, "model_dump") else x for x in v] if isinstance(v, list) else v for k, v in body.items()})
    lines = ["FINOVA ALIGNIQ", f"{submission.module.upper()} — Generated synthetic review", "Synthetic demonstration — not for clinical use", "", notice, summary,
        "", "FACTUAL OBSERVATIONS — PARSED SOURCE VALUES"]
    for o in observations:
        lines += ["", f"Tooth token {quoted(o.original_tooth)}", o.text]
    if illustrations:
        lines += ["", phrases["F0003" if submission.module == "micro" else "F0004"].upper(), "SIMULATED DEMO — NOT CALCULATED TREATMENT DECISIONS"]
        for item in illustrations:
            lines += [f"Tooth token {quoted(item.original_tooth)}: {item.text}"]
    lines += ["", "LIMITATIONS", *limitations, "", "SOURCE AND PROVENANCE", f"Report ID: {report_id}", f"Input SHA-256: {parsed.raw_sha256}",
        f"Parser: {parsed.parser_version}; engine: {review.engine_version}; rules: {review.rule_set_version}",
        f"Wording: {generation.used_mode}; status: {generation.reason}; provider attempts: {generation.attempts}"]
    for o in observations:
        for m in o.measurements:
            location = f"L{m.span.line}:C{m.span.column_start}-C{m.span.column_end}; offsets {m.span.start}:{m.span.end}" if m.span else "omitted cell; no source span"
            lines += [f"{m.id}; tooth_ref {o.tooth_ref}; {location}; {m.numeric_status}; raw sign {quoted(m.raw_sign)}; raw direction {quoted(m.raw_direction)}; magnitude {m.magnitude_decimal}", cell_text(m)]
    lines += ["", "RULE EVALUATION LEDGER — CLINICAL AUTHORITY UNCHANGED"]
    lines += [f"{e.rule_id} v{e.version}: {e.status}; execution {e.execution}; approval {e.approval_status}" for e in review.evaluations]
    lines += ["", "ORIGINAL INPUT — VERBATIM", parsed.raw_text, "", "Synthetic demonstration — not for clinical use"]
    return InteractiveReport(report_id=report_id, export_text="\n".join(lines) + "\n", **body)
