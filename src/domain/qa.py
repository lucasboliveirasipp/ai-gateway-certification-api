
import requests
from src.domain.gateway_apim_auth_service import Autenticator
from src.logger import LoggedSession

session  = LoggedSession()

def ask_question(payload, connection_mode: str):
    """
    Realiza uma pergunta no chat e retorna a resposta (modo síncrono).
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.qa_url}/chats/questions"
    
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.post(url=url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
       print(f"❌ Erro ao realizar pergunta: {e}")
       return None
    


def answer(id_context: str, db_name: str, db_container: str, connection_mode: str):
    """
    Obtém a resposta de uma pergunta no chat (modo assíncrono).
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.qa_url}/chats/answers"
    
    params = {
        "id_context": id_context,
        "db_name": db_name,
        "db_container": db_container
    }
    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao obter resposta: {e}")
        return None



def side_histories(page: int, size: int, sort_column: str, sort_order: str,
                       db_name: str, db_container: str, connection_mode: str):
    """
    Obtém histórico resumido da barra lateral do chat.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.qa_url}/chats/side-histories"
    
    params = {
        "page": page,
        "size": size,
        "sort_column": sort_column,
        "sort_order": sort_order,
        "db_name": db_name,
        "db_container": db_container
    }
    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao obter histórico resumido: {e}")
        return None


def chat_history(id_context: str, db_name: str, db_container: str, connection_mode: str):
    """
    Obtém histórico completo de um contexto do chat.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.qa_url}/chats/histories"
    
    params = {
        "id_context": id_context,
        "db_name": db_name,
        "db_container": db_container
    }
    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao obter histórico completo: {e}")
        return None



def delete_chat_history(id_context: str, db_name: str, db_container: str, connection_mode: str):
    """
    Exclui histórico de um contexto do chat.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.qa_url}/chats/histories"
    
    params = {
        "id_context": id_context,
        "db_name": db_name,
        "db_container": db_container
    }
    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.delete(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao excluir histórico: {e}")
        return None


def end_chat(id_context: str, db_name: str, db_container: str, connection_mode: str):
    """
    Encerra um chat (bloqueia a conversa).
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.qa_url}/chats/end"
    
    payload = {
        "id_context": id_context,
        "db_name": db_name,
        "db_container": db_container
    }
    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao encerrar chat: {e}")
        return None


