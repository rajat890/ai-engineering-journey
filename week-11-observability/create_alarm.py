import boto3

cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
sns = boto3.client("sns", region_name="us-east-1")

def create_lambda_error_alarm():
    cloudwatch.put_metric_alarm(
        AlarmName="aria-chatbot-high-errors",
        AlarmDescription="Fires when aria-chatbot errors exceed 5 in 5 minutes",
        MetricName="Errors",
        Namespace="AWS/Lambda",
        Dimensions=[
            {"Name": "FunctionName", "Value": "aria-chatbot"}
        ],
        Period=300,
        EvaluationPeriods=1,
        Threshold=5,
        ComparisonOperator="GreaterThanThreshold",
        Statistic="Sum",
        TreatMissingData="notBreaching"
    )
    print("Error alarm created ✓")

def create_lambda_duration_alarm():
    cloudwatch.put_metric_alarm(
        AlarmName="aria-chatbot-high-latency",
        AlarmDescription="Fires when aria-chatbot p99 duration exceeds 10 seconds",
        MetricName="Duration",
        Namespace="AWS/Lambda",
        Dimensions=[
            {"Name": "FunctionName", "Value": "aria-chatbot"}
        ],
        Period=300,
        EvaluationPeriods=1,
        Threshold=10000,
        ComparisonOperator="GreaterThanThreshold",
        ExtendedStatistic="p99",
        TreatMissingData="notBreaching"
    )
    print("Latency alarm created ✓")

if __name__ == "__main__":
    create_lambda_error_alarm()
    create_lambda_duration_alarm()
    print("\nAlarms visible at:")
    print("https://us-east-1.console.aws.amazon.com/cloudwatch/home#alarmsV2:")