import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from src.api.filemanager_controller import filemanager_route

app = FastAPI()
app.include_router(filemanager_route)

client = TestClient(app)

def test_upload_pdf_success():
    file_content = b"%PDF-1.4 fake pdf content"

    with patch("src.api.filemanager_controller.upload_file") as mock_upload:
        mock_upload.return_value = "12345"

        response = client.post(
            "/upload_file",
            files={"file": ("test.pdf", file_content, "application/pdf")}
        )

    assert response.status_code == 200
    assert response.json() == {"file_id": "12345"}
    mock_upload.assert_called_once()


def test_download_file_success():
    mock_result = {
        "file_id": "123",
        "download_url": "https://storage/test.pdf"
    }

    with patch("src.api.filemanager_controller.download_file") as mock_download:
        mock_download.return_value = mock_result

        response = client.post("/download_file/123")

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_download.assert_called_once_with("123", "APIM")


def test_delete_file_success():
    mock_result = {"message": "Arquivo deletado com sucesso"}

    with patch("src.api.filemanager_controller.delete_file") as mock_delete:
        mock_delete.return_value = mock_result

        response = client.delete("/delete_file/123")

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_delete.assert_called_once_with("123", "APIM")


def test_list_files_success():
    mock_result = {
        "files": [
            {"file_id": "1", "file_name": "file1.pdf"},
            {"file_id": "2", "file_name": "file2.pdf"}
        ],
        "page": 0,
        "page_size": 10
    }

    with patch("src.api.filemanager_controller.list_files") as mock_list:
        mock_list.return_value = mock_result

        response = client.get("/list_files")

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_list.assert_called_once_with("", "", "", 0, 10, "APIM")


def test_list_files_internal_error():
    with patch("src.api.filemanager_controller.list_files") as mock_list:
        mock_list.side_effect = Exception("Azure error")

        response = client.get("/list_files")

    assert response.status_code == 500
    assert "Erro ao listar arquivos" in response.json()["detail"]


def test_get_container_success():
    mock_result = {
        "container_name": "meu-container",
        "sas_url": "https://seu-recurso.blob.core.windows.net/meu-container?sas_token"
    }

    with patch("src.api.filemanager_controller.get_container") as mock_get_container:
        mock_get_container.return_value = mock_result

        response = client.get("/get_container/meu-container")

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_get_container.assert_called_once_with("meu-container", "APIM")


def test_get_container_internal_error():
    with patch("src.api.filemanager_controller.get_container") as mock_get_container:
        mock_get_container.side_effect = Exception("Azure error")

        response = client.get("/get_container/meu-container")

    assert response.status_code == 500
    assert "Erro ao obter container" in response.json()["detail"]

def test_get_container_files_success():
    mock_result = {
        "files": [
            {"name": "doc1.pdf"},
            {"name": "doc2.pdf"}
        ]
    }

    with patch("src.api.filemanager_controller.get_container_files") as mock_get_files:
        mock_get_files.return_value = mock_result

        response = client.get(
            "/get_container_files",
            params={"path": "docs", "container_name": "meu-container"}
        )

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_get_files.assert_called_once_with("docs", "meu-container", "APIM")


def test_get_container_files_internal_error():
    with patch("src.api.filemanager_controller.get_container_files") as mock_get_files:
        mock_get_files.side_effect = Exception("Azure error")

        response = client.get(
            "/get_container_files",
            params={"path": "docs", "container_name": "meu-container"}
        )

    assert response.status_code == 500
    assert "Erro ao listar arquivos do container" in response.json()["detail"]