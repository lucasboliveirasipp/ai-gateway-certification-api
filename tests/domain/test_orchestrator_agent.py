from unittest.mock import patch, MagicMock
import requests

from src.domain.orchestrator_agent import call_agent


# -------------------------
# CALL AGENT SUCCESS
# -------------------------

def test_call_agent_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"result": "ok"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.orchestrator_agent.Autenticator") as mock_auth, \
         patch("src.domain.orchestrator_agent.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.orchestrator_agent_url = "http://test"

        mock_post.return_value = mock_response

        result = call_agent(
            "agent-code",
            "1.0",
            {"input": "data"},
            "APIM"
        )

    assert result == {"result": "ok"}


# -------------------------
# CALL AGENT EXCEPTION
# -------------------------

def test_call_agent_exception():

    with patch("src.domain.orchestrator_agent.Autenticator") as mock_auth, \
         patch("src.domain.orchestrator_agent.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.orchestrator_agent_url = "http://test"

        mock_post.side_effect = requests.RequestException()

        result = call_agent(
            "agent-code",
            "1.0",
            {"input": "data"},
            "APIM"
        )

    assert result is None