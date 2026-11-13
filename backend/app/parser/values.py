"""Parse complete numeric tokens with Decimal. Never infer a physical direction."""

import re
from decimal import Decimal

from app.domain.models import ParsedMeasurement, ParseIssue, RawCell
from app.parser.labels import UNIT_ALIASES, recognize_label, token

NUMBER = re.compile(r"(?P<number>[+\-−]?(?:[0-9]+(?:[.,][0-9]*)?|[.,][0-9]+))(?P<suffix>.*)", re.DOTALL)
UNIT = re.compile(r"^(millimeters?|millimetres?|degrees?|deg|mm|°)", re.IGNORECASE)
DIRECTIONS = {"b", "l", "m", "d", "i", "e", "buccal", "lingual", "mesial", "distal", "intrusion", "extrusion", "cw", "ccw", "clockwise", "counterclockwise"}
MISSING = {"": "BLANK", "-": "DASH", "—": "DASH", "–": "DASH", "n/a": "NOT_APPLICABLE_TOKEN", "na": "NOT_APPLICABLE_TOKEN", "?": "NOT_REPORTED"}


def parse_value(identifier: str, tooth_ref: str, label_cell: RawCell, cell: RawCell | None,
                decimal_separator: str) -> tuple[ParsedMeasurement, list[ParseIssue]]:
    label = recognize_label(label_cell.raw)
    measurement = ParsedMeasurement(
        id=identifier, tooth_ref=tooth_ref, raw_label=label_cell.raw, recognized_label=label.family,
        raw_value=cell.raw if cell else None, span=cell.span if cell else None,
        header_span=label_cell.span, header_unit=label.unit,
        numeric_status="NOT_PRESENT", field_status="NOT_PRESENT",
    )
    issues = []

    def issue(code: str, message: str, field: str, severity: str = "WARNING") -> None:
        issues.append(ParseIssue(code=code, severity=severity, message=message,
                                 span=cell.span if cell else label_cell.span,
                                 measurement_ids=[identifier], field=field))
        if field not in measurement.clarification_fields:
            measurement.clarification_fields.append(field)

    if label.family is None:
        issue("UNSUPPORTED_LABEL", "This label has no recognized lexical alias; no movement axis is assigned.", "movement_label")
    if label.raw_unit and not label.unit:
        issue("UNSUPPORTED_HEADER_UNIT", "The header's explicit unit is unsupported; no unit is inferred.", "unit")
    if cell is None:
        measurement.missing_kind = "OMITTED_CELL"
        issue("CELL_NOT_PRESENT", "A trailing delimited cell is omitted; it is not zero.", "value")
        return measurement, issues
    text = cell.raw.replace("\u00a0", " ").strip()
    if token(text) in MISSING:
        measurement.numeric_status = "MISSING"
        measurement.field_status = "NOT_PRESENT"
        measurement.missing_kind = MISSING[token(text)]
        issue("MISSING_VALUE", "A blank or missing marker is retained without assigning zero or tooth status.", "value")
        return measurement, issues

    match = NUMBER.fullmatch(text)
    if not match or len(match["number"]) > 128:
        measurement.numeric_status = "INVALID"
        measurement.field_status = "PARSE_INVALID"
        issue("INVALID_NUMBER", "Expected a finite plain decimal with optional explicit unit/direction; exponents and formulas are unsupported.", "value", "ERROR")
        return measurement, issues
    raw_number = match["number"]
    measurement.raw_number = raw_number
    measurement.raw_sign = raw_number[0] if raw_number[0] in "+-−" else None
    suffix = match["suffix"].strip()
    measurement.raw_suffix = suffix or None
    unit_match = UNIT.match(suffix)
    if unit_match:
        measurement.raw_unit = unit_match[0]
        measurement.cell_unit = UNIT_ALIASES[unit_match[0].lower()]
        suffix = suffix[unit_match.end():].strip()
    if suffix:
        if suffix.lower() not in DIRECTIONS:
            measurement.numeric_status = "AMBIGUOUS"
            measurement.field_status = "AMBIGUOUS"
            issue("AMBIGUOUS_VALUE_SUFFIX", "The complete token has an unsupported unit, separator, exponent, or direction suffix; no numeric value is accepted.", "value", "ERROR")
            return measurement, issues
        measurement.raw_direction = suffix

    if ("," in raw_number and decimal_separator != "COMMA") or ("." in raw_number and decimal_separator == "COMMA"):
        measurement.numeric_status = "AMBIGUOUS"
        measurement.field_status = "AMBIGUOUS"
        issue("DECIMAL_CONVENTION_REQUIRED", "This separator conflicts with the decimal convention claim; grouping separators are not supported.", "decimal_separator", "ERROR")
        return measurement, issues
    derived_number = raw_number.replace("−", "-")
    if decimal_separator == "COMMA":
        derived_number = derived_number.replace(",", ".")
    value = Decimal(derived_number)
    measurement.signed_decimal = value
    measurement.magnitude_decimal = value.copy_abs()  # No context-dependent rounding, even beyond 28 digits.
    measurement.numeric_status = "EXPLICIT_ZERO" if value.is_zero() else "PARSED"
    measurement.field_status = "EXPLICIT_ZERO" if value.is_zero() else "SEMANTICS_UNKNOWN"
    measurement.unit = measurement.cell_unit or label.unit
    if measurement.cell_unit and label.unit and measurement.cell_unit != label.unit:
        measurement.unit = None
        measurement.field_status = "AMBIGUOUS"
        issue("UNIT_CONFLICT", "Explicit header and cell units conflict; neither is selected as the measurement unit.", "unit", "ERROR")
    elif not measurement.unit:
        issue("UNIT_REQUIRED", "No supported explicit unit was supplied. A movement label does not establish a unit.", "unit")
    if label.family is None:
        measurement.field_status = "UNSUPPORTED"
    issue("DIRECTION_UNVERIFIED", "The literal sign/direction is preserved; physical direction and axis mappings are not verified.", "direction_mapping")
    return measurement, issues
