from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.orchestrator_agent_controller import orchestrator_agent_route

app = FastAPI()
app.include_router(orchestrator_agent_route)

client = TestClient(app)


# --- Teste de sucesso --- #
def test_api_call_agent_success():
    payload = {
        "messages": [
            {"type": "text", "content": {"text": "o que você pode falar?"}}
        ],
        "session_id": "",
        "metadata": {}
    }
    mock_result = {"response": "ok"}

    with patch("src.api.orchestrator_agent_controller.call_agent") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.post("/call_agent", json=payload)

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with(
        "WF_AGENTE_FERRAMENTA",
        "draft",
        payload,
        "APIM"
    )


# --- Teste de exceção --- #
def test_api_call_agent_exception():
    payload = {
        "messages": [
            {"type": "text", "content": {"text": "o que você pode falar?"}}
        ],
        "session_id": "",
        "metadata": {}
    }

    with patch("src.api.orchestrator_agent_controller.call_agent") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.post("/call_agent", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao criar item: failure"