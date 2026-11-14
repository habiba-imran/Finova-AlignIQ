"""Offline published-reference evaluation, not vendor compatibility or clinical review.

Uses the existing LexicalInput/library parser without falsely confirming that
published research values are synthetic. No HTTP, cloud, review engine, fixture
admission or production registry update is involved. Inputs are never modified.
"""
import argparse
from collections import Counter
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.domain.models import LexicalInput  # noqa: E402
from app.parser.service import parse_table  # noqa: E402
from app.semantics.normalization import assess_semantics  # noqa: E402
from app.semantics.registry import APPROVED_RELEASE_DIGESTS  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "references/public_tmt"
CSV = REFERENCE / "FINOVA_Published_TMT_Values_Reference.csv"
REVIEW = REFERENCE / "transcription_review.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load():
    with CSV.open(encoding="utf-8-sig", newline="") as stream:
        rows = [{**r, "csv_line": i} for i, r in enumerate(csv.DictReader(stream), 2)]
    tables = json.loads(REVIEW.read_text(encoding="utf-8"))["tables"]
    keys = [(r["source"], r["source_figure"], r["excerpt"], r["movement"], r["tooth_id"]) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("DUPLICATE_REFERENCE_CELL")
    if any(r["not_clipboard_export"] != "TRUE" for r in rows):
        raise ValueError("REFERENCE_SCOPE_CHANGED")
    expected = {(t["source"], t["figure"], t["excerpt"], row["csv_label"], tooth)
                for t in tables for row in t["rows"] for tooth in t["teeth"]}
    if set(keys) != expected:
        raise ValueError("REFERENCE_COVERAGE_CHANGED")
    return rows, tables


def render(table, rows, *, transpose=False, corrected=False):
    """Supported generic TSV, retaining the supplied labels/tokens; no alias invention."""
    indexed = {(r["movement"], r["tooth_id"]): r["displayed_value"] for r in rows}
    if corrected:
        indexed = {(r["csv_label"], tooth): value for r in table["rows"]
                   for tooth, value in zip(table["teeth"], r["values"].split(), strict=True)}
    labels = [r["csv_label"] for r in table["rows"]]
    lines = ["# RE-TYPESET PUBLIC REFERENCE; NOT ORIGINAL CLIPBOARD; OFFLINE LEXICAL EVALUATION ONLY",
             f"# {table['source']} / {table['figure']} / {table['excerpt']}",
             f"# Attribution: {table['article_url']}; {table['license']} {table['license_url']}",
             "# " + ("Source-reviewed correction overlay applied; original CSV unchanged." if corrected else "As supplied in CSV; known transcription conflict retained, not silently corrected.")]
    if transpose:
        lines.append("\t".join(["Tooth", *labels]))
        lines.extend("\t".join([tooth, *(indexed[label, tooth] for label in labels)]) for tooth in table["teeth"])
    else:
        lines.append("\t".join(["Movement", *table["teeth"]]))
        lines.extend("\t".join([label, *(indexed[label, tooth] for tooth in table["teeth"])]) for label in labels)
    return "\n".join(lines) + "\n"


def check_table(table, rows, *, transpose=False, corrected=False):
    raw = render(table, rows, transpose=transpose, corrected=corrected)
    parsed = parse_table(LexicalInput(raw_text=raw))
    semantics = assess_semantics(parsed)
    teeth = {t.id: t for t in parsed.teeth}
    actual = {}
    for m in parsed.measurements:
        key = (m.raw_label, teeth[m.tooth_ref].token)
        if key in actual:
            raise ValueError("DUPLICATE_PARSED_ASSOCIATION")
        actual[key] = m
    original = {(r["movement"], r["tooth_id"]): r for r in rows}
    source_lines = raw.splitlines(keepends=True)

    def expected_span(line, column):
        # Independent coordinates in the deliberately authored TSV, not parser output.
        fields = source_lines[line].rstrip("\n").split("\t")
        start = sum(map(len, source_lines[:line])) + sum(len(v) + 1 for v in fields[:column])
        return start, start + len(fields[column])

    results = []
    for row_index, row in enumerate(table["rows"], 1):
        gold = row["values"].split()
        if len(gold) != len(table["teeth"]):
            raise ValueError("REVIEW_ROW_WIDTH_INVALID")
        for column, (tooth, figure_value) in enumerate(zip(table["teeth"], gold, strict=True), 1):
            source = original[row["csv_label"], tooth]
            value = figure_value if corrected else source["displayed_value"]
            m = actual.get((row["csv_label"], tooth))
            line, cell_column = (4 + column, row_index) if transpose else (4 + row_index, column)
            value_span = expected_span(line, cell_column)
            label_span = expected_span(4, row_index) if transpose else expected_span(line, 0)
            tooth_span = expected_span(line, 0) if transpose else expected_span(4, column)
            number = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)([A-Z]?)", value)
            expected_status = "MISSING" if value == "-" else "EXPLICIT_ZERO" if number and Decimal(number[1]).is_zero() else "PARSED"
            exact = bool(m and m.raw_value == value and m.numeric_status == expected_status
                and m.header_unit == ("mm" if row["csv_label"].endswith("(mm)") else "deg")
                and m.span and raw[m.span.start:m.span.end] == value
                and (m.span.start, m.span.end) == value_span
                and (m.header_span.start, m.header_span.end) == label_span
                and (teeth[m.tooth_ref].span.start, teeth[m.tooth_ref].span.end) == tooth_span
                and raw[m.header_span.start:m.header_span.end] == row["csv_label"]
                and raw[teeth[m.tooth_ref].span.start:teeth[m.tooth_ref].span.end] == tooth)
            if value == "-":
                exact = exact and m.signed_decimal is None and m.missing_kind == "DASH"
            elif number:
                exact = exact and m.raw_number == number[1] and str(m.signed_decimal) == number[1] and m.raw_direction == (number[2] or None)
            else:
                exact = False
            results.append({"csv_line": source["csv_line"], "figure": table["figure"], "excerpt": table["excerpt"],
                "figure_row": row_index, "figure_column": column, "tooth": tooth,
                "csv_label": row["csv_label"], "figure_label": row["figure_label"],
                "csv_value": source["displayed_value"], "figure_value_compact": figure_value,
                "transcription_status": "AGREES" if source["displayed_value"] == figure_value else "CONFLICT",
                "evaluated_value": value, "lexical_exact": exact, "numeric_status": m.numeric_status if m else None,
                "label_supported": bool(m and m.recognized_label), "field_status": m.field_status if m else None,
                "expected_retypeset_span": list(value_span),
                "parser_span": m.span.model_dump() if m and m.span else None})
    summary = {"id": table["id"], "figure": table["figure"], "excerpt": table["excerpt"],
        "orientation": parsed.layout.orientation, "tooth_order": [t.token for t in parsed.teeth],
        "source_cells": len(results), "independently_reviewed_cells": len(results),
        "transcription_agrees": sum(r["transcription_status"] == "AGREES" for r in results),
        "transcription_conflicts": sum(r["transcription_status"] == "CONFLICT" for r in results),
        "parsed_exact": sum(r["lexical_exact"] for r in results),
        "missing_or_unrecognized_positions": sum((r["csv_label"], r["tooth"]) not in actual for r in results),
        "incorrect_associations_or_values": sum(not r["lexical_exact"] and (r["csv_label"], r["tooth"]) in actual for r in results),
        "extra_positions": len(actual.keys() - original.keys()),
        "numeric_statuses": dict(Counter(r["numeric_status"] for r in results)),
        "label_supported_positions": sum(r["label_supported"] for r in results),
        "label_unsupported_positions": sum(not r["label_supported"] for r in results),
        "field_statuses": dict(Counter(r["field_status"] for r in results)),
        "ambiguous_values_in_original_corpus": 0, "correctly_withheld_ambiguous_values": 0,
        "semantic_status": semantics.status,
        "semantically_ready": sum(m.canonical_measurement_ready or m.evidence_complete_for_test for m in semantics.measurements),
        "input_sha256": parsed.raw_sha256, "cells": results}
    return summary, raw


