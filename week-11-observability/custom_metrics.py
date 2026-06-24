import boto3
import json
import time
from datetime import datetime

cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
KNOWLEDGE_BASE_ID = "5Q2FNMHEF0"
NAMESPACE = "Aria/AIMetrics"

def push_metric(metric_name, value, unit="Count", dimensions=None):
    metric_data = {
        "MetricName": metric_name,
        "Value": value,
        "Unit": unit,
        "Timestamp": datetime.utcnow()
    }
    if dimensions:
        metric_data["Dimensions"] = dimensions

    cloudwatch.put_metric_data(
        Namespace=NAMESPACE,
        MetricData=[metric_data]
    )

def ask_with_metrics(question):
    print(f"\nQuestion: {question}")
    start_time = time.time()

    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": question}]}],
        system=[{"text": "You are Aria, an AWS DevOps specialist. Be concise."}],
        inferenceConfig={"maxTokens": 150}
    )

    end_time = time.time()
    latency_ms = (end_time - start_time) * 1000

    input_tokens = response['usage']['inputTokens']
    output_tokens = response['usage']['outputTokens']
    total_tokens = response['usage']['totalTokens']

    input_cost = input_tokens * (0.80 / 1_000_000)
    output_cost = output_tokens * (4.00 / 1_000_000)
    total_cost = input_cost + output_cost

    push_metric("InputTokens", input_tokens)
    push_metric("OutputTokens", output_tokens)
    push_metric("TotalTokens", total_tokens)
    push_metric("LatencyMs", latency_ms, unit="Milliseconds")
    push_metric("QueryCostUSD", total_cost * 1000, unit="Count")

    answer = response['output']['message']['content'][0]['text']

    print(f"Answer: {answer[:100]}...")
    print(f"Tokens: {input_tokens} in / {output_tokens} out")
    print(f"Latency: {latency_ms:.0f}ms")
    print(f"Cost: ${total_cost:.6f}")

    return {
        "answer": answer,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "latency_ms": latency_ms,
        "cost": total_cost
    }

if __name__ == "__main__":
    results = []
    questions = [
        "What is AWS Lambda in one sentence?",
        "What is our EKS cluster name?"
    ]

    for q in questions:
        result = ask_with_metrics(q)
        results.append(result)
        time.sleep(1)

    print(f"\n{'='*50}")
    print("Session Summary")
    print(f"{'='*50}")
    total_cost = sum(r['cost'] for r in results)
    avg_latency = sum(r['latency_ms'] for r in results) / len(results)
    total_tokens = sum(r['input_tokens'] + r['output_tokens'] for r in results)
    print(f"Queries:       {len(results)}")
    print(f"Total tokens:  {total_tokens}")
    print(f"Avg latency:   {avg_latency:.0f}ms")
    print(f"Total cost:    ${total_cost:.6f}")
    print(f"\nCustom metrics pushed to CloudWatch namespace: {NAMESPACE}")