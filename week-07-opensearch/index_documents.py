import boto3
import json
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from chromadb.utils import embedding_functions

OPENSEARCH_ENDPOINT = "y0wd7n9mabu6y08lht2f.us-east-1.aoss.amazonaws.com"
REGION = "us-east-1"
INDEX_NAME = "aria-knowledge"
S3_BUCKET = "aria-rag-knowledge-base-396510133350"
S3_KEY = "knowledge_base.txt"

# AWS auth for OpenSearch Serverless
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    REGION,
    "aoss",
    session_token=credentials.token
)

# OpenSearch client
os_client = OpenSearch(
    hosts=[{"host": OPENSEARCH_ENDPOINT, "port": 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

# Embedding model — same as ChromaDB used locally
ef = embedding_functions.DefaultEmbeddingFunction()

def create_index():
    if os_client.indices.exists(index=INDEX_NAME):
        print(f"Index {INDEX_NAME} already exists")
        return
    
    mapping = {
        "mappings": {
            "properties": {
                "content": {"type": "text"},
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 384
                }
            }
        },
        "settings": {
            "index": {
                "knn": True
            }
        }
    }
    
    os_client.indices.create(index=INDEX_NAME, body=mapping)
    print(f"Index {INDEX_NAME} created")

def load_documents_from_s3():
    s3 = boto3.client("s3", region_name=REGION)
    response = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
    content = response["Body"].read().decode("utf-8")
    chunks = content.split("\n\n")
    print(f"Loaded {len(chunks)} chunks from S3")
    return chunks

def index_documents(chunks):
    for i, chunk in enumerate(chunks):
        embedding = ef([chunk])[0]
        
        doc = {
            "content": chunk,
            "embedding": embedding
        }
        
        os_client.index(
            index=INDEX_NAME,
            body=doc
        )
        print(f"Indexed chunk {i+1}")
    
    print(f"Successfully indexed {len(chunks)} documents")

if __name__ == "__main__":
    print("Creating index...")
    create_index()
    
    print("Loading documents from S3...")
    chunks = load_documents_from_s3()
    
    print("Indexing documents...")
    index_documents(chunks)
    
    print("Done!")