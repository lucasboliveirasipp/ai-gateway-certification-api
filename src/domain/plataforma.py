from src.domain.gateway_apim_auth_service import Autenticator
from src.logger import LoggedSession

session  = LoggedSession()

def myself(connection_mode: str):
    auth = Autenticator(connection_mode)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth.get_token()}"
    }

    url = f"{auth.plataforma_url}/usuarios/myself"
    response = session.get(url, headers=headers)
    response.raise_for_status()

    return response.json()

