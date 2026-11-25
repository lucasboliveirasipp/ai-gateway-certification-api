from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_app_metadata():
    assert app.title == "Hub BFF Gateway"
    assert app.description == "API de validação dos endpoints da gateway"
    assert app.version == "0.1.1"
    assert app.root_path == "/api-certificacao-gateway"


def test_docs_endpoints():
    response = client.get("/docs")
    assert response.status_code == 200

    response = client.get("/redoc")
    assert response.status_code == 200

    response = client.get("/openapi.json")
    assert response.status_code == 200

