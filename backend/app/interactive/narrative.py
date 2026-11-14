"""Grounded Macro, Micro and Nano prose. Numeric facts are parsed locally, never invented by an LLM.

Only normalized movement records and opaque per-request references leave this
module. Raw tables, free-text labels, tooth identifiers and patient/context notes
are excluded. Provider prose can arrange complete fact placeholders; it cannot
relabel a value, omit a cell, change a number or introduce clinical assertions.
"""
import json
import os
import re
import time
from collections import Counter
from math import ceil

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
presents profile programmed provided record recorded records reflects
remaining reported reports review reviewed separately shows source specified supplied table
that the their these this those together values which with within""".split())
CONNECTIVES = CONNECTIVES | frozenset("""tooth token tokens item items additional accompanied
accompanies accompanying feature features noted notes forms comprise comprises comprising comprised showing listing recording combining containing reflecting presenting further shown are include
set featuring details case along well paired summary additionally combined plus noting accompany presented part parts whereas while among across present represented represent seen can still there otherwise included context""".split())
TOKEN = re.compile(r"\{(M\d{4})\}")
MAX_TEETH = 32
MAX_CELLS = 256
MAX_PROMPT_BYTES = 24_000


class PlanningWordingSettings(ReportSettings):
    temperature: float = Field(default=0.2, ge=0, le=0.3)
    timeout_seconds: float = Field(default=25, ge=1, le=45)
    max_completion_tokens: int = Field(default=3072, ge=256, le=4096)


def load_planning_settings():
    original = load_settings()
    values = original.model_dump()
    values.update(api_key=original.api_key, synthetic_transmission_enabled=True,
                  temperature=0.2,
                  timeout_seconds=os.environ.get("FINOVA_PLANNING_TIMEOUT_SECONDS", "25"),
                  max_completion_tokens=3072, max_retries=0)
    return PlanningWordingSettings.model_validate(values)


class ToothWording(Contract):
    tooth_ref: str = Field(pattern=r"^T\d{3}$")
    text: str = Field(min_length=1, max_length=3000)


class PlanningWordingBatch(Contract):
    comments: list[ToothWording] = Field(min_length=1, max_length=MAX_TEETH)


def response_schema():
    schema = PlanningWordingBatch.model_json_schema()
    return {"type": "json_schema", "json_schema": {"name": "finova_planning_wording_v1", "strict": True, "schema": schema}}


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
            # Never pass raw/free-text strings to the model as instructions/data.
            direction = m.raw_direction if m.raw_direction in {"D", "M", "B", "L", "E", "I"} else None
            accepted = m.numeric_status in {"PARSED", "EXPLICIT_ZERO"} and m.field_status != "AMBIGUOUS"
            # Shared array order avoids repeating complete English clauses and
            # JSON field names for every cell. All displayed facts remain local.
            entries.append(dict(ref=ref, facts=[LABELS.get(m.recognized_label, "unrecognized field"),
                str(m.signed_decimal) if accepted else None, m.unit if m.unit in {"mm", "deg"} else None,
                direction, m.numeric_status if m.field_status != "AMBIGUOUS" else "AMBIGUOUS"]))
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
        openings = Counter()
        for c in batch.comments:
            expected = substitutions[c.tooth_ref]
            masked = c.text
            rendered = dict(expected)
            refs = TOKEN.findall(masked)
            if refs:
                if len(refs) != len(expected) or set(refs) != set(expected):
                    raise ValueError()
            else:
                # Accept genuinely composed prose only when each complete local
                # fact is copied exactly once. Mask those immutable clauses before
                # checking model-authored language, so changed facts cannot pass.
                for ref, phrase in sorted(expected.items(), key=lambda item: -len(item[1])):
                    match = re.search(re.escape(phrase), masked, flags=re.IGNORECASE)
                    if match is None:
                        raise ValueError()
                    if match.group(0)[0].isupper():
                        rendered[ref] = phrase[0].upper() + phrase[1:]
                    masked = masked[:match.start()] + "{" + ref + "}" + masked[match.end():]
            prose = TOKEN.sub(" ", masked)
            # Restrict model-authored material to connective language. Complete
            # factual clauses (including unknowns and zeros) are inserted locally.
            if re.search(r"[^A-Za-z\s.,;:()\-]", prose):
                raise ValueError()
            words = re.findall(r"[A-Za-z]+", prose.lower())
            all_values_unknown = all(phrase.startswith(("an unreported ", "an ambiguous ", "an unreadable ")) for phrase in expected.values())
            allowed = CONNECTIVES | ({"unknown"} if all_values_unknown else set())
            if not words or any(word not in allowed for word in words):
                raise ValueError()
            before_first_fact = masked.split("{", 1)[0]
            openings[tuple(re.findall(r"[A-Za-z]+", before_first_fact.lower())[:3])] += 1
            text = TOKEN.sub(lambda match: rendered[match.group(1)], masked)
            output[tooth_map[c.tooth_ref]] = text
        if len(output) != len(substitutions):
            raise ValueError()
        # A valid provider response is not sufficient if it gives every differing
        # source profile the same boilerplate. Do not manufacture variety locally
        # by rotating prefixes: reject repetitive output and label fallback honestly.
        profiles = {tuple(facts.values()) for facts in substitutions.values()}
        if len(batch.comments) >= 4 and len(openings) < min(3, len(profiles)):
            raise ValueError()
        if len(batch.comments) >= 8 and len(profiles) > 1 and max(openings.values()) > ceil(len(batch.comments) * 0.6):
            raise ValueError()
        return output
    except (ValueError, TypeError, KeyError, RecursionError):
        return None


def planning_wording(parsed, *, module="macro", settings=None, client=None):
    started = time.monotonic()
    contexts = {"macro": "planning review of the recorded movement profile", "micro": "attachment review of the recorded movement profile", "nano": "sequencing review of the recorded movement profile"}
    context = contexts[module]
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
                    "Compose readable tooth-wise comments for " + context + ". Return one comments item with tooth_ref and text for each supplied tooth. JSON only. "
                    "Each movement has ref and facts in this exact array order: movement family, exact scalar, unit, supplied direction label, state. "
                    "Use the facts only to choose sentence grouping. Use every own ref exactly once in braces, e.g. {M0001}. "
                    "Each placeholder becomes a COMPLETE noun phrase locally, including movement name, exact value, unit, direction and unknown/zero state. "
                    "Never type source facts or state claims yourself. Never add movement names, values, units, adjectives, comparisons, conclusions, advice or clinical decisions outside placeholders. "
                    "Write two short sentences for three or more refs; one sentence is sufficient for fewer refs. Every sentence must contain refs. "
                    "Vary the first three words and sentence grouping across teeth. Choose varied openings from: The record includes; This entry presents; Recorded components are; Within this profile; Here the record shows; Across the entry; Among the listed components; The supplied values include. "
                    "Use only words in those openings and these neutral linking phrases: and; alongside; together with; also; the record includes; are listed; are recorded; are present. "
                    "Do not use the same first three words for most entries. Use ordinary sentence case and punctuation. The source is unverified; no attachment or stage choices are inferred."

                )},
                {"role": "user", "content": json.dumps({"programmed_movements": groups}, separators=(",", ":"))},
            ]
            if len(json.dumps(messages).encode()) > MAX_PROMPT_BYTES:
                reason = "GROQ_PROMPT_LIMIT"
            else:
                result = (client or GroqClient(settings)).generate(messages, response_schema=response_schema())
                attempts, reason = result.attempts, result.code
                if result.content is not None:
                    validated = validate(result.content, substitutions, tooth_map)
                    if validated is not None:
                        chosen, accepted, reason = validated, len(groups), "GROQ_VALIDATED"
                    else:
                        reason = "GROQ_UNSUPPORTED_WORDING"
                        # Correct only an actually rejected successful response,
                        # once, within the same total timeout budget. Never retry a
                        # missing key, provider error, timeout or rate limit.
                        remaining = settings.timeout_seconds - (time.monotonic() - started)
                        if attempts < 2 and remaining >= 1:
                            repair_groups = [{"tooth_ref": group["tooth_ref"], "refs": [m["ref"] for m in group["movements"]]} for group in groups]
                            repair_messages = [
                                {"role": "system", "content": (
                                    "Compose one readable paragraph for each supplied tooth_ref using every own ref exactly once as {M0001}. "
                                    "The placeholders are complete noun phrases and will be replaced locally with immutable source facts. "
                                    "Return comments containing tooth_ref and text, JSON only. No numbers, units, movement names, states or clinical assertions outside placeholders. "
                                    "Use varied openings across entries. Choose from: The record includes; This entry presents; Recorded components are; Within this profile; Here the record shows; Across the entry; Among the listed components; The supplied values include. "
                                    "Compose one or two sentences. Use only those opening words and these neutral connecting phrases: and; alongside; together with; also; the record includes; are listed; are recorded; are present. "
                                    "Do not add adjectives, comparisons, recommendations, missing/zero claims, negation or facts. Do not use the same first three words for most entries."
                                )},
                                {"role": "user", "content": json.dumps({"entries": repair_groups}, separators=(",", ":"))},
                            ]
                            repair_settings = settings.model_copy(update={"timeout_seconds": remaining, "max_retries": 0, "max_completion_tokens": 2048})
                            repaired = (client or GroqClient(repair_settings)).generate(repair_messages, response_schema=response_schema())
                            attempts += repaired.attempts
                            reason = repaired.code
                            if repaired.content is not None:
                                corrected = validate(repaired.content, substitutions, tooth_map)
                                if corrected is not None:
                                    chosen, accepted, reason = corrected, len(groups), "GROQ_VALIDATED"
                                else:
                                    reason = "GROQ_UNSUPPORTED_WORDING"
    info = PlanningGenerationInfo(requested_mode="AUTO", used_mode="GROQ_AI" if accepted else "STANDARD_TEMPLATES",
        reason=reason, attempts=attempts, provider="GROQ" if attempts else None,
        model="openai/gpt-oss-120b" if attempts else None, eligible_wording_findings=len(groups), accepted_comments=accepted)
    return chosen, info
