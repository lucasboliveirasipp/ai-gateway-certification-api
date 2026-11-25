import requests
from src.logger import LoggedSession
from src.domain.gateway_apim_auth_service import Autenticator

session  = LoggedSession()

def index_metadata(payload, connection_mode: str):
    auth = Autenticator(connection_mode)
    url = f"{auth.indexer_url}/index"
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    try:
        response = session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro na indexação: {e}")
        return None


def remove_metadata(payload, connection_mode: str):
    auth = Autenticator(connection_mode)
    url = f"{auth.indexer_url}/index/remove"    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    try:
        response = session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"❌ Erro ao remover metadados: {e}")
        return None


def list_index_items(index_name, cosmos_database,
                     cosmos_container, page, page_size, connection_mode: str):
    auth = Autenticator(connection_mode)
    url = f"{auth.indexer_url}/index/{index_name}"
    params = {
        "cosmos_database": cosmos_database,
        "cosmos_container": cosmos_container,
        "page": page,
        "page_size": page_size
    }
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    try:
        response = requests.get(url, headers=headers, params=params)
        response = session.get(url=url, headers=headers, params=params)
        response.raise_for_status()    
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao listar itens: {e}")
        return None

def index_info(index_name, connection_mode: str):
    """
    Recupera os metadados de um índice específico.
    
    :param index_name: Nome do índice.
    :param connection_mode: Modo de conexão para autenticação.
    :return: Resposta JSON da API ou None em caso de erro.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.indexer_url}/index/{index_name}/informacoes"
    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao recuperar informações do índice: {e}")
        return None


def delete_index(index_name, connection_mode: str):
    """
    Exclui um índice pelo nome.
    
    :param index_name: Nome do índice a ser excluído.
    :param connection_mode: Modo de conexão para autenticação.
    :return: True/False ou None em caso de erro.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.indexer_url}/index/{index_name}"
    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao excluir índice: {e}")
        return None

def lote(payload, connection_mode: str):
    """
    Retorna o estado do lote (Batch Indexer).
    :param    :return: Resposta JSON da API ou None em caso de erro.    
    :param batch_indexer_id: ID do lote.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.indexer_url}/lote"
    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao consultar estado do lote: {e}")
        return None



def workflow_template(payload, connection_mode: str):
    """
    Obtém o template para o workflow do Indexador.
    
    :param workflow_configuration_code: Código da configuração do workflow.
    :param user_email: E-mail do usuário solicitante.
    :param connection_mode: Modo de conexão para autenticação.
    :return: Resposta JSON da API ou None em caso de erro.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.indexer_url}/orchestrators/template-workflow"
    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao obter template do workflow: {e}")
        return None



def start_workflow(payload, connection_mode: str):
    """
    Inicia a execução do fluxo do Indexador.
    
    :param workflow_configuration_code: Código da configuração do workflow.
    :param user_email: E-mail do usuário solicitante.
    :param user_id: ID do usuário solicitante.
    :param input_collection: Estrutura contendo as propriedades de entrada do workflow.
    :param connection_mode: Modo de conexão para autenticação.
    :return: Resposta JSON da API ou None em caso de erro.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.indexer_url}/orchestrators/start-workflow"
    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao iniciar workflow: {e}")
        return None