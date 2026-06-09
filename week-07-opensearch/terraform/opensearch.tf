resource "aws_opensearchserverless_security_policy" "encryption" {
  name  = "${var.project_name}-encryption"
  type  = "encryption"
  policy = jsonencode({
    Rules = [
      {
        Resource     = ["collection/${var.project_name}"]
        ResourceType = "collection"
      }
    ]
    AWSOwnedKey = true
  })
}

resource "aws_opensearchserverless_security_policy" "network" {
  name  = "${var.project_name}-network"
  type  = "network"
  policy = jsonencode([
    {
      Rules = [
        {
          Resource     = ["collection/${var.project_name}"]
          ResourceType = "collection"
        },
        {
          Resource     = ["collection/${var.project_name}"]
          ResourceType = "dashboard"
        }
      ]
      AllowFromPublic = true
    }
  ])
}

resource "aws_opensearchserverless_access_policy" "data" {
  name  = "${var.project_name}-access"
  type  = "data"
  policy = jsonencode([
    {
      Rules = [
        {
          Resource     = ["collection/${var.project_name}"]
          ResourceType = "collection"
          Permission   = [
            "aoss:CreateCollectionItems",
            "aoss:DeleteCollectionItems",
            "aoss:UpdateCollectionItems",
            "aoss:DescribeCollectionItems"
          ]
        },
        {
          Resource     = ["index/${var.project_name}/*"]
          ResourceType = "index"
          Permission   = [
            "aoss:CreateIndex",
            "aoss:DeleteIndex",
            "aoss:UpdateIndex",
            "aoss:DescribeIndex",
            "aoss:ReadDocument",
            "aoss:WriteDocument"
          ]
        }
      ]
      Principal = [
        "arn:aws:iam::${var.account_id}:user/rajat-ai",
        "arn:aws:iam::396510133350:role/aria-chatbot-lambda-role"
      ]
    }
  ])
}

resource "aws_opensearchserverless_collection" "aria" {
  name = var.project_name
  type = "VECTORSEARCH"

  depends_on = [
    aws_opensearchserverless_security_policy.encryption,
    aws_opensearchserverless_security_policy.network
  ]
}