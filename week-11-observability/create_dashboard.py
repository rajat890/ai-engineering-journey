import boto3
import json

cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")

DASHBOARD_NAME = "Aria-AI-Platform"
REGION = "us-east-1"

dashboard_body = {
    "widgets": [
        {
            "type": "metric",
            "x": 0, "y": 0, "width": 12, "height": 6,
            "properties": {
                "title": "Lambda Invocations",
                "region": REGION,
                "metrics": [
                    ["AWS/Lambda", "Invocations", "FunctionName", "aria-chatbot"]
                ],
                "period": 300,
                "stat": "Sum",
                "view": "timeSeries",
                "annotations": {"horizontal": []}
            }
        },
        {
            "type": "metric",
            "x": 12, "y": 0, "width": 12, "height": 6,
            "properties": {
                "title": "Lambda Duration (ms)",
                "region": REGION,
                "metrics": [
                    ["AWS/Lambda", "Duration", "FunctionName", "aria-chatbot",
                     {"stat": "Average", "label": "Average"}],
                    ["AWS/Lambda", "Duration", "FunctionName", "aria-chatbot",
                     {"stat": "p99", "label": "p99"}]
                ],
                "period": 300,
                "view": "timeSeries",
                "annotations": {"horizontal": []}
            }
        },
        {
            "type": "metric",
            "x": 0, "y": 6, "width": 12, "height": 6,
            "properties": {
                "title": "Lambda Errors",
                "region": REGION,
                "metrics": [
                    ["AWS/Lambda", "Errors", "FunctionName", "aria-chatbot"]
                ],
                "period": 300,
                "stat": "Sum",
                "view": "timeSeries",
                "annotations": {"horizontal": []}
            }
        },
        {
            "type": "metric",
            "x": 12, "y": 6, "width": 12, "height": 6,
            "properties": {
                "title": "Lambda Throttles",
                "region": REGION,
                "metrics": [
                    ["AWS/Lambda", "Throttles", "FunctionName", "aria-chatbot"]
                ],
                "period": 300,
                "stat": "Sum",
                "view": "timeSeries",
                "annotations": {"horizontal": []}
            }
        }
    ]
}

def create_dashboard():
    response = cloudwatch.put_dashboard(
        DashboardName=DASHBOARD_NAME,
        DashboardBody=json.dumps(dashboard_body)
    )
    print(f"Dashboard created: {DASHBOARD_NAME}")
    print(f"View at: https://us-east-1.console.aws.amazon.com/cloudwatch/home#dashboards:name={DASHBOARD_NAME}")
    return response

if __name__ == "__main__":
    create_dashboard()