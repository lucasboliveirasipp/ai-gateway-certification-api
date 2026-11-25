from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.api.filemanager_controller import filemanager_route
from src.api.indexer_controller import indexer_route
from src.api.orchestrator_agent_controller import orchestrator_agent_route
from src.api.plataforma_controller import plataforma_route
from src.api.qa_controller import qa_route
from src.api.workflow_request_controller import workflow_request_route
from src.api.workflow_response_controller import workflow_response_route
from src.api.health_controller import health_route

app = FastAPI(
    title="Hub BFF Gateway",
    description="API de validação dos endpoints da gateway",
    version="0.1.1",
    root_path="/api-certificacao-gateway",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(CORSMiddleware,
                   allow_credentials=True,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(filemanager_route)
app.include_router(indexer_route)
app.include_router(qa_route)
app.include_router(workflow_request_route)
app.include_router(workflow_response_route)
app.include_router(plataforma_route)
app.include_router(orchestrator_agent_route)
app.include_router(health_route)