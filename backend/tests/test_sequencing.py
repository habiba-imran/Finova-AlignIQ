"""Nano supplied-content and stage/provenance boundaries; no live provider."""
import json
from pathlib import Path

from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from app.main import app
from app.parser.receipts import resolve
from app.planning.demo import fixed_input
from app.reports.groq_client import GroqClient
from app.review.context import StageRecord, TestRuleContext, input_digest
from app.review.service import review_table
from app.semantics.registry import APPROVED_RELEASE_DIGESTS
from app.sequencing.demo import ROOT, draft_demo, fixed_scenario
from app.sequencing.models import EmptyDemoRequest, SequencingDemoInput, SequencingDraft, SequencingScenario, SequencingSubmission, StageWindow
from app.sequencing.service import assemble

client = TestClient(app)
INPUT, DEMO, NORMAL = "/api/v1/development/sequencer-demo/input", "/api/v1/development/sequencer-demo/draft", "/api/v1/sequencing/draft"


@pytest.fixture(autouse=True)
def forbid_provider(monkeypatch):
    monkeypatch.setattr(GroqClient, "generate", lambda *_a, **_k: pytest.fail("Unexpected provider call from Nano"))


def enable(monkeypatch):
    monkeypatch.setenv("FINOVA_ENVIRONMENT", "development")
    monkeypatch.setenv("FINOVA_SEQUENCER_DEMO_ENABLED", "true")


@pytest.mark.parametrize("environment,flag", [(None, None), ("production", "true"), ("development", "false"), ("development", "TRUE"), ("development", "1")])
def test_no_production_or_request_flag_authority(monkeypatch, environment, flag):
    for k, v in (("FINOVA_ENVIRONMENT", environment), ("FINOVA_SEQUENCER_DEMO_ENABLED", flag)):
        monkeypatch.delenv(k, raising=False)
        if v is not None: monkeypatch.setenv(k, v)
    assert client.post(INPUT, json={}).status_code == client.post(DEMO, json={}).status_code == 404


@pytest.mark.parametrize("route,field", [(route, field) for route in (INPUT, DEMO, NORMAL)
    for field in ("raw_text", "context", "test_only", "stage_records", "scenario", "fixture_path", "strategy", "anchorage", "policy_id", "verified_arch", "force")
    if route != NORMAL or field not in {"raw_text", "context"}])
def test_http_refuses_supplied_stages_strategies_and_authority(monkeypatch, route, field):
    enable(monkeypatch)
    base = {"raw_text": "SYNTHETIC", "synthetic_data_confirmed": True} if route == NORMAL else {}
    response = client.post(route, json={**base, field: "PRIVATE_INJECTED_VALUE"})
    assert response.status_code == 422 and "PRIVATE_INJECTED_VALUE" not in response.text


def test_fixed_demo_real_services_provenance_export_and_disabled_engine(monkeypatch):
    enable(monkeypatch)
    before = {p.name: p.read_bytes() for p in ROOT.iterdir() if p.is_file()}
    loaded, response = client.post(INPUT, json={}), client.post(DEMO, json={})
    assert loaded.status_code == response.status_code == 200
    assert loaded.headers["cache-control"] == response.headers["cache-control"] == "no-store"
    report = SequencingDraft.model_validate_json(response.content)
    assert report == draft_demo() == draft_demo()
    assert report.parsed.raw_sha256 == loaded.json()["parsed"]["raw_sha256"]
    assert report.synthetic_notice == "SYNTHETIC DEMONSTRATION — NOT CLINICAL ADVICE"
    assert report.evidence_domain == "TEST_ONLY" and report.provider is None and report.provider_attempts == 0
    assert {e.section for e in report.entries} == {"UPPER_ARCH", "LOWER_ARCH", "SEGMENTS", "RIGHT_ANCHORAGE", "LEFT_ANCHORAGE", "UNAVAILABLE"}
    assert len([e for e in report.entries if e.result_type == "SUPPLIED_SYNTHETIC"]) == 6
    assert {a.role for a in report.fictional_arches} == {"UPPER", "LOWER"}
    assert report.stage_inspection.status == "SUPPLIED_SYNTHETIC_METADATA" and len(report.stage_inspection.records) == 5
    assert next(e for e in report.engine_review.evaluations if e.rule_id == "G15").status == "OBSERVED"
    assert next(e for e in report.engine_review.evaluations if e.rule_id == "N07").status == "NOT_APPLICABLE"
    assert report.engine_review.coverage.eligible_positions == 4
    assert next(e for e in report.entries if e.original_tooth_refs == ("tooth-5",)).movement_scope == "UNKNOWN"
    assert all(e.verified_arch is None and e.verified_segment is None and not e.verified_tooth_refs and e.policy_id is None for e in report.entries)
    assert all(e.approval_status == "NOT APPROVED" and not e.clinical_predicate_evaluated for e in report.entries)
    for side in ("RIGHT", "LEFT"):
        entries = [e for e in report.entries if e.section == f"{side}_ANCHORAGE"]
        assert len(entries) == 1 and entries[0].side == side and entries[0].origin == "SUPPLIED_SCENARIO"
    assert len(report.engine_review.evaluations) == 96
    assert sum(e.execution == "DISABLED" for e in report.engine_review.evaluations) == 27
    for rid in ("R13", *(f"T{i:02}" for i in range(1, 9))):
        result = next(e for e in report.engine_review.evaluations if e.rule_id == rid)
        assert result.status == "DISABLED" and not result.evaluated
    assert not APPROVED_RELEASE_DIGESTS
    assert report.export_text.startswith("FINOVA ALIGNIQ — SEQUENCER / NANO REVIEW\nDRAFT — Requires Orthodontist Review")
    assert report.synthetic_notice in report.export_text and "1.2300 D" in report.export_text and "0.4500 B" in report.export_text
    for e in report.entries:
        assert e.text in report.export_text and e.entry_id in report.export_text
        assert all(ref in report.export_text for ref in e.evidence_refs)
    assert all(l in report.export_text for l in report.limitations)
    assert "RULE EVALUATION LEDGER" in report.export_text
    assert report.stage_inspection.movement_binding == "NO_STAGE_MOVEMENT_BINDING"
    assert "NO_STAGE_MOVEMENT_BINDING" in report.export_text
    assert before == {p.name: p.read_bytes() for p in ROOT.iterdir() if p.is_file()}


