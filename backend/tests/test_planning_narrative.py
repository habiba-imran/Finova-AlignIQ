import json

import httpx
import pytest

from app.interactive.narrative import PlanningWordingSettings, planning_wording, records, validate
from app.parser.receipts import resolve
from app.reports.groq_client import GroqClient
from app.reports.groq_client import GroqResult
from test_interactive import LARGE, ROWS, submission


def response_for(parsed):
    groups, _, _, _ = records(parsed)
    openings = ["The programmed profile combines ", "This entry records ", "Recorded movement components are "]
    return {"comments": [{"tooth_ref": t["tooth_ref"], "text": openings[i % len(openings)] + " alongside ".join("{" + m["ref"] + "}" for m in t["movements"]) + "."} for i, t in enumerate(groups)]}


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


@pytest.mark.parametrize("mutation", ["number", "recommendation", "planned_attachment", "planned_sequence", "severity", "achieved", "injection", "omission", "duplicate", "cross_tooth", "negation", "unknown_tooth"])
def test_generated_words_cannot_add_claims_or_change_fact_associations(mutation):
    parsed = resolve(submission())
    _, refs, teeth, _ = records(parsed)
    value = response_for(parsed)
    first = value["comments"][0]
    if mutation == "number": first["text"] += " 2 mm."
    if mutation == "recommendation": first["text"] += " Recommend extraction."
    if mutation == "planned_attachment": first["text"] += " The attachment is planned."
    if mutation == "planned_sequence": first["text"] += " The sequencing is planned."
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


def test_repeated_boilerplate_is_not_accepted_as_distinct_planning_wording():
    parsed = resolve(submission(LARGE))
    groups, refs, teeth, _ = records(parsed)
    repeated = {"comments": [{"tooth_ref": t["tooth_ref"], "text": "The recorded profile combines " + " and ".join("{" + m["ref"] + "}" for m in t["movements"]) + "."} for t in groups]}
    assert validate(json.dumps(repeated), refs, teeth) is None
    assert validate(json.dumps(response_for(parsed)), refs, teeth) is not None


def test_planning_sampling_does_not_change_legacy_wording_settings(monkeypatch):
    from app.interactive.narrative import load_planning_settings
    from app.reports.settings import load_settings
    monkeypatch.delenv("GROQ_TEMPERATURE", raising=False)
    assert load_planning_settings().temperature == 0.2
    assert load_settings().temperature == 0


def test_natural_paragraphs_must_preserve_every_complete_fact_verbatim():
    parsed = resolve(submission())
    _, refs, teeth, _ = records(parsed)
    value = response_for(parsed)
    for comment in value["comments"]:
        for ref, phrase in refs[comment["tooth_ref"]].items():
            comment["text"] = comment["text"].replace("{" + ref + "}", phrase)
    result = validate(json.dumps(value), refs, teeth)
    assert result is not None
    assert result[parsed.teeth[0].id] == value["comments"][0]["text"]
    changed = json.loads(json.dumps(value))
    changed["comments"][0]["text"] = changed["comments"][0]["text"].replace("-2.7500", "99.0000")
    assert validate(json.dumps(changed), refs, teeth) is None
    changed = json.loads(json.dumps(value))
    changed["comments"][0]["text"] = changed["comments"][0]["text"].replace("rotation", "angulation")
    assert validate(json.dumps(changed), refs, teeth) is None


def test_unknown_summary_cannot_be_added_to_a_recorded_numeric_profile():
    parsed = resolve(submission())
    _, refs, teeth, _ = records(parsed)
    value = response_for(parsed)
    value["comments"][0]["text"] = "Across the unknown entries " + value["comments"][0]["text"]
    assert validate(json.dumps(value), refs, teeth) is None


def test_unknown_unit_does_not_allow_claiming_the_numeric_value_is_unknown():
    refs = {"T001": {"M0001": "rotation of 2.0 (unit unknown)"}}
    value = {"comments": [{"tooth_ref": "T001", "text": "Across the unknown entries {M0001} is recorded."}]}
    assert validate(json.dumps(value), refs, {"T001": "local-tooth"}) is None


def test_rejected_wording_gets_one_reference_only_correction_without_releasing_checks():
    parsed = resolve(submission())
    valid = response_for(parsed)
    invalid = json.loads(json.dumps(valid))
    invalid["comments"][0]["text"] += " Recommend extraction."
    calls = []

    class Client:
        def generate(self, messages, *, response_schema):
            calls.append(messages)
            return GroqResult(json.dumps(invalid if len(calls) == 1 else valid), "GROQ_RESPONSE_RECEIVED", 1)

    result, info = planning_wording(parsed, settings=PlanningWordingSettings(api_key="PRIVATE_KEY", synthetic_transmission_enabled=True), client=Client())
    assert info.used_mode == "GROQ_AI" and info.attempts == 2 and info.accepted_comments == 4
    assert len(calls) == 2
    correction = json.dumps(calls[1])
    assert "Recommend extraction" not in correction and "PRIVATE_KEY" not in correction and parsed.raw_text not in correction
    assert "-2.7500" not in correction and "M0001" in correction
    assert result == validate(json.dumps(valid), records(parsed)[1], records(parsed)[2])


def test_second_rejection_remains_standard_and_never_loops():
    parsed = resolve(submission())
    calls = []

    class Client:
        def generate(self, messages, *, response_schema):
            calls.append(messages)
            return GroqResult('{"comments":[]}', "GROQ_RESPONSE_RECEIVED", 1)

    _, info = planning_wording(parsed, settings=PlanningWordingSettings(api_key="PRIVATE_KEY", synthetic_transmission_enabled=True), client=Client())
    assert len(calls) == info.attempts == 2
    assert info.used_mode == "STANDARD_TEMPLATES" and info.accepted_comments == 0


def test_correction_uses_remaining_original_deadline_and_smaller_output_budget(monkeypatch):
    parsed = resolve(submission())
    responses = ['{"comments":[]}', json.dumps(response_for(parsed))]
    configurations = []
    clock = iter([10.0, 14.0])
    monkeypatch.setattr("app.interactive.narrative.time.monotonic", lambda: next(clock))

    class Client:
        def generate(self, messages, *, response_schema):
            return GroqResult(responses.pop(0), "GROQ_RESPONSE_RECEIVED", 1)

    def factory(config):
        configurations.append(config)
        return Client()

    monkeypatch.setattr("app.interactive.narrative.GroqClient", factory)
    _, info = planning_wording(parsed, settings=PlanningWordingSettings(api_key="PRIVATE_KEY", synthetic_transmission_enabled=True))
    assert info.used_mode == "GROQ_AI"
    assert [c.timeout_seconds for c in configurations] == [25, 21]
    assert configurations[1].max_completion_tokens == 2048 and configurations[1].max_retries == 0


def test_exhausted_request_budget_does_not_start_a_correction(monkeypatch):
    parsed = resolve(submission())
    clock = iter([10.0, 35.0])
    monkeypatch.setattr("app.interactive.narrative.time.monotonic", lambda: next(clock))
    calls = []

    class Client:
        def generate(self, messages, *, response_schema):
            calls.append(messages)
            return GroqResult('{"comments":[]}', "GROQ_RESPONSE_RECEIVED", 1)

    _, info = planning_wording(parsed, settings=PlanningWordingSettings(api_key="PRIVATE_KEY", synthetic_transmission_enabled=True), client=Client())
    assert len(calls) == info.attempts == 1
    assert info.used_mode == "STANDARD_TEMPLATES"
