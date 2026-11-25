from typing import Literal
from fastapi import APIRouter, Query, HTTPException
from src.domain.workflow_response import (
    get_workflow_execution_status
)
from src.utils import CONNECTION_DESCRIPTION

workflow_response_route = APIRouter()

@workflow_response_route.get("/response/workflow-execution-status/{workflow_execution_id}", tags=["Workflow Response"], summary="Retorna status e informações da execução de um workflow")
def api_get_workflow_execution_status(
        workflow_execution_id: str, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    """
    Obtém o status da execução de um workflow.
    """
    try:
        return get_workflow_execution_status(workflow_execution_id, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter status do workflow: {str(e)}")