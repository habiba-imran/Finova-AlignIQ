import json

import httpx
import pytest

from app.interactive.narrative import PlanningWordingSettings, planning_wording, records, validate
from app.parser.receipts import resolve
from app.reports.groq_client import GroqClient
from test_interactive import LARGE, ROWS, submission


def response_for(parsed):
    groups, _, _, _ = records(parsed)
    return {"comments": [{"tooth_ref": t["tooth_ref"], "text": "The programmed profile combines " + " alongside ".join("{" + m["ref"] + "}" for m in t["movements"]) + "."} for t in groups]}


def test_grounded_paragraphs_use_values_and_cover_all_112_cells_without_promoting_rules():
    parsed = resolve(submission(LARGE))
    captured = []
    settings = PlanningWordingSettings(api_key="PRIVATE_KEY", synthetic_transmission_enabled=True)

    def handler(request):
        payload = json.loads(request.content)
        captured.append(payload)
        return httpx.Response(200, json={"model": settings.model, "choices": [{"finish_reason": "stop", "message": {"role": "assistant", "content": json.dumps(response_for(parsed))}}]})

    comments, info = planning_wording(parsed, settings=settings, client=GroqClient(settings, transport=httpx.MockTransport(handler)))
    assert info.used_mode == "GROQ_AI" and info.accepted_comments == 16
    assert info.output_validation == "GROUNDED_PLANNING_WORDING_V1"
    assert len(comments) == 16 and len(captured) == 1
    payload = json.dumps(captured[0])
    assert "1.2300" in payload and "0.4500" in payload
    assert "raw_text" not in payload and "PRIVATE_KEY" not in payload and parsed.raw_sha256 not in payload
    assert captured[0]["response_format"]["json_schema"]["name"] == "finova_planning_wording_v1"
    assert "Original cell" not in comments[parsed.teeth[0].id]
    assert "rotation of 0.1250 deg" in comments[parsed.teeth[0].id]
    assert "unreported intrusion value (unknown, not zero)" in comments[parsed.teeth[0].id]
    assert "{M" not in " ".join(comments.values())


@pytest.mark.parametrize("mutation", ["number", "recommendation", "severity", "achieved", "injection", "omission", "duplicate", "cross_tooth", "negation", "unknown_tooth"])
def test_generated_words_cannot_add_claims_or_change_fact_associations(mutation):
    parsed = resolve(submission())
    _, refs, teeth, _ = records(parsed)
    value = response_for(parsed)
    first = value["comments"][0]
    if mutation == "number": first["text"] += " 2 mm."
    if mutation == "recommendation": first["text"] += " Recommend extraction."
    if mutation == "severity": first["text"] += " High risk."
    if mutation == "achieved": first["text"] += " Achieved movement."
    if mutation == "injection": first["text"] += " <script>"
    if mutation == "omission": first["text"] = first["text"].replace("{M0001}", "")
    if mutation == "duplicate": first["text"] += " {M0001}"
    if mutation == "cross_tooth": first["text"] = first["text"].replace("{M0001}", "{M0004}")
    if mutation == "negation": first["text"] = "No " + first["text"]
    if mutation == "unknown_tooth": first["tooth_ref"] = "T999"
    assert validate(json.dumps(value), refs, teeth) is None


def test_patient_notes_raw_labels_and_original_identifiers_are_excluded():
    raw = "Patient: PRIVATE_PATIENT\n" + ROWS.replace("11\t", "PRIVATE_TOOTH\t")
    parsed = resolve(submission(raw))
    groups, _, _, _ = records(parsed)
    serialized = json.dumps(groups)
    assert "PRIVATE" not in serialized and "Original cell" not in serialized
    assert "T001" in serialized and "-2.7500" in serialized


def test_fallback_still_reads_as_comments_and_preserves_unknowns_and_zeros():
    parsed = resolve(submission())
    comments, info = planning_wording(parsed, settings=PlanningWordingSettings())
    first = comments[parsed.teeth[0].id]
    assert first.startswith("The programmed movement record lists")
    assert "-2.7500" in first and "explicitly recorded zero" in first
    assert "Original cell" not in first
    assert "unknown, not zero" in comments[parsed.teeth[1].id]
    assert info.used_mode == "STANDARD_TEMPLATES" and info.attempts == 0


def test_planning_timeout_is_separate_from_legacy_settings(monkeypatch):
    from app.interactive.narrative import load_planning_settings
    from app.reports.settings import load_settings
    monkeypatch.setenv("FINOVA_PLANNING_TIMEOUT_SECONDS", "30")
    monkeypatch.delenv("GROQ_TIMEOUT_SECONDS", raising=False)
    assert load_planning_settings().timeout_seconds == 30
    assert load_settings().timeout_seconds == 6
    monkeypatch.setenv("FINOVA_PLANNING_TIMEOUT_SECONDS", "999")
    with pytest.raises(ValueError): load_planning_settings()
