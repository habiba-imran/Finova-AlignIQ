"""Reproducible synthetic snapshots; --live makes three bounded configured calls."""
import argparse
import hashlib
import json
import logging
from pathlib import Path
import sys

import httpx

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))
from app.interactive.models import InteractiveSubmission
from app.interactive.service import generate_interactive
from app.interactive.narrative import load_planning_settings
from app.reports.groq_client import GroqClient
from app.reports.settings import ReportSettings


def main():
    args = argparse.ArgumentParser()
    modes = args.add_mutually_exclusive_group()
    modes.add_argument("--live", action="store_true")
    modes.add_argument("--mock", action="store_true")
    args.add_argument("--output", default="evidence/analysis-pipeline")
    options = args.parse_args()
    live = options.live
    output = (ROOT / options.output).resolve()
    if not output.is_relative_to(ROOT):
        raise ValueError("OUTPUT_OUTSIDE_PROJECT")
    output.mkdir(parents=True, exist_ok=True)
    raw = (ROOT / "backend/tests/fixtures/analysis_15_tooth.md").read_text(encoding="utf-8")
    if live:
        from app.development_env import load_development_env
        load_development_env(ROOT / ".env.local")
        settings = load_planning_settings()
        if not settings.configured:
            print("Live verification skipped: Groq is not configured.")
            return
    else:
        settings = ReportSettings(api_key="synthetic-test-only-key", synthetic_transmission_enabled=True) if options.mock else ReportSettings()
    records = []
    for module in ("macro", "micro", "nano"):
        request = InteractiveSubmission(raw_text=raw, raw_sha256=hashlib.sha256(raw.encode()).hexdigest(),
            synthetic_data_confirmed=True, module=module)
        calls = []
        def handler(http_request):
            payload = json.loads(http_request.content)
            calls.append(len(json.dumps(payload["messages"]).encode()))
            data = json.loads(payload["messages"][1]["content"])
            response = {"sections": [{"section_id": s["section_id"], "text": "\n\n".join("{"+f["ref"]+"}" for f in s["findings"])} for s in data["sections"]]}
            return httpx.Response(200, json={"model": settings.model, "choices": [{"finish_reason": "stop", "message": {"role": "assistant", "content": json.dumps(response)}}]})
        client = GroqClient(settings, transport=httpx.MockTransport(handler)) if options.mock else None
        report = generate_interactive(request, settings=settings, client=client)
        prefix = module + ("-live" if live else "-mock" if options.mock else "")
        (output / f"{prefix}.json").write_text(report.model_dump_json(indent=2), encoding="utf-8")
        (output / f"{prefix}.txt").write_text(report.export_text, encoding="utf-8")
        records.append(dict(module=module, **report.generation.model_dump()))
        if options.mock:
            assert len(calls) == 1 and report.generation.used_mode == "GROQ_AI"
            records[-1].update(mock_http_requests=len(calls), prompt_bytes=calls[0])
    (output / ("live-summary.json" if live else "mock-summary.json" if options.mock else "offline-summary.json")).write_text(json.dumps(records, indent=2), encoding="utf-8")
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
