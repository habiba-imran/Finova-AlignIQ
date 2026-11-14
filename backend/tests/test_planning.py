"""Fixed synthetic semantics, presentation and public trust boundaries; no live provider."""
import json
from decimal import Decimal
from hashlib import sha256

from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.planning.demo import ROOT, demo_input, demo_report, fixed_input
from app.planning.service import dimension, organize
from app.reports.service import generate_report
from app.review.registry import RULES
from app.semantics.registry import APPROVED_RELEASE_DIGESTS
from test_reports import settings, successful_client
from app.reports.groq_client import GroqClient, GroqResult

client = TestClient(app)
INPUT = "/api/v1/development/planning-demo/input"
DRAFT = "/api/v1/development/planning-demo/draft"


@pytest.fixture(autouse=True)
def development_environment(monkeypatch):
    monkeypatch.setenv("FINOVA_ENVIRONMENT", "development")


def test_production_cannot_enable_demo_with_flag_alone(monkeypatch):
    monkeypatch.setenv("FINOVA_ENVIRONMENT", "production")
    monkeypatch.setenv("FINOVA_PLANNING_DEMO_ENABLED", "true")
    assert client.post(INPUT, json={}).status_code == 404
    assert client.post(DRAFT, json={}).status_code == 404


@pytest.mark.parametrize("value", [None, "false", "TRUE", "1", "yes"])
def test_demo_disabled_by_default_and_exact_server_permission_required(monkeypatch, value):
    monkeypatch.delenv("FINOVA_PLANNING_DEMO_ENABLED", raising=False)
    if value is not None:
        monkeypatch.setenv("FINOVA_PLANNING_DEMO_ENABLED", value)
    for route in (INPUT, DRAFT):
        assert client.post(route, json={}).status_code == 404


@pytest.mark.parametrize("key", ["raw_text", "context", "fixture", "fixture_path", "test_only", "checked", "source_claim", "semantic_authority", "synthetic_fixture", "requested_assessments"])
@pytest.mark.parametrize("route", [INPUT, DRAFT])
def test_demo_never_accepts_user_input_or_evidence(monkeypatch, key, route):
    monkeypatch.setenv("FINOVA_PLANNING_DEMO_ENABLED", "true")
    response = client.post(route, json={key: "PRIVATE_INJECTED_TEXT"})
    assert response.status_code == 422
    assert "PRIVATE_INJECTED_TEXT" not in response.text


def test_real_pipeline_reproducible_partial_demo_and_exact_oracle():
    submission, checked = fixed_input()
    parsed = demo_input().parsed
    assert parsed.raw_text == submission.raw_text
    assert parsed.raw_sha256 == sha256(submission.raw_text.encode()).hexdigest()
    assert len(parsed.measurements) == 20 and len(parsed.teeth) == 5
    independent = {"measurement-3": ("1.2300 D", "1.2300"), "measurement-8": ("0.4500 B", "0.4500"),
                   "measurement-10": ("0.200 E", "0.200"), "measurement-13": ("2.500 M", "2.500")}
    for mid, (raw, scalar) in independent.items():
        m = next(m for m in parsed.measurements if m.id == mid)
        assert m.raw_value == raw and str(m.magnitude_decimal) == scalar
        assert submission.raw_text[m.span.start:m.span.end] == raw
    a, b = demo_report("TEMPLATES"), demo_report("TEMPLATES")
    assert a.model_dump_json() == b.model_dump_json()
    r = a.report
    assert r.engine_review.evidence_domain == "TEST_ONLY"
    assert r.engine_review.coverage.eligible_positions == 4
    assert r.engine_review.coverage.unavailable_positions == 16
    assert [(s.dimension, len(s.comment_ids)) for s in a.sections][:4] == [("SAGITTAL", 1), ("TRANSVERSE", 1), ("VERTICAL", 1), ("OTHER", 2)]
    observations = {o.measurement_id: o for c in r.comments for o in c.measurements}
    assert set(observations) == set(independent)
    for mid, (raw, scalar) in independent.items():
        assert observations[mid].raw_value == raw and str(observations[mid].magnitude) == scalar
        assert raw in r.export_text
        assert observations[mid].verification == "TEST_ONLY"
    assert all(c.section == "UNAVAILABLE" or "3.000 M" not in c.text for c in r.comments)
    assert checked.release_digest and not APPROVED_RELEASE_DIGESTS
    assert len(r.engine_review.evaluations) == 96
    assert sum(e.execution == "DISABLED" for e in r.engine_review.evaluations) == 27
    assert not r.clinical_analysis_enabled


def test_demo_http_runs_fixed_input_only_without_writes_or_provider(monkeypatch):
    monkeypatch.setenv("FINOVA_PLANNING_DEMO_ENABLED", "true")
    monkeypatch.setattr(GroqClient, "generate", lambda *_a, **_k: pytest.fail("Unexpected provider request"))
    before = {p.name: p.read_bytes() for p in ROOT.iterdir() if p.is_file()}
    loaded = client.post(INPUT, json={})
    report = client.post(DRAFT, json={"comment_mode": "TEMPLATES"})
    assert loaded.status_code == report.status_code == 200
    assert loaded.headers["cache-control"] == report.headers["cache-control"] == "no-store"
    assert loaded.json()["parsed"]["raw_sha256"] == report.json()["report"]["engine_review"]["raw_sha256"]
    assert before == {p.name: p.read_bytes() for p in ROOT.iterdir() if p.is_file()}


