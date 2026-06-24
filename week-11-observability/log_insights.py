import boto3
import time

logs = boto3.client("logs", region_name="us-east-1")

LOG_GROUP = "/aws/lambda/aria-chatbot"

def find_slow_requests(threshold_ms=5000, hours=24):
    query = f"""
    fields @timestamp, @duration, @message
    | filter @type = "REPORT"
    | filter @duration > {threshold_ms}
    | sort @duration desc
    | limit 10
    """

    print(f"Finding requests slower than {threshold_ms}ms...")

    response = logs.start_query(
        logGroupName=LOG_GROUP,
        startTime=int((time.time() - hours * 3600) * 1000),
        endTime=int(time.time() * 1000),
        queryString=query
    )

    query_id = response['queryId']

    while True:
        result = logs.get_query_results(queryId=query_id)
        if result['status'] == 'Complete':
            break
        time.sleep(1)

    results = result['results']
    if not results:
        print(f"No requests slower than {threshold_ms}ms found ✓")
        return

    print(f"\nSlow requests found: {len(results)}")
    for r in results:
        fields = {f['field']: f['value'] for f in r}
        print(f"  Time: {fields.get('@timestamp')} | Duration: {fields.get('@duration')}ms")

def find_errors(hours=24):
    query = """
    fields @timestamp, @message
    | filter @message like /ERROR/
    | sort @timestamp desc
    | limit 20
    """

    print(f"\nSearching for errors in last {hours} hours...")

    response = logs.start_query(
        logGroupName=LOG_GROUP,
        startTime=int((time.time() - hours * 3600) * 1000),
        endTime=int(time.time() * 1000),
        queryString=query
    )

    query_id = response['queryId']

    while True:
        result = logs.get_query_results(queryId=query_id)
        if result['status'] == 'Complete':
            break
        time.sleep(1)

    results = result['results']
    if not results:
        print("No errors found ✓")
        return

    print(f"Errors found: {len(results)}")
    for r in results:
        fields = {f['field']: f['value'] for f in r}
        print(f"  {fields.get('@timestamp')}: {fields.get('@message')[:100]}")

if __name__ == "__main__":
    find_slow_requests(threshold_ms=5000)
    find_errors()