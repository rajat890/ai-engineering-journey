from dotenv import load_dotenv
import os
load_dotenv()

import boto3
import json
import math

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "")

tools = [
    {
        "toolSpec": {
            "name": "calculator",
            "description": "Performs mathematical calculations. Use this when the user asks any math question.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "The mathematical expression to evaluate e.g. '2 + 2' or 'sqrt(16)'"
                        }
                    },
                    "required": ["expression"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "search_knowledge_base",
            "description": "Searches the company knowledge base for AWS infrastructure, incident response and CI/CD information. Use this for any questions about our internal systems.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query to find relevant information"
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    }
]

def calculator(expression):
    try:
        result = eval(expression, {"__builtins__": {}}, {
            "sqrt": math.sqrt,
            "pow": math.pow,
            "abs": abs,
            "round": round
        })
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def search_knowledge_base(query):
    response = bedrock_agent.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalQuery={"text": query},
        retrievalConfiguration={
            "vectorSearchConfiguration": {"numberOfResults": 2}
        }
    )
    
    results = response['retrievalResults']
    if not results:
        return "No relevant information found in knowledge base."
    
    chunks = [r['content']['text'] for r in results]
    return "\n\n".join(chunks)

def run_agent(user_message):
    print(f"\nUser: {user_message}")
    print("-" * 50)
    
    messages = [{"role": "user", "content": [{"text": user_message}]}]
    
    while True:
        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=messages,
            toolConfig={"tools": tools},
            system=[{"text": "You are Aria, an AWS and DevOps specialist with access to our company knowledge base and a calculator. Always use the appropriate tool to answer questions accurately."}]
        )
        
        stop_reason = response['stopReason']
        output_message = response['output']['message']
        messages.append(output_message)
        
        if stop_reason == "end_turn":
            final_answer = output_message['content'][0]['text']
            print(f"Aria: {final_answer}")
            return final_answer
        
        elif stop_reason == "tool_use":
            tool_results = []
            
            for block in output_message['content']:
                if 'toolUse' in block:
                    tool_use = block['toolUse']
                    tool_name = tool_use['name']
                    tool_input = tool_use['input']
                    tool_use_id = tool_use['toolUseId']
                    
                    print(f"[Tool called: {tool_name}]")
                    print(f"[Input: {tool_input}]")
                    
                    if tool_name == "calculator":
                        result = calculator(tool_input['expression'])
                    elif tool_name == "search_knowledge_base":
                        result = search_knowledge_base(tool_input['query'])
                    else:
                        result = "Tool not found"
                    
                    print(f"[Result: {result[:100]}...]")
                    
                    tool_results.append({
                        "toolResult": {
                            "toolUseId": tool_use_id,
                            "content": [{"text": result}]
                        }
                    })
            
            messages.append({
                "role": "user",
                "content": tool_results
            })

if __name__ == "__main__":
    run_agent("Our EKS cluster has 3 nodes minimum and 10 maximum. If each node costs $0.096 per hour, what is our monthly cost at maximum capacity?")
