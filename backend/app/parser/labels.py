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
    "translation": ("translation", "displacement"),
}
ALIASES = {alias: family for family, aliases in LABEL_ALIASES.items() for alias in aliases}


def token(text: str) -> str:
    return " ".join(text.replace("\u00a0", " ").strip().lower().split())


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
    return Label(ALIASES.get(label), UNIT_ALIASES.get(raw_unit), raw_unit)
