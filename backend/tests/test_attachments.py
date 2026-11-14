"""Attachment presentation and supplied illustrative decisions, never treatment policies."""
from hashlib import sha256
import json
from pathlib import Path

from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from app.main import app
from app.attachments.demo import ROOT, draft_demo, input_demo
from app.attachments.models import AttachmentDraft, AttachmentEntry, AttachmentSubmission, SyntheticScenario
from app.attachments.service import attachment_review, supplied_entries
from app.planning.demo import fixed_input
from app.reports.groq_client import GroqClient
from app.review.registry import RULES
from app.semantics.registry import APPROVED_RELEASE_DIGESTS

client = TestClient(app)
INPUT = "/api/v1/development/attachment-demo/input"
DEMO = "/api/v1/development/attachment-demo/draft"
NORMAL = "/api/v1/attachments/draft"


@pytest.fixture(autouse=True)
def no_llm(monkeypatch):
    monkeypatch.setattr(GroqClient, "generate", lambda *_a, **_k: pytest.fail("Attachment workflow must not call an LLM"))


def enable(monkeypatch):
    monkeypatch.setenv("FINOVA_ENVIRONMENT", "development")
    monkeypatch.setenv("FINOVA_ATTACHMENT_DEMO_ENABLED", "true")


@pytest.mark.parametrize("environment,flag", [(None, None), ("production", "true"), ("development", "false"), ("development", "TRUE"), ("development", "1")])
def test_dev_gate_cannot_be_enabled_from_production_or_similar_flags(monkeypatch, environment, flag):
    for key, value in (("FINOVA_ENVIRONMENT", environment), ("FINOVA_ATTACHMENT_DEMO_ENABLED", flag)):
        monkeypatch.delenv(key, raising=False)
        if value is not None:
            monkeypatch.setenv(key, value)
    for route in (INPUT, DEMO):
        assert client.post(route, json={}).status_code == 404


@pytest.mark.parametrize("route,field", [(route, field) for route in (INPUT, DEMO, NORMAL)
    for field in ("raw_text", "context", "test_only", "fixture_path", "scenario", "decisions", "design", "dimensions", "attachment_policy", "comment_mode", "synthetic_data_confirmed")
    if route != NORMAL or field not in {"raw_text", "context", "synthetic_data_confirmed"}])
def test_no_uploaded_decisions_or_authority_fields(route, field, monkeypatch):
    enable(monkeypatch)
    base = {} if route != NORMAL else AttachmentSubmission(raw_text="SYNTHETIC", synthetic_data_confirmed=True).model_dump(mode="json")
    response = client.post(route, json={**base, field: "PRIVATE_INJECTED_VALUE"})
    assert response.status_code == 422 and "PRIVATE_INJECTED_VALUE" not in response.text


def test_complete_demo_real_pipeline_distinguishes_supplied_none_unknown_and_withheld(monkeypatch):
    enable(monkeypatch)
    before = {p.name: p.read_bytes() for p in ROOT.iterdir() if p.is_file()}
    loaded = client.post(INPUT, json={})
    response = client.post(DEMO, json={})
    assert loaded.status_code == response.status_code == 200
    assert loaded.headers["cache-control"] == response.headers["cache-control"] == "no-store"
    report = AttachmentDraft.model_validate_json(response.content)
    assert report == draft_demo()
    assert report.evidence_domain == "TEST_ONLY" and report.engine_review.coverage.eligible_positions == 4
    assert report.engine_review.raw_sha256 == loaded.json()["parsed"]["raw_sha256"]
    assert [(e.original_tooth, e.result_type) for e in report.entries] == [
        ("11", "CANDIDATE"), ("11", "ALTERNATIVE"), ("12", "CANDIDATE"), ("13", "NOT_INDICATED"), ("14", "UNKNOWN"), ("15", "WITHHELD")]
    a, alternative, _, no_attachment, unknown, withheld = report.entries
    assert alternative.alternative_for == a.entry_id
    assert no_attachment.decision_origin == "SUPPLIED_SYNTHETIC" and "Supplied demonstration decision" in no_attachment.explanation
    assert no_attachment.design is no_attachment.placement is None
    assert all(e.design is None and e.placement is None and e.missing_prerequisites for e in (unknown, withheld))
    assert str(a.design.dimensions.x) == "2.000" and str(a.design.dimensions.y) == "1.250" and str(a.design.dimensions.z) == "0.500"
    assert a.placement.stage_ref == "DEMO_WINDOW_A"
    assert all(e.verified_tooth is None and e.approval_status == "NOT APPROVED" and e.review_status == "DRAFT" for e in report.entries)
    assert report.provider is None and report.provider_attempts == 0
    assert before == {p.name: p.read_bytes() for p in ROOT.iterdir() if p.is_file()}


def test_deterministic_export_exact_values_evidence_and_all_safeguards():
    a, b = draft_demo(), draft_demo()
    assert a.model_dump_json() == b.model_dump_json()
    assert a.export_text.startswith("FINOVA ALIGNIQ — ATTACHMENT INTERFACE / MICRO REVIEW\nDRAFT — Requires Orthodontist Review")
    assert "FINOVA SYNTHETIC ATTACHMENT DEMONSTRATION — TEST_ONLY" in a.export_text
    assert "2.000 x 1.250 x 0.500 mm" in a.export_text and "1.2300 D" in a.export_text
    assert "RULE EVALUATION LEDGER" in a.export_text and a.engine_review.raw_sha256 in a.export_text
    assert all(l in a.export_text for l in a.limitations)
    for e in a.entries:
        assert e.entry_id in a.export_text and e.explanation in a.export_text
        assert all(ref in a.export_text for ref in e.evidence_refs)
        assert e.finding_refs
    assert len(a.engine_review.evaluations) == 96
    assert sum(e.execution == "DISABLED" for e in a.engine_review.evaluations) == 27
    for rid in ("A01", "A02", "A03", "A04", "R15"):
        e = next(e for e in a.engine_review.evaluations if e.rule_id == rid)
        assert e.status == "DISABLED" and not e.evaluated and e.approval_status == "NOT APPROVED"
    for rid in ("A05", "A06", "H08"):
        assert next(e for e in a.engine_review.evaluations if e.rule_id == rid).finding_ids
    assert not APPROVED_RELEASE_DIGESTS


