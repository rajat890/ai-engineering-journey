from dotenv import load_dotenv
import os
load_dotenv()
from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
import boto3
import os
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

app = FastAPI()

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# OpenSearch was used in Week 7 — replaced by Bedrock KB in Week 8
# OPENSEARCH_ENDPOINT moved to environment variables
OPENSEARCH_ENDPOINT = os.getenv("OPENSEARCH_ENDPOINT", "")
REGION = "us-east-1"
INDEX_NAME = "aria-knowledge"

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    REGION,
    "aoss",
    session_token=credentials.token
)

os_client = OpenSearch(
    hosts=[{"host": OPENSEARCH_ENDPOINT, "port": 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30
)

SYSTEM_PROMPT = """You are Aria, an AWS and DevOps specialist.
Answer questions using the context provided.
If context contains the answer, use it.
If not, answer from your AWS and DevOps knowledge.
Keep answers concise and technical."""

messages = []

class ChatRequest(BaseModel):
    message: str

def get_embedding(text):
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=__import__('json').dumps({"inputText": text})
    )
    body = __import__('json').loads(response['body'].read())
    return body['embedding']

def search_knowledge_base(question):
    try:
        embedding = get_embedding(question)
        
        query = {
            "size": 1,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": embedding,
                        "k": 1
                    }
                }
            }
        }
        
        response = os_client.search(index=INDEX_NAME, body=query)
        hits = response['hits']['hits']
        
        if hits:
            score = hits[0]['_score']
            if score < 0.4:
                return None
            return hits[0]['_source']['content']
        return None
        
    except Exception as e:
        print(f"OpenSearch error: {type(e).__name__}: {str(e)}")
        return None
    
@app.post("/chat")
def chat(request: ChatRequest):
    try:
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
    
    except Exception as e:
        print(f"Chat error: {type(e).__name__}: {str(e)}")
        return {"response": f"Error: {str(e)}"}

handler = Mangum(app)