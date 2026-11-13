"""Server-only settings. No provider URL override or real-patient transmission switch."""

import os
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, SecretStr


class ReportSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    api_key: SecretStr = Field(default_factory=lambda: SecretStr(""), repr=False, exclude=True)
    synthetic_transmission_enabled: bool = False
    model: Literal["openai/gpt-oss-120b"] = "openai/gpt-oss-120b"
    temperature: float = Field(default=0, ge=0, le=0.3)
    max_completion_tokens: int = Field(default=2048, ge=256, le=4096)
    reasoning_effort: Literal["low", "medium", "high"] = "low"
    timeout_seconds: float = Field(default=6, ge=0.1, le=8)
    max_retries: int = Field(default=0, ge=0, le=1)
    max_retry_delay_seconds: float = Field(default=1, ge=0, le=1)
    max_wording_findings: int = Field(default=16, ge=1, le=24)

    @property
    def configured(self) -> bool:
        key = self.api_key.get_secret_value()
        return bool(key) and not any(ord(c) < 33 or ord(c) > 126 for c in key) and self.synthetic_transmission_enabled


def load_settings() -> ReportSettings:
    names = {
        "GROQ_API_KEY": "api_key", "FINOVA_GROQ_SYNTHETIC_ENABLED": "synthetic_transmission_enabled",
        "GROQ_MODEL": "model", "GROQ_TEMPERATURE": "temperature", "GROQ_MAX_COMPLETION_TOKENS": "max_completion_tokens",
        "GROQ_REASONING_EFFORT": "reasoning_effort", "GROQ_TIMEOUT_SECONDS": "timeout_seconds",
        "GROQ_MAX_RETRIES": "max_retries", "GROQ_MAX_RETRY_DELAY_SECONDS": "max_retry_delay_seconds",
        "GROQ_MAX_WORDING_FINDINGS": "max_wording_findings",
    }
    return ReportSettings.model_validate({field: os.environ[name] for name, field in names.items() if name in os.environ})
