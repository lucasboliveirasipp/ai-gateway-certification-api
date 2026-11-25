
from src.domain.gateway_apim_auth_service import Autenticator
from src.logger import LoggedSession
import requests

session  = LoggedSession()

def call_agent(code, version, payload, connection_mode):
    auth = Autenticator(connection_mode)
    url = f"{auth.orchestrator_agent_url}/orchestrators/{code}/task/send?version={version}"
    print(url)
    headers = {"Authorization": f"Bearer {auth.get_token()}"}

    try:
        response = session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erro ao fazer chamada no orquestrador de agentes: {e}")
        return None