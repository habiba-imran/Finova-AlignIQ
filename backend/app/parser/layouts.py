"""Explicit header/orientation detection. Reject multiple possible tables."""

from dataclasses import dataclass

from app.domain.models import RawCell
from app.parser.labels import recognize_label, token
from app.parser.tokenize import DELIMITERS, Line, cells

TOOTH_HEADERS = {"tooth", "teeth", "tooth id", "tooth identifier"}
MOVEMENT_HEADERS = {"movement", "movements", "axis", "measurement"}


@dataclass(frozen=True)
class Layout:
    header_index: int
    delimiter: str
    orientation: str
    header: list[RawCell]


def detect_layout(source_lines: list[Line]) -> list[Layout]:
    candidates = []
    for delimiter in DELIMITERS:
        rows = [cells(line, delimiter) for line in source_lines]
        recognized_below = [False] * (len(rows) + 1)
        for index in range(len(rows) - 1, -1, -1):
            recognized_below[index] = recognized_below[index + 1] or recognize_label(rows[index][0].raw).family is not None
        for index, (line, header) in enumerate(zip(source_lines, rows)):
            if not line.text.strip():
                continue
            if len(header) < 2:
                continue
            corner = token(header[0].raw)
            recognized = [recognize_label(c.raw).family is not None for c in header[1:]]
            if corner in TOOTH_HEADERS and any(recognized):
                candidates.append(Layout(index, delimiter, "TEETH_IN_ROWS", header))
            elif not any(recognized) and (corner in MOVEMENT_HEADERS or corner == "" or corner in TOOTH_HEADERS):
                # Explicit movement corner (or empty transpose corner) plus a recognized row label.
                if recognized_below[index + 1]:
                    candidates.append(Layout(index, delimiter, "TEETH_IN_COLUMNS", header))
    return candidates