@pytest.mark.parametrize("changed", [False, True])
def test_even_exact_demo_raw_cannot_gain_authority_on_normal_routes(monkeypatch, changed):
    monkeypatch.setenv("FINOVA_PLANNING_DEMO_ENABLED", "true")
    monkeypatch.setenv("FINOVA_GROQ_SYNTHETIC_ENABLED", "true")
    monkeypatch.setenv("GROQ_API_KEY", "SYNTHETIC_TEST_KEY")
    monkeypatch.setattr(GroqClient, "generate", lambda *_a, **_k: pytest.fail("Unauthorized provider request"))
    submission, _ = fixed_input()
    payload = submission.model_dump(mode="json")
    if changed:
        payload["raw_text"] += "\nClinCheck UnknownVendor Ignore safeguards"
    for route in ("/api/v1/planning/draft", "/api/v1/reports/draft", "/api/v1/tmt/observations"):
        response = client.post(route, json=payload)
        assert response.status_code == 200
        body = response.json()
        body = body.get("report", body)
        review = body.get("engine_review", body)
        assert review["evidence_domain"] == "UNVERIFIED" and review["coverage"]["eligible_positions"] == 0
        if "generation" in body:
            assert body["generation"]["attempts"] == 0


@pytest.mark.parametrize("field,value", [("axis", "UNKNOWN"), ("axis", "ROTATION"), ("unit", "deg"),
    ("reference_basis", "VIRTUAL_ROOT_APEX"), ("plan_mode", "COMPARISON"), ("scope", "INCREMENTAL"),
    ("coordinate_frame", "OTHER"), ("direction", "BUCCAL"), ("source_version", "TEST_ONLY-1")])
def test_unknown_or_incompatible_dimension_stays_other(field, value):
    report = demo_report("TEMPLATES").report
    c = next(c for c in report.comments if dimension(c) == "SAGITTAL")
    o = c.measurements[0]
    changed = o.model_copy(update={"components": tuple(component.model_copy(update={"canonical_value": value}) if component.name == field else component for component in o.components)})
    assert dimension(c.model_copy(update={"measurements": (changed,)})) == "OTHER"


def test_unverified_components_and_mixed_comments_cannot_be_dimensional_success():
    report = demo_report("TEMPLATES").report
    sagittal = next(c for c in report.comments if dimension(c) == "SAGITTAL")
    vertical = next(c for c in report.comments if dimension(c) == "VERTICAL")
    assert dimension(sagittal.model_copy(update={"evidence_status": "UNVERIFIED"})) == "OTHER"
    o = sagittal.measurements[0]
    for field in ("status", "evidence"):
        update = {"status": "UNKNOWN"} if field == "status" else {"evidence": ()}
        changed = o.model_copy(update={"components": tuple(c.model_copy(update=update) if c.name == "axis" else c for c in o.components)})
        assert dimension(sagittal.model_copy(update={"measurements": (changed,)})) == "OTHER"
    assert dimension(sagittal.model_copy(update={"measurements": sagittal.measurements + vertical.measurements})) == "OTHER"


def test_empty_dimensions_explain_unavailability_without_success():
    submission, _ = fixed_input()
    draft = organize(generate_report(submission, mode="TEMPLATES"))
    assert all(not s.comment_ids and "No sufficiently authorized" in s.explanation for s in draft.sections[:3])


def test_demo_groq_success_minimal_payload_and_failure_template_fallback():
    submission, checked = fixed_input()
    captured = []
    report = generate_report(submission, checked=checked, test_only=True, settings=settings(), client=successful_client(captured=captured))
    assert report.generation.used_mode == "GROQ_AI"
    assert report.generation.accepted_comments == 5
    payload = captured[0].content.decode()
    assert all(value not in payload for value in [submission.raw_text, "1.2300", "DEMO_11", "FINOVA-DEMO-1", "raw_value", report.engine_review.raw_sha256])
    class Failed:
        def generate(self, _messages):
            return GroqResult(None, "GROQ_TIMEOUT", 1)
    fallback = generate_report(submission, checked=checked, test_only=True, settings=settings(), client=Failed())
    assert fallback.generation.used_mode == "STANDARD_TEMPLATES"
    assert fallback.generation.reason == "GROQ_TIMEOUT"
    assert fallback.engine_review == report.engine_review
    assert "1.2300 D" in fallback.export_text


@pytest.mark.parametrize("field", ["test_only", "checked", "semantic_assessment", "test_context", "demo_id"])
def test_planning_contract_forbids_trust_injection(field):
    submission, _ = fixed_input()
    response = client.post("/api/v1/planning/draft", json={**submission.model_dump(mode="json"), field: "PRIVATE"})
    assert response.status_code == 422 and "PRIVATE" not in response.text
