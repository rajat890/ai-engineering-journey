from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
import boto3
import json

app = FastAPI()

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

KNOWLEDGE_BASE = [
    {
        "id": "doc_1",
        "content": """DOCUMENT 1 - EKS Setup
Our EKS cluster name is prod-cluster-mumbai. 
Node group uses t3.large instances with minimum 3 nodes and maximum 10 nodes.
Cluster version is Kubernetes 1.28.
Namespace convention: production, staging, monitoring."""
    },
    {
        "id": "doc_2", 
        "content": """DOCUMENT 2 - Incident Response
On-call rotation is managed via PagerDuty.
P1 incidents: page on-call immediately, create Slack thread in #incidents.
P2 incidents: create Jira ticket, notify team lead.
Runbook location: confluence.company.com/runbooks"""
    },
    {
        "id": "doc_3",
        "content": """DOCUMENT 3 - CI/CD Pipeline
All deployments use GitHub Actions.
Production deployments require 2 approvals.
Staging deploys automatically on merge to main branch.
Rollback command: kubectl rollout undo deployment/<name> -n production"""
    }
]

SYSTEM_PROMPT = """You are Aria, an AWS and DevOps specialist.
Answer questions using the context provided.
If context contains the answer, use it.
If not, answer from your AWS and DevOps knowledge.
Keep answers concise and technical."""

messages = []

class ChatRequest(BaseModel):
    message: str

def search_knowledge_base(question):
    question_lower = question.lower()
    best_match = None
    best_score = 0
    
    for doc in KNOWLEDGE_BASE:
        words = question_lower.split()
        score = sum(1 for word in words if word in doc['content'].lower())
        if score > best_score:
            best_score = score
            best_match = doc['content']
    
    if best_score > 0:
        return best_match
    return None

@app.post("/chat")
def chat(request: ChatRequest):
    relevant_chunk = search_knowledge_base(request.message)
    
    if relevant_chunk:
        prompt = f"Context:\n{relevant_chunk}\n\nQuestion: {request.message}"
    else:
        prompt = request.message
    
    messages.append({
        "role": "user",
        "content": [{"text": prompt}]
    })
    
    response = bedrock.converse(
        modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        system=[{"text": SYSTEM_PROMPT}],
        messages=messages,
        inferenceConfig={"maxTokens": 150}
    )
    
    reply = response['output']['message']['content'][0]['text']
    
    messages.append({
        "role": "assistant",
        "content": [{"text": reply}]
    })
    
    return {"response": reply}

handler = Mangum(app)