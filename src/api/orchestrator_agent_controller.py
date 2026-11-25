from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from src.domain.orchestrator_agent import call_agent
from src.utils import CONNECTION_DESCRIPTION

orchestrator_agent_route = APIRouter()

@orchestrator_agent_route.post("/call_agent", tags=["Orchestrators"], summary="Chama a orchestrator ")
def api_call_agent(
        orchestrator_workflow_code: str = "WF_AGENTE_FERRAMENTA",
        version: str = "draft",
        payload: dict = {
                "messages": [
                    {
                        "type": "text",
                        "content": {
                            "text": "o que você pode falar?"
                        }
                    }
                ],
                "session_id": "",
                "metadata": {}
        },
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return call_agent(orchestrator_workflow_code, version, payload, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar item: {str(e)}")

