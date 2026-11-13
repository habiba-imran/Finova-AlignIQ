"""Exact closed-language validation, stronger than JSON shape or keyword blacklists."""

import json

from app.reports.models import WordingBatch
from app.reports.templates import wording_options
from app.review.models import Finding


def _unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("DUPLICATE_JSON_KEY")
        obj[key] = value
    return obj


def private_json(text: str):
    return json.loads(text, object_pairs_hook=_unique_object,
                      parse_constant=lambda _value: (_ for _ in ()).throw(ValueError("NONFINITE_JSON")))


def validate_wording(content: str, refs: dict[str, Finding]) -> tuple[dict[str, str], str]:
    try:
        batch = WordingBatch.model_validate_json(json.dumps(private_json(content), allow_nan=False))
    except (ValueError, TypeError, RecursionError):
        return {}, "GROQ_MALFORMED_OUTPUT"
    ids = [c.finding_ids[0] for c in batch.comments]
    if len(ids) != len(set(ids)) or set(ids) != set(refs):
        return {}, "GROQ_FINDING_REFERENCES_INVALID"
    accepted = {refs[c.finding_ids[0]].finding_id: c.text for c in batch.comments
                if c.text in wording_options(refs[c.finding_ids[0]])}
    return accepted, "GROQ_VALIDATED" if len(accepted) == len(refs) else "GROQ_UNSUPPORTED_WORDING"
