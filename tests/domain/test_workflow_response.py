from unittest.mock import patch, MagicMock
import requests

from src.domain.workflow_response import get_workflow_execution_status


def test_get_workflow_execution_status_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "completed"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.workflow_response.Autenticator") as mock_auth, \
         patch("src.domain.workflow_response.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.workflow_response_url = "http://test"

        mock_get.return_value = mock_response

        result = get_workflow_execution_status("123", "APIM")

    assert result == {"status": "completed"}

def test_get_workflow_execution_status_exception():

    with patch("src.domain.workflow_response.Autenticator") as mock_auth, \
         patch("src.domain.workflow_response.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.workflow_response_url = "http://test"

        mock_get.side_effect = requests.RequestException()

        result = get_workflow_execution_status("123", "APIM")

    assert result is None