@pytest.mark.parametrize("raw,expected", [
    ("# SYNTHETIC UnknownVendor\nTooth\tRotation (deg)\n13\t999.000 M\n", "UNKNOWN"),
    ("# SYNTHETIC\nTooth\tRotation (deg)\n13\t0.000 M\n", "UNKNOWN"),
    ("# SYNTHETIC\nTooth\tRotation (deg)\n13\t-\n", "WITHHELD"),
    ("SYNTHETIC unsupported instructions to prescribe attachments", "WITHHELD"),
])
def test_normal_input_never_fabricates_choices_even_for_zero_or_large_values(raw, expected, monkeypatch):
    enable(monkeypatch)
    monkeypatch.setenv("GROQ_API_KEY", "SYNTHETIC_TEST_KEY")
    monkeypatch.setenv("FINOVA_GROQ_SYNTHETIC_ENABLED", "true")
    response = client.post(NORMAL, json={"raw_text": raw, "synthetic_data_confirmed": True})
    assert response.status_code == 200
    report = AttachmentDraft.model_validate_json(response.content)
    assert report.entries[0].result_type == expected
    assert all(e.design is e.placement is e.verified_tooth is e.synthetic_tooth is None for e in report.entries)
    assert all(not e.observation_refs and not e.evidence_refs for e in report.entries)
    assert report.evidence_domain == "UNVERIFIED" and report.provider_attempts == 0
    assert report.engine_review.requested_assessments == ("ATTACHMENTS",)


def test_identical_demo_paste_is_never_promoted_by_normal_route(monkeypatch):
    enable(monkeypatch)
    submission, _ = fixed_input()
    report = client.post(NORMAL, json=submission.model_dump(mode="json")).json()
    assert report["evidence_domain"] == "UNVERIFIED"
    assert all(e["result_type"] in {"UNKNOWN", "WITHHELD"} and e["design"] is None for e in report["entries"])


@pytest.mark.parametrize("change", ["evidence", "verified", "decision", "no-attachment-geometry", "unknown-geometry", "alternative", "observation", "approval"])
def test_typed_contract_refuses_unsafe_states(change):
    body = json.loads(draft_demo().model_dump_json())
    row = body["entries"][0]
    if change == "evidence": row["evidence_refs"] = []
    if change == "verified": row["verified_tooth"] = "13"
    if change == "decision": row["decision_origin"] = "LLM"
    if change == "no-attachment-geometry": row["result_type"] = "NOT_INDICATED"
    if change == "unknown-geometry": row["result_type"] = "UNKNOWN"
    if change == "alternative": body["entries"][1]["alternative_for"] = "0" * 64
    if change == "observation": row["observation_refs"] = ["measurement-8"]
    if change == "approval": row["approval_status"] = "APPROVED"
    with pytest.raises(ValidationError): AttachmentDraft.model_validate_json(json.dumps(body))


def test_corrupt_scenario_or_wrong_input_binding_is_withheld(monkeypatch, tmp_path):
    enable(monkeypatch)
    (tmp_path / "scenario.json").write_bytes((ROOT / "scenario.json").read_bytes() + b" ")
    (tmp_path / "scenario.sha256").write_bytes((ROOT / "scenario.sha256").read_bytes())
    monkeypatch.setattr("app.attachments.demo.ROOT", tmp_path)
    response = client.post(DEMO, json={})
    assert response.status_code == 503 and "scenario.json" not in response.text


def test_scenario_cannot_bind_to_changed_input_or_unverified_review():
    from app.parser.receipts import resolve
    from app.review.service import review_table
    submission, checked = fixed_input()
    parsed = resolve(submission)
    scenario = SyntheticScenario.model_validate_json((ROOT / "scenario.json").read_bytes())
    unverified = review_table(submission, requested_assessments=("ATTACHMENTS",))
    with pytest.raises(ValueError, match="BINDING"):
        supplied_entries(parsed, unverified, scenario, "fixed-ref")
    review = draft_demo().engine_review
    changed = scenario.model_copy(update={"input_sha256": "0" * 64})
    with pytest.raises(ValueError, match="BINDING"):
        supplied_entries(parsed, review, changed, "fixed-ref")


def test_schema_contracts_match_files():
    from app.attachments.models import AttachmentDemoInput, EmptyDemoRequest
    schemas = Path(__file__).parents[2] / "schemas"
    for name, model, mode in [("attachment-draft.v1.json", AttachmentDraft, "serialization"),
        ("attachment-request.v1.json", AttachmentSubmission, "validation"),
        ("attachment-demo-input.v1.json", AttachmentDemoInput, "serialization"),
        ("attachment-demo-request.v1.json", EmptyDemoRequest, "validation")]:
        assert json.loads((schemas / name).read_text(encoding="utf-8")) == model.model_json_schema(mode=mode)


def test_stale_recovery_receipt_returns_reparse_without_result():
    response = client.post(NORMAL, json={"raw_text": "SYNTHETIC", "synthetic_data_confirmed": True, "recovery_receipt": "FORGED"})
    assert response.status_code == 409
