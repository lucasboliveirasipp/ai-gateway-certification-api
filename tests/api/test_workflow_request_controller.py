import os
# tests/test_workflow_request.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.workflow_request_controller import workflow_request_route
from fastapi import FastAPI, Query

from src.domain.workflow_request import get_full_workflow_template, get_workflow_status, get_workflow_template, start_workflow
from src.utils import CONNECTION_DESCRIPTION

app = FastAPI()
app.include_router(workflow_request_route)

client = TestClient(app)

OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "")
MODEL_CHAT = "open_ai_chat_completion_body.model"
TEMPERATURE_CHAT = "open_ai_chat_completion_body.temperature"
MAX_TOKENS_CHAT = "open_ai_chat_completion_body.max_tokens"
TOP_P_CHAT = "open_ai_chat_completion_body.top_p"
FREQUENCY_PENALTY_CHAT = "open_ai_chat_completion_body.frequency_penalty"
PRESENCE_PENALTY_CHAT = "open_ai_chat_completion_body.presence_penalty"

@pytest.fixture
def mock_start_workflow():
    with patch("src.api.workflow_request_controller.start_workflow") as mock:
        mock.return_value = {"status": "success", "workflow_id": "12345"}
        yield mock

def test_api_start_workflow_default_payload(mock_start_workflow):
    response = client.post("/request/start-workflow")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["workflow_id"] == "12345"
    mock_start_workflow.assert_called_once()
    

def test_api_start_workflow_custom_payload(mock_start_workflow):
    payload = {
        "workflow_configuration_code": "CUSTOM_CODE",
        "input_collection": {}
    }
    response = client.post("/request/start-workflow?connection_mode=GATEWAY", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["workflow_id"] == "12345"
    mock_start_workflow.assert_called()

def test_api_get_full_workflow_template_success():
    mock_result = {"template": "full"}

    with patch("src.api.workflow_request_controller.get_full_workflow_template") as mock_fn:
        mock_fn.return_value = mock_result

        response = client.get(
            "/request/template-full-workflow",
            params={"workflow_configuration_code": "WF001"}
        )

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with("WF001", "APIM")


def test_api_get_full_workflow_template_exception():
    with patch("src.api.workflow_request_controller.get_full_workflow_template") as mock_fn:
        mock_fn.side_effect = Exception("failure")

        response = client.get(
            "/request/template-full-workflow",
            params={"workflow_configuration_code": "WF001"}
        )

    assert response.status_code == 500


# ---------------------------
# GET WORKFLOW TEMPLATE
# ---------------------------

def test_api_get_workflow_template_success():
    mock_result = {"template": "simple"}

    with patch("src.api.workflow_request_controller.get_workflow_template") as mock_fn:
        mock_fn.return_value = mock_result

        response = client.get(
            "/request/template-workflow",
            params={"workflow_configuration_code": "WF001"}
        )

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with("WF001", "APIM")


def test_api_get_workflow_template_exception():
    with patch("src.api.workflow_request_controller.get_workflow_template") as mock_fn:
        mock_fn.side_effect = Exception("failure")

        response = client.get(
            "/request/template-workflow",
            params={"workflow_configuration_code": "WF001"}
        )

    assert response.status_code == 500


# ---------------------------
# GET WORKFLOW STATUS
# ---------------------------

def test_api_get_workflow_status_success():
    mock_result = {"status": "completed"}

    with patch("src.api.workflow_request_controller.get_workflow_status") as mock_fn:
        mock_fn.return_value = mock_result

        response = client.get(
            "/request/workflow-status/123"
        )

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with("123", "APIM")


def test_api_get_workflow_status_exception():
    with patch("src.api.workflow_request_controller.get_workflow_status") as mock_fn:
        mock_fn.side_effect = Exception("failure")

        response = client.get(
            "/request/workflow-status/123"
        )

    assert response.status_code == 500