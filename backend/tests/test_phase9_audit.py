"""Cross-module metamorphic checks: structural recovery never transfers authority."""
import json

from fastapi.testclient import TestClient
import httpx
import pytest

from app.main import app
from app.parser.cloud import ParserSettings
from app.parser.contracts import PipelineSubmission, SyntheticFixture
from app.parser.generated import generate
from app.parser.phase4 import parse_pipeline
from app.reports.groq_client import GroqClient
from app.review.registry import RULES

client = TestClient(app)
ROUTES = ("planning", "attachments", "sequencing")


def engine(module, body):
    return body["report"]["engine_review"] if module == "planning" else body["engine_review"]


def assert_unverified(module, body, positions):
    review = engine(module, body)
    assert review["evidence_domain"] == "UNVERIFIED"
    assert review["coverage"]["declared_positions"] == positions
    assert review["coverage"]["eligible_positions"] == 0
    assert {e["rule_id"] for e in review["evaluations"]} == {r.rule_id for r in RULES}
    disabled = [e for e in review["evaluations"] if e["execution"] == "DISABLED"]
    assert len(disabled) == 27
    assert all(e["status"] == "DISABLED" and not e["evaluated"] for e in disabled)
    assert "DRAFT — Requires Orthodontist Review" in body["export_text"]
    if module == "planning":
        assert body["report"]["generation"]["attempts"] == 0
        assert all(c["section"] == "UNAVAILABLE" for c in body["report"]["comments"])
    else:
        assert body["provider_attempts"] == 0
        assert all(e["result_type"] in {"UNKNOWN", "WITHHELD", "DISABLED"} for e in body["entries"])


@pytest.mark.parametrize("environment", [None, "production", "test", "Development"])
def test_fixture_generator_refuses_non_development_without_side_effects(monkeypatch, environment):
    monkeypatch.delenv("FINOVA_ENVIRONMENT", raising=False)
    if environment is not None:
        monkeypatch.setenv("FINOVA_ENVIRONMENT", environment)
    # Even all three demo flags cannot override the environment boundary.
    for flag in ("PLANNING", "ATTACHMENT", "SEQUENCER"):
        monkeypatch.setenv(f"FINOVA_{flag}_DEMO_ENABLED", "true")
    response = client.post("/api/v1/development/synthetic", json={"recipe": "wrapped", "seed": 17})
    assert response.status_code == 404
    assert response.headers["cache-control"] == "no-store"


@pytest.mark.parametrize("recipe", ["mixed_rows", "wrapped", "partial"])
def test_accepted_structural_receipt_replays_across_modules_without_semantic_authority(monkeypatch, recipe):
    identity = SyntheticFixture(recipe=recipe, seed=73)
    sample = generate(identity)
    submission = PipelineSubmission(raw_text=sample.raw_text, synthetic_fixture=identity, synthetic_data_confirmed=True)
    settings = ParserSettings(api_key="SYNTHETIC_MOCK", environment="development", synthetic_transmission_enabled=True)
    calls = []

    def provider(request):
        calls.append(request)
        return httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {
            "role": "assistant", "content": json.dumps({"associations": [g["association"] for g in sample.gold]})}}]})

    recovered = parse_pipeline(submission, settings=settings, client=GroqClient(settings, transport=httpx.MockTransport(provider)))
    assert len(calls) == 1 and recovered.pipeline.assistance.status == "ACCEPTED"
    assert recovered.pipeline.recovery_receipt
    # Subsequent module review must use the signed receipt, without repeating cloud recovery.
    monkeypatch.setattr(GroqClient, "generate", lambda *_a, **_k: pytest.fail("Unexpected downstream provider call"))
    payload = {"raw_text": sample.raw_text, "synthetic_data_confirmed": True,
               "recovery_receipt": recovered.pipeline.recovery_receipt}
    for module in ROUTES:
        response = client.post(f"/api/v1/{module}/draft", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert_unverified(module, body, len(recovered.measurements))
        assert engine(module, body)["raw_sha256"] == recovered.raw_sha256
        if module == "sequencing":
            original = [(m.id, m.raw_value, m.signed_decimal, m.numeric_status) for m in recovered.measurements]
            replay = [(m["id"], m["raw_value"], m["signed_decimal"], m["numeric_status"]) for m in body["parsed"]["measurements"]]
            assert [(a, b, str(c) if c is not None else None, d) for a, b, c, d in original] == replay
        # A receipt cannot survive a context change, even when every numeric byte is unchanged.
        changed = client.post(f"/api/v1/{module}/draft", json={**payload, "context": {"scope": "TOTAL"}})
        assert changed.status_code == 409


def test_demo_visits_do_not_enroll_the_shared_raw_table_in_normal_modules(monkeypatch):
    monkeypatch.setenv("FINOVA_ENVIRONMENT", "development")
    for flag in ("PLANNING", "ATTACHMENT", "SEQUENCER"):
        monkeypatch.setenv(f"FINOVA_{flag}_DEMO_ENABLED", "true")
    monkeypatch.setattr(GroqClient, "generate", lambda *_a, **_k: pytest.fail("Unexpected provider call"))
    for demo in ("planning-demo", "attachment-demo", "sequencer-demo"):
        loaded = client.post(f"/api/v1/development/{demo}/input", json={}).json()
        raw, context = loaded["parsed"]["raw_text"], loaded["context"]
        result = client.post(f"/api/v1/development/{demo}/draft", json={"comment_mode": "TEMPLATES"} if demo == "planning-demo" else {})
        assert result.status_code == 200
        for module in ROUTES:
            ordinary = client.post(f"/api/v1/{module}/draft", json={"raw_text": raw, "context": context, "synthetic_data_confirmed": True})
            assert ordinary.status_code == 200
            assert_unverified(module, ordinary.json(), 20)