def evaluate(*, write_fixtures=False):
    rows, tables = load()
    primary, transposed, corrected = [], [], []
    for table in tables:
        selected = [r for r in rows if (r["source"], r["source_figure"], r["excerpt"]) == (table["source"], table["figure"], table["excerpt"])]
        for target, transpose, overlay in ((primary, False, False), (transposed, True, False), (corrected, False, True)):
            result, raw = check_table(table, selected, transpose=transpose, corrected=overlay)
            target.append(result)
            if write_fixtures:
                directory = REFERENCE / "retypeset"
                directory.mkdir(exist_ok=True)
                suffix = "corrected" if overlay else "rows" if transpose else "as-supplied"
                (directory / f"{table['id']}-{suffix}.tsv").write_text(raw, encoding="utf-8")
    assert not APPROVED_RELEASE_DIGESTS, "Vendor registry changed; re-review reference evaluation boundary"
    return {"scope": "OFFLINE_RE_TYPESET_REFERENCE_ONLY_NOT_VENDOR_COMPATIBILITY",
        "input_hashes": {p.name: sha(p) for p in (CSV, REVIEW, REFERENCE / "FINOVA_Public_TMT_Verification_Pack.pdf")},
        "review_basis": "Agent visual comparison against publisher-hosted figures; no dual-human clinical review",
        "reviewed_cells": sum(t["independently_reviewed_cells"] for t in primary),
        "confirmed_csv_cells": sum(t["transcription_agrees"] for t in primary),
        "conflicting_csv_cells": sum(t["transcription_conflicts"] for t in primary),
        "primary_source_cells": len(rows), "primary_parsed_exact": sum(t["parsed_exact"] for t in primary),
        "primary_numeric_cells": sum(sum(v for k, v in t["numeric_statuses"].items() if k in {"PARSED", "EXPLICIT_ZERO"}) for t in primary),
        "approved_vendor_releases": len(APPROVED_RELEASE_DIGESTS), "provider_calls": 0,
        "primary_as_supplied": primary, "transpose_control_same_cells": transposed,
        "explicit_source_correction_overlay": corrected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-fixtures", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate(write_fixtures=args.write_fixtures)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if not isinstance(v, list)}, indent=2))
    return int(result["primary_parsed_exact"] != result["primary_source_cells"])


if __name__ == "__main__":
    raise SystemExit(main())
