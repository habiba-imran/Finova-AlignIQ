"""Revalidate captured synthetic Groq prose without a network request.

These are real provider responses, not hand-authored expected paragraphs. The
generation attempt describes the captured request; this script makes zero calls.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from app.interactive.models import InteractiveSubmission
from app.interactive.narrative import PlanningWordingSettings
from app.interactive.service import generate_interactive
from app.reports.groq_client import GroqResult


def main():
    output = ROOT / "evidence/unified-wording"
    original = json.loads((ROOT / "evidence/planning-wording/user-synthetic-live-report.json").read_text(encoding="utf-8"))["parsed"]
    summary = []
    for module in ("macro", "micro", "nano"):
        capture = (output / f"captured-{module}.json").read_text(encoding="utf-8")

        class CapturedResponse:
            def generate(self, messages, *, response_schema):
                return GroqResult(capture, "GROQ_RESPONSE_RECEIVED", 1, http_status=200)

        request = InteractiveSubmission(raw_text=original["raw_text"], raw_sha256=original["raw_sha256"],
            synthetic_data_confirmed=True, module=module, context=original["source"]["context"])
        report = generate_interactive(request, settings=PlanningWordingSettings(api_key="OFFLINE_REPLAY_ONLY", synthetic_transmission_enabled=True), client=CapturedResponse())
        assert report.generation.used_mode == "GROQ_AI", (module, report.generation.reason)
        assert report.generation.accepted_comments == len(report.observations) == 16
        assert len(report.parsed.measurements) == 112
        assert len(report.engine_review.evaluations) == 96
        (output / f"approved-{module}.json").write_text(report.model_dump_json(indent=2) + "\n", encoding="utf-8")
        (output / f"approved-{module}.txt").write_text(report.export_text, encoding="utf-8")
        summary.append({"module": module, "verification": "OFFLINE_REVALIDATION_OF_CAPTURED_REAL_PROVIDER_RESPONSE",
            "new_provider_calls": 0, "capture_sha256": hashlib.sha256(capture.encode()).hexdigest(),
            "accepted_comments": report.generation.accepted_comments,
            "distinct_first_three_words": len({tuple(o.text.lower().split()[:3]) for o in report.observations}),
            "positions": len(report.parsed.measurements), "rules": len(report.engine_review.evaluations)})
    (output / "approved-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
