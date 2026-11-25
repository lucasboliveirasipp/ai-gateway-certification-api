from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.workflow_response_controller import workflow_response_route

app = FastAPI()
app.include_router(workflow_response_route)

client = TestClient(app)


# --- Teste de sucesso --- #
def test_api_get_workflow_execution_status_success():
    mock_result = {"status": "completed"}

    with patch("src.api.workflow_response_controller.get_workflow_execution_status") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.get("/response/workflow-execution-status/123")

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with("123", "APIM")


# --- Teste de exceção --- #
def test_api_get_workflow_execution_status_exception():
    with patch("src.api.workflow_response_controller.get_workflow_execution_status") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.get("/response/workflow-execution-status/123")

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao obter status do workflow: failure"