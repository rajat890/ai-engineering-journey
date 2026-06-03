import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

response = bedrock.converse(
    modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    messages=[
        {
            "role": "user",
            "content": [{"text": "What is AWS Bedrock in one paragraph?"}]
        }
    ]
)

text = response['output']['message']['content'][0]['text']
usage = response['usage']

print("\n--- Claude's Response ---")
print(text)
print("\n--- Token Usage ---")
print(f"Input tokens:  {usage['inputTokens']}")
print(f"Output tokens: {usage['outputTokens']}")
print(f"Total tokens:  {usage['totalTokens']}")
print(f"Latency:       {response['metrics']['latencyMs']}ms")