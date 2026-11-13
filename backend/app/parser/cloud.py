"""Independent parser credentials; external structural proposals disabled by default."""

import os
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, SecretStr


class ParserSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)
    api_key: SecretStr = Field(default_factory=lambda: SecretStr(""), repr=False, exclude=True)
    synthetic_transmission_enabled: bool = False
    environment: Literal["development", "test", "production"] = "production"
    model: str = Field(default="openai/gpt-oss-120b", min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_./:-]+$")
    timeout_seconds: float = Field(default=8, ge=0.1, le=30)
    max_completion_tokens: int = Field(default=2048, ge=256, le=8192)
    reasoning_effort: Literal["low", "medium", "high"] = "low"
    temperature: Literal[0] = 0
    max_retries: Literal[0] = 0
    max_retry_delay_seconds: Literal[0] = 0

    @property
    def configured(self) -> bool:
        key = self.api_key.get_secret_value()
        return (self.environment == "development" and self.synthetic_transmission_enabled and bool(key)
                and all(33 <= ord(c) <= 126 for c in key))


def load_parser_settings() -> ParserSettings:
    names = {"GROQ_API_KEY_2": "api_key", "FINOVA_PARSER_GROQ_ENABLED": "synthetic_transmission_enabled",
             "FINOVA_ENVIRONMENT": "environment", "GROQ_PARSER_MODEL": "model",
             "GROQ_PARSER_TIMEOUT_SECONDS": "timeout_seconds", "GROQ_PARSER_MAX_COMPLETION_TOKENS": "max_completion_tokens",
             "GROQ_PARSER_REASONING_EFFORT": "reasoning_effort"}
    return ParserSettings.model_validate({field: os.environ[name] for name, field in names.items() if name in os.environ})
