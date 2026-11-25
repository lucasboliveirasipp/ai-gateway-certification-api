from typing import Literal
import os
from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from src.domain.filemanager import delete_file, download_file, get_container, get_container_files, list_files, upload_file
from src.utils import CONNECTION_DESCRIPTION

filemanager_route = APIRouter()

@filemanager_route.post("/upload_file", tags=["File Manager"], summary="Realiza upload de arquivo para o Azure Blob Storage")
async def api_upload_file(
        file: UploadFile, 
        container_name : str = "meu-container", 
        create_container : bool = True, 
        overwrite : bool = True, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="O arquivo enviado não é um PDF.")
        
        pdf_bytes = await file.read()

        file_id = upload_file(file.filename, pdf_bytes,  container_name, create_container, overwrite, connection_mode)
                        
        return {"file_id": file_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o PDF: {str(e)}")
    
@filemanager_route.post("/download_file/{file_id}", tags=["File Manager"], summary="Gera uma URL para download do arquivo pelo ID")
def api_download_file(
        file_id: str, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        result = download_file(file_id, connection_mode)
        if not result:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado ou erro no download.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao baixar o arquivo: {str(e)}")
    

@filemanager_route.delete("/delete_file/{file_id}", tags=["File Manager"], summary="Deleta um arquivo do Azure Blob Storage pelo ID")
def api_delete_file(
        file_id: str, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return delete_file(file_id, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir o arquivo: {str(e)}")
    
@filemanager_route.get("/list_files", tags=["File Manager"], summary="Lista arquivos com filtros (nome, data, container)")
def api_list_files(
    file_name: str = "",
    created_date: str = "",
    container_name: str = "",
    page: int = 0,
    page_size: int = 10, 
    connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        result = list_files(file_name, created_date, container_name, page, page_size, connection_mode)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhum arquivo encontrado.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar arquivos: {str(e)}")
    
@filemanager_route.get("/get_container/{container_name}", tags=["File Manager"], summary="Obtém SAS URI do container e blob")
def api_get_container(
        container_name: str, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        result = get_container(container_name, connection_mode)
        if not result:
            raise HTTPException(status_code=404, detail="Container não encontrado.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter container: {str(e)}")
    

@filemanager_route.get("/get_container_files", tags=["File Manager"], summary="Lista arquivos em um caminho específico no container")
def api_get_container_files(
    path: str = "",
    container_name: str = "", 
    connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        result = get_container_files(path, container_name, connection_mode)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhum arquivo encontrado no container.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar arquivos do container: {str(e)}")