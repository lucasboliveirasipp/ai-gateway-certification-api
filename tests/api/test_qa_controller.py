from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.qa_controller import qa_route

app = FastAPI()
app.include_router(qa_route)

client = TestClient(app)

def test_api_ask_question_success():
    payload = {"question": "teste"}
    mock_result = {"answer": "resposta"}

    with patch("src.api.qa_controller.ask_question") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.post("/chats/questions", json=payload)

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with(payload, "APIM")


def test_api_get_answer_success():
    mock_result = {"answer": "resposta"}

    with patch("src.api.qa_controller.answer") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.get("/chats/answers", params={"id_context": "123"})

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with("123", "genai-qa", "chat", "APIM")


def test_api_get_side_histories_success():
    mock_result = {"histories": []}

    with patch("src.api.qa_controller.side_histories") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.get(
            "/chats/side-histories",
            params={"sort_column": "date", "sort_order": "asc"}
        )

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with(0, 10, "date", "asc", "genai-qa", "chat", "APIM")


def test_api_get_chat_history_success():
    mock_result = {"history": []}

    with patch("src.api.qa_controller.chat_history") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.get("/chats/histories", params={"id_context": "123"})

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with("123", "genai-qa", "chat", "APIM")


def test_api_delete_chat_history_success():
    mock_result = {"deleted": True}

    with patch("src.api.qa_controller.delete_chat_history") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.delete("/chats/histories", params={"id_context": "123"})

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with("123", "genai-qa", "chat", "APIM")


def test_api_end_chat_success():
    mock_result = {"ended": True}

    with patch("src.api.qa_controller.end_chat") as mock_fn:
        mock_fn.return_value = mock_result
        response = client.post("/chats/end", params={"id_context": "123"})

    assert response.status_code == 200
    assert response.json() == mock_result
    mock_fn.assert_called_once_with("123", "genai-qa", "chat", "APIM")


# --- Testes de exceção --- #

def test_api_ask_question_exception():
    payload = {"question": "teste"}

    with patch("src.api.qa_controller.ask_question") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.post("/chats/questions", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao realizar pergunta: failure"


def test_api_get_answer_exception():
    with patch("src.api.qa_controller.answer") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.get("/chats/answers", params={"id_context": "123"})

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao obter resposta: failure"


def test_api_get_side_histories_exception():
    with patch("src.api.qa_controller.side_histories") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.get(
            "/chats/side-histories",
            params={"sort_column": "date", "sort_order": "asc"}
        )

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao obter histórico resumido: failure"


def test_api_get_chat_history_exception():
    with patch("src.api.qa_controller.chat_history") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.get("/chats/histories", params={"id_context": "123"})

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao obter histórico completo: failure"


def test_api_delete_chat_history_exception():
    with patch("src.api.qa_controller.delete_chat_history") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.delete("/chats/histories", params={"id_context": "123"})

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao excluir histórico: failure"


def test_api_end_chat_exception():
    with patch("src.api.qa_controller.end_chat") as mock_fn:
        mock_fn.side_effect = Exception("failure")
        response = client.post("/chats/end", params={"id_context": "123"})

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao encerrar chat: failure"