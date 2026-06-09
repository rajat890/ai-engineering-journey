# Learning Log — Week 07

## Week 07 — Session 1 — 08 June 2026

### What was built
- S3 bucket for knowledge base document storage
- OpenSearch Serverless collection with vector search
- index_documents.py — reads S3, generates embeddings, indexes to OpenSearch
- search_test.py — verifies semantic search working with score threshold

### Architecture
knowledge_base.txt
→ S3 bucket (source of truth)
→ index_documents.py (one time setup)
→ OpenSearch Serverless (text + vectors)
→ search_test.py (semantic search)
→ score threshold 0.4 (relevance filter)

### Concepts learned
- OpenSearch Serverless = managed vector DB on AWS — no cluster management
- knn_vector field = special index for finding similar vectors
- knn query = k-nearest neighbours — finds closest meaning match
- Score vs distance — OpenSearch uses score (higher=better), ChromaDB uses distance (lower=better)
- Score threshold 0.4 — below this = irrelevant, don't return
- AWS4Auth — signs OpenSearch requests with IAM credentials
- S3 = source of truth for documents, OpenSearch = search engine
- index_documents.py runs once — search_test.py runs every query

### Key numbers
Rollback command  → score 0.463 → relevant ✓
P1 incident       → score 0.408 → relevant ✓
EKS cluster name  → score 0.661 → relevant ✓
Photosynthesis    → score 0.360 → not relevant ✓ filtered out

### Elasticsearch knowledge that transferred directly
- Index creation → same concept, added knn_vector field
- Query DSL → same structure, added knn query type
- Bulk indexing → same API
- Shards/replicas → same concepts

### What's new vs Elasticsearch
- knn_vector field type — stores 384-dimension vectors
- knn query — finds semantically similar documents
- AWS4Auth — request signing for OpenSearch Serverless
- Score threshold — filters irrelevant results

### Cost this session
OpenSearch Serverless  → ~$0.48/hour × session duration
S3 bucket              → ~$0.00 (tiny documents)
DESTROYED after session → no ongoing cost

### Key insight
S3 is source of truth — documents stored here permanently.
OpenSearch is the search engine — can be destroyed and recreated from S3.
Same principle as Terraform state — source of truth separate from running infrastructure.

### Problems solved
- Custom document IDs not supported in OpenSearch Serverless → removed id parameter
- Photosynthesis returning wrong results → raised threshold from 0.3 to 0.4

## Week 07 — Session 2 — 09 June 2026

### What was built
- Updated Lambda to use OpenSearch for semantic search
- Replaced keyword search with Titan Embeddings + OpenSearch knn query
- Full cloud RAG pipeline working end to end
- Added error handling to Lambda for better debugging

### Full pipeline
curl
→ API Gateway
→ Lambda
→ Titan Embeddings (converts question to vector)
→ OpenSearch (finds relevant chunk)
→ Bedrock Claude Haiku (generates answer)
→ JSON response

### Key changes from Week 06
- Removed keyword search → replaced with OpenSearch knn query
- Added Titan Embeddings → cloud embedding model, no local model needed
- Added opensearch-py + requests-aws4auth to Lambda requirements
- Added aoss:APIAccessAll to Lambda IAM role
- Added Lambda role to OpenSearch access policy Principal

### Concepts learned
- Titan Embeddings = AWS managed embedding model on Bedrock
- dimension 1024 for Titan vs 384 for local ChromaDB model — must match
- Lambda IAM role needs aoss:APIAccessAll to query OpenSearch
- OpenSearch access policy Principal must include Lambda role ARN
- try/except in Lambda = always return response, never crash silently
- RAG does NOT train the model — injects information at runtime
- Training = permanent, expensive. RAG = runtime, cheap, updatable

### RAG vs Training
Training  → change model weights permanently — days, expensive
RAG       → inject documents into prompt — instant, cents per query

### Cost this session
OpenSearch  → ~$0.48/hour × ~2 hours = ~$1.00
Titan Embeddings → ~$0.00 (tiny usage)
Bedrock calls → ~$0.001 per question
Total → ~$1.00 ✓

### Problems solved
- Lambda 403 on OpenSearch → added Lambda role to access policy Principal
- Error not visible in logs → added try/except with print statements
- Old container cached → force updated via update-function-configuration