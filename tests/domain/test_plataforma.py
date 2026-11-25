from unittest.mock import patch, MagicMock
import pytest
import requests

from src.domain.plataforma import myself


# -------------------------
# MYSELF SUCCESS
# -------------------------

def test_myself_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"user": "teste"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.plataforma.Autenticator") as mock_auth, \
         patch("src.domain.plataforma.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.plataforma_url = "http://test"

        mock_get.return_value = mock_response

        result = myself("APIM")

    assert result == {"user": "teste"}


# -------------------------
# MYSELF EXCEPTION
# -------------------------

def test_myself_exception():

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.RequestException()

    with patch("src.domain.plataforma.Autenticator") as mock_auth, \
         patch("src.domain.plataforma.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.plataforma_url = "http://test"

        mock_get.return_value = mock_response

        with pytest.raises(requests.RequestException):
            myself("APIM")