@pytest.mark.parametrize("scope", ["UNKNOWN", "TOTAL", "INCREMENTAL"])
@pytest.mark.parametrize("source", ["Unknown", "ClinCheck", "SureSmile"])
def test_normal_input_has_no_anatomy_stages_sequence_or_anchorage_even_with_claims(monkeypatch, scope, source):
    enable(monkeypatch)
    body = {"raw_text": "# SYNTHETIC\nTooth\tRotation (deg)\n13\t999.000 M\n14\t-\n", "synthetic_data_confirmed": True,
            "source_claim": source, "context": {"scope": scope, "stage_index": 3 if scope == "INCREMENTAL" else None}}
    response = client.post(NORMAL, json=body)
    assert response.status_code == 200
    report = SequencingDraft.model_validate_json(response.content)
    assert report.evidence_domain == "UNVERIFIED" and report.stage_inspection.status == "MISSING"
    assert not report.stage_inspection.records and not report.fictional_arches and not report.fictional_segments
    assert all(e.result_type in {"UNKNOWN", "WITHHELD", "DISABLED"} and not e.stage_window and not e.synthetic_arch_id for e in report.entries)
    assert report.engine_review.coverage.eligible_positions == 0
    for side in ("RIGHT", "LEFT"):
        note = next(e for e in report.entries if e.section == f"{side}_ANCHORAGE")
        assert note.result_type == "UNKNOWN" and "unknown" in note.text
    g15 = next(e for e in report.engine_review.evaluations if e.rule_id == "G15")
    assert g15.status == ("CONTEXT_REQUIRED" if scope == "INCREMENTAL" else "NOT_APPLICABLE")


@pytest.mark.parametrize("raw", ["SYNTHETIC UnknownVendor", "Tooth\tRotation (deg)\n13\t0.000 M\n", "Tooth\tRotation (deg)\n13\t-\n"])
def test_missing_zero_and_unknown_layout_preserved_without_schedule(raw):
    report = client.post(NORMAL, json={"raw_text": raw, "synthetic_data_confirmed": True}).json()
    assert report["parsed"]["raw_text"] == raw
    assert report["stage_inspection"]["status"] == "MISSING"
    assert all(e["result_type"] != "SUPPLIED_SYNTHETIC" for e in report["entries"])
    if "0.000" in raw:
        assert report["parsed"]["measurements"][0]["numeric_status"] == "EXPLICIT_ZERO" and "0.000 M" in report["export_text"]
    elif "\t-" in raw:
        assert report["parsed"]["measurements"][0]["numeric_status"] == "MISSING"


def render_scenario(scenario):
    submission, checked = fixed_input()
    context = TestRuleContext(input_digest=input_digest(submission), stages=scenario.stages)
    review = review_table(submission, checked=checked, test_only=True, test_context=context,
        requested_assessments=("COLLISIONS", "COMPLEX_INTERVENTION"))
    return assemble(resolve(submission), review, scenario=scenario, evidence_ref="FINOVA-NANO-1:independent-test-fixture")


