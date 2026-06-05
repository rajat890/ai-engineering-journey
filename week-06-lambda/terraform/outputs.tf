output "api_url" {
  value = "${aws_apigatewayv2_stage.aria.invoke_url}/chat"
}