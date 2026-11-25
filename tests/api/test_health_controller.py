from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_liveness_endpoint():
    response = client.get("/health/liveness")

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Estado da aplicação"
    assert data["description"] == "Utilizado pela esteira para validar o estado da aplicação"
    assert data["version"] == "v1.0"
    assert data["status"] == "OK"


def test_readiness_endpoint():
    response = client.get("/health/readiness")

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Status da prontidão"
    assert data["description"] == "Utilizado pela esteira para validar a prontidão da aplicação"
    assert data["version"] == "v1.0"
    assert data["status"] == "OK"