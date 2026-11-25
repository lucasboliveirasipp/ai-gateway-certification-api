from typing import Literal
from fastapi import APIRouter, HTTPException, Query
from src.domain.indexer import delete_index, index_info, index_metadata, list_index_items, lote, remove_metadata, start_workflow, workflow_template
from src.utils import CONNECTION_DESCRIPTION

indexer_route = APIRouter()

@indexer_route.post("/index", tags=["Indexer"], summary="Realiza a indexação de metadados")
def api_index_metadata(
    payload: dict = {
            "workflow_code": "string",
            "id_file_manager": "string",
            "index_name": "string",
            "cosmos_database": "genai-indexer",
            "cosmos_container": "indexer",
            "ocr_boolean": False,
            "summarize_tables": False,
            "chunk_size": 500,
            "chunk_type": "TokenTextSplitter",
            "chunk_separator": "string",
            "chunk_overlap": 0,
            "full_representation": False,
            "dynamic_metadata": [
                {
                "name": "string",
                "searchable": False,
                "filterable": False,
                "embedding": False,
                "value": ""
                }
            ],
            "embedding_engine": "string",
            "embedding_version": "string",
            "embedding_dimension": 0,
            "index_line": False,
            "term_set": [
                "string"
            ],
            "tag_set": [
                "string"
            ],
            "batch_indexer": {
                "batch_indexer_id": "string",
                "page": 0,
                "items_by_page": 0
            },
            "ocr_hybrid_boolean": False,
            "ocr_hybrid_settings": {
                "document_settings": {
                "pages": "string",
                "locale": "string"
                },
                "figure_settings": {
                "api_version": "2024-08-01-preview",
                "vision_model": "gpt-4o",
                "system_prompt": "Classifique a imagem abaixo em uma das três categorias listadas e siga as instruções correspondentes. Você não deve incluir a classificação em sua resposta.\n\n1.) Tabela: Reproduza integralmente, em formato markdown, a tabela presente na imagem.\n\n2.) Gráfico: Descreva o gráfico presente na imagem. Nessa descrição, sempre inclua o tipo de gráfico (linha, barra, etc), as variáveis e os limites dos eixos. Se existirem data labels visíveis no gráfico, reproduza seus valores em uma tabela em formato markdown. Caso não seja possível gerar uma tabela, descreva textualmente a evolução dos dados no gráfico, procurando por possíveis tendências e sazonalidades.\n\n3.) Genérico (nenhuma das anteriores): Explique a imagem detalhadamente. Sua explicação deve incluir tanto os elementos textuais quanto apenas visuais.",
                "temperature": 0,
                "image_format": "PNG",
                "image_dpi": 200,
                "optimize_model_calls": True,
                "image_hash_size": 256,
                "max_pixel_width_or_height_difference": 25,
                "max_hamming_distance": 0.175,
                "detailed_output": False
                },
                "table_settings": {
                "output_format": "MARKDOWN",
                "cell_confidence_agg_method": "MIN",
                "analyze_headers": True,
                "detailed_output": False
                },
                "warning_settings": {
                "confidence_threshold": 0
                }
            }
        }, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return index_metadata(payload, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao indexar: {str(e)}")


@indexer_route.post("/index/remove", tags=["Indexer"], summary="Remove metadados do índice")
def api_remove_metadata(
        payload: dict = {
            "CD_INDEXER_DELETE_document_id": "00000000-0000-0000-0000-000000000000",
            "CD_INDEXER_DELETE_id_file_manager": "00000000-0000-0000-0000-000000000000",
            "CD_INDEXER_DELETE_project_index": "inteligenciamercado",
            "CD_INDEXER_DELETE_embedding_engine": "text-embedding-3-large",
            "CD_INDEXER_DELETE_embedding_dimension": 3072
        }, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return remove_metadata(payload, connection_mode)
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Erro ao remover metadados: {str(e)}")

@indexer_route.get("/index/{index_name}", tags=["Indexer"], summary="Consulta itens em bases e containers")
def api_list_index_items(
    index_name: str,
    cosmos_database: str = "",
    cosmos_container: str = "",
    page: int = 0,
    page_size: int = 10, 
    connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return list_index_items(index_name, cosmos_database, cosmos_container, page, page_size, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar itens: {str(e)}")

@indexer_route.get("/index/{index_name}/informacoes", tags=["Indexer"], summary="Retorna informações detalhadas de um índice")
def api_index_info(
        index_name: str, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return index_info(index_name, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar informações do índice: {str(e)}")


@indexer_route.delete("/index/{index_name}", tags=["Indexer"], summary="Remove um índice específico")
def api_delete_index(
        index_name: str, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return delete_index(index_name, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir índice: {str(e)}")


@indexer_route.post("/lote", tags=["Indexer"], summary="Retorna o estado do lote")
def api_lote(
        payload: dict = {
            "batch_indexer_id": "string",
            "workflow_execution_id": "string"
        },
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return lote(payload, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar estado do lote: {str(e)}")


@indexer_route.post("/orchestrators/template-workflow", tags=["Indexer"], summary="Retorna template para execução do workflow")
def api_workflow_template(
        payload: dict = {
            "workflow_configuration_code": "string",
            "user_email": "string"
        }, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return workflow_template(payload, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter template do workflow: {str(e)}")


@indexer_route.post("/orchestrators/start-workflow", tags=["Indexer"], summary="Inicia execução do fluxo do Indexador")
def api_start_workflow(
        payload: dict = {
            "step_workflow_configuration_code": "string",
            "workflow_configuration_code": "string",
            "user_email": "string",
            "user_id": "string",
            "input_collection": {
                "input_properties": []
            },
            "is_valid": True,
            "message": "string"
        }, 
        connection_mode: Literal["APIM", "GATEWAY"] = Query("APIM", description=CONNECTION_DESCRIPTION)):
    try:
        return start_workflow(payload, connection_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar workflow: {str(e)}")

    