# Learning Log — Week 04

## Week 04 — Session 1 — 01 June 2026

### What was built
- FastAPI server exposing Aria as a REST API on /chat endpoint
- Pydantic ChatRequest model for request validation
- Full RAG pipeline integrated into HTTP endpoint
- Tested with curl from terminal

### Concepts learned
- FastAPI = API Gateway in code — defines endpoints, validates requests, returns JSON
- POST vs GET — POST for sending data, GET for reading data
- Pydantic BaseModel = API Gateway request validator — wrong schema rejected automatically
- uvicorn --reload = live reload on file save, no restart needed
- 127.0.0.1 = localhost only, 0.0.0.0 = network accessible
- curl = testing an API from terminal — same pattern for AWS API Gateway in Week 6

### Key insight
Same Aria from Week 3 — just wrapped in HTTP.
Week 1 = function, Week 2 = chatbot, Week 3 = RAG, Week 4 = API.
Each week adds one layer around the same core LLM call.


## Week 04 — Session 2 — 02 June 2026

### What was built
- Dockerfile for Aria FastAPI app
- .dockerignore to keep image clean
- requirements.txt with minimal dependencies
- Aria running fully in Docker container

### Concepts learned
- Dockerfile = userdata script for containers — install, copy, start
- FROM python:3.11-slim — slim base image keeps size down
- COPY requirements.txt first — Docker layer caching, faster rebuilds
- -p 8000:8000 — port mapping host:container, like security group inbound rule
- host.docker.internal — Mac's IP from inside container, like EC2 private IP
- 0.0.0.0 vs 127.0.0.1 — 0.0.0.0 accepts external connections, 127.0.0.1 localhost only
- --reload is dev only — never use in production containers
