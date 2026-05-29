import ollama
import chromadb
from datetime import datetime

client = chromadb.Client()
collection = client.create_collection("aria_knowledge")

with open("knowledge_base.txt", "r") as f:
    content = f.read()

chunks = content.split("\n\n")
for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk],
        ids=[f"doc_{i+1}"]
    )

history = [
    {"role": "system", "content": """You are Aria, an AWS and DevOps specialist.
Answer questions using the context provided.
If the context contains the answer, use it.
If not, answer from your AWS and DevOps knowledge.
Keep answers concise and technical."""}
]

def search_knowledge_base(question):
    results = collection.query(
        query_texts=[question],
        n_results=1
    )
    return results['documents'][0][0]

def ask_aria(question, history):
    relevant_chunk = search_knowledge_base(question)
    
    prompt_with_context = f"""Context from knowledge base:
{relevant_chunk}

Question: {question}"""
    
    history.append({
        "role": "user",
        "content": prompt_with_context,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    response = ollama.chat(
        model="mistral",
        messages=history,
        options={"num_predict": 150}
    )
    
    history.append({
        "role": "assistant",
        "content": response.message.content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    return response.message.content

if __name__ == "__main__":
    print("Aria — RAG powered AWS Assistant. Type 'exit' to quit.\n")
    while True:
        user_input = input("Rajat: ")
        if user_input.lower() == "exit":
            break
        response = ask_aria(user_input, history)
        print(f"\nAria: {response}\n")