@pytest.mark.parametrize("change", ["order", "duplicate-id", "duplicate-index", "zero-kind", "missing-window", "wrong-window-arch", "reverse-window", "no-records"])
def test_inconsistent_or_missing_stages_withhold_only_dependent_notes_and_do_not_sum_totals(change):
    scenario, _ = fixed_scenario()
    stages, statements = list(scenario.stages), list(scenario.statements)
    if change == "order": stages[1], stages[2] = stages[2], stages[1]
    if change == "duplicate-id": stages[1] = stages[1].model_copy(update={"stage_id": stages[0].stage_id})
    if change == "duplicate-index": stages[1] = stages[1].model_copy(update={"index": 0})
    if change == "zero-kind": stages[0] = stages[0].model_copy(update={"kind": "ACTIVE"})
    if change == "missing-window": statements[0] = statements[0].model_copy(update={"stage_window": StageWindow(start_id="MISSING", end_id="DEMO_U_B_RECORD")})
    if change == "wrong-window-arch": statements[0] = statements[0].model_copy(update={"stage_window": StageWindow(start_id="DEMO_L_BASE", end_id="DEMO_U_B_RECORD")})
    if change == "reverse-window": statements[0] = statements[0].model_copy(update={"stage_window": StageWindow(start_id="DEMO_U_B_RECORD", end_id="DEMO_U_BASE")})
    if change == "no-records": stages = []
    report = render_scenario(scenario.model_copy(update={"stages": tuple(stages), "statements": tuple(statements)}))
    assert report.stage_inspection.status == ("MISSING" if change == "no-records" else "INVALID")
    assert all(not e.stage_window and not e.stage_kinds for e in report.entries)
    assert all(e.result_type == "WITHHELD" for e in report.entries if e.section in {"UPPER_ARCH", "LOWER_ARCH"})
    assert all(e.result_type == "SUPPLIED_SYNTHETIC" for e in report.entries if e.section.endswith("_ANCHORAGE"))
    assert report.engine_review.coverage.eligible_positions == 4  # TOTAL observations are independent of the extra stage dataset.
    if change in {"order", "duplicate-id", "duplicate-index", "zero-kind"}:
        assert next(e for e in report.engine_review.evaluations if e.rule_id == "G15").status == "PARSE_INVALID"


@pytest.mark.parametrize("change", ["side", "policy", "verified", "original-token", "missing-section", "window", "scope", "arch", "segment-side"])
def test_report_contract_rejects_promoted_or_misbound_output(change):
    body = json.loads(draft_demo().model_dump_json())
    if change == "side": next(e for e in body["entries"] if e["section"] == "RIGHT_ANCHORAGE")["side"] = "LEFT"
    if change == "policy": body["entries"][0]["policy_id"] = "APPROVED"
    if change == "verified": body["entries"][0]["result_type"] = "VERIFIED_OBSERVATION"
    if change == "original-token": body["entries"][0]["original_tooth_tokens"][0] = "99"
    if change == "missing-section": body["entries"] = [e for e in body["entries"] if e["section"] != "LEFT_ANCHORAGE"]
    if change == "window": body["entries"][0]["stage_window"]["end_id"] = "NONEXISTENT"
    if change == "scope": body["entries"][0]["movement_scope"] = "INCREMENTAL"
    if change == "arch": body["entries"][0]["synthetic_arch_id"] = "DEMO_LOWER"
    if change == "segment-side": body["entries"][2]["synthetic_segment_id"] = "DEMO_U_B"
    with pytest.raises(ValidationError): SequencingDraft.model_validate_json(json.dumps(body))


def test_identical_fixed_text_through_normal_route_stays_unverified(monkeypatch):
    enable(monkeypatch)
    submission, _ = fixed_input()
    result = client.post(NORMAL, json=submission.model_dump(mode="json")).json()
    assert result["evidence_domain"] == "UNVERIFIED" and all(e["origin"] == "ENGINE_GUARD" for e in result["entries"])


def test_corrupted_scenario_is_sanitized_and_input_binding_cannot_be_changed(monkeypatch, tmp_path):
    enable(monkeypatch)
    scenario, _ = fixed_scenario()
    (tmp_path / "scenario.json").write_bytes((ROOT / "scenario.json").read_bytes() + b" ")
    (tmp_path / "scenario.sha256").write_bytes((ROOT / "scenario.sha256").read_bytes())
    monkeypatch.setattr("app.sequencing.demo.ROOT", tmp_path)
    response = client.post(DEMO, json={})
    assert response.status_code == 503 and "scenario.json" not in response.text
    with pytest.raises(ValueError, match="MISMATCH"):
        render_scenario(scenario.model_copy(update={"input_sha256": "0" * 64}))


def test_schema_files_and_invalid_stage_kind():
    root = Path(__file__).parents[2] / "schemas"
    for name, model, mode in (("sequencing-draft.v1.json", SequencingDraft, "serialization"), ("sequencing-request.v1.json", SequencingSubmission, "validation"),
        ("sequencing-demo-input.v1.json", SequencingDemoInput, "serialization"), ("sequencing-demo-request.v1.json", EmptyDemoRequest, "validation")):
        assert json.loads((root / name).read_text(encoding="utf-8")) == model.model_json_schema(mode=mode)
    with pytest.raises(ValidationError): StageRecord(stage_id="DEMO", index=0, arch="DEMO", kind="UNKNOWN", evidence_ref="TEST_ONLY")


def test_recovery_receipt_rechecked():
    assert client.post(NORMAL, json={"raw_text": "SYNTHETIC", "synthetic_data_confirmed": True, "recovery_receipt": "FORGED"}).status_code == 409
