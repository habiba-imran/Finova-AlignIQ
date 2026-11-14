"""Grounded Macro prose. Numeric facts are parsed locally, never invented by an LLM.

Only normalized movement records and opaque per-request references leave this
module. Raw tables, free-text labels, tooth identifiers and patient/context notes
are excluded. Provider prose can arrange complete fact placeholders; it cannot
relabel a value, omit a cell, change a number or introduce clinical assertions.
"""
import json
import os
import re

from pydantic import Field

from app.domain.models import Contract
from app.interactive.models import PlanningGenerationInfo
from app.reports.groq_client import GroqClient
from app.reports.settings import ReportSettings, load_settings
from app.reports.validation import private_json

LABELS = {
    "rotation": "rotation", "angulation": "angulation", "inclination": "inclination",
    "extrusion": "extrusion", "intrusion": "intrusion", "vertical": "vertical movement",
    "relative_vertical": "relative vertical movement", "buccolingual": "buccolingual translation",
    "mesiodistal": "mesiodistal translation",
}
# Connective prose only. All movement terminology, values and unknown/zero states
# are complete local facts. Neither clinical assertions nor comparative judgments
# can be expressed through this vocabulary. This is separate from legacy rules.
CONNECTIVES = frozenset("""a an and alongside also appear appears as at be been being between
by combines combination components contains consists corresponding data describes description
entry entries evident field fields following for from grouped has have here in includes including
information is it its listed lists movement movements observed observations of on other overall
plan planned planning presents profile programmed provided record recorded records reflects
remaining reported reports review reviewed separately shows source specified supplied table
that the their these this those together values which with within""".split())
TOKEN = re.compile(r"\{(M\d{4})\}")
MAX_TEETH = 32
MAX_CELLS = 256
MAX_PROMPT_BYTES = 24_000


class PlanningWordingSettings(ReportSettings):
    timeout_seconds: float = Field(default=25, ge=1, le=45)
    max_completion_tokens: int = Field(default=4096, ge=256, le=4096)


def load_planning_settings():
    original = load_settings()
    values = original.model_dump()
    values.update(api_key=original.api_key, synthetic_transmission_enabled=True,
                  timeout_seconds=os.environ.get("FINOVA_PLANNING_TIMEOUT_SECONDS", "25"),
                  max_completion_tokens=4096, max_retries=0)
    return PlanningWordingSettings.model_validate(values)


class ToothWording(Contract):
    tooth_ref: str = Field(pattern=r"^T\d{3}$")
    text: str = Field(min_length=1, max_length=3000)


class PlanningWordingBatch(Contract):
    comments: list[ToothWording] = Field(min_length=1, max_length=MAX_TEETH)


def fact(m):
    label = LABELS.get(m.recognized_label, "unrecognized movement field")
    if m.field_status == "AMBIGUOUS" or m.numeric_status == "AMBIGUOUS":
        return f"an ambiguous {label} entry (value remains unknown)"
    if m.numeric_status in {"MISSING", "NOT_PRESENT"}:
        return f"an unreported {label} value (unknown, not zero)"
    if m.numeric_status not in {"PARSED", "EXPLICIT_ZERO"}:
        return f"an unreadable {label} entry (value remains unknown)"
    value = str(m.signed_decimal)
    unit = f" {m.unit}" if m.unit else " (unit unknown)"
    description = f"{label} of {value}{unit}"
    if m.numeric_status == "EXPLICIT_ZERO":
        description += " (explicitly recorded zero)"
    if m.raw_direction:
        description += f" (supplied direction label {json.dumps(m.raw_direction, ensure_ascii=False)})"
    return description


def records(parsed):
    """Build a minimized payload and a complete local substitution map."""
    by_tooth = {}
    for m in parsed.measurements:
        by_tooth.setdefault(m.tooth_ref, []).append(m)
    groups, substitutions, tooth_map, fallback = [], {}, {}, {}
    index = 0
    for tooth in parsed.teeth:
        cells = by_tooth.get(tooth.id, [])
        if not cells:
            continue
        alias = f"T{len(groups) + 1:03d}"
        entries, facts = [], {}
        for m in cells:
            index += 1
            ref = f"M{index:04d}"
            facts[ref] = fact(m)
            accepted = m.numeric_status in {"PARSED", "EXPLICIT_ZERO"} and m.field_status != "AMBIGUOUS"
            # Never pass raw/free-text strings to the model as instructions/data.
            direction = m.raw_direction if m.raw_direction in {"D", "M", "B", "L", "E", "I"} else None
            entries.append(dict(ref=ref, movement=LABELS.get(m.recognized_label, "unknown"),
                                value=str(m.signed_decimal) if accepted else None,
                                unit=m.unit if m.unit in {"mm", "deg"} else None,
                                direction_label=direction, state=m.numeric_status if m.field_status != "AMBIGUOUS" else "AMBIGUOUS"))
        groups.append(dict(tooth_ref=alias, movements=entries))
        substitutions[alias], tooth_map[alias] = facts, tooth.id
        fallback[tooth.id] = "The programmed movement record lists " + "; ".join(facts.values()) + "."
    return groups, substitutions, tooth_map, fallback


