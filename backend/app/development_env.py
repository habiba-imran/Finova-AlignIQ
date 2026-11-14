"""Explicit development-only env file loading; no eval, interpolation or diagnostics.

Only known Groq configuration names are imported. Existing process settings win.
Nothing is written back; this helper never returns or prints secret values.
"""

import os
from pathlib import Path
import re

ALLOWED = frozenset({
    "GROQ_API_KEY", "GROQ_API_KEY_2", "FINOVA_ENVIRONMENT", "FINOVA_GROQ_SYNTHETIC_ENABLED",
    "FINOVA_PARSER_GROQ_ENABLED", "GROQ_MODEL", "GROQ_TEMPERATURE", "GROQ_MAX_COMPLETION_TOKENS",
    "GROQ_REASONING_EFFORT", "GROQ_TIMEOUT_SECONDS", "GROQ_MAX_RETRIES", "GROQ_MAX_RETRY_DELAY_SECONDS",
    "GROQ_MAX_WORDING_FINDINGS", "GROQ_PARSER_MODEL", "GROQ_PARSER_TIMEOUT_SECONDS",
    "GROQ_PARSER_MAX_COMPLETION_TOKENS", "GROQ_PARSER_REASONING_EFFORT",
    "FINOVA_PLANNING_DEMO_ENABLED",
    "FINOVA_ATTACHMENT_DEMO_ENABLED",
    "FINOVA_SEQUENCER_DEMO_ENABLED",
})


def load_development_env(path: Path) -> None:
    try:
        data = path.read_bytes()
        if len(data) > 65_536: raise ValueError()
        values = {}
        for line in data.decode("utf-8-sig").splitlines():
            if not line.strip() or line.lstrip().startswith("#"): continue
            match = re.fullmatch(r"\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*", line)
            if not match: raise ValueError()
            name, value = match.groups()
            if name not in ALLOWED: continue
            if name in values: raise ValueError()
            if value.startswith(('"', "'")):
                if len(value) < 2 or value[-1] != value[0]: raise ValueError()
                value = value[1:-1]
            values[name] = value
        for name, value in values.items(): os.environ.setdefault(name, value)
    except (OSError, ValueError, UnicodeError):
        raise ValueError("DEVELOPMENT_ENV_UNAVAILABLE_OR_INVALID") from None
