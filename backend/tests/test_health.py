from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "finova-aligniq", "phase": 1}


def test_only_authorized_routes_exist():
    paths = app.openapi()["paths"]
    assert set(paths) == {"/api/health", "/api/parse", "/api/v1/tmt/observations", "/api/v1/reports/draft",
                          "/api/v1/tmt/parse", "/api/v1/tmt/parse/assisted", "/api/v1/development/synthetic"}
    assert set(paths["/api/health"]) == {"get"}
    assert set(paths["/api/parse"]) == {"post"}
    assert set(paths["/api/v1/tmt/observations"]) == {"post"}
    assert set(paths["/api/v1/reports/draft"]) == {"post"}
    assert set(paths["/api/v1/tmt/parse"]) == {"post"}
    assert set(paths["/api/v1/tmt/parse/assisted"]) == {"post"}
    assert client.get("/openapi.json").status_code == 404


def test_no_input_submission_endpoint():
    assert client.post("/api/health").status_code == 405
    assert client.post("/api/analyze").status_code == 404
