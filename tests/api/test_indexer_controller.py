from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.indexer_controller import indexer_route

app = FastAPI()
app.include_router(indexer_route)

client = TestClient(app)


def test_api_index_metadata_success():
    mock_result = {"status": "ok"}
    payload = {"workflow_code": "abc"}

    with patch("src.api.indexer_controller.index_metadata") as mock_index:
        mock_index.return_value = mock_result

        response = client.post("/index", json=payload)

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_index.assert_called_once_with(payload, "APIM")


def test_api_index_metadata_exception():
    payload = {"workflow_code": "abc"}

    with patch("src.api.indexer_controller.index_metadata") as mock_index:
        mock_index.side_effect = Exception("failure")

        response = client.post("/index", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao indexar: failure"
    mock_index.assert_called_once_with(payload, "APIM")


def test_api_remove_metadata_success():
    payload = {"CD_INDEXER_DELETE_document_id": "abc"}
    mock_result = {"deleted": True}

    with patch("src.api.indexer_controller.remove_metadata") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.post("/index/remove", json=payload)

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with(payload, "APIM")


def test_api_list_index_items_success():
    mock_result = {"items": [1, 2, 3]}

    with patch("src.api.indexer_controller.list_index_items") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.get("/index/test_index")

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with("test_index", "", "", 0, 10, "APIM")


def test_api_index_info_success():
    mock_result = {"info": "details"}

    with patch("src.api.indexer_controller.index_info") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.get("/index/test_index/informacoes")

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with("test_index", "APIM")


def test_api_delete_index_success():
    mock_result = {"deleted": True}

    with patch("src.api.indexer_controller.delete_index") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.delete("/index/test_index")

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with("test_index", "APIM")


def test_api_lote_success():
    payload = {"batch_indexer_id": "abc"}
    mock_result = {"status": "ok"}

    with patch("src.api.indexer_controller.lote") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.post("/lote", json=payload)

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with(payload, "APIM")


def test_api_workflow_template_success():
    payload = {"workflow_configuration_code": "abc"}
    mock_result = {"template": "data"}

    with patch("src.api.indexer_controller.workflow_template") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.post("/orchestrators/template-workflow", json=payload)

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with(payload, "APIM")


def test_api_start_workflow_success():
    payload = {"workflow_configuration_code": "abc"}
    mock_result = {"workflow_id": "123"}

    with patch("src.api.indexer_controller.start_workflow") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.post("/orchestrators/start-workflow", json=payload)

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with(payload, "APIM")


# --- Testes de exceção --- #

def test_api_remove_metadata_exception():
    payload = {"CD_INDEXER_DELETE_document_id": "abc"}

    with patch("src.api.indexer_controller.remove_metadata") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.post("/index/remove", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao remover metadados: failure"


def test_api_list_index_items_exception():
    with patch("src.api.indexer_controller.list_index_items") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.get("/index/test_index")

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao listar itens: failure"


def test_api_index_info_exception():
    with patch("src.api.indexer_controller.index_info") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.get("/index/test_index/informacoes")

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao recuperar informações do índice: failure"


def test_api_delete_index_exception():
    with patch("src.api.indexer_controller.delete_index") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.delete("/index/test_index")

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao excluir índice: failure"


def test_api_lote_exception():
    payload = {"batch_indexer_id": "abc"}

    with patch("src.api.indexer_controller.lote") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.post("/lote", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao consultar estado do lote: failure"


def test_api_workflow_template_exception():
    payload = {"workflow_configuration_code": "abc"}

    with patch("src.api.indexer_controller.workflow_template") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.post("/orchestrators/template-workflow", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao obter template do workflow: failure"


def test_api_start_workflow_exception():
    payload = {"workflow_configuration_code": "abc"}

    with patch("src.api.indexer_controller.start_workflow") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.post("/orchestrators/start-workflow", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao iniciar workflow: failure"