"""Independent synthetic inputs, provider adversarial cases and source preservation."""
import json
from pathlib import Path

from fastapi.testclient import TestClient
import httpx
import pytest

from app.interactive.models import InteractiveReport, InteractiveSubmission
from app.interactive.service import WORDINGS, generate_interactive
from app.main import app
from app.parser.receipts import resolve
from app.reports.groq_client import GroqClient
from app.reports.settings import ReportSettings
from app.review.registry import RULES

ROWS = "Tooth\tRotation (deg)\tExtrusion (mm)\tMesial/Distal (mm)\n11\t-2.7500 M\t0\t1.2300 D\n12\t0\t—\t0.450 L\n13\t3.25 D\t0.1250\t\n14\t-1.50\tN/A\t0"
COLUMNS = "Movement\t21\t22\t23\nRotation (deg)\t4.500 D\t0\t-1.250 M\nExtrusion (mm)\t0.250\t—\t0.500"
MARKDOWN = "| Tooth | Rotation (deg) | Extrusion (mm) |\n| --- | --- | --- |\n| 31 | -3.4500 M | 0.2200 |\n| 32 | 0 | N/A |"
LARGE = "Tooth\tRotation (deg)\tInclination (deg)\tAngulation (deg)\tExtrusion (mm)\tIntrusion (mm)\tMesial/Distal (mm)\tBuccal/Lingual (mm)\n" + "\n".join(
    f"{tooth}\t{index}.1250 D\t-1.5000\t0\t0.2000\t—\t1.2300 D\t0.4500 B"
    for index, tooth in enumerate([18,17,16,15,14,13,12,11,21,22,23,24,25,26,27,28]))


def submission(raw=ROWS, module="macro", **changes):
    import hashlib
    return InteractiveSubmission(raw_text=raw, raw_sha256=hashlib.sha256(raw.encode()).hexdigest(),
        synthetic_data_confirmed=True, module=module, **changes)


@pytest.mark.parametrize("raw,count", [(ROWS, 12), (COLUMNS, 6), (MARKDOWN, 4), (LARGE, 112)])
@pytest.mark.parametrize("module", ["macro", "micro", "nano"])
def test_arbitrary_source_cells_and_provenance_preserved(raw, count, module):
    request = submission(raw, module)
    parsed = resolve(request)
    report = generate_interactive(request, settings=ReportSettings())
    assert len(parsed.measurements) == count
    assert report.parsed == parsed
    actual = [m for o in report.observations for m in o.measurements]
    assert {m.id: m for m in actual} == {m.id: m for m in parsed.measurements}
    assert len(report.observations) == len(parsed.teeth)
    for o in report.observations:
        for m in o.measurements:
            assert json.dumps(m.raw_value, ensure_ascii=False) in report.export_text
            if m.numeric_status in {"PARSED", "EXPLICIT_ZERO"}:
                assert str(m.signed_decimal) in o.text
                if m.raw_direction: assert json.dumps(m.raw_direction) in o.text
            else:
                assert "unknown" in o.text
            if m.span:
                assert raw[m.span.start:m.span.end] == m.raw_value
    assert report.clinical_analysis_enabled is False
    assert report.engine_review.evidence_domain == "UNVERIFIED"
    assert len(report.engine_review.evaluations) == len(RULES) == 96
    assert all(not f.observed_measurements for f in report.engine_review.findings)
    assert all(not e.evaluated for e in report.engine_review.evaluations if e.execution == "DISABLED")
    assert report.generation.used_mode == "STANDARD_TEMPLATES"
    assert report.wording_notice == "Standard report wording."
    assert report.export_text.split("ORIGINAL INPUT — VERBATIM\n", 1)[1].startswith(raw)
    assert len(report.illustrations) == 0
    for item in report.illustrations:
        assert item.origin == "SIMULATED_DEMO" and item.clinical_status == "NOT_EVALUATED"
        assert "Illustration only" in item.text
    assert "RULE EVALUATION LEDGER" in report.export_text


def test_illustrative_choices_are_independent_of_movement_values():
    for module in ("micro", "nano"):
        a = generate_interactive(submission(module=module), settings=ReportSettings())
        b = generate_interactive(submission(ROWS.replace("-2.7500 M", "999.9500 D"), module), settings=ReportSettings())
        assert a.illustrations == b.illustrations == []
        assert a.sections == b.sections
        assert a.observations != b.observations


def provider(status=200, mutate=None):
    settings = ReportSettings(api_key="PRIVATE_SERVER_KEY", synthetic_transmission_enabled=True)
    captured = []
    def handler(request):
        captured.append(json.loads(request.content))
        data = json.loads(captured[-1]["messages"][1]["content"])
        if "programmed_movements" in data:
            openings = ["The recorded profile includes ", "This entry records ", "Programmed movement components are "]
            output = {"comments": [{"tooth_ref": t["tooth_ref"], "text": openings[i % len(openings)] + " and ".join("{" + m["ref"] + "}" for m in t["movements"]) + "."} for i, t in enumerate(data["programmed_movements"])]}
        else:
            output = {"comments": [{"finding_ids": [ref], "text": options[1]} for ref, options in WORDINGS.items()]}
        if mutate: mutate(output)
        return httpx.Response(status, json={"model": settings.model, "choices": [{"finish_reason": "stop", "message": {"role": "assistant", "content": json.dumps(output)}}]})
    return settings, GroqClient(settings, transport=httpx.MockTransport(handler)), captured


