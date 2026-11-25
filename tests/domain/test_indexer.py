from unittest.mock import patch, MagicMock
import requests

from src.domain.indexer import (
    index_metadata,
    remove_metadata,
    list_index_items,
    index_info,
    delete_index,
    lote,
    workflow_template,
    start_workflow
)


# -------------------------
# INDEX METADATA
# -------------------------

def test_index_metadata_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "indexed"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_post.return_value = mock_response

        result = index_metadata({"data": "test"}, "APIM")

    assert result == {"status": "indexed"}


def test_index_metadata_exception():

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_post.side_effect = requests.RequestException()

        result = index_metadata({"data": "test"}, "APIM")

    assert result is None


# -------------------------
# REMOVE METADATA
# -------------------------

def test_remove_metadata_success():

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_post.return_value = mock_response

        result = remove_metadata({"id": "123"}, "APIM")

    assert result == mock_response


def test_remove_metadata_exception():

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_post.side_effect = requests.RequestException()

        result = remove_metadata({"id": "123"}, "APIM")

    assert result is None



def test_list_index_items_exception():

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_get.side_effect = requests.RequestException()

        result = list_index_items(
            "index",
            "db",
            "container",
            1,
            10,
            "APIM"
        )

    assert result is None


# -------------------------
# INDEX INFO
# -------------------------

def test_index_info_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"name": "index"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_get.return_value = mock_response

        result = index_info("index", "APIM")

    assert result == {"name": "index"}


def test_index_info_exception():

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_get.side_effect = requests.RequestException()

        result = index_info("index", "APIM")

    assert result is None


# -------------------------
# DELETE INDEX
# -------------------------

def test_delete_index_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"deleted": True}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.delete") as mock_delete:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_delete.return_value = mock_response

        result = delete_index("index", "APIM")

    assert result == {"deleted": True}


def test_delete_index_exception():

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.delete") as mock_delete:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_delete.side_effect = requests.RequestException()

        result = delete_index("index", "APIM")

    assert result is None


# -------------------------
# LOTE
# -------------------------

def test_lote_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "running"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_post.return_value = mock_response

        result = lote({"id": "batch"}, "APIM")

    assert result == {"status": "running"}


def test_lote_exception():

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_post.side_effect = requests.RequestException()

        result = lote({"id": "batch"}, "APIM")

    assert result is None


# -------------------------
# WORKFLOW TEMPLATE
# -------------------------

def test_workflow_template_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"template": "ok"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_post.return_value = mock_response

        result = workflow_template({"wf": "1"}, "APIM")

    assert result == {"template": "ok"}


def test_workflow_template_exception():

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_post.side_effect = requests.RequestException()

        result = workflow_template({"wf": "1"}, "APIM")

    assert result is None


# -------------------------
# START WORKFLOW
# -------------------------

def test_start_workflow_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"workflow": "started"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_post.return_value = mock_response

        result = start_workflow({"wf": "1"}, "APIM")

    assert result == {"workflow": "started"}


def test_start_workflow_exception():

    with patch("src.domain.indexer.Autenticator") as mock_auth, \
         patch("src.domain.indexer.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.indexer_url = "http://test"

        mock_post.side_effect = requests.RequestException()

        result = start_workflow({"wf": "1"}, "APIM")

    assert result is None