import json
import pytest

from app.interactive.models import ReviewDetails
from app.interactive.service import generate_interactive
from app.reports.settings import ReportSettings
from test_interactive import ROWS, submission, provider


def test_three_modules_have_distinct_content_and_identical_source_values():
    reports = {module: generate_interactive(submission(module=module), settings=ReportSettings()) for module in ("macro", "micro", "nano")}
    assert reports["macro"].sections == []
    assert [section.section_id for section in reports["micro"].sections] == ["ATTACHMENT_RECORDS", "ATTACHMENT_DESIGN", "ATTACHMENT_PLACEMENT", "ATTACHMENT_LIMITS"]
    assert [section.section_id for section in reports["nano"].sections] == ["STAGE_RECORDS", "STAGE_ALLOCATIONS", "ANCHORAGE_RECORDS", "SEQUENCING_LIMITS"]
    assert all(any(section.status == "SOURCE_REPORTED" for section in reports[module].sections) for module in ("micro", "nano"))
    assert all(reports[module].sections[-1].status == "UNAVAILABLE" for module in ("micro", "nano"))
    for report in reports.values():
        assert report.parsed.measurements == reports["macro"].parsed.measurements
        assert len(report.engine_review.evaluations) == 96 and report.clinical_analysis_enabled is False
        assert not report.illustrations
        assert "Illustrative" not in report.export_text and "fictional demonstration group" not in report.export_text
    assert "-2.7500" in reports["micro"].sections[0].text
    assert "1.2300" in reports["nano"].sections[1].text
    assert "0.1250" in reports["nano"].sections[2].text
    assert all(not section.missing_fields for module in ("micro", "nano") for section in reports[module].sections)


def test_supplied_attachment_details_remain_unverified_and_never_reach_groq_as_free_text():
    base = generate_interactive(submission(), settings=ReportSettings())
    detail = dict(tooth_ref=base.parsed.teeth[0].id, choice="ATTACHMENT", design="PRIVATE_DESIGN <script>", width_mm="1.2300", height_mm="0.00", surface="PRIVATE_SURFACE", orientation="PRIVATE_ORIENTATION")
    settings, client, captured = provider()
    report = generate_interactive(submission(module="micro", review_details=ReviewDetails(attachments=[detail])), settings=settings, client=client)
    assert report.generation.used_mode == "GROQ_AI" and report.generation.accepted_comments == 4
    assert report.sections[0].status == report.sections[1].status == "SUPPLIED_UNVERIFIED"
    assert "1.2300 mm" in report.sections[1].text and "0.00 mm" in report.sections[1].text
    assert "depth unknown" in report.sections[1].text
    assert report.sections[-1].status == "UNAVAILABLE"
    assert report.review_details.attachments[0].design == detail["design"]
    payload = json.dumps(captured)
    assert "PRIVATE_" not in payload and "<script>" not in payload and "1.2300" not in payload
    assert "SUPPLIED_UNVERIFIED" in payload


def test_stage_amounts_are_supplied_separately_from_totals_and_notes_are_not_cloud_payloads():
    source = generate_interactive(submission(), settings=ReportSettings()).parsed
    movement = next(m for m in source.measurements if m.unit == "mm")
    details = ReviewDetails(stages=[dict(stage_id="PRIVATE_STAGE", order=3, duration_days=8)],
        allocations=[dict(stage_id="PRIVATE_STAGE", tooth_ref=movement.tooth_ref, measurement_ref=movement.id, amount="0.1250", unit="mm")],
        anchorage_notes=[dict(tooth_ref=movement.tooth_ref, note="PRIVATE_NOTE - supplied only")])
    settings, client, captured = provider()
    report = generate_interactive(submission(module="nano", review_details=details), settings=settings, client=client)
    assert report.generation.used_mode == "GROQ_AI"
    assert "0.1250 mm" in report.sections[1].text
    assert "reported order 3" in report.sections[0].text and "8 days" in report.sections[0].text
    assert "PRIVATE_NOTE" in report.sections[2].text and "not an independently assessed" in report.sections[2].text
    assert "PRIVATE_" not in json.dumps(captured)
    assert report.sections[-1].status == "UNAVAILABLE"
    assert report.engine_review.evidence_domain == "UNVERIFIED"


def test_stage_reference_without_amount_does_not_copy_source_total_or_assume_zero():
    parsed = generate_interactive(submission(), settings=ReportSettings()).parsed
    m = parsed.measurements[0]
    details = ReviewDetails(stages=[dict(stage_id="A", order=1)], allocations=[dict(stage_id="A", tooth_ref=m.tooth_ref, measurement_ref=m.id)])
    report = generate_interactive(submission(module="nano", review_details=details), settings=ReportSettings())
    assert "stage amount unknown" in report.sections[1].text
    assert "-2.7500" not in report.sections[1].text
    assert report.sections[1].missing_fields


def test_unverified_context_stage_index_is_reported_without_creating_a_schedule():
    from app.domain.models import SourceContext
    report = generate_interactive(submission(module="nano", context=SourceContext(stage_index=5)), settings=ReportSettings())
    assert "source-context stage index of 5" in report.sections[0].text
    assert report.sections[0].status == "SOURCE_REPORTED"
    assert not report.sections[0].missing_fields and not report.review_details.stages
    assert report.sections[1].status == "SOURCE_REPORTED"


def test_contract_capabilities_require_no_provider_call_or_development_gate(monkeypatch):
    from fastapi.testclient import TestClient
    from app.main import app
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    response = TestClient(app).get('/api/v1/interactive/capabilities')
    assert response.status_code == 200
    assert response.json()["report_format"] == "MODULE_SPECIFIC_V1"
    assert response.json()["clinical_analysis_enabled"] is False


@pytest.mark.parametrize("change,code", [("tooth", "ATTACHMENT_REFERENCE_INVALID"), ("duplicate_attachment", "ATTACHMENT_REFERENCE_INVALID"), ("choice", "ATTACHMENT_CHOICE_CONFLICT"), ("stage", "STAGE_REFERENCE_INVALID"), ("allocation", "ALLOCATION_REFERENCE_INVALID"), ("unit", "ALLOCATION_UNIT_INVALID"), ("anchor", "ANCHORAGE_REFERENCE_INVALID"), ("module", "DETAILS_MODULE_MISMATCH")])
def test_supplied_detail_reference_and_scope_failures_are_not_silently_interpreted(change, code):
    parsed = generate_interactive(submission(), settings=ReportSettings()).parsed
    m = parsed.measurements[0]
    details, module = {}, "nano"
    if change in {"tooth", "duplicate_attachment", "choice", "module"}:
        module = "micro"
        rows = [dict(tooth_ref="missing" if change == "tooth" else m.tooth_ref, choice="UNKNOWN")]
        if change == "duplicate_attachment": rows += rows
        if change == "choice": rows[0]["design"] = "a design with no supplied attachment choice"
        details["attachments"] = rows
        if change == "module": module = "macro"
    if change == "stage": details["stages"] = [dict(stage_id="A", order=1), dict(stage_id="A", order=2)]
    if change in {"allocation", "unit"}:
        details.update(stages=[dict(stage_id="A", order=1)], allocations=[dict(stage_id="B" if change == "allocation" else "A", tooth_ref=m.tooth_ref, measurement_ref=m.id, amount="0.5", unit="mm")])
    if change == "anchor": details["anchorage_notes"] = [dict(tooth_ref="missing", note="supplied note")]
    with pytest.raises(ValueError, match=code):
        generate_interactive(submission(module=module, review_details=ReviewDetails(**details)), settings=ReportSettings())
