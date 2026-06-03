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

## Week 05 — Session 2 — 03 June 2026

### What was built
- bedrock_chatbot.py — Aria RAG chatbot using Claude Haiku via Bedrock
- Replaced Ollama/Mistral with boto3 Bedrock client
- Token cost monitoring on every response

### Concepts learned
- Bedrock Converse API separates system prompt from messages
- Bedrock message content is a list of blocks — allows text + images
- inferenceConfig replaces ollama options — same concept, different syntax
- Claude notices when context is irrelevant — better self-awareness than Mistral
- History accumulates tokens — longer conversation = higher cost per call

### Key numbers from session
- EKS question:      164 tokens → $0.000656
- Rollback question: 281 tokens → $0.001124
- Lambda question:   486 tokens → $0.001944
- Full session cost: $0.003724 — less than half a cent

### Mistral vs Claude Haiku
- Claude faster: 2300ms vs 3500ms
- Claude better formatting: code blocks, bullet points
- Claude self-aware: tells you when answer is outside context
- Claude costs money: ~$0.001/question vs free local

### Next session
- Week 6 — Deploy Aria to AWS Lambda + API Gateway
- Aria goes live on the internet
- First public URL for your AI API