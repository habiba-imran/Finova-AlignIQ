"""Lossless spans into the original string; normalize only derived tokens elsewhere."""

import re
from dataclasses import dataclass

from app.domain.models import RawCell, SourceSpan

DELIMITERS = {"TAB": r"\t", "PIPE": r"\|", "SEMICOLON": r";", "MULTISPACE": r"[ \u00a0]{2,}"}


@dataclass(frozen=True)
class Line:
    number: int
    start: int
    text: str

    @property
    def span(self) -> SourceSpan:
        return SourceSpan(line=self.number, column_start=1, column_end=len(self.text) + 1,
                          start=self.start, end=self.start + len(self.text))


def lines(raw_text: str) -> list[Line]:
    result = []
    for match in re.finditer(r"([^\r\n]*)(?:\r\n|\r|\n|$)", raw_text):
        if match.start() == match.end():
            continue
        result.append(Line(len(result) + 1, match.start(), match.group(1)))
    return result


def cells(line: Line, delimiter: str) -> list[RawCell]:
    boundaries = list(re.finditer(DELIMITERS[delimiter], line.text))
    if delimiter == "MULTISPACE":
        # Outer indentation belongs to the first/last raw cell, not extra columns.
        boundaries = [m for m in boundaries if m.start() != 0 and m.end() != len(line.text)]
    parts = []
    start = 0
    for end, following in [(m.start(), m.end()) for m in boundaries] + [(len(line.text), len(line.text))]:
        parts.append(RawCell(raw=line.text[start:end], span=SourceSpan(
            line=line.number, column_start=start + 1, column_end=end + 1,
            start=line.start + start, end=line.start + end, cell_index=len(parts) + 1,
        )))
        start = following
    return parts
