import boto3
import chromadb
from datetime import datetime

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("aria_knowledge")

if collection.count() == 0:
    with open("knowledge_base.txt", "r") as f:
        content = f.read()
    chunks = content.split("\n\n")
    for i, chunk in enumerate(chunks):
        collection.add(documents=[chunk], ids=[f"doc_{i+1}"])
    print("Knowledge base loaded.")
else:
    print(f"ChromaDB ready — {collection.count()} documents.")

SYSTEM_PROMPT = """You are Aria, an AWS and DevOps specialist.
Answer questions using the context provided.
If context contains the answer, use it.
If not, answer from your AWS and DevOps knowledge.
Keep answers concise and technical."""

messages = []

def search_knowledge_base(question):
    results = collection.query(
        query_texts=[question],
        n_results=1,
        include=["documents", "distances"]
    )
    distance = results['distances'][0][0]
    if distance > 1.5:
        return None
    return results['documents'][0][0]

def ask_aria(question):
    relevant_chunk = search_knowledge_base(question)
    
    if relevant_chunk:
        prompt = f"Context:\n{relevant_chunk}\n\nQuestion: {question}"
    else:
        prompt = question
    
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
    usage = response['usage']
    
    messages.append({
        "role": "assistant",
        "content": [{"text": reply}]
    })
    
    print(f"[tokens: {usage['totalTokens']} | cost: ~${usage['totalTokens'] * 0.000004:.6f}]")
    
    return reply

if __name__ == "__main__":
    print("Aria — Bedrock powered AWS Assistant. Type 'exit' to quit.\n")
    while True:
        user_input = input("Rajat: ")
        if user_input.lower() == "exit":
            break
        response = ask_aria(user_input)
        print(f"\nAria: {response}\n")