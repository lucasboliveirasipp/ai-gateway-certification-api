import requests
from typing import Optional
from src.domain.gateway_apim_auth_service import Autenticator
from src.logger import LoggedSession
from src.utils import APPLICATION_JSON

session  = LoggedSession()

def upload_file(file_name: str, file_bytes: bytes, container_name: str, create_container : bool, overwrite : bool, connection_mode : str) -> Optional[str]:
        """Envia um arquivo PDF e retorna o ID do arquivo no sistema."""
        auth = Autenticator(connection_mode)

        files = {"file": (file_name, file_bytes)}
        data = {
            "container_name": container_name,
            "create_container": create_container,
            "overwrite": overwrite,
        }

        headers = {"Authorization": f"Bearer {auth.get_token()}"}
        
        url = f"{auth.file_manager_url}/files/upload"

        try:
            response = session.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Erro no upload: {e}")
            return None
        
def download_file(id: str, connection_mode : str):
    auth = Autenticator(connection_mode)

    url = f"{auth.file_manager_url}/files/{id}/download"
    
    headers = {
        "Content-Type": APPLICATION_JSON,
        "Authorization": f"Bearer {auth.get_token()}"
    }        
    try:
        response = session.get(url, headers=headers)
        return response.json()
    except requests.exceptions.RequestException:
        return None
    
def delete_file(id: str, connection_mode : str):
    auth = Autenticator(connection_mode)

    url = f"{auth.file_manager_url}/files/{id}"
    
    headers = {
        "Content-Type": APPLICATION_JSON,
        "Authorization": f"Bearer {auth.get_token()}"
    }        
    try:
        response = session.delete(url, headers=headers)
        return response.json()
    except requests.exceptions.RequestException:
        return None
    

def list_files(file_name: str, created_date: str, container_name : str, page: int, page_size: int, connection_mode : str):
    auth = Autenticator(connection_mode)

    params = {
        "file_name": file_name,
        "created_date": created_date,
        "container_name" : container_name,
        "page": page,
        "page_size": page_size
    }
    
    headers = {
        "Content-Type": APPLICATION_JSON,
        "Authorization": f"Bearer {auth.get_token()}"
    }

    url = f"{auth.file_manager_url}/files"

    try:
        response = session.get(url, params=params, headers=headers)
        return response.json()
    except requests.exceptions.RequestException:
        return None
    
    
def get_container(container_name : str, connection_mode : str):
    auth = Autenticator(connection_mode)

    params = {
        "container_name" : container_name
    }
    
    headers = {
        "Content-Type": APPLICATION_JSON,
        "Authorization": f"Bearer {auth.get_token()}"
    }

    url = f"{auth.file_manager_url}/storages/container"

    try:
        response = session.get(url, params=params, headers=headers)
        return response.json()
    except requests.exceptions.RequestException:
        return None

def get_container_files(path: str, container_name : str, connection_mode : str):
    auth = Autenticator(connection_mode)

    params = {
        "path": path,
        "container_name": container_name
    }
    
    headers = {
        "Content-Type": APPLICATION_JSON,
        "Authorization": f"Bearer {auth.get_token()}"
    }

    url = f"{auth.file_manager_url}/storages/files"

    try:
        response = session.get(url, params=params, headers=headers)
        return response.json()
    except requests.exceptions.RequestException:
        return None