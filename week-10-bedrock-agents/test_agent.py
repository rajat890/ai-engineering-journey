import boto3
import uuid

bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

AGENT_ID = "PQBYOIILHH"
AGENT_ALIAS_ID = "TSTALIASID"  # default test alias

def ask_agent(question):
    print(f"\nUser: {question}")
    print("-" * 50)
    
    response = bedrock_agent.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=str(uuid.uuid4()),
        inputText=question
    )
    
    full_response = ""
    for event in response['completion']:
        if 'chunk' in event:
            chunk = event['chunk']['bytes'].decode('utf-8')
            full_response += chunk
    
    print(f"Aria: {full_response}")
    return full_response

if __name__ == "__main__":
    ask_agent("What is our rollback command and what is 10 to the power of 3?")