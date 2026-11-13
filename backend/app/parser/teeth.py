"""Syntax checks under declared notation only; no anatomical identity conversion."""

import re

from app.domain.models import ParseIssue, RawCell, SourceContext, ToothIdentifier


def parse_tooth(identifier: str, cell: RawCell, context: SourceContext) -> tuple[ToothIdentifier, list[ParseIssue]]:
    text = cell.raw.strip()
    result = ToothIdentifier(id=identifier, raw_identifier=cell.raw, token=text,
                             notation_claim=context.notation, identifier_status="UNVERIFIED", span=cell.span)
    issues = []

    def issue(code: str, message: str, field: str, status: str, severity: str = "WARNING") -> None:
        result.identifier_status = status
        result.clarification_fields.append(field)
        issues.append(ParseIssue(code=code, severity=severity, message=message, span=cell.span, field=field))

    if not text:
        issue("MISSING_TOOTH_IDENTIFIER", "The tooth identifier is empty; no tooth is invented.", "tooth_identifier", "INVALID", "ERROR")
    elif context.notation == "UNKNOWN":
        issue("TOOTH_NOTATION_AMBIGUOUS", "A tooth token cannot establish its numbering system; no anatomical identity is assigned.", "notation", "AMBIGUOUS")
    elif context.notation == "PALMER":
        issue("PALMER_UNSUPPORTED", "Palmer serialization and quadrant symbols require verified fixtures; the identifier is retained only.", "notation", "UNSUPPORTED")
    elif context.notation == "FDI":
        permanent = bool(re.fullmatch(r"[1-4][1-8]", text))
        primary = bool(re.fullmatch(r"[5-8][1-5]", text))
        valid = permanent or primary
        if context.dentition == "PERMANENT":
            valid = permanent
        elif context.dentition == "PRIMARY":
            valid = primary
        if not valid:
            issue("TOOTH_SYNTAX_CONFLICT", "Identifier syntax conflicts with the declared FDI/dentition claims; it is not reinterpreted.", "tooth_identifier", "INVALID", "ERROR")
        elif context.arch in {"UPPER", "LOWER"}:
            upper = text[0] in "1256"
            if upper != (context.arch == "UPPER"):
                issue("ARCH_CLAIM_CONFLICT", "Identifier syntax conflicts with the independently supplied arch claim.", "arch", "INVALID", "ERROR")
    elif context.notation == "UNIVERSAL":
        permanent = bool(re.fullmatch(r"(?:[1-9]|[12][0-9]|3[0-2])", text))
        primary = bool(re.fullmatch(r"[A-T]", text))
        valid = permanent or primary
        if context.dentition == "PERMANENT":
            valid = permanent
        elif context.dentition == "PRIMARY":
            valid = primary
        if not valid:
            issue("TOOTH_SYNTAX_CONFLICT", "Identifier syntax conflicts with the declared Universal/dentition claims; it is not converted.", "tooth_identifier", "INVALID", "ERROR")
    if result.identifier_status == "UNVERIFIED":
        result.clarification_fields.append("source_notation_verification")
    return result, issues
