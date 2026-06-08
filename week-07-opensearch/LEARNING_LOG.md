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
