terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_lambda_function" "aria" {
  function_name = var.project_name
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = "396510133350.dkr.ecr.us-east-1.amazonaws.com/aria-chatbot:latest"
  timeout       = 60
  memory_size   = 1024
  architectures = ["arm64"]

  image_config {
    command = ["main.handler"]
  }
}