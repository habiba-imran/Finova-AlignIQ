"""Independent expectations for the archived benchmark and ordinary synthetic inputs."""
import json
import logging
from pathlib import Path

import httpx
import pytest

from app.interactive.analytical_wording import validate_analytical
from app.interactive.analysis import analyze
from app.interactive.service import generate_interactive
from app.parser.receipts import resolve
from app.reports.groq_client import GroqClient
from app.reports.settings import ReportSettings
from test_interactive import submission, ROWS, COLUMNS, MARKDOWN

RAW = (Path(__file__).parent / "fixtures/analysis_15_tooth.md").read_text(encoding="utf-8")


def mock_provider(status=200, mutate=None):
    settings = ReportSettings(api_key="PRIVATE_TEST_KEY", synthetic_transmission_enabled=True)
    calls = []
    def handle(request):
        calls.append(json.loads(request.content))
        data = json.loads(calls[-1]["messages"][1]["content"])
        answer = {"sections": [{"section_id": s["section_id"], "text": "\n\n".join("{"+f["ref"]+"}" for f in s["findings"])} for s in data["sections"]]}
        if mutate:
            mutate(answer)
        return httpx.Response(status, json={"model": settings.model, "choices": [{"finish_reason": "stop", "message": {"role": "assistant", "content": json.dumps(answer)}}]})
    return settings, GroqClient(settings, transport=httpx.MockTransport(handle)), calls


@pytest.mark.parametrize("module", ["macro", "micro", "nano"])
def test_benchmark_exact_parser_and_complete_provenance(module):
    request = submission(RAW, module)
    original = resolve(request)
    report = generate_interactive(request, settings=ReportSettings())
    assert len(original.teeth) == 15 and len(original.measurements) == 105
    assert sum(m.numeric_status in {"PARSED", "EXPLICIT_ZERO"} for m in original.measurements) == 103
    assert sum(m.numeric_status in {"MISSING", "NOT_PRESENT"} for m in original.measurements) == 2
    assert not any(m.numeric_status in {"INVALID", "AMBIGUOUS"} for m in original.measurements)
    assert report.parsed == original
    assert "Successfully parsed with 2 missing values" in report.limitations[0]
    for m in original.measurements:
        assert m.span and RAW[m.span.start:m.span.end] == m.raw_value
        assert m.id in report.export_text
    assert len(report.engine_review.evaluations) == 96
    assert sum(e.execution == "DISABLED" for e in report.engine_review.evaluations) == 27
    assert not report.clinical_analysis_enabled
    for s in report.sections:
        assert s.text and s.text in report.export_text
    assert "ANALYTICAL FINDING PROVENANCE" in report.export_text
    assert report.export_text.count("SOURCE AND PROVENANCE") == 1


def test_macro_dimension_comparisons_and_no_source_inventory():
    r = generate_interactive(submission(RAW), settings=ReportSettings())
    assert len(r.sections) == 5
    text = "\n".join(s.text for s in r.sections)
    for phrase in ["Tooth 13: largest recorded mesiodistal translation magnitude, 3.30 mm (D-labelled)",
                   "Teeth 11, 21: largest recorded buccolingual translation magnitude, 2.50 mm",
                   "Teeth 11, 21, 22: largest recorded vertical movement magnitude, 2.20 mm (I-labelled)",
                   "Tooth 11: largest recorded rotation magnitude, 18.90°",
                   "Tooth 11: largest recorded angulation magnitude, 28.80°", "D: 13; M: 1; unlabelled: 1", "Tooth 18: vertical movement unavailable"]:
        assert phrase in text
    assert "Original cell" not in text and "original tooth token" not in text
    maximum = next(f for f in r.analytical_findings if f.kind == "MAXIMUM")
    assert len(maximum.source_refs) == 15 and len(maximum.selected_refs) == 1


def test_micro_prioritizes_11_with_evidence_based_demo_candidates():
    r = generate_interactive(submission(RAW, "micro"), settings=ReportSettings())
    assert r.sections[0].text.startswith("Tooth 11:")
    assert "18.90°" in r.sections[0].text and "28.80°" in r.sections[0].text
    kinds = {f.kind for f in r.analytical_findings if f.origin == "SIMULATED_DEMO"}
    assert {"CANDIDATE", "ALTERNATIVE", "NO_CANDIDATE"} <= kinds
    assert "Tooth 18 — no candidate" in r.sections[1].text
    assert "rectangular" not in r.sections[1].text and "oval" not in r.sections[1].text
    assert r.sections[1].status == "SIMULATED_DEMO"
    lines = RAW.splitlines()
    reverse = "\n".join(lines[:4] + list(reversed([line for line in lines[4:] if line.strip()])))
    other = generate_interactive(submission(reverse, "micro"), settings=ReportSettings())
    assert [s.text for s in r.sections] == [s.text for s in other.sections]


