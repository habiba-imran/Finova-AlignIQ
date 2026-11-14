"""Reproducible synthetic HTTP/library probes; never performs a live provider call."""
from collections import Counter
import json
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402
from app.planning.demo import demo_report  # noqa: E402
from app.reports.groq_client import GroqClient, GroqResult  # noqa: E402
from app.review.registry import RULES  # noqa: E402
from app.semantics.registry import APPROVED_RELEASE_DIGESTS  # noqa: E402


def main():
    client = TestClient(app)
    cases = {
        "clean": "Tooth\tRotation (deg)\tExtrusion (mm)\n13\t-1.2300 M\t0.000 E\n14\t-\t0.200 E\n",
        "markdown": "| Tooth | Rotation (deg) |\n| --- | --- |\n| 13 | 0.000 M |\n",
        "ambiguous": "Tooth  Rotation (deg)  Extrusion (mm)\n13  1\n",
        "irrelevant": "Product\tPrice\nBook\t13\n",
        "unknown_vendor": "Source: SureSmile\nTooth\tRotation (deg)\n13\t999.000 M\n",
        "unverified_recoverable": "Tooth: 13\nRotation (deg):\n1.2300 M\n",
    }
    results = []
    with patch.object(GroqClient, "generate", side_effect=AssertionError("Unexpected provider call")):
        for name, raw in cases.items():
            payload = {"raw_text": raw, "synthetic_data_confirmed": True}
            parsed_response = client.post("/api/v1/tmt/parse", json=payload)
            assert parsed_response.status_code == 200
            parsed = parsed_response.json()
            record = {"case": name, "raw_sha256": parsed["raw_sha256"], "raw_preserved": parsed["raw_text"] == raw,
                      "classification": parsed["pipeline"]["quality"]["classification"],
                      "positions": len(parsed["measurements"]), "numeric_statuses": dict(Counter(m["numeric_status"] for m in parsed["measurements"])),
                      "parser_provider_attempts": parsed["pipeline"]["assistance"]["attempts"], "modules": {}}
            for module in ("planning", "attachments", "sequencing"):
                response = client.post(f"/api/v1/{module}/draft", json=payload)
                assert response.status_code == 200
                body = response.json()
                review = body["report"]["engine_review"] if module == "planning" else body["engine_review"]
                assert review["evidence_domain"] == "UNVERIFIED" and review["coverage"]["eligible_positions"] == 0
                assert len(review["evaluations"]) == 96
                assert review["raw_sha256"] == parsed["raw_sha256"]
                record["modules"][module] = {"http_status": response.status_code, "evidence_domain": review["evidence_domain"],
                    "coverage": review["coverage"], "evaluation_states": dict(Counter(e["status"] for e in review["evaluations"])),
                    "entry_states": dict(Counter(e["result_type"] for e in body.get("entries", []))),
                    "provider_attempts": body["report"]["generation"]["attempts"] if module == "planning" else body["provider_attempts"],
                    "export_contains_draft": "DRAFT — Requires Orthodontist Review" in body["export_text"]}
            results.append(record)
    demos = {}
    environment = {"FINOVA_ENVIRONMENT": "development", "FINOVA_PLANNING_DEMO_ENABLED": "true",
                   "FINOVA_ATTACHMENT_DEMO_ENABLED": "true", "FINOVA_SEQUENCER_DEMO_ENABLED": "true"}
    with patch.dict("os.environ", environment), patch.object(GroqClient, "generate", side_effect=AssertionError("Unexpected provider call")):
        for module, demo in (("planning", "planning"), ("attachments", "attachment"), ("sequencing", "sequencer")):
            response = client.post(f"/api/v1/development/{demo}-demo/draft", json={"comment_mode": "TEMPLATES"} if module == "planning" else {})
            assert response.status_code == 200
            body = response.json()
            review = body["report"]["engine_review"] if module == "planning" else body["engine_review"]
            demos[module] = {"evidence_domain": review["evidence_domain"], "coverage": review["coverage"],
                "rule_states": {e["rule_id"]: {k: e[k] for k in ("status", "execution", "evaluated", "implementation_kind")} for e in review["evaluations"]},
                "entry_states": dict(Counter(e["result_type"] for e in body.get("entries", []))),
                "origins": dict(Counter(e.get("origin", e.get("decision_origin")) for e in body.get("entries", [])))}
    with patch.dict("os.environ", {"GROQ_API_KEY": "SYNTHETIC_MOCK", "FINOVA_GROQ_SYNTHETIC_ENABLED": "true"}), patch.object(
        GroqClient, "generate", return_value=GroqResult(None, "GROQ_RATE_LIMIT", 1)) as mocked:
        fallback = demo_report("AUTO")
        assert mocked.call_count == 1 and fallback.report.generation.used_mode == "STANDARD_TEMPLATES"
        provider_failure = fallback.report.generation.model_dump(mode="json")
    print(json.dumps({"synthetic_only": True, "live_provider_calls": 0,
        "registry": {"total": len(RULES), "execution": dict(Counter(r.execution for r in RULES)),
                     "implementation_kind": dict(Counter(r.implementation_kind for r in RULES)),
                     "disposition": dict(Counter(r.disposition for r in RULES)), "approved_vendor_releases": len(APPROVED_RELEASE_DIGESTS)},
        "normal_cases": results, "fixed_demos": demos, "mocked_wording_failure": provider_failure}, indent=2))


if __name__ == "__main__":
    main()
