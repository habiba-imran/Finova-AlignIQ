"""Groq Cloud only, bounded calls, no SDK retries/logging or provider diagnostics."""

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import math
import time
from typing import Protocol

import httpx
from pydantic import SecretStr

from app.reports.prompt import response_format
from app.reports.validation import private_json

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MAX_PROVIDER_BYTES = 131_072
MAX_PROMPT_BYTES = 24_000


@dataclass(frozen=True)
class GroqResult:
    content: str | None
    code: str
    attempts: int
    elapsed_seconds: float | None = None
    http_status: int | None = None
    model_matches: bool | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


class ChatSettings(Protocol):
    """Both server-only settings types satisfy this; credentials never cross services."""
    configured: bool
    api_key: SecretStr
    model: str
    temperature: float
    max_completion_tokens: int
    reasoning_effort: str
    timeout_seconds: float
    max_retries: int
    max_retry_delay_seconds: float


def retry_delay(header: str | None, limit: float) -> float | None:
    if header is None:
        return None  # No immediate/repeated retry on an unknown rate-limit window.
    try:
        try:
            seconds = float(header)
        except ValueError:
            date = parsedate_to_datetime(header)
            if date.utcoffset() is None:
                return None
            seconds = max(0, (date - datetime.now(timezone.utc)).total_seconds())
        return seconds if math.isfinite(seconds) and 0 <= seconds <= limit else None
    except (TypeError, ValueError, OverflowError):
        return None


class GroqClient:
    def __init__(self, settings: ChatSettings, *, transport: httpx.BaseTransport | None = None, sleep=time.sleep, clock=time.monotonic):
        self.settings = settings
        self.transport = transport
        self.sleep = sleep
        self.clock = clock

    def generate(self, messages: list[dict], *, response_schema: dict | None = None) -> GroqResult:
        import json
        started = time.perf_counter()
        status = None
        metrics = {}

        def finish(content, code, attempts):
            return GroqResult(content, code, attempts, round(time.perf_counter() - started, 4), status, **metrics)

        if not self.settings.configured:
            return finish(None, "GROQ_NOT_CONFIGURED", 0)
        if len(json.dumps(messages).encode()) > MAX_PROMPT_BYTES:
            return finish(None, "GROQ_PROMPT_LIMIT", 0)
        payload = dict(model=self.settings.model, messages=messages, temperature=self.settings.temperature,
                       max_completion_tokens=self.settings.max_completion_tokens, reasoning_effort=self.settings.reasoning_effort,
                       include_reasoning=False, response_format=response_schema or response_format(), stream=False, n=1)
        try:
            with httpx.Client(timeout=self.settings.timeout_seconds, follow_redirects=False, trust_env=False,
                              transport=self.transport) as client:
                for attempt in range(1, self.settings.max_retries + 2):
                    deadline = self.clock() + self.settings.timeout_seconds
                    with client.stream("POST", GROQ_URL, json=payload,
                                       headers={"Authorization": "Bearer " + self.settings.api_key.get_secret_value(), "Accept": "application/json"}) as response:
                        status = response.status_code
                        if self.clock() >= deadline:
                            return finish(None, "GROQ_TIMEOUT", attempt)
                        if response.status_code in {429, 503}:
                            delay = retry_delay(response.headers.get("retry-after"), self.settings.max_retry_delay_seconds)
                            if attempt <= self.settings.max_retries and delay is not None:
                                # The provider response is closed before sleeping; no body is read or exposed.
                                response.close()
                                self.sleep(delay)
                                continue
                            return finish(None, "GROQ_RATE_LIMIT" if response.status_code == 429 else "GROQ_UNAVAILABLE", attempt)
                        if response.status_code != 200:
                            return finish(None, "GROQ_HTTP_ERROR", attempt)
                        body = bytearray()
                        for chunk in response.iter_bytes():
                            if self.clock() >= deadline:
                                return finish(None, "GROQ_TIMEOUT", attempt)
                            if len(body) + len(chunk) > MAX_PROVIDER_BYTES:
                                return finish(None, "GROQ_RESPONSE_LIMIT", attempt)
                            body.extend(chunk)
                    try:
                        envelope = private_json(body.decode("utf-8"))
                        if not isinstance(envelope, dict):
                            return finish(None, "GROQ_MALFORMED_OUTPUT", attempt)
                        # Only numeric usage counters and model equality are retained.
                        # Provider bodies, IDs, reasoning and error diagnostics are never logged.
                        usage = envelope.get("usage", {})
                        metrics["model_matches"] = envelope.get("model") == self.settings.model if "model" in envelope else None
                        if isinstance(usage, dict):
                            for name in ("prompt_tokens", "completion_tokens", "total_tokens"):
                                value = usage.get(name)
                                if type(value) is int and value >= 0:
                                    metrics[name] = value
                        if metrics.get("model_matches") is False:
                            return finish(None, "GROQ_MODEL_MISMATCH", attempt)
                        choices = envelope["choices"]
                        if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
                            return finish(None, "GROQ_MALFORMED_OUTPUT", attempt)
                        if choices[0]["finish_reason"] != "stop":
                            return finish(None, "GROQ_INCOMPLETE_OUTPUT", attempt)
                        message = choices[0]["message"]
                        if not isinstance(message, dict):
                            return finish(None, "GROQ_MALFORMED_OUTPUT", attempt)
                        if message.get("tool_calls") or message.get("refusal") or message.get("role") != "assistant":
                            return finish(None, "GROQ_REFUSAL_OR_TOOL_OUTPUT", attempt)
                        content = message["content"]
                        if not isinstance(content, str) or not content or len(content) > 32_000:
                            return finish(None, "GROQ_MALFORMED_OUTPUT", attempt)
                        return finish(content, "GROQ_RESPONSE_RECEIVED", attempt)
                    except (KeyError, IndexError, TypeError, ValueError, RecursionError):
                        return finish(None, "GROQ_MALFORMED_OUTPUT", attempt)
        except httpx.TimeoutException:
            return finish(None, "GROQ_TIMEOUT", attempt)
        except (httpx.HTTPError, OSError, ValueError):
            return finish(None, "GROQ_CONNECTION_ERROR", attempt if 'attempt' in locals() else 0)
        return finish(None, "GROQ_UNAVAILABLE", 0)
