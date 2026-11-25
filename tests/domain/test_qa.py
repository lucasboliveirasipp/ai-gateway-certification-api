from unittest.mock import patch, MagicMock
import requests

from src.domain.qa import (
    ask_question,
    answer,
    side_histories,
    chat_history,
    delete_chat_history,
    end_chat
)


# -------------------------
# ASK QUESTION
# -------------------------

def test_ask_question_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"answer": "ok"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.qa.Autenticator") as mock_auth, \
         patch("src.domain.qa.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.qa_url = "http://test"

        mock_post.return_value = mock_response

        result = ask_question({"question": "hello"}, "APIM")

    assert result == {"answer": "ok"}


def test_ask_question_exception():
    with patch("src.domain.qa.Autenticator") as mock_auth, \
         patch("src.domain.qa.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.qa_url = "http://test"

        mock_post.side_effect = requests.RequestException()

        result = ask_question({"question": "hello"}, "APIM")

    assert result is None


# -------------------------
# ANSWER
# -------------------------

def test_answer_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "ok"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.qa.Autenticator") as mock_auth, \
         patch("src.domain.qa.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.qa_url = "http://test"

        mock_get.return_value = mock_response

        result = answer("ctx1", "db", "container", "APIM")

    assert result == {"response": "ok"}


def test_answer_exception():
    with patch("src.domain.qa.Autenticator") as mock_auth, \
         patch("src.domain.qa.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.qa_url = "http://test"

        mock_get.side_effect = requests.RequestException()

        result = answer("ctx1", "db", "container", "APIM")

    assert result is None


# -------------------------
# SIDE HISTORIES
# -------------------------

def test_side_histories_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"histories": []}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.qa.Autenticator") as mock_auth, \
         patch("src.domain.qa.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.qa_url = "http://test"

        mock_get.return_value = mock_response

        result = side_histories(1, 10, "column", "asc", "db", "container", "APIM")

    assert result == {"histories": []}


def test_side_histories_exception():
    with patch("src.domain.qa.Autenticator") as mock_auth, \
         patch("src.domain.qa.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.qa_url = "http://test"

        mock_get.side_effect = requests.RequestException()

        result = side_histories(1, 10, "column", "asc", "db", "container", "APIM")

    assert result is None


# -------------------------
# CHAT HISTORY
# -------------------------

def test_chat_history_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"messages": []}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.qa.Autenticator") as mock_auth, \
         patch("src.domain.qa.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.qa_url = "http://test"

        mock_get.return_value = mock_response

        result = chat_history("ctx1", "db", "container", "APIM")

    assert result == {"messages": []}


def test_chat_history_exception():
    with patch("src.domain.qa.Autenticator") as mock_auth, \
         patch("src.domain.qa.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.qa_url = "http://test"

        mock_get.side_effect = requests.RequestException()

        result = chat_history("ctx1", "db", "container", "APIM")

    assert result is None


# -------------------------
# DELETE CHAT HISTORY
# -------------------------

def test_delete_chat_history_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"deleted": True}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.qa.Autenticator") as mock_auth, \
         patch("src.domain.qa.session.delete") as mock_delete:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.qa_url = "http://test"

        mock_delete.return_value = mock_response

        result = delete_chat_history("ctx1", "db", "container", "APIM")

    assert result == {"deleted": True}


def test_delete_chat_history_exception():
    with patch("src.domain.qa.Autenticator") as mock_auth, \
         patch("src.domain.qa.session.delete") as mock_delete:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.qa_url = "http://test"

        mock_delete.side_effect = requests.RequestException()

        result = delete_chat_history("ctx1", "db", "container", "APIM")

    assert result is None


# -------------------------
# END CHAT
# -------------------------

def test_end_chat_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"ended": True}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.qa.Autenticator") as mock_auth, \
         patch("src.domain.qa.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.qa_url = "http://test"

        mock_post.return_value = mock_response

        result = end_chat("ctx1", "db", "container", "APIM")

    assert result == {"ended": True}


def test_end_chat_exception():
    with patch("src.domain.qa.Autenticator") as mock_auth, \
         patch("src.domain.qa.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.qa_url = "http://test"

        mock_post.side_effect = requests.RequestException()

        result = end_chat("ctx1", "db", "container", "APIM")

    assert result is None