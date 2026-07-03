# AI Engineering Journey
### AWS DevOps Engineer → AI Platform Engineer — 24 weeks

A structured self-directed curriculum building production-grade AI systems on AWS.
Every week has working code, committed to this repo.

---

## 🏗️ Architecture
User Request

→ API Gateway (HTTPS)

→ Lambda (FastAPI + Mangum)

→ Bedrock Knowledge Base (managed RAG)

→ Claude Haiku (LLM)

→ JSON Response
Bedrock Agent (autonomous):

→ Calculator tool (Lambda)

→ Knowledge Base search (aria-kb)

→ Orchestrated by Claude

---

## 📚 Progress

| Week | Topic | Key Technology | Status |
|------|-------|---------------|--------|
| 01 | Local LLM setup | Ollama + Mistral | ✅ |
| 02 | CLI Chatbot | Prompt engineering + Memory | ✅ |
| 03 | Local RAG | ChromaDB + Embeddings | ✅ |
| 04 | API + Docker | FastAPI + Mangum | ✅ |
| 05 | Cloud LLM | AWS Bedrock + Claude Haiku | ✅ |
| 06 | Serverless Deploy | Lambda + API Gateway + ECR | ✅ |
| 07 | Cloud RAG | OpenSearch + Titan Embeddings | ✅ |
| 08 | Managed RAG | Bedrock Knowledge Bases + S3 Vectors | ✅ |
| 09 | Custom Agents | Bedrock Converse API + Tools | ✅ |
| 10 | Managed Agents | Bedrock Agents + Lambda Tools | ✅ |
| 11 | Observability | CloudWatch + Cost Tracking | ✅ |
| 12 | Consolidation | Architecture + Documentation | ✅ |
| 13 | MLOps — SageMaker training scripts + local model training | SageMaker | ✅ Done |
| 17-20 | Portfolio Project | Full AI Product | ⏳ |
| 21-24 | Advanced | Fine-tuning + Specialisation | ⏳ |

---

## 🛠️ Tech Stack

**AI/ML**
- AWS Bedrock (Claude Haiku, Titan Embeddings)
- Bedrock Knowledge Bases + S3 Vectors
- Bedrock Agents
- Ollama + Mistral (local development)

**AWS Infrastructure**
- Lambda + API Gateway
- ECR (container registry)
- S3 (document storage)
- CloudWatch (observability)
- IAM (security)

**Application**
- Python 3.11
- FastAPI + Mangum
- Docker
- ChromaDB (local RAG)

**IaC**
- Terraform

---

## 💰 Running Costs

Current monthly AWS spend:

| Service | Cost |
|---------|------|
| ECR storage | ~$0.06 |
| S3 bucket | ~$0.00 |
| Lambda + API GW | Free tier |
| Bedrock (per query) | ~$0.001 |
| CloudWatch alarms | ~$0.20 |
| **Total idle** | **~$0.26/month** |

---

## 📁 Repository Structure
ai-engineering-journey/

├── week-01-local-setup/     # Ollama + first LLM call

├── week-02-cli-chatbot/     # Aria chatbot + prompt engineering

├── week-03-rag-local/       # ChromaDB + semantic search

├── week-04-fastapi/         # FastAPI + Docker

├── week-05-bedrock/         # AWS Bedrock + Terraform IAM

├── week-06-lambda/          # Lambda + API Gateway deployment

├── week-07-opensearch/      # OpenSearch + Titan Embeddings

├── week-08-bedrock-kb/      # Bedrock Knowledge Bases

├── week-09-agents/          # Custom AI agents with tools

├── week-10-bedrock-agents/  # Managed Bedrock Agents

├── week-11-observability/   # CloudWatch + cost tracking

└── LEARNING_LOG.md          # Concepts learned each week

---

## 🎯 Goal

Build production-ready AI Platform Engineering skills:
- Design and deploy RAG systems on AWS
- Build and orchestrate AI Agents
- Monitor and optimise AI system costs
- Infrastructure as Code with Terraform

---

*Built by Rajat — AWS Solutions Architect + Terraform Certified*
*10 years AWS DevOps experience transitioning to AI Platform Engineering*