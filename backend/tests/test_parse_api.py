import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.domain.models import MAX_REQUEST_BYTES, ParseResult, RawTMTSubmission
from app.main import app

client = TestClient(app)
RAW = "# SYNTHETIC\r\nTooth\tRotation (deg)\r\n13\t−1.2300 M\r\n"


def payload(**overrides):
    return {"raw_text": RAW, "source_claim": "ClinCheck", "synthetic_data_confirmed": True, **overrides}


def test_parse_contract_exact_decimal_raw_and_no_cache(caplog):
    caplog.set_level("DEBUG")
    response = client.post("/api/parse", json=payload())
    assert response.status_code == 200
    data = response.json()
    assert data["raw_text"] == RAW
    assert data["measurements"][0]["signed_decimal"] == "-1.2300"
    assert data["measurements"][0]["magnitude_decimal"] == "1.2300"
    assert data["source"]["verification_status"] == "UNVERIFIED"
    assert data["source"]["candidate_adapter"]["verified"] is False
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert "not for clinical use" in data["notice"]
    assert RAW not in caplog.text
    # Decimal strings deserialize through JSON, without binary floating point.
    assert ParseResult.model_validate_json(response.content).raw_text == RAW


@pytest.mark.parametrize("overrides", [
    {"raw_text": 42}, {"raw_text": None}, {"raw_text": "x" * 100_001},
    {"source_claim": "SomeOtherVendor"}, {"context": {"source_verified": True}},
    {"context": {"stage_index": -1}}, {"context": {"stage_index": True}},
    {"context": {"notation": "auto"}}, {"synthetic_data_confirmed": False},
    {"synthetic_data_confirmed": 1}, {"raw_text": "\ud800"},
    {"context": {"source_version": "\ud800"}},
    {"context": {"stage_index": 2147483648}},
])
def test_invalid_requests_are_sanitized(overrides):
    response = client.post("/api/parse", content=json.dumps(payload(**overrides)), headers={"Content-Type": "application/json"})
    assert response.status_code == 422
    assert set(response.json()) == {"detail"}
    assert response.headers["cache-control"] == "no-store"
    assert "raw_text" not in response.text
    assert "x" * 100 not in response.text


def test_unknown_extra_keys_and_invalid_json_are_not_echoed():
    for kwargs in [
        {"json": payload(**{"DO_NOT_ECHO_SYNTHETIC_IDENTIFIER": RAW})},
        {"content": '{"raw_text":"DO_NOT_ECHO_SYNTHETIC_IDENTIFIER",', "headers": {"Content-Type": "application/json"}},
        {"json": {"raw_text": RAW}},
    ]:
        response = client.post("/api/parse", **kwargs)
        assert response.status_code == 422
        assert "DO_NOT_ECHO_SYNTHETIC_IDENTIFIER" not in response.text
        assert RAW not in response.text


def test_unsupported_input_is_a_structured_abstention_not_http_failure():
    response = client.post("/api/parse", json=payload(raw_text="not a table"))
    assert response.status_code == 200
    assert response.json()["status"] == "UNSUPPORTED"
    assert response.json()["measurements"] == []


def test_declared_and_chunked_body_size_limits():
    oversized = b"x" * (MAX_REQUEST_BYTES + 1)
    for content in [oversized, iter([oversized[:500_000], oversized[500_000:]])]:
        response = client.post("/api/parse", content=content, headers={"Content-Type": "application/json"})
        assert response.status_code == 413
        assert "x" * 100 not in response.text
        assert response.headers["cache-control"] == "no-store"


def test_exported_schema_is_current_and_decimals_serialize_as_strings():
    directory = Path(__file__).resolve().parents[2] / "schemas"
    for name, model, mode in [("parse-request.v1.json", RawTMTSubmission, "validation"), ("parse-result.v1.json", ParseResult, "serialization")]:
        assert json.loads((directory / name).read_text(encoding="utf-8")) == model.model_json_schema(mode=mode)
    result_schema = ParseResult.model_json_schema(mode="serialization")
    numeric = result_schema["$defs"]["ParsedMeasurement"]["properties"]["signed_decimal"]
    assert {entry["type"] for entry in numeric["anyOf"]} == {"string", "null"}
