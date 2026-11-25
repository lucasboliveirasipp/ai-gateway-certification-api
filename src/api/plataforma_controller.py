from typing import Literal
from fastapi import APIRouter, HTTPException, Query
from src.domain.plataforma import myself
from src.utils import CONNECTION_DESCRIPTION

plataforma_route = APIRouter()

@plataforma_route.post("/myself", tags=["Plataforma"], summary="Retorna os dados do usuario com base no token")
def api_myself(
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return myself(connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar dados do usuario: {str(e)}")
    