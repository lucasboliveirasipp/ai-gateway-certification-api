
import requests
from src.domain.gateway_apim_auth_service import Autenticator
from src.logger import LoggedSession

session  = LoggedSession()

def get_workflow_execution_status(workflow_execution_id: str, connection_mode):
    """
    Obtém o status da execução de um workflow.
    """
    auth = Autenticator(connection_mode)
    url = f"{auth.workflow_response_url}/response/workflow-execution-status/{workflow_execution_id}"
    
    headers = {"Authorization": f"Bearer {auth.get_token()}"}
    
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao obter status do workflow: {e}")
        return None
