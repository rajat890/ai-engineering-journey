import boto3
import json
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from chromadb.utils import embedding_functions

OPENSEARCH_ENDPOINT = "y0wd7n9mabu6y08lht2f.us-east-1.aoss.amazonaws.com"
REGION = "us-east-1"
INDEX_NAME = "aria-knowledge"

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
    connection_class=RequestsHttpConnection
)

ef = embedding_functions.DefaultEmbeddingFunction()

def search(question):
    embedding = ef([question])[0]
    
    query = {
        "size": 1,
        "query": {
            "knn": {
                "embedding": {
                    "vector": embedding,
                    "k": 1
                }
            }
        }
    }
    
    response = os_client.search(index=INDEX_NAME, body=query)
    hits = response['hits']['hits']
    
    if hits:
        score = hits[0]['_score']
        print(f"[DEBUG] Score: {score:.3f}")
        if score < 0.4:
            return None
        return hits[0]['_source']['content']
    return None

if __name__ == "__main__":
    questions = [
        "What is our rollback command?",
        "How do I handle a P1 incident?",
        "What is our EKS cluster name?",
        "What is photosynthesis?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        result = search(question)
        print(f"Found: {result[:80]}..." if result else "No match found")