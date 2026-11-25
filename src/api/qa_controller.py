
from fastapi import APIRouter, Query, HTTPException
from typing import Literal, Optional, Dict, List
from src.utils import CONNECTION_DESCRIPTION
from src.domain.qa import (
    ask_question, answer, side_histories,
    chat_history, delete_chat_history, end_chat
)

qa_route = APIRouter()

@qa_route.post("/chats/questions", tags=["QA"], summary="Envia uma pergunta e obtém resposta síncrona")
def api_ask_question(
        payload: dict = {
            "db_name": "genai-qa",
            "db_container": "chat",
            "step_workflow_code": "STEP_QA_DEMO",
            "workflow_code": "WF_QA_DEMO_SYNC",
            "question": "Do que você pode falar?"
        },
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return ask_question(payload, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar pergunta: {str(e)}")

@qa_route.get("/chats/answers", tags=["QA"], summary="Recupera resposta de forma assíncrona")
def api_get_answer(
        id_context: str,
        db_name: Optional[str] = "genai-qa",
        db_container: Optional[str] = "chat", 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return answer(id_context, db_name, db_container, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter resposta: {str(e)}")

@qa_route.get("/chats/side-histories", tags=["QA"], summary="Retorna histórico resumido para barra lateral")
def api_get_side_histories(    
        sort_column: str,
        sort_order: str,
        page: int = 0,
        size: int = 10,
        db_name: Optional[str] = "genai-qa",
        db_container: Optional[str] = "chat", 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return side_histories(page, size, sort_column, sort_order, db_name, db_container, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter histórico resumido: {str(e)}")

@qa_route.get("/chats/histories", tags=["QA"], summary="Retorna histórico completo de uma conversa")
def api_get_chat_history(
        id_context: str,
        db_name: Optional[str] = "genai-qa",
        db_container: Optional[str] = "chat", 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return chat_history(id_context, db_name, db_container, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter histórico completo: {str(e)}")

@qa_route.delete("/chats/histories", tags=["QA"], summary="Remove histórico completo de uma conversa")
def api_delete_chat_history(
        id_context: str,
        db_name: Optional[str] = "genai-qa",
        db_container: Optional[str] = "chat", 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return delete_chat_history(id_context, db_name, db_container, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir histórico: {str(e)}")

@qa_route.post("/chats/end", tags=["QA"], summary="Bloqueia a conversa")
def api_end_chat(
        id_context: str,
        db_name: str = "genai-qa",
        db_container: str = "chat", 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return end_chat(id_context, db_name, db_container, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao encerrar chat: {str(e)}")
