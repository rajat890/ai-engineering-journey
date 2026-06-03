# Learning Log — Week 05

## Week 05 — Session 1 — 03 June 2026

### What was built
- IAM policy for Bedrock via Terraform
- first_bedrock_call.py — first cloud LLM call using Claude Haiku
- Token usage and latency monitoring

### Concepts learned
- bedrock-runtime vs bedrock — data plane vs management plane
- Cross-region inference profiles — us. prefix routes across US regions
- Newer Bedrock models require inference profile IDs not direct model IDs
- Token usage visible in every response — foundation for cost monitoring
- Claude Haiku 4.5 pricing: $0.80/million input, $4.00/million output

### Key numbers
- 17 input tokens + 132 output tokens = 149 total = $0.0005
- Latency: 2296ms — faster than local Mistral (3568ms)

### Key insight
boto3.client("bedrock-runtime") follows identical pattern to boto3.client("s3")
Same AWS SDK, same credential chain, same response pattern — just different service.

### Next session
- Replace Ollama/Mistral with Bedrock Claude in rag_chatbot.py
- Same RAG pipeline, cloud LLM underneath
- Compare response quality Mistral vs Claude