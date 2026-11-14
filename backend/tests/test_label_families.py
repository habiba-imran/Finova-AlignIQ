"""Generic lexical recognition never supplies source semantics or vendor authority."""
import pytest

from app.domain.models import LexicalInput
from app.parser.labels import LABEL_ALIASES, alias_key, alias_map, recognize_label
from app.parser.service import parse_table
from app.semantics.normalization import assess_semantics
from app.semantics.registry import APPROVED_RELEASE_DIGESTS


@pytest.mark.parametrize("label,family", [
    ("Extrusion / Intrusion", "vertical"),
    ("Relative Ext / Int", "relative_vertical"),
    ("Relative Extrusion / Intrusion", "relative_vertical"),
    ("Translation B / L", "buccolingual"),
    ("Translation M / D", "mesiodistal"),
])
@pytest.mark.parametrize("formatting", [lambda s: s, lambda s: s.upper(), lambda s: s.replace(" / ", "/"),
    lambda s: s.replace(" ", "\u00a0"), lambda s: s.replace(" / ", "/ ")])
def test_documented_format_variants(label, family, formatting):
    raw_label = formatting(label) + " [mm]"
    assert recognize_label(raw_label).family == family
    raw = f"Tooth\t{raw_label}\nA\t−1.2300 D\nB\t0.000\nC\t-\n"
    parsed = parse_table(LexicalInput(raw_text=raw))
    a, b, c = parsed.measurements
    assert all(m.recognized_label == family and m.raw_label == raw_label and m.header_unit == "mm" for m in (a, b, c))
    assert a.unit == b.unit == "mm" and c.unit is None  # missing cells never acquire a measured unit
    assert a.raw_value == "−1.2300 D" and str(a.signed_decimal) == "-1.2300" and a.raw_direction == "D"
    assert b.numeric_status == "EXPLICIT_ZERO" and str(b.signed_decimal) == "0.000"
    assert c.numeric_status == "MISSING" and c.signed_decimal is None
    for m in parsed.measurements:
        assert raw[m.header_span.start:m.header_span.end] == raw_label
        assert raw[m.span.start:m.span.end] == m.raw_value
        assert m.canonical_axis is m.canonical_direction is m.mapping_id is None and not m.semantics_verified
    semantics = assess_semantics(parsed)
    assert semantics.status == "DISABLED" and not any(m.canonical_measurement_ready for m in semantics.measurements)
    assert not APPROVED_RELEASE_DIGESTS


@pytest.mark.parametrize("label", ["Translation B / L / M / D", "Relative Ext / Int / Rotation", "Translation B or L",
    "Translation B\\L", "Relative Ext", "Extrusion + Intrusion", "Translation B / L correction", "Translation M / L"])
def test_ambiguous_composite_or_approximate_names_stay_unknown(label):
    assert recognize_label(label + " (mm)").family is None


def test_alias_collisions_are_withheld_and_relative_is_not_absolute():
    assert alias_map({"first": ("A / B",), "second": ("a/b",)}) == {"a/b": None}
    assert None not in alias_map(LABEL_ALIASES).values()
    assert recognize_label("Relative Ext/Int").family != recognize_label("Extrusion/Intrusion").family
    assert recognize_label("Relative Ext/Int").unit is None  # no implicit unit/basis


def test_every_previous_alias_and_explicit_unit_stays_compatible():
    for family, aliases in LABEL_ALIASES.items():
        for alias in aliases:
            assert recognize_label(alias).family == family
            assert recognize_label(alias + " (deg)").unit == "deg"
            assert alias_key(alias) in alias_map(LABEL_ALIASES)


def test_synonymous_duplicate_columns_are_retained_as_conflicts_not_merged():
    parsed = parse_table(LexicalInput(raw_text="Tooth\tB/L (mm)\tTranslation B / L (mm)\nA\t1.00B\t2.00L\n"))
    assert len(parsed.measurements) == 2
    assert all(m.duplicate_group is not None and m.field_status == "AMBIGUOUS" for m in parsed.measurements)
    assert [m.raw_value for m in parsed.measurements] == ["1.00B", "2.00L"]
