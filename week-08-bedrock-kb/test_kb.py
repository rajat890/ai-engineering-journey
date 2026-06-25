from dotenv import load_dotenv
import os
load_dotenv()

KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "")
AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ARN = f"arn:aws:bedrock:{AWS_REGION}:{AWS_ACCOUNT_ID}:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0"

bedrock_agent = boto3.client("bedrock-agent-runtime", region_name=REGION)

def ask_kb(question):
    response = bedrock_agent.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                "modelArn": MODEL_ARN
            }
        }
    )
    return response['output']['text']

if __name__ == "__main__":
    questions = [
        "What is our EKS cluster name?",
        "What is our rollback command?",
        "How do I handle a P1 incident?",
        "What is photosynthesis?"
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        answer = ask_kb(question)
        print(f"A: {answer}")