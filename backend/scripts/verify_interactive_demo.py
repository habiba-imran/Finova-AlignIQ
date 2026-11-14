"""Reproducible synthetic acceptance artifacts; --live explicitly probes configured Groq.

Never prints credentials or provider response bodies. No submitted patient data.
"""
import argparse
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from app.development_env import load_development_env
from app.domain.models import RawTMTSubmission
from app.interactive.service import generate_interactive, load_wording_settings
from app.interactive.narrative import load_planning_settings
from app.parser.cloud import ParserSettings
from app.parser.pipeline import automatic_parse
from app.reports.settings import ReportSettings, load_settings


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--live", action="store_true")
    options = args.parse_args()
    samples = runpy.run_path(str(ROOT / "backend/tests/test_interactive.py"))
    evidence = ROOT / "evidence/interactive-demo"
    if options.live:
        load_development_env(ROOT / ".env.local")
        settings = load_wording_settings()
        results = []
        for module in ("macro", "micro", "nano"):
            report = generate_interactive(samples["submission"](samples["LARGE"], module), settings=load_planning_settings() if module == "macro" else settings)
            results.append({"module": module, "generation": report.generation.model_dump(mode="json"),
                "notice": report.wording_notice, "tooth_tokens": len(report.observations), "positions": len(report.parsed.measurements)})
        write(evidence / "live-groq.json", {"configured": settings.configured, "results": results})
        print(json.dumps({"configured": settings.configured, "results": results}))
        return
    summaries, examples = [], []
    for name in ("ROWS", "COLUMNS", "MARKDOWN", "LARGE"):
        raw = samples[name]
        examples.append({"id": name.lower(), "raw_text": raw})
        for module in ("macro", "micro", "nano"):
            report = generate_interactive(samples["submission"](raw, module), settings=ReportSettings())
            summaries.append({"sample": name, "module": module, "positions": len(report.parsed.measurements), "teeth": len(report.observations), "illustrations": len(report.illustrations), "generation": report.generation.model_dump(mode="json")})
            if name == "ROWS":
                write(ROOT / f"frontend/src/test/fixtures/interactive-{module}.json", report.model_dump(mode="json"))
            if name == "LARGE":
                write(evidence / f"{module}-112.json", report.model_dump(mode="json"))
                (evidence / f"{module}-112.txt").write_text(report.export_text, encoding="utf-8")
    raw = samples["ROWS"]
    parsed = automatic_parse(RawTMTSubmission(raw_text=raw, synthetic_data_confirmed=True), settings=ParserSettings())
    write(ROOT / "frontend/src/test/fixtures/interactive-input.json", parsed.model_dump(mode="json"))
    write(ROOT / "examples/interactive-synthetic-tmts.json", examples)
    write(evidence / "synthetic-summary.json", summaries)
    print(f"Verified artifacts for {len(summaries)} synthetic reviews; no provider calls.")


if __name__ == "__main__":
    main()
