import boto3

KNOWLEDGE_BASE_ID = "5Q2FNMHEF0"
REGION = "us-east-1"
MODEL_ARN = "arn:aws:bedrock:us-east-1:396510133350:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0"

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