def test_nano_groups_translations_vertical_and_multiple_components_without_schedule():
    r = generate_interactive(submission(RAW, "nano"), settings=ReportSettings())
    text = "\n".join(s.text for s in r.sections)
    assert "Upper-arch anterior: 6" in text and "Upper-arch posterior: 9" in text
    assert "Lower-arch" not in text
    assert "Teeth 12, 13, 14, 15, 16, 17" in text and "3.10–3.30 mm" in text
    assert "Teeth 11, 21, 22" in text and "2.20 mm (I-labelled)" in text
    assert "Tooth 11:" in r.sections[3].text
    assert "not a calculated movement sequence or treatment schedule" in text
    assert not any(word in text for word in ["days", "weeks", "stages required", "cN"])


@pytest.mark.parametrize("raw", [ROWS, COLUMNS, MARKDOWN, "Tooth\tRotation (deg)\tVertical (mm)\n11\t2.500 D\t\n12\t0\t—", RAW.replace('| 17 |', '|    17    |')])
@pytest.mark.parametrize("module", ["macro", "micro", "nano"])
def test_supported_ordinary_inputs_remain_analytical(raw, module):
    r = generate_interactive(submission(raw, module), settings=ReportSettings())
    assert r.sections and r.analytical_findings
    assert r.parsed == resolve(submission(raw, module))
    assert r.generation.used_mode == "STANDARD_TEMPLATES"


@pytest.mark.parametrize("module", ["macro", "micro", "nano"])
def test_actual_http_client_mock_automatic_single_call_and_safe_diagnostics(module, caplog, monkeypatch):
    settings, client, calls = mock_provider()
    monkeypatch.setenv("GROQ_API_KEY", "PRIVATE_TEST_KEY")
    monkeypatch.setattr("app.interactive.analytical_wording.GroqClient", lambda config: client)
    with caplog.at_level(logging.INFO, logger="finova.analysis"):
        r = generate_interactive(submission("Patient: PRIVATE_PERSON\n"+RAW, module))
    assert r.generation.used_mode == "GROQ_AI" and r.generation.attempts == len(calls) == 1
    payload = json.dumps(calls)
    assert "3.30" in payload and "18.90" in payload and "selected" in payload and "comparison_sets" in payload
    assert not any(x in payload for x in ["PRIVATE_PERSON", "PRIVATE_TEST_KEY", "Patient:", "raw_text", "raw_identifier"])
    assert "analysis_ai_requested" in caplog.text and "contacted=True" in caplog.text and "fallback=False" in caplog.text
    assert "PRIVATE" not in caplog.text and "18.90" not in caplog.text
    assert len(json.dumps(calls[0]["messages"]).encode()) < 24000


@pytest.mark.parametrize("mutation", ["value", "omit", "duplicate", "cross_section", "unknown", "clinical", "geometry"])
def test_provider_mutations_reject_once_keep_complete_analysis(mutation, caplog):
    def change(answer):
        first = answer["sections"][0]
        if mutation == "value": first["text"] += " 999.00 mm"
        if mutation == "omit": first["text"] = ""
        if mutation == "duplicate": first["text"] += "{F0001}"
        if mutation == "cross_section": first["text"] = answer["sections"][1]["text"]
        if mutation == "unknown": first["section_id"] = "INVENTED"
        if mutation == "clinical": first["text"] += " Safe movement."
        if mutation == "geometry": first["text"] += " Rectangular 2 mm attachment."
    settings, client, calls = mock_provider(mutate=change)
    r = generate_interactive(submission(RAW), settings=settings, client=client)
    assert r.generation.used_mode == "STANDARD_TEMPLATES" and r.generation.reason == "GROQ_UNSUPPORTED_WORDING"
    assert len(calls) == 1
    baseline, _ = analyze(r.parsed, "macro")
    assert r.sections == baseline


@pytest.mark.parametrize("status", [401, 429, 503])
def test_provider_errors_do_not_retry_or_mislabel(status):
    settings, client, calls = mock_provider(status=status)
    r = generate_interactive(submission(RAW), settings=settings, client=client)
    assert len(calls) == r.generation.attempts == 1
    assert r.generation.used_mode == "STANDARD_TEMPLATES" and r.generation.accepted_comments == 0


def test_incomplete_units_ambiguous_directions_duplicates_and_alternative_numbering():
    raw = "Tooth\tRotation (deg)\tTranslation M / D (mm)\n11\t—\t3.300 X\n12\t0\t1.20 D\n13\t0\t—"
    r = generate_interactive(submission(raw, "micro"), settings=ReportSettings())
    assert not any(f.kind == "NO_CANDIDATE" for f in r.analytical_findings)
    assert "unknown" in "\n".join(s.text.lower() for s in r.sections)
    raw = "Tooth\tRotation\tRotation\n11\t4\t8"
    r = generate_interactive(submission(raw), settings=ReportSettings())
    assert not any(f.kind == "MAXIMUM" for f in r.analytical_findings)
