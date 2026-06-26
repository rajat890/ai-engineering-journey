from dotenv import load_dotenv
import os
load_dotenv()
import boto3
import json
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

OPENSEARCH_ENDPOINT = os.getenv("OPENSEARCH_ENDPOINT", "")
REGION = "us-east-1"
INDEX_NAME = "aria-knowledge"
S3_BUCKET = os.getenv("S3_BUCKET", "")
S3_KEY = "knowledge_base.txt"

bedrock_client = boto3.client("bedrock-runtime", region_name=REGION)

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    REGION,
    "aoss",
    session_token=credentials.token
)

os_client = OpenSearch(
    hosts=[{"host": OPENSEARCH_ENDPOINT, "port": 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30
)

def get_embedding(text):
    response = bedrock_client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": text})
    )
    body = json.loads(response['body'].read())
    return body['embedding']

def create_index():
    if os_client.indices.exists(index=INDEX_NAME):
        print(f"Deleting existing index {INDEX_NAME}...")
        os_client.indices.delete(index=INDEX_NAME)
    
    mapping = {
        "mappings": {
            "properties": {
                "content": {"type": "text"},
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 1024
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
    print(f"Index {INDEX_NAME} created with dimension 1024")

def load_documents_from_s3():
    s3 = boto3.client("s3", region_name=REGION)
    response = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
    content = response["Body"].read().decode("utf-8")
    chunks = content.split("\n\n")
    print(f"Loaded {len(chunks)} chunks from S3")
    return chunks

def index_documents(chunks):
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        
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