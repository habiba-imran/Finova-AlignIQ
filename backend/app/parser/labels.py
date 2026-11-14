"""English label recognition only. These are NOT validated cross-vendor axis maps."""

import re
from dataclasses import dataclass

UNIT_ALIASES = {
    "°": "deg", "deg": "deg", "degree": "deg", "degrees": "deg",
    "mm": "mm", "millimeter": "mm", "millimeters": "mm", "millimetre": "mm", "millimetres": "mm",
}
LABEL_ALIASES = {
    "rotation": ("rotation", "rot", "rotate"),
    "inclination": ("inclination", "incl"),
    "angulation": ("angulation", "ang"),
    "extrusion": ("extrusion", "extrude"),
    "intrusion": ("intrusion", "intrude"),
    "buccolingual": ("buccolingual", "buccal/lingual", "buccal lingual", "b/l", "bucco-lingual"),
    "mesiodistal": ("mesiodistal", "mesial/distal", "mesial distal", "m/d", "mesio-distal"),
    "vertical": ("vertical", "intrusion/extrusion", "extrusion/intrusion", "i/e"),
    # Lexical labels only: "relative" deliberately remains a distinct family.
    # None of these spellings establishes an axis, direction or reference basis.
    "relative_vertical": ("relative ext/int", "relative extrusion/intrusion"),
    "translation": ("translation", "displacement"),
}
LABEL_ALIASES["buccolingual"] += ("translation b/l",)
LABEL_ALIASES["mesiodistal"] += ("translation m/d",)


def token(text: str) -> str:
    return " ".join(text.replace("\u00a0", " ").strip().lower().split())


def alias_key(text: str) -> str:
    """Case/whitespace and ASCII-slash spacing only; never fuzzy/substring matching."""
    return re.sub(r"\s*/\s*", "/", token(text))


def alias_map(families: dict[str, tuple[str, ...]]) -> dict[str, str | None]:
    """A conflicting normalized alias is withheld rather than last-writer-wins."""
    candidates: dict[str, set[str]] = {}
    for family, aliases in families.items():
        for alias in aliases:
            candidates.setdefault(alias_key(alias), set()).add(family)
    return {key: next(iter(values)) if len(values) == 1 else None for key, values in candidates.items()}


ALIASES = alias_map(LABEL_ALIASES)


@dataclass(frozen=True)
class Label:
    family: str | None
    unit: str | None
    raw_unit: str | None


def recognize_label(raw: str) -> Label:
    label = token(raw)
    raw_unit = None
    # Only explicit suffix units are allowed; a movement name never implies a unit.
    match = re.search(r"\s*(?:\(([^()]*)\)|\[([^\[\]]*)\]|\s+(°|deg|degrees?|mm))\s*$", label)
    if not match and label.endswith("°"):
        raw_unit = "°"
        label = label[:-1].strip()
    elif match:
        raw_unit = next(v for v in match.groups() if v is not None).strip()
        label = label[:match.start()].strip()
    return Label(ALIASES.get(alias_key(label)), UNIT_ALIASES.get(raw_unit), raw_unit)
