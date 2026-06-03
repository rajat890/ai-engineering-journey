output "bedrock_policy_arn" {
  description = "Bedrock IAM policy ARN"
  value       = aws_iam_policy.bedrock_policy.arn
}