import os
import requests
import urllib3

from src.logger import LoggedSession
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PATH_CRT_FILE = os.getenv("PATH_CRT_FILE")
PATH_KEY_FILE = os.getenv("PATH_KEY_FILE")
PATH_ROOT_CA = "/app/api-certificacao-gateway/root.crt"

session  = LoggedSession()

class Autenticator:
    def __init__(self, connection_mode="APIM"):
        """
        mode: 'GATEWAY' ou 'APIM'
        """
        if connection_mode not in ["GATEWAY", "APIM"]:
            raise ValueError("Modo inválido! Use 'gateway' ou 'APIM'.")

        prefix = "GATEWAY_" if connection_mode == "GATEWAY" else "APIM_"
        self.connection_mode = connection_mode

        self.base_url = os.getenv(f"{prefix}URL")

        self.classifier_url = self.base_url+os.getenv(f"{prefix}CLASSIFIER_URL") 
        self.embedding_url = self.base_url+os.getenv(f"{prefix}EMBEDDING_URL")
        self.evaluation_url = self.base_url+os.getenv(f"{prefix}EVALUATION_URL")
        self.extraction_url = self.base_url+os.getenv(f"{prefix}EXTRACTION_URL")
        self.file_manager_url = self.base_url+os.getenv(f"{prefix}FILEMANAGER_URL")
        self.indexer_url = self.base_url+os.getenv(f"{prefix}INDEXER_URL")
        self.orchestrator_url = self.base_url+os.getenv(f"{prefix}ORCHESTRATOR_URL")
        self.orchestrator_agent_url = self.base_url+os.getenv(f"{prefix}ORCHESTRATOR_AGENT_URL")
        self.qa_url = self.base_url+os.getenv(f"{prefix}QA_URL")
        self.summarization_url = self.base_url+os.getenv(f"{prefix}SUMMARIZATION_URL")
        self.text_generator_url = self.base_url+os.getenv(f"{prefix}TEXTGENERATOR_URL")
        self.transcript_url = self.base_url+os.getenv(f"{prefix}TRANSCRIPT_URL")
        self.workflow_request_url = self.base_url+os.getenv(f"{prefix}WORKFLOW-REQUEST_URL")
        self.workflow_response_url = self.base_url+os.getenv(f"{prefix}WORKFLOW-RESPONSE_URL")
        self.ocr_url = self.base_url+os.getenv(f"{prefix}OCR_URL")
        self.plataforma_url = self.base_url+os.getenv(f"{prefix}PLATAFORMA_URL")
        
        self.usuario = os.getenv('GATEWAY_USUARIO')
        self.senha = os.getenv('GATEWAY_SENHA')

        self.gateway_auth_url = self.base_url+os.getenv("GATEWAY_AUTH_URL")

        self.verify_ssl : bool  = False

    def show_config(self):
        print("Configuração atual:")
        print(f"Modo de conexão: {self.connection_mode}")
        print(f"Classifier: {self.classifier_url}")
        print(f"Embedding: {self.embedding_url}")
        print(f"Evaluation: {self.evaluation_url}")
        print(f"Extraction: {self.extraction_url}")
        print(f"File Manager: {self.file_manager_url}")
        print(f"Indexer: {self.indexer_url}")
        print(f"Orchestrator: {self.orchestrator_url}")
        print(f"QA: {self.qa_url}")
        print(f"Summarization: {self.summarization_url}")
        print(f"Text Generator: {self.text_generator_url}")
        print(f"Transcript: {self.transcript_url}")
        print(f"Workflow Request: {self.workflow_request_url}")
        print(f"Workflow Response: {self.workflow_response_url}")
        print(f"OCR: {self.ocr_url}")
        print(f"Plataforma: {self.plataforma_url}")
        
    def authenticate_apim(self):
        tenant_id = os.getenv("TENANTID")
        client_id = os.getenv("HUBCERTIFAPPID")
        scope = os.getenv("SCOPEAPIMID")
        print(scope)
        
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": os.getenv("HUBCERTIFCLIENTSECRET"),
            "scope": scope.replace("APIMAuth.Read", ".default")
        }
        
        auth = session.post(token_url, data=token_data)

        print("---------------------------Autenticado-------------------------------")
        data = auth.json()
        return data.get("access_token")
    
    def authenticate_gateway(self):
        """Autentica o usuário na gateway."""
        try:
            response = requests.post(
                self.gateway_auth_url,
                json={"identificador": self.usuario, "senha": self.senha},
                headers={"Content-Type": "application/json"}, 
                verify=True, cert=(PATH_CRT_FILE, PATH_KEY_FILE))
            response.raise_for_status()
            data = response.json()        
            return data.get("token")
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na autenticação: {e}")
            return None
        
    def get_token(self):
        if self.connection_mode == "APIM":
            return self.authenticate_apim()
        else:
            return self.authenticate_gateway()