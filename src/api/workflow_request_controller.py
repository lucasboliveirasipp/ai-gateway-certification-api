import os

from fastapi import APIRouter, Query, HTTPException
from typing import Literal, Optional, Dict
from src.domain.workflow_request import (
    start_workflow, get_full_workflow_template, get_workflow_template,
    get_workflow_status
)
from src.utils import CONNECTION_DESCRIPTION

workflow_request_route = APIRouter()

OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "")
MODEL_CHAT = "open_ai_chat_completion_body.model"
TEMPERATURE_CHAT = "open_ai_chat_completion_body.temperature"
MAX_TOKENS_CHAT = "open_ai_chat_completion_body.max_tokens"
TOP_P_CHAT = "open_ai_chat_completion_body.top_p"
FREQUENCY_PENALTY_CHAT = "open_ai_chat_completion_body.frequency_penalty"
PRESENCE_PENALTY_CHAT = "open_ai_chat_completion_body.presence_penalty"

@workflow_request_route.post("/request/start-workflow", tags=["Workflow Request"], summary="Inicia execução de um workflow")
def api_start_workflow(
        payload: dict =
            {
            "workflow_configuration_code": "WF_TESTE_INDEXADOR_V2",
            "input_collection": {
                "input_properties": [
                    {
                        "workflow_step_order": 0,
                        "workflow_step_properties": [
                            {
                                "full_path": "CD_INDEXER_id_project",
                                "actual_value": "00000000-0000-0000-0000-000000000000*",
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_id_file_manager",
                                "actual_value": "00000000-0000-0000-0000-000000000000",
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_project_index",
                                "actual_value": "demohub",
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_ocr_boolean",
                                "actual_value": False,
                                "is_valid": False
                            },
                            {
                                "full_path": "CD_INDEXER_index_line",
                                "actual_value": False,
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_ocr_hybrid_boolean",
                                "actual_value": True,
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_embedding_engine",
                                "actual_value": "text-embedding-3-large",
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_embedding_version",
                                "actual_value": "2023-09-01-preview",
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_chunk_size",
                                "actual_value": 800,
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_chunk_type",
                                "actual_value": "TokenTextSplitter",
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_chunk_separator",
                                "actual_value": "",
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_chunk_overlap",
                                "actual_value": "300",
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_full_representation",
                                "actual_value": True,
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_summarize_tables",
                                "actual_value": False,
                                "is_valid": True
                            },
                            {
                                "full_path": "CD_INDEXER_embedding_dimension",
                                "actual_value": 3072,
                                "is_valid": True
                            }
                        ]
                    }
                ]
            }
        },
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    """
    Inicia um workflow com parâmetros específicos para indexação.
    """
    try:
        return start_workflow(payload, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar workflow: {str(e)}")


@workflow_request_route.get("/request/template-full-workflow", tags=["Workflow Request"], summary="Retorna template completo do workflow")
def api_get_full_workflow_template(
        workflow_configuration_code: str, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return get_full_workflow_template(workflow_configuration_code, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar template completo: {str(e)}")

@workflow_request_route.get("/request/template-workflow", tags=["Workflow Request"], summary="Retorna template simplificado do workflow")
def api_get_workflow_template(
        workflow_configuration_code: str, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return get_workflow_template(workflow_configuration_code, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar template simplificado: {str(e)}")

@workflow_request_route.get("/request/workflow-status/{workflow_execution_id}", tags=["Workflow Request"], summary="Retorna status e resultado da execução do workflow")
def api_get_workflow_status(
        workflow_execution_id: str, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return get_workflow_status(workflow_execution_id, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar status do workflow: {str(e)}")