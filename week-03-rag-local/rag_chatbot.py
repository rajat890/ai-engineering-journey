import ollama
import chromadb
from datetime import datetime

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("aria_knowledge")

if collection.count() == 0:
    with open("knowledge_base.txt", "r") as f:
        content = f.read()
    
    chunks = content.split("\n\n")
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"doc_{i+1}"]
        )
    print("Knowledge base loaded into ChromaDB.")
else:
    print(f"ChromaDB already has {collection.count()} documents. Skipping load.")

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
        n_results=1,
        include=["documents", "distances"]
    )
    
    distance = results['distances'][0][0]
    print(f"[DEBUG] Distance score: {distance:.3f}")
    
    if distance > 1.5:
        return None
    
    return results['documents'][0][0]

def ask_aria(question, history):
    relevant_chunk = search_knowledge_base(question)
    
    if relevant_chunk:
        prompt = f"Context from knowledge base:\n{relevant_chunk}\n\nQuestion: {question}"
    else:
        prompt = question
    
    history.append({
        "role": "user",
        "content": prompt,
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