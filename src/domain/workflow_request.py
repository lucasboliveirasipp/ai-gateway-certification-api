import requests

from src.domain.gateway_apim_auth_service import Autenticator
from src.logger import LoggedSession

session  = LoggedSession()

def start_workflow(payload, connection_mode: str):
    """
    Inicia um workflow na Plataforma GenAI.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.workflow_request_url}/request/start-workflow"    

    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao iniciar workflow: {e}")
        return None



def get_full_workflow_template(workflow_configuration_code: str, connection_mode: str):
    """
    Recupera o template completo do workflow.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.workflow_request_url}/request/template-full-workflow"
    
    params = {"workflow-configuration-code": workflow_configuration_code}
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao recuperar template completo: {e}")
        return None



def get_workflow_template(workflow_configuration_code: str, connection_mode: str):
    """
    Recupera o template simplificado do workflow.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.workflow_request_url}/request/template-workflow"
    
    params = {"workflow-configuration-code": workflow_configuration_code}
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao recuperar template simplificado: {e}")
        return None


def get_workflow_status(workflow_execution_id: str, connection_mode: str):
    """
    Verifica status e resultado de um workflow.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.workflow_request_url}/request/workflow-status/{workflow_execution_id}"
    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao verificar status do workflow: {e}")
        return None