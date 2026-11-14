"""Generate final synthetic report fixtures; --live explicitly calls configured Groq.

No credentials or provider error bodies are printed. Supplied examples are user
inputs for engineering verification, never calculated treatment recommendations.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
import re
import httpx

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))
from app.development_env import load_development_env
from app.interactive.models import InteractiveSubmission, ReviewDetails
from app.interactive.narrative import load_planning_settings
from app.interactive.service import generate_interactive
from app.parser.receipts import resolve
from app.reports.settings import ReportSettings
from app.reports.groq_client import GroqClient
import app.interactive.narrative as narrative_module


class DiagnosticTransport(httpx.BaseTransport):
    """Retain only safe quota metadata, never raw errors or submitted content."""
    def __init__(self, output):
        self.inner = httpx.HTTPTransport()
        self.output = output

    def handle_request(self, request):
        response = self.inner.handle_request(request)
        if response.status_code == 429:
            body = response.read()
            try:
                error = json.loads(body).get("error", {})
                message = str(error.get("message", ""))
                period = re.search(r"(?:tokens|requests) per (minute|day)", message, flags=re.I)
                self.output.append({"http_status": 429, "code": error.get("code"), "quota_period": period.group(1).lower() if period else "unknown",
                    "retry_after": response.headers.get("retry-after"), "token_reset": response.headers.get("x-ratelimit-reset-tokens")})
            except ValueError:
                self.output.append({"http_status": 429, "quota_period": "unknown"})
        return response

    def close(self):
        self.inner.close()


def supplied_details(parsed, module):
    if module == "micro":
        return ReviewDetails(attachments=[dict(tooth_ref=parsed.teeth[0].id, choice="ATTACHMENT", design="Supplied oval design", width_mm="1.2300", height_mm="0.50", depth_mm="0.75", surface="Supplied buccal surface", orientation="Supplied vertical orientation")])
    movement = next(m for m in parsed.measurements if m.unit == "mm")
    return ReviewDetails(stages=[dict(stage_id="SUPPLIED-1", order=1, duration_days=7)],
        allocations=[dict(stage_id="SUPPLIED-1", tooth_ref=movement.tooth_ref, measurement_ref=movement.id, amount="0.1250", unit="mm")],
        anchorage_notes=[dict(tooth_ref=movement.tooth_ref, note="Supplied synthetic anchorage note; no independent indication assessment.")])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--module", choices=["macro", "micro", "nano"], default="macro")
    parser.add_argument("--supplied", action="store_true")
    parser.add_argument("--diagnostic", action="store_true")
    args = parser.parse_args()
    output = ROOT / "evidence/module-final"
    output.mkdir(parents=True, exist_ok=True)
    if args.live:
        load_development_env(ROOT / ".env.local")
        source = json.loads((ROOT / "evidence/planning-wording/user-synthetic-live-report.json").read_text(encoding="utf-8"))["parsed"]
        cases = [(args.module, source["raw_text"], args.supplied, "live")]
        settings = load_planning_settings()
        if not settings.configured:
            raise SystemExit("No local provider key configured; live verification was not performed.")
    else:
        rows = next(item["raw_text"] for item in json.loads((ROOT / "examples/interactive-synthetic-tmts.json").read_text(encoding="utf-8")) if item["id"] == "rows")
        cases = [(module, rows, False, "fixture") for module in ("macro", "micro", "nano")] + [(module, rows, True, "fixture") for module in ("micro", "nano")]
        settings = ReportSettings()
    for module, raw, supplied, prefix in cases:
        request = InteractiveSubmission(raw_text=raw, raw_sha256=hashlib.sha256(raw.encode()).hexdigest(), synthetic_data_confirmed=True, module=module)
        if supplied:
            request = request.model_copy(update={"review_details": supplied_details(resolve(request), module)})
        diagnostics = []
        metrics = []
        provider_responses = []
        class AuditClient(GroqClient):
            def generate(self, *arguments, **keywords):
                result = super().generate(*arguments, **keywords)
                if args.diagnostic and result.content is not None:
                    provider_responses.append(result.content)
                metrics.append(dict(http_status=result.http_status, code=result.code, seconds=result.elapsed_seconds,
                    prompt_tokens=result.prompt_tokens, completion_tokens=result.completion_tokens, completion_budget=self.settings.max_completion_tokens))
                return result
        original_factory = narrative_module.GroqClient
        if args.live:
            narrative_module.GroqClient = lambda config: AuditClient(config, transport=DiagnosticTransport(diagnostics) if args.diagnostic else None)
        try:
            report = generate_interactive(request, settings=settings)
        finally:
            narrative_module.GroqClient = original_factory
        data = report.model_dump_json(indent=2)
        name = f"{prefix}-{module}" + ("-supplied" if supplied else "")
        (output / f"{name}.json.gz").write_bytes(gzip.compress(data.encode(), mtime=0))
        summary = dict(module=module, supplied=supplied, generation=report.generation.model_dump(mode="json"),
            sections=[dict(id=section.section_id, status=section.status) for section in report.sections],
            source_positions=len(report.parsed.measurements), rules=len(report.engine_review.evaluations),
            source_sha256=report.parsed.raw_sha256)
        if diagnostics:
            summary["quota_diagnostics"] = diagnostics
        if metrics:
            summary["provider_calls"] = metrics
        (output / f"{name}-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        if provider_responses:
            (output / f"{name}-provider.json.gz").write_bytes(gzip.compress(json.dumps(provider_responses).encode(), mtime=0))
        if not args.live:
            suffix = "-supplied" if supplied else ""
            (ROOT / f"frontend/src/test/fixtures/interactive-{module}{suffix}.json").write_text(data + "\n", encoding="utf-8")
        print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
