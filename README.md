# AI Gateway Certification API

A FastAPI service that exercises every capability of the company's internal AI gateway (file manager, indexer, Q&A, workflows, orchestrator agents, platform identity) through both access routes, so a new environment or release can be certified end to end before agents depend on it.

**Stack:** Python · FastAPI · requests · OAuth2 client credentials · mutual TLS · pytest (108 tests)
**Role:** Lead developer: design and implementation

> Built at a large Brazilian insurer. The company is replaced by the fictional **Acme Seguros**, and every name, document and data point here is fictional. Code, prompts and UI are in Portuguese, written for Brazilian business teams.

## Problem

All of the company's AI agents called models, search and storage through one internal AI gateway, reachable either through Azure API Management or directly. When something broke, it was hard to tell whether the cause was the agent, the gateway route or authentication, and there was no repeatable way to check a new deployment.

## What I built

| Router | Endpoints |
|---|---|
| File manager | upload, download URL, delete, list with filters, container SAS, container files |
| Indexer | index and remove metadata, list items, index info, delete index, batch status, workflow template, start workflow |
| Q&A | synchronous question, asynchronous answer |
| Workflows | start a workflow, read its response |
| Orchestrator | call an orchestrated agent |
| Platform | "who am I" from the token |
| Health | liveness and readiness probes |

- **Two connection modes per call** (`APIM` or `GATEWAY`), with the same request, so the two routes can be compared directly.
- **Authentication service** with OAuth2 client credentials, and mutual TLS for the direct route.
- **Logged HTTP session:** every outbound call is logged as JSON with timing, which makes the service usable as a diagnostic tool.
- **108 tests** covering controllers and domain clients, all with mocked HTTP.

## Limitations

This was an internal test tool for a private network: the logged session skips TLS certificate verification and logs full request bodies. Both should be changed before using it anywhere else.

## Run it

```bash
python -m venv .venv && .venv\Scripts\activate   # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest                                             # no keys needed
cp .env.example .env                               # gateway URLs + Entra ID app
uvicorn src.main:app --reload                      # Swagger at /docs
```

---
Part of my [AI engineering portfolio](https://github.com/lucasboliveirasipp).
