"""Fixed shipped synthetic examples only; never learn an allowlist from user input."""

from hashlib import sha256
import json
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[3] / "examples" / "parser-finalization-synthetic.json"


def synthetic_examples() -> list[dict]:
    return json.loads(CATALOG.read_text(encoding="utf-8"))["fixtures"]


def cloud_example_allowed(raw: str) -> bool:
    # Byte-exact UTF-8 binding after normal browser textarea newline handling.
    # A '# SYNTHETIC' prefix/checkbox alone is not evidence of non-patient content.
    digest = sha256(raw.encode("utf-8")).digest()
    try:
        return any(item["cloud_allowed"] and sha256(item["raw_text"].encode("utf-8")).digest() == digest
                   for item in synthetic_examples())
    except (OSError, ValueError, TypeError, KeyError):
        return False  # A missing/malformed shipped asset cannot break local parsing or permit cloud access.
