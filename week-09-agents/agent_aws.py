from dotenv import load_dotenv
import os
load_dotenv()

import boto3
import json
import math
from datetime import datetime, timedelta

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
lambda_client = boto3.client("lambda", region_name="us-east-1")
logs_client = boto3.client("logs", region_name="us-east-1")

MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "")

tools = [
    {
        "toolSpec": {
            "name": "calculator",
            "description": "Performs mathematical calculations. Use for any math question.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to evaluate e.g. '2 + 2'"
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
            "description": "Searches company knowledge base for AWS infrastructure, incident response and CI/CD information.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for the knowledge base"
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "check_lambda_status",
            "description": "Checks the status, configuration and health of an AWS Lambda function. Use when asked about Lambda function status, memory, timeout or runtime.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "function_name": {
                            "type": "string",
                            "description": "Name of the Lambda function to check"
                        }
                    },
                    "required": ["function_name"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "get_recent_logs",
            "description": "Fetches recent CloudWatch logs for a Lambda function. Use when asked about errors, logs or recent activity.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "function_name": {
                            "type": "string",
                            "description": "Name of the Lambda function"
                        },
                        "minutes": {
                            "type": "integer",
                            "description": "How many minutes back to fetch logs, default 30"
                        }
                    },
                    "required": ["function_name"]
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
    try:
        response = bedrock_agent.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": query},
            retrievalConfiguration={
                "vectorSearchConfiguration": {"numberOfResults": 2}
            }
        )
        results = response['retrievalResults']
        if not results:
            return "No relevant information found."
        chunks = [r['content']['text'] for r in results]
        return "\n\n".join(chunks)
    except Exception as e:
        return f"Error searching KB: {str(e)}"

def check_lambda_status(function_name):
    try:
        response = lambda_client.get_function(FunctionName=function_name)
        config = response['Configuration']
        return json.dumps({
            "function_name": config['FunctionName'],
            "status": config['State'],
            "runtime": config.get('Runtime', 'container'),
            "memory_mb": config['MemorySize'],
            "timeout_seconds": config['Timeout'],
            "last_modified": config['LastModified'],
            "code_size_bytes": config['CodeSize']
        }, indent=2)
    except Exception as e:
        return f"Error checking Lambda: {str(e)}"

def get_recent_logs(function_name, minutes=30):
    try:
        log_group = f"/aws/lambda/{function_name}"
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=minutes)

        response = logs_client.filter_log_events(
            logGroupName=log_group,
            startTime=int(start_time.timestamp() * 1000),
            endTime=int(end_time.timestamp() * 1000),
            limit=20
        )

        events = response.get('events', [])
        if not events:
            return f"No logs found in the last {minutes} minutes."

        log_lines = []
        for event in events:
            timestamp = datetime.utcfromtimestamp(
                event['timestamp'] / 1000
            ).strftime('%H:%M:%S')
            log_lines.append(f"[{timestamp}] {event['message'].strip()}")

        return "\n".join(log_lines)
    except Exception as e:
        return f"Error fetching logs: {str(e)}"

def run_agent(user_message):
    print(f"\nUser: {user_message}")
    print("-" * 50)

    messages = [{"role": "user", "content": [{"text": user_message}]}]

    while True:
        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=messages,
            toolConfig={"tools": tools},
            system=[{"text": """You are Aria, an AWS DevOps AI assistant.
You have access to tools to check real AWS resources and search company knowledge.
Always use tools to get accurate real-time information rather than guessing."""}]
        )

        stop_reason = response['stopReason']
        output_message = response['output']['message']
        messages.append(output_message)

        if stop_reason == "end_turn":
            final_answer = output_message['content'][0]['text']
            print(f"\nAria: {final_answer}")
            return final_answer

        elif stop_reason == "tool_use":
            tool_results = []

            for block in output_message['content']:
                if 'toolUse' in block:
                    tool_use = block['toolUse']
                    tool_name = tool_use['name']
                    tool_input = tool_use['input']
                    tool_use_id = tool_use['toolUseId']

                    print(f"[Tool: {tool_name} | Input: {tool_input}]")

                    if tool_name == "calculator":
                        result = calculator(tool_input['expression'])
                    elif tool_name == "search_knowledge_base":
                        result = search_knowledge_base(tool_input['query'])
                    elif tool_name == "check_lambda_status":
                        result = check_lambda_status(tool_input['function_name'])
                    elif tool_name == "get_recent_logs":
                        result = get_recent_logs(
                            tool_input['function_name'],
                            tool_input.get('minutes', 30)
                        )
                    else:
                        result = "Tool not found"

                    print(f"[Result preview: {str(result)[:80]}...]")

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
    run_agent("Check our aria-chatbot Lambda status and tell me what our EKS cluster name is")