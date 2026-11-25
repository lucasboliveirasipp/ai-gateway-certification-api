from unittest.mock import patch, MagicMock
import requests

from src.domain.workflow_request import (
    start_workflow,
    get_full_workflow_template,
    get_workflow_template,
    get_workflow_status
)


# -------------------------
# START WORKFLOW
# -------------------------

def test_start_workflow_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"workflow": "started"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.workflow_request.Autenticator") as mock_auth, \
         patch("src.domain.workflow_request.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.workflow_request_url = "http://test"

        mock_post.return_value = mock_response

        result = start_workflow({"input": "data"}, "APIM")

    assert result == {"workflow": "started"}


def test_start_workflow_exception():

    with patch("src.domain.workflow_request.Autenticator") as mock_auth, \
         patch("src.domain.workflow_request.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.workflow_request_url = "http://test"

        mock_post.side_effect = requests.RequestException()

        result = start_workflow({"input": "data"}, "APIM")

    assert result is None


# -------------------------
# FULL WORKFLOW TEMPLATE
# -------------------------

def test_get_full_workflow_template_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"template": "full"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.workflow_request.Autenticator") as mock_auth, \
         patch("src.domain.workflow_request.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.workflow_request_url = "http://test"

        mock_get.return_value = mock_response

        result = get_full_workflow_template("WF001", "APIM")

    assert result == {"template": "full"}


def test_get_full_workflow_template_exception():

    with patch("src.domain.workflow_request.Autenticator") as mock_auth, \
         patch("src.domain.workflow_request.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.workflow_request_url = "http://test"

        mock_get.side_effect = requests.RequestException()

        result = get_full_workflow_template("WF001", "APIM")

    assert result is None


# -------------------------
# WORKFLOW TEMPLATE
# -------------------------

def test_get_workflow_template_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"template": "simple"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.workflow_request.Autenticator") as mock_auth, \
         patch("src.domain.workflow_request.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.workflow_request_url = "http://test"

        mock_get.return_value = mock_response

        result = get_workflow_template("WF001", "APIM")

    assert result == {"template": "simple"}


def test_get_workflow_template_exception():

    with patch("src.domain.workflow_request.Autenticator") as mock_auth, \
         patch("src.domain.workflow_request.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.workflow_request_url = "http://test"

        mock_get.side_effect = requests.RequestException()

        result = get_workflow_template("WF001", "APIM")

    assert result is None


# -------------------------
# WORKFLOW STATUS
# -------------------------

def test_get_workflow_status_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "running"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.workflow_request.Autenticator") as mock_auth, \
         patch("src.domain.workflow_request.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.workflow_request_url = "http://test"

        mock_get.return_value = mock_response

        result = get_workflow_status("123", "APIM")

    assert result == {"status": "running"}


def test_get_workflow_status_exception():

    with patch("src.domain.workflow_request.Autenticator") as mock_auth, \
         patch("src.domain.workflow_request.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.workflow_request_url = "http://test"

        mock_get.side_effect = requests.RequestException()

        result = get_workflow_status("123", "APIM")

    assert result is None