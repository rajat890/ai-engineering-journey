from fastapi import FastAPI
from pydantic import BaseModel
import ollama
import chromadb
from datetime import datetime

app = FastAPI()

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

history = [
    {"role": "system", "content": """You are Aria, an AWS and DevOps specialist.
Answer questions using the context provided.
If context contains the answer, use it.
If not, answer from your AWS and DevOps knowledge.
Keep answers concise and technical."""}
]

class ChatRequest(BaseModel):
    message: str

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

@app.post("/chat")
def chat(request: ChatRequest):
    relevant_chunk = search_knowledge_base(request.message)
    
    if relevant_chunk:
        prompt = f"Context:\n{relevant_chunk}\n\nQuestion: {request.message}"
    else:
        prompt = request.message
    
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
    
    return {"response": response.message.content}