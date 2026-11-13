"""Compose deterministic layers; return partial evidence without clinical interpretation."""

from collections import defaultdict
from hashlib import sha256
import re

from app.domain.models import (
    MAX_CELLS, MAX_CELL_CHARS, MAX_COLUMNS, MAX_LINES, AxisCoverage, LayoutInfo,
    ParsedMeasurement, ParseIssue, ParseResult, LexicalInput, UnparsedLine,
)
from app.parser.adapters import source_info
from app.parser.labels import token
from app.parser.layouts import Layout, detect_layout
from app.parser.teeth import parse_tooth
from app.parser.tokenize import cells, lines
from app.parser.values import parse_value


def parse_table(submission: LexicalInput, *, certified_layout: Layout | None = None,
                certified_rows: dict | None = None, separator_lines: frozenset[int] = frozenset()) -> ParseResult:
    """The optional grid is library-only, supplied by the independent structural certifier.

    HTTP callers cannot supply grids. Both paths use the same lexical value/identity
    routines and preserve original spans; neither path authorizes source semantics.
    """
    raw = submission.raw_text
    source_lines = lines(raw)
    source, issues, signature_lines = source_info(submission, source_lines)
    result = ParseResult(status="UNSUPPORTED", raw_text=raw,
                         raw_sha256=sha256(raw.encode("utf-8")).hexdigest(),
                         source=source, layout=LayoutInfo(), issues=issues)
    result.clarification_fields = [
        "source_verification", "source_version", "notation", "dentition", "arch",
        "plan_mode", "reference_basis", "scope", "coordinate_frame", "direction_mapping",
    ]

    def reject_line(line, reason: str, severity: str = "ERROR") -> None:
        result.unparsed_lines.append(UnparsedLine(raw=line.text, span=line.span, reason=reason))
        result.issues.append(ParseIssue(code=reason, severity=severity,
                                       message="This line was retained but not assigned to tooth/movement cells.", span=line.span))

    if not raw.strip():
        result.status = "INVALID"
        result.issues.append(ParseIssue(code="EMPTY_INPUT", severity="ERROR", message="Input contains no table text."))
        return result
    if len(source_lines) > MAX_LINES:
        result.status = "INVALID"
        result.issues.append(ParseIssue(code="LINE_LIMIT", severity="ERROR", message="Input exceeds the 2,000-line engineering limit."))
        return result
    if any(max(line.text.count("\t"), line.text.count("|"), line.text.count(";"),
               len(re.findall(r"[ \u00a0]{2,}", line.text))) >= MAX_COLUMNS for line in source_lines):
        result.status = "INVALID"
        result.issues.append(ParseIssue(code="GRID_LIMIT", severity="ERROR", message="A line exceeds the 128-column engineering limit."))
        return result
    layouts = [certified_layout] if certified_layout else detect_layout(source_lines)
    if len(layouts) != 1:
        result.issues.append(ParseIssue(code="AMBIGUOUS_LAYOUT" if layouts else "UNSUPPORTED_LAYOUT", severity="ERROR",
                                       message="Exactly one explicit table header/orientation/delimiter is required; no closest layout is selected."))
        for line in source_lines:
            if line.text.strip():
                result.unparsed_lines.append(UnparsedLine(raw=line.text, span=line.span, reason="LAYOUT_UNRESOLVED"))
        return result
    layout = layouts[0]
    width = len(layout.header)
    body = source_lines[layout.header_index + 1:]
    if width > MAX_COLUMNS or width * sum(bool(line.text.strip()) for line in body) > MAX_CELLS:
        result.status = "INVALID"
        result.issues.append(ParseIssue(code="GRID_LIMIT", severity="ERROR", message="Table exceeds the 128-column or 10,000-cell engineering limit."))
        return result
    result.layout = LayoutInfo(orientation=layout.orientation, delimiter=layout.delimiter,
                               header_line=source_lines[layout.header_index].number,
                               header_cells=layout.header, declared_column_count=width)
    if any(len(cell.raw) > MAX_CELL_CHARS for cell in layout.header):
        result.status = "INVALID"
        result.issues.append(ParseIssue(code="CELL_LIMIT", severity="ERROR", message="A header exceeds the 2,000-character engineering limit."))
        return result
    for line in source_lines[:layout.header_index]:
        if line.text.strip() and line.number not in signature_lines:
            if line.text.lstrip().startswith("# SYNTHETIC"):
                result.unparsed_lines.append(UnparsedLine(raw=line.text, span=line.span, reason="SYNTHETIC_PREAMBLE"))
            else:
                reject_line(line, "UNRECOGNIZED_PREAMBLE", "WARNING")

    def add_tooth(cell):
        tooth, tooth_issues = parse_tooth(f"tooth-{len(result.teeth) + 1}", cell, submission.context)
        result.teeth.append(tooth)
        result.issues.extend(tooth_issues)
        return tooth.id

    horizontal_teeth = [add_tooth(cell) for cell in layout.header[1:]] if layout.orientation == "TEETH_IN_COLUMNS" else []
    for line in body:
        if not line.text.strip():
            continue
        if line.number in separator_lines:
            result.unparsed_lines.append(UnparsedLine(raw=line.text, span=line.span, reason="STRUCTURAL_SEPARATOR"))
            continue
        row = certified_rows[line.number] if certified_rows is not None else cells(line, layout.delimiter)
        if len(row) > width or (layout.delimiter == "MULTISPACE" and len(row) != width) or len(row) == 1:
            reject_line(line, "ROW_ALIGNMENT_UNRESOLVED")
            continue
        if any(len(cell.raw) > MAX_CELL_CHARS for cell in row):
            reject_line(line, "CELL_LIMIT")
            continue
        if len(row) < width:
            result.issues.append(ParseIssue(code="SHORT_DELIMITED_ROW", severity="WARNING", span=line.span,
                                           message="Trailing delimited cells are absent. Existing positions are retained; no missing value is zero."))
        row_tooth = add_tooth(row[0]) if layout.orientation == "TEETH_IN_ROWS" else None
        for index in range(1, width):
            label_cell = layout.header[index] if row_tooth else row[0]
            tooth_ref = row_tooth or horizontal_teeth[index - 1]
            measurement, cell_issues = parse_value(
                f"measurement-{len(result.measurements) + 1}", tooth_ref, label_cell,
                row[index] if index < len(row) else None, submission.context.decimal_separator,
            )
            result.measurements.append(measurement)
            result.issues.extend(cell_issues)

    mark_duplicates(result)
    if not result.measurements:
        result.status = "INVALID"
        result.issues.append(ParseIssue(code="NO_DATA_ROWS", severity="ERROR", message="The header has no structurally assignable data rows."))
    else:
        partial = any(issue.severity == "ERROR" or issue.code in {
            "MISSING_VALUE", "CELL_NOT_PRESENT", "UNSUPPORTED_LABEL", "UNIT_REQUIRED", "UNRECOGNIZED_PREAMBLE",
            "DUPLICATE_FIELD", "PALMER_UNSUPPORTED", "UNSUPPORTED_HEADER_UNIT",
        } for issue in result.issues)
        result.status = "PARTIAL" if partial else "PARSED_UNVERIFIED"
    ms = result.measurements
    result.coverage = AxisCoverage(
        declared_measurements=len(ms), numeric_present=sum(m.signed_decimal is not None for m in ms),
        explicit_zero=sum(m.numeric_status == "EXPLICIT_ZERO" for m in ms),
        missing=sum(m.numeric_status in {"MISSING", "NOT_PRESENT"} for m in ms),
        invalid=sum(m.numeric_status == "INVALID" for m in ms),
        ambiguous=sum(m.field_status == "AMBIGUOUS" for m in ms),
        unsupported=sum(m.field_status == "UNSUPPORTED" for m in ms), unverified=len(ms),
    )
    result.clarification_fields = sorted(set(result.clarification_fields + [
        issue.field for issue in result.issues if issue.field
    ]))
    return result


def mark_duplicates(result: ParseResult) -> None:
    """Preserve repeated positions, including potential comparison columns; never merge."""
    by_tooth = {tooth.id: tooth.token for tooth in result.teeth}
    groups: dict[tuple, list[ParsedMeasurement]] = defaultdict(list)
    context = result.source.context
    for measurement in result.measurements:
        key = (context.case_id, context.plan_id, context.reference_basis, context.scope, context.stage_index,
               by_tooth[measurement.tooth_ref], measurement.recognized_label or token(measurement.raw_label))
        groups[key].append(measurement)
    group_index = 0
    for group in groups.values():
        if len(group) < 2:
            continue
        group_index += 1
        for measurement in group:
            measurement.duplicate_group = f"duplicate-{group_index}"
            measurement.field_status = "AMBIGUOUS"
            measurement.clarification_fields.append("duplicate_scope_or_field")
        values = {(m.signed_decimal, m.unit, m.raw_direction) for m in group}
        result.issues.append(ParseIssue(
            code="CONFLICTING_FIELD" if len(values) > 1 else "DUPLICATE_FIELD",
            severity="ERROR" if len(values) > 1 else "WARNING", measurement_ids=[m.id for m in group],
            field="duplicate_scope_or_field", message="Repeated tooth/label positions are retained separately. Clarify plan, basis, scope, and stage before interpretation.",
        ))
