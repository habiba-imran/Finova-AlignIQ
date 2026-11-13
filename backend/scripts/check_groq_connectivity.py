"""Explicit opt-in, one fixed synthetic request per key. Never invoked by pytest.

This checks actual transport/model/schema/validators, not vendor evidence or the
eligibility of clinical findings. No raw responses, keys or provider errors print.
"""

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.development_env import load_development_env  # noqa: E402
from app.parser.certification import certify_markdown, structural_prompt, validate_proposal  # noqa: E402
from app.parser.cloud import ParserSettings  # noqa: E402
from app.parser.contracts import StructuralProposal  # noqa: E402
from app.parser.synthetic import synthetic_examples  # noqa: E402
from app.reports.groq_client import GroqClient  # noqa: E402
from app.reports.prompt import build_prompt  # noqa: E402
from app.reports.settings import ReportSettings  # noqa: E402
from app.reports.validation import validate_wording  # noqa: E402
from app.review.models import Finding, RuleRef  # noqa: E402
from app.review.templates import TEMPLATES  # noqa: E402


def comment_probe():
    # A synthetic unavailable placeholder, never an authorized observation/report.
    # Only its enum-like alias and approved wording options enter build_prompt.
    placeholder = Finding(finding_id="SYNTHETIC_CONNECTIVITY_ONLY", rule_id="D01", triggering_rules=(RuleRef(rule_id="D01"),),
                          status="SEMANTICS_UNKNOWN", applicable=None, evaluated=False, finding_type="UNAVAILABLE",
                          template_id="inventory", message=TEMPLATES["inventory"], abstain_reason="SYNTHETIC_TRANSPORT_CHECK_ONLY")
    return build_prompt((placeholder,))


def probe(service: str, *, transport=None) -> dict:
    key_name = "GROQ_API_KEY" if service == "comments" else "GROQ_API_KEY_2"
    key = os.environ.get(key_name, "")
    if not key:
        return {"service": service, "status": "SKIPPED", "reason": "KEY_NOT_CONFIGURED", "attempts": 0}
    if service == "comments":
        config = ReportSettings(api_key=key, synthetic_transmission_enabled=True, timeout_seconds=8)
        messages, refs = comment_probe()
        response = GroqClient(config, transport=transport).generate(messages)
        valid = False
        validation = response.code
        if response.content is not None:
            accepted, validation = validate_wording(response.content, refs)
            valid = validation == "GROQ_VALIDATED" and len(accepted) == 1
    else:
        config = ParserSettings(api_key=key, synthetic_transmission_enabled=True, environment="development", timeout_seconds=15)
        raw = next(f["raw_text"] for f in synthetic_examples() if f["id"] == "synthetic-markdown-columns")
        certificate = certify_markdown(raw)
        schema = {"type": "json_schema", "json_schema": {"name": "finova_structure_v1", "strict": True,
                  "schema": StructuralProposal.model_json_schema(mode="validation")}}
        response = GroqClient(config, transport=transport).generate(structural_prompt(certificate), response_schema=schema)
        valid = response.content is not None and validate_proposal(response.content, certificate)
        validation = "ALL_CELL_ASSOCIATIONS_CERTIFIED" if valid else "PROPOSAL_REJECTED" if response.content else response.code
    metrics = asdict(response)
    metrics.pop("content")  # Never retain model output, even from these fixed synthetic probes.
    return {"service": service, "status": "PASSED" if valid and response.model_matches is True else "FAILED",
            "validation": validation, "requested_model": config.model, "synthetic_only": True,
            "authentication": "ACCEPTED" if response.http_status == 200 else "REJECTED" if response.http_status in {401, 403} else "NOT_ESTABLISHED",
            "strict_structured_output_validated": valid, **metrics}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Explicitly authorize at most one small synthetic request per configured service")
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--service", choices=["both", "comments", "parser"], default="both")
    args = parser.parse_args()
    if not args.live:
        print(json.dumps({"status": "SKIPPED", "reason": "EXPLICIT_LIVE_OPT_IN_REQUIRED", "attempts": 0}))
        return 0
    if args.env_file:
        try: load_development_env(args.env_file)
        except ValueError:
            print(json.dumps({"status": "FAILED", "reason": "DEVELOPMENT_ENV_UNAVAILABLE_OR_INVALID", "attempts": 0}))
            return 1
    services = ("comments", "parser") if args.service == "both" else (args.service,)
    results = [probe(s) for s in services]
    print(json.dumps({"checked_at_utc": datetime.now(timezone.utc).isoformat(), "results": results}, indent=2))
    return int(any(r["status"] == "FAILED" for r in results))


if __name__ == "__main__":
    raise SystemExit(main())