def validate(content, substitutions, tooth_map):
    try:
        batch = PlanningWordingBatch.model_validate(private_json(content))
        if len(batch.comments) != len(substitutions) or len({c.tooth_ref for c in batch.comments}) != len(batch.comments):
            raise ValueError()
        output = {}
        for c in batch.comments:
            expected = substitutions[c.tooth_ref]
            refs = TOKEN.findall(c.text)
            if len(refs) != len(expected) or set(refs) != set(expected):
                raise ValueError()
            prose = TOKEN.sub(" ", c.text)
            # Restrict model-authored material to connective language. Complete
            # factual clauses (including unknowns and zeros) are inserted locally.
            if re.search(r"[^A-Za-z\s.,;:()\-]", prose):
                raise ValueError()
            words = re.findall(r"[A-Za-z]+", prose.lower())
            if not words or any(word not in CONNECTIVES for word in words):
                raise ValueError()
            text = TOKEN.sub(lambda match: expected[match.group(1)], c.text)
            output[tooth_map[c.tooth_ref]] = text
        if len(output) != len(substitutions):
            raise ValueError()
        return output
    except (ValueError, TypeError, KeyError, RecursionError):
        return None


def planning_wording(parsed, *, settings=None, client=None):
    groups, substitutions, tooth_map, fallback = records(parsed)
    reason, attempts, accepted = "GROQ_NOT_CONFIGURED", 0, 0
    chosen = fallback
    try:
        settings = settings or load_planning_settings()
    except ValueError:
        reason = "GROQ_CONFIGURATION_INVALID"
    else:
        if len(groups) > MAX_TEETH or len(parsed.measurements) > MAX_CELLS:
            reason = "GROQ_PLANNING_LIMIT"
        elif settings.configured:
            messages = [
                {"role": "system", "content": (
                    "Compose readable tooth-wise descriptive planning comments from the structured programmed movement records. "
                    "Use varied, coherent sentences, not a heading or raw-value dump. Return one comments item per tooth_ref. "
                    "Each text must use every movement reference for that tooth exactly once in the form {M0001}. "
                    "Each placeholder will be replaced locally with the COMPLETE movement label, exact value, supplied direction and missing/zero status. "
                    "Do not type values, units, movement names, tooth identifiers, comparisons, clinical interpretation, risk, advice or treatment choices outside placeholders. "
                    "Do not infer physical directions, tooth anatomy or simultaneous/staged movements. The source is unverified. "
                    "Use only these connective words outside placeholders: " + " ".join(sorted(CONNECTIVES)) + ". "
                    "Example sentence structure: The recorded profile combines {M0001} and {M0002}, alongside {M0003}. "
                    "Use only the references supplied for the respective tooth, and return JSON only."
                )},
                {"role": "user", "content": json.dumps({"programmed_movements": groups}, separators=(",", ":"))},
            ]
            if len(json.dumps(messages).encode()) > MAX_PROMPT_BYTES:
                reason = "GROQ_PROMPT_LIMIT"
            else:
                schema = {"type": "json_schema", "json_schema": {"name": "finova_planning_wording_v1", "strict": True,
                          "schema": PlanningWordingBatch.model_json_schema()}}
                result = (client or GroqClient(settings)).generate(messages, response_schema=schema)
                attempts, reason = result.attempts, result.code
                if result.content is not None:
                    validated = validate(result.content, substitutions, tooth_map)
                    if validated is not None:
                        chosen, accepted, reason = validated, len(groups), "GROQ_VALIDATED"
                    else:
                        reason = "GROQ_UNSUPPORTED_WORDING"
    info = PlanningGenerationInfo(requested_mode="AUTO", used_mode="GROQ_AI" if accepted else "STANDARD_TEMPLATES",
        reason=reason, attempts=attempts, provider="GROQ" if attempts else None,
        model="openai/gpt-oss-120b" if attempts else None, eligible_wording_findings=len(groups), accepted_comments=accepted)
    return chosen, info
