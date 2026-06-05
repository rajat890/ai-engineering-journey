resource "aws_apigatewayv2_api" "aria" {
  name          = "${var.project_name}-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "aria" {
  api_id      = aws_apigatewayv2_api.aria.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "aria" {
  api_id                 = aws_apigatewayv2_api.aria.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.aria.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "aria" {
  api_id    = aws_apigatewayv2_api.aria.id
  route_key = "POST /chat"
  target    = "integrations/${aws_apigatewayv2_integration.aria.id}"
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.aria.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.aria.execution_arn}/*/*"
}