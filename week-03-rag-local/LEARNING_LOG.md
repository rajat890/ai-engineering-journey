# Learning Log — Week 03

## Week 03 — Session 1 — 29 May 2026

### What was built
- store_docs.py — loads knowledge_base.txt into ChromaDB
- rag_chatbot.py — RAG powered Aria using ChromaDB + Mistral
- knowledge_base.txt — simulated company knowledge base

### Concepts learned
- RAG = giving LLM access to your own documents at runtime
- ChromaDB stores text as embeddings (numbers representing meaning)
- Semantic search finds meaning similarity not keyword match
- ChromaDB finds the right chunk, Mistral extracts the exact answer
- Chunk size matters — too big = noisy, too small = missing context
- knowledge_base.txt = source, store_docs.py = importer, ChromaDB = database

### Key analogies
- knowledge_base.txt → Terraform .tf files
- store_docs.py → terraform apply  
- ChromaDB → AWS infrastructure
- RAG → Lambda function with S3 access at runtime
