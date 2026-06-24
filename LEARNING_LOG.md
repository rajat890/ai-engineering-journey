# Learning Log — Week 11

## Week 11 — Sessions 1 & 2 — 24 June 2026

### What was built
- create_dashboard.py — CloudWatch dashboard with 4 Lambda metrics
- create_alarm.py — error and latency alarms
- cost_tracker.py — pulls CloudWatch metrics, calculates costs, projects monthly spend
- custom_metrics.py — pushes token usage and latency to CloudWatch custom namespace
- log_insights.py — queries logs for slow requests and errors

### Architecture
Every Lambda request

→ CloudWatch auto-captures: Invocations, Duration, Errors, Throttles

→ Your code pushes: InputTokens, OutputTokens, LatencyMs, QueryCostUSD

→ Dashboard visualises everything

→ Alarms fire when thresholds breached

→ cost_tracker.py reports spend anytime

→ log_insights.py finds problems automatically

### Concepts learned
- CloudWatch metrics = raw data source
- Dashboard = visual layer on metrics
- Alarms = automated alerts on metrics
- Custom metrics = your own data pushed via put_metric_data()
- Log Insights = SQL-like queries on CloudWatch logs
- Namespace = logical grouping of metrics (AWS/Lambda vs Aria/AIMetrics)
- Custom metrics cost: first 10 free, then $0.30/metric/month

### Key numbers from session
2 queries tested:

→ Lambda: $0.000180 compute

→ Bedrock: $0.000586 tokens

→ Monthly projection at current rate: $0.16

→ Average latency: 2100ms

### CloudWatch costs
Dashboard  → $3.00/month → DELETED after session

Alarms (2) → $0.20/month → KEPT (protection worth it)

Logs       → ~$0.015/month

Custom metrics → free tier

Total kept → ~$0.22/month

### Key insight
Same observability principles from DevOps apply to AI:
- Invocations = requests per second
- Duration = response time
- Errors = error rate
- Custom metrics = business-level KPIs
The only new thing is token cost tracking — unique to LLM systems