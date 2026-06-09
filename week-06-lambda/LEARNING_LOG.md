# Learning Log — Week 06

## Week 06 — Session 1 — 05 June 2026

### What was built
- Docker image built for ARM64 and pushed to ECR
- Lambda function running Aria container image
- API Gateway HTTP API with public HTTPS endpoint
- Aria accessible from internet at AWS URL
- CloudWatch logs automatically capturing every request

### Concepts learned
- ECR = private Docker Hub on AWS — stores container images
- Lambda container image = serverless container runtime — no server management
- Mangum = adapter between Lambda events and FastAPI requests
- ENTRYPOINT + CMD = how Lambda knows to call your Python handler
- ARM64 Lambda = 20% cheaper than x86, matches M2 Mac architecture
- /tmp = only writable path in Lambda — 512MB ephemeral scratch space
- ChromaDB incompatible with Lambda — needs persistent storage, Lambda is stateless
- Simple keyword search used instead — replaced properly in Week 7 with OpenSearch
- Cold start = Init Duration in logs — only on first request after Lambda sleeps
- Warm start = no Init Duration — subsequent requests much faster

### Architecture
curl/browser
→ API Gateway (public HTTPS URL)
→ Lambda (container image)
→ search_knowledge_base() (keyword search)
→ Bedrock Claude Haiku
→ JSON response

### CloudWatch log structure
START        → request received by Lambda
END          → request completed
REPORT       → Duration, Billed Duration, Memory Used
Init Duration → cold start time (first request only)

### Key numbers from session
Cold start:     ~1088ms init + 742ms duration
Memory used:    108MB out of 1024MB allocated
Billed:         1832ms per cold start request
Warm requests:  ~700ms expected

### Cost this session
ECR storage:        ~$0.06/month (581MB image)
Lambda invocations: Free tier (first 1M requests)
API Gateway:        Free tier (first 1M requests)
Bedrock calls:      ~$0.001 per question
Total:              ~$0.06/month

### Key insight
Lambda is ephemeral compute — not storage.
ChromaDB needs persistent state — wrong tool for Lambda.
Correct pattern: Lambda (compute) + OpenSearch (storage) — Week 7.
Same principle as EC2 + EBS — separate compute from state.

### Problems solved this session
- ARM64 vs x86 image format mismatch → rebuilt with --provenance=false
- Lambda base image SQLite version → switched to python:3.11-slim + awslambdaric
- ChromaDB cold start download in Lambda → removed, replaced with keyword search
- Reserved environment variable → removed AWS_DEFAULT_REGION from Terraform

## Week 06 — Session 2 — 09 June 2026

### What was updated
- Connected Lambda to OpenSearch Serverless for semantic search
- Added Titan Embeddings for cloud-based vector generation
- Added opensearch-py and requests-aws4auth to requirements.txt
- Added error handling with try/except throughout

### Key insight
Lambda code lives in week-06-lambda — changes here rebuild the Docker image.
week-07-opensearch contains local tooling only — not deployed to Lambda.