import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
logs = boto3.client("logs", region_name="us-east-1")

LAMBDA_FUNCTION = "aria-chatbot"
LOG_GROUP = f"/aws/lambda/{LAMBDA_FUNCTION}"

# Bedrock Claude Haiku pricing
INPUT_TOKEN_COST  = 0.80 / 1_000_000   # $0.80 per million
OUTPUT_TOKEN_COST = 4.00 / 1_000_000   # $4.00 per million
LAMBDA_COST_PER_MS = 0.0000000167      # $0.0000000167 per ms at 1024MB

def get_lambda_metrics(hours=24):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    def get_metric(metric_name, stat):
        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/Lambda",
            MetricName=metric_name,
            Dimensions=[
                {"Name": "FunctionName", "Value": LAMBDA_FUNCTION}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=[stat]
        )
        datapoints = response['Datapoints']
        if not datapoints:
            return 0
        return sum(d[stat] for d in datapoints)

    invocations = get_metric("Invocations", "Sum")
    errors = get_metric("Errors", "Sum")
    duration_ms = get_metric("Duration", "Sum")

    return {
        "invocations": int(invocations),
        "errors": int(errors),
        "duration_ms": duration_ms,
        "error_rate": f"{(errors/invocations*100):.1f}%" if invocations > 0 else "0%"
    }

def estimate_costs(metrics):
    lambda_compute_cost = metrics['duration_ms'] * LAMBDA_COST_PER_MS
    
    # Estimate Bedrock tokens per invocation
    avg_input_tokens = 500
    avg_output_tokens = 150
    bedrock_cost = metrics['invocations'] * (
        (avg_input_tokens * INPUT_TOKEN_COST) +
        (avg_output_tokens * OUTPUT_TOKEN_COST)
    )
    
    total = lambda_compute_cost + bedrock_cost
    
    return {
        "lambda_compute": f"${lambda_compute_cost:.6f}",
        "bedrock_estimated": f"${bedrock_cost:.6f}",
        "total_estimated": f"${total:.6f}"
    }

def print_report(hours=24):
    print(f"\n{'='*50}")
    print(f"Aria Cost Report — Last {hours} hours")
    print(f"{'='*50}")
    
    metrics = get_lambda_metrics(hours)
    costs = estimate_costs(metrics)
    
    print(f"\n📊 Usage:")
    print(f"  Invocations:  {metrics['invocations']}")
    print(f"  Errors:       {metrics['errors']} ({metrics['error_rate']})")
    print(f"  Total Duration: {metrics['duration_ms']:.0f}ms")
    
    print(f"\n💰 Estimated Costs:")
    print(f"  Lambda compute: {costs['lambda_compute']}")
    print(f"  Bedrock tokens: {costs['bedrock_estimated']}")
    print(f"  Total:          {costs['total_estimated']}")
    
    print(f"\n📈 Projections:")
    invocations = metrics['invocations']
    if invocations > 0:
        cost_per_query = float(costs['total_estimated'].replace('$','')) / invocations
        print(f"  Cost per query:     ${cost_per_query:.6f}")
        print(f"  Daily (same rate):  ${cost_per_query * invocations:.4f}")
        print(f"  Monthly projection: ${cost_per_query * invocations * 30:.2f}")
    else:
        print(f"  No invocations in last {hours} hours")
    
    print(f"\n{'='*50}")

if __name__ == "__main__":
    print_report(hours=24)