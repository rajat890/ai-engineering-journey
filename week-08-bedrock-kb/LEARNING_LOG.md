# Learning Log — Week 08

## Week 08 — Session 1 — 17 June 2026

### What was built
- Bedrock Knowledge Base (aria-kb) via AWS Console
- S3 Vectors as vector store — zero idle cost
- test_kb.py — verified KB answers correctly
- Updated Lambda to use retrieve_and_generate() API
- Removed OpenSearch, ChromaDB, manual embedding code

### Architecture
curl

→ API Gateway

→ Lambda (week-08 image)

→ bedrock-agent-runtime.retrieve_and_generate()

→ Bedrock KB handles: embed + search + generate

→ JSON response

### Code comparison
Week 7 manual RAG    Week 8 Bedrock KB

─────────────────    ─────────────────

100+ lines           15 lines

opensearch-py        boto3 only

get_embedding()      not needed

knn query            not needed

score threshold      not needed

$0.48/hour           $0.00 idle cost

### Concepts learned
- Bedrock Knowledge Base = fully managed RAG pipeline
- S3 Vectors = new AWS vector store, pay per query not per hour
- retrieve_and_generate() = one API call replaces entire RAG pipeline
- Sync = manual trigger to index S3 documents into KB
- Auto-sync = S3 event → Lambda → start_ingestion_job() (Week 17)
- Bedrock KB handles relevance automatically — no score threshold needed
- RAG ≠ training — injects docs at runtime, model unchanged

### Key insight
Manual RAG (Week 7) teaches you HOW it works.
Bedrock KB (Week 8) is HOW enterprises actually deploy it.
Knowing both = you can build AND debug any RAG system. ✓

### AWS resources running
- Lambda + API Gateway → free tier
- ECR image → ~$0.06/month
- S3 bucket → ~$0.00
- Bedrock KB → pay per query only
- No OpenSearch → $0.00 idle cost ✓

### Next session — Week 09
- AI Agents — LangChain + Bedrock Agents
- Agents that can decide which tool to call
- First autonomous AI system