@pytest.mark.parametrize("module", ["macro", "micro", "nano"])
def test_groq_grounded_module_payload_and_local_facts(module):
    settings, client, captured = provider()
    request = submission("Patient: PRIVATE_PATIENT_ABC\n" + LARGE, module)
    report = generate_interactive(request, settings=settings, client=client)
    assert report.generation.used_mode == "GROQ_AI"
    assert report.generation.accepted_comments == (16 if module == "macro" else 4) and report.generation.attempts == 1
    assert report.wording_notice == "AI-assisted report wording."
    payload = json.dumps(captured)
    for value in ("PRIVATE_PATIENT_ABC", "PRIVATE_SERVER_KEY", request.raw_sha256, "Rotation", "Mesial", "Patient"):
        assert value not in payload
    assert "0.4500" in report.export_text and "1.2300" in report.export_text
    other_settings, other_client, other_captured = provider()
    generate_interactive(submission(ROWS, module), settings=other_settings, client=other_client)
    if module == "macro":
        assert captured != other_captured
        assert "1.2300" in payload and "0.4500" in payload
    else:
        assert captured == other_captured  # No attachment/stage facts were supplied in either TMT.
        assert "1.2300" not in payload and "0.4500" not in payload
    assert "raw_text" not in payload and "source_version" not in payload


@pytest.mark.parametrize("status", [401, 429, 500, 503])
def test_provider_failure_honest_fallback(status):
    settings, client, _ = provider(status)
    report = generate_interactive(submission(), settings=settings, client=client)
    assert report.generation.used_mode == "STANDARD_TEMPLATES"
    assert report.generation.accepted_comments == 0
    assert report.generation.attempts == 1
    assert report.wording_notice == "Standard report wording."
    assert "PRIVATE_SERVER_KEY" not in report.model_dump_json()


@pytest.mark.parametrize("bad_text", ["Use 2.000 mm attachments", "Recommended extraction", "All movements are clinically safe", "Recorded values 99", "<script>bad</script>"])
def test_unsupported_groq_numbers_and_decisions_rejected(bad_text):
    settings, client, _ = provider(mutate=lambda d: d["comments"][0].update(text=bad_text))
    report = generate_interactive(submission(), settings=settings, client=client)
    assert report.generation.used_mode == "STANDARD_TEMPLATES"
    assert report.generation.reason == "GROQ_UNSUPPORTED_WORDING"
    assert bad_text not in report.export_text


def test_duplicate_or_incomplete_wording_is_rejected():
    for mutate in (lambda d: d["comments"].pop(), lambda d: d["comments"].__setitem__(1, d["comments"][0])):
        settings, client, _ = provider(mutate=mutate)
        report = generate_interactive(submission(), settings=settings, client=client)
        assert report.generation.used_mode == "STANDARD_TEMPLATES"


def test_backend_key_automatically_enables_grounded_wording(monkeypatch):
    settings, client, captured = provider()
    monkeypatch.setenv("GROQ_API_KEY", "PRIVATE_SERVER_KEY")
    monkeypatch.setenv("FINOVA_GROQ_SYNTHETIC_ENABLED", "false")
    monkeypatch.setattr("app.interactive.service.GroqClient", lambda config: client)
    monkeypatch.setattr("app.interactive.narrative.GroqClient", lambda config: client)
    report = generate_interactive(submission())
    assert report.generation.used_mode == "GROQ_AI" and len(captured) == 1


def test_api_no_fixed_demo_permission_needed_and_private_errors(monkeypatch):
    for name in ("FINOVA_PLANNING_DEMO_ENABLED", "FINOVA_ATTACHMENT_DEMO_ENABLED", "FINOVA_SEQUENCER_DEMO_ENABLED", "GROQ_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    client = TestClient(app)
    body = submission().model_dump(mode="json")
    response = client.post("/api/v1/interactive/review", json=body)
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert InteractiveReport.model_validate_json(response.content).observations
    for key, value in [("synthetic_data_confirmed", False), ("clinical_analysis_enabled", True), ("api_key", "SECRET"), ("checked", {}), ("module", "clinical")]:
        bad = dict(body); bad[key] = value
        response = client.post("/api/v1/interactive/review", json=bad)
        assert response.status_code == 422 and "SECRET" not in response.text and ROWS not in response.text
    body["raw_sha256"] = "0" * 64
    assert client.post("/api/v1/interactive/review", json=body).status_code == 409
    invalid = submission("not a table").model_dump(mode="json")
    assert client.post("/api/v1/interactive/review", json=invalid).status_code == 422


def test_exported_interactive_contracts_match():
    root = Path(__file__).resolve().parents[2] / "schemas"
    for name, cls, mode in [("interactive-request.v1.json", InteractiveSubmission, "validation"), ("interactive-report.v1.json", InteractiveReport, "serialization")]:
        assert json.loads((root / name).read_text(encoding="utf-8")) == cls.model_json_schema(mode=mode)
