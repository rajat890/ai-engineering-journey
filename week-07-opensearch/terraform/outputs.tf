output "opensearch_endpoint" {
  value = aws_opensearchserverless_collection.aria.collection_endpoint
}

output "s3_bucket_name" {
  value = aws_s3_bucket.knowledge_base.bucket
}