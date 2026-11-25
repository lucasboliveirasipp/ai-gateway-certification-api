from unittest.mock import patch, MagicMock
import requests

from src.domain.filemanager import (
    upload_file,
    download_file,
    delete_file,
    list_files,
    get_container,
    get_container_files,
)


# -------------------------
# UPLOAD FILE
# -------------------------

def test_upload_file_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "file123"}
    mock_response.raise_for_status.return_value = None

    with patch("src.domain.filemanager.Autenticator") as mock_auth, \
         patch("src.domain.filemanager.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.file_manager_url = "http://test"

        mock_post.return_value = mock_response

        result = upload_file(
            "file.pdf",
            b"bytes",
            "container",
            True,
            True,
            "APIM"
        )

    assert result == {"id": "file123"}


def test_upload_file_exception():

    with patch("src.domain.filemanager.Autenticator") as mock_auth, \
         patch("src.domain.filemanager.session.post") as mock_post:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.file_manager_url = "http://test"

        mock_post.side_effect = requests.RequestException("error")

        result = upload_file(
            "file.pdf",
            b"bytes",
            "container",
            True,
            True,
            "APIM"
        )

    assert result is None


# -------------------------
# DOWNLOAD FILE
# -------------------------

def test_download_file_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"file": "data"}

    with patch("src.domain.filemanager.Autenticator") as mock_auth, \
         patch("src.domain.filemanager.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.file_manager_url = "http://test"

        mock_get.return_value = mock_response

        result = download_file("123", "APIM")

    assert result == {"file": "data"}


def test_download_file_exception():

    with patch("src.domain.filemanager.Autenticator") as mock_auth, \
         patch("src.domain.filemanager.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.file_manager_url = "http://test"

        mock_get.side_effect = requests.exceptions.RequestException()

        result = download_file("123", "APIM")

    assert result is None


# -------------------------
# DELETE FILE
# -------------------------

def test_delete_file_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"deleted": True}

    with patch("src.domain.filemanager.Autenticator") as mock_auth, \
         patch("src.domain.filemanager.session.delete") as mock_delete:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.file_manager_url = "http://test"

        mock_delete.return_value = mock_response

        result = delete_file("123", "APIM")

    assert result == {"deleted": True}


def test_delete_file_exception():

    with patch("src.domain.filemanager.Autenticator") as mock_auth, \
         patch("src.domain.filemanager.session.delete") as mock_delete:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.file_manager_url = "http://test"

        mock_delete.side_effect = requests.exceptions.RequestException()

        result = delete_file("123", "APIM")

    assert result is None


# -------------------------
# LIST FILES
# -------------------------

def test_list_files_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"files": []}

    with patch("src.domain.filemanager.Autenticator") as mock_auth, \
         patch("src.domain.filemanager.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.file_manager_url = "http://test"

        mock_get.return_value = mock_response

        result = list_files(
            "file",
            "2024-01-01",
            "container",
            1,
            10,
            "APIM"
        )

    assert result == {"files": []}


def test_list_files_exception():

    with patch("src.domain.filemanager.Autenticator") as mock_auth, \
         patch("src.domain.filemanager.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.file_manager_url = "http://test"

        mock_get.side_effect = requests.exceptions.RequestException()

        result = list_files(
            "file",
            "2024-01-01",
            "container",
            1,
            10,
            "APIM"
        )

    assert result is None


# -------------------------
# GET CONTAINER
# -------------------------

def test_get_container_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"container": "data"}

    with patch("src.domain.filemanager.Autenticator") as mock_auth, \
         patch("src.domain.filemanager.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.file_manager_url = "http://test"

        mock_get.return_value = mock_response

        result = get_container("container", "APIM")

    assert result == {"container": "data"}


def test_get_container_exception():

    with patch("src.domain.filemanager.Autenticator") as mock_auth, \
         patch("src.domain.filemanager.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.file_manager_url = "http://test"

        mock_get.side_effect = requests.exceptions.RequestException()

        result = get_container("container", "APIM")

    assert result is None


# -------------------------
# GET CONTAINER FILES
# -------------------------

def test_get_container_files_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {"files": []}

    with patch("src.domain.filemanager.Autenticator") as mock_auth, \
         patch("src.domain.filemanager.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.file_manager_url = "http://test"

        mock_get.return_value = mock_response

        result = get_container_files("path", "container", "APIM")

    assert result == {"files": []}


def test_get_container_files_exception():

    with patch("src.domain.filemanager.Autenticator") as mock_auth, \
         patch("src.domain.filemanager.session.get") as mock_get:

        mock_auth.return_value.get_token.return_value = "token"
        mock_auth.return_value.file_manager_url = "http://test"

        mock_get.side_effect = requests.exceptions.RequestException()

        result = get_container_files("path", "container", "APIM")

    assert result is None