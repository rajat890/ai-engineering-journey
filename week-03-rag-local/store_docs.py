import chromadb

with open("knowledge_base.txt", "r") as f:
    content = f.read()

chunks = content.split("\n\n")

client = chromadb.Client()
collection = client.create_collection("aria_knowledge")

for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk],
        ids=[f"doc_{i+1}"]
    )

print(f"Stored {len(chunks)} documents in ChromaDB")
print("Done.")

results = collection.get()
for i, doc in enumerate(results['documents']):
    print(f"\n--- Stored Document {i+1} ---")
    print(f"ID: {results['ids'][i]}")
    print(f"Content: {doc}")

query = "How do I undo a deployment?"
search_results = collection.query(
    query_texts=[query],
    n_results=1
)

print(f"\n--- Search Query ---")
print(f"Question: {query}")
print(f"Most relevant chunk found:")
print(search_results['documents'][0][0])