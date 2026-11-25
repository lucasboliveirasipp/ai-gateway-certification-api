from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.plataforma_controller import plataforma_route

app = FastAPI()
app.include_router(plataforma_route)

client = TestClient(app)


# --- Teste de sucesso --- #
def test_api_myself_success():
    mock_result = {"user": "teste"}

    with patch("src.api.plataforma_controller.myself") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.post("/myself")

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with("APIM")


# --- Teste de exceção --- #
def test_api_myself_exception():
    with patch("src.api.plataforma_controller.myself") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.post("/myself")

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao consultar dados do usuario: failure"