from dotenv import load_dotenv
import os
load_dotenv()
from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
import boto3

app = FastAPI()

bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "")
MODEL_ARN = f"arn:aws:bedrock:{os.getenv('AWS_REGION')}:{os.getenv('AWS_ACCOUNT_ID')}:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0"

messages = []

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = bedrock_agent.retrieve_and_generate(
            input={"text": request.message},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": MODEL_ARN
                }
            }
        )
        reply = response['output']['text']
        return {"response": reply}

    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        return {"response": f"Error: {str(e)}"}

handler = Mangum(app)