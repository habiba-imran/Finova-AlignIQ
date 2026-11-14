"""Public figure-derived offline tests; no vendor or clinical authority is supplied."""
import hashlib
import socket

import pytest

from app.domain.models import LexicalInput
from app.parser.service import parse_table
from app.reports.groq_client import GroqClient
from app.semantics.registry import APPROVED_RELEASE_DIGESTS
from scripts.evaluate_public_tmt import CSV, REFERENCE, check_table, evaluate, load, render


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def refuse(*_args, **_kwargs):
        pytest.fail("Published-reference evaluation attempted a provider/network call")
    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(GroqClient, "generate", refuse)


@pytest.mark.parametrize("index,count", [(0, 112), (1, 42), (2, 42)])
@pytest.mark.parametrize("transpose", [False, True])
def test_original_csv_cells_exact_with_independent_spans_and_no_semantic_promotion(index, count, transpose):
    rows, tables = load()
    table = tables[index]
    selected = [r for r in rows if (r["source"], r["source_figure"]) == (table["source"], table["figure"])]
    result, _ = check_table(table, selected, transpose=transpose)
    assert result["source_cells"] == result["parsed_exact"] == count
    assert result["tooth_order"] == table["teeth"]
    assert result["orientation"] == ("TEETH_IN_ROWS" if transpose else "TEETH_IN_COLUMNS")
    assert result["missing_or_unrecognized_positions"] == result["incorrect_associations_or_values"] == result["extra_positions"] == 0
    assert result["semantic_status"] == "DISABLED" and result["semantically_ready"] == 0
    assert result["label_unsupported_positions"] == (64 if index == 0 else 24)
    assert not APPROVED_RELEASE_DIGESTS


def test_known_transcription_conflict_is_preserved_with_a_separate_source_correction():
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (CSV, REFERENCE / "FINOVA_Public_TMT_Verification_Pack.pdf")}
    result = evaluate()
    assert (result["reviewed_cells"], result["confirmed_csv_cells"], result["conflicting_csv_cells"]) == (196, 195, 1)
    supplied = next(c for c in result["primary_as_supplied"][0]["cells"] if c["csv_line"] == 94)
    corrected = next(c for c in result["explicit_source_correction_overlay"][0]["cells"] if c["csv_line"] == 94)
    assert supplied["tooth"] == "25" and supplied["csv_label"] == "Angulation (deg)"
    assert supplied["csv_value"] == supplied["evaluated_value"] == "24D"
    assert supplied["figure_value_compact"] == corrected["evaluated_value"] == "2.4D"
    assert supplied["lexical_exact"] and corrected["lexical_exact"]
    assert before == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (CSV, REFERENCE / "FINOVA_Public_TMT_Verification_Pack.pdf")}


def test_two_phases_are_separate_excerpts_and_cannot_silently_merge():
    rows, tables = load()
    a = [r for r in rows if r["source_figure"] == "Figure 4a"]
    b = [r for r in rows if r["source_figure"] == "Figure 4b"]
    ra, _ = check_table(tables[1], a)
    rb, _ = check_table(tables[2], b)
    assert ra["input_sha256"] != rb["input_sha256"]
    assert ra["cells"][0]["csv_value"] == "0" and rb["cells"][0]["csv_value"] == "0.5E"
    both = render(tables[1], a) + render(tables[2], b)
    parsed = parse_table(LexicalInput(raw_text=both))
    assert not parsed.measurements and any(i.code == "AMBIGUOUS_LAYOUT" for i in parsed.issues)


def test_numeric_ambiguity_in_a_separate_mutation_is_withheld_without_source_guessing():
    raw = "Movement\tA\tB\nRotation (deg)\t1.2Q\t1e3\n"
    parsed = parse_table(LexicalInput(raw_text=raw))
    assert len(parsed.measurements) == 2
    assert all(m.numeric_status == "AMBIGUOUS" and m.signed_decimal is None for m in parsed.measurements)


def test_reference_scope_is_not_mislabeled_synthetic_or_admitted_as_a_vendor_fixture():
    result = evaluate()
    assert "synthetic_data_confirmed" not in LexicalInput.model_fields
    assert result["provider_calls"] == result["approved_vendor_releases"] == 0
    assert sum(t["numeric_statuses"].get("MISSING", 0) for t in result["primary_as_supplied"]) == 14
    assert sum(t["numeric_statuses"].get("EXPLICIT_ZERO", 0) for t in result["primary_as_supplied"]) == 8
