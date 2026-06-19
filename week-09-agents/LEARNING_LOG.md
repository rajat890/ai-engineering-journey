# Learning Log — Week 09

## Week 09 — Session 1 — 19 June 2026

### What was built
- AI Agent using Bedrock Converse API with tools
- calculator() tool — math using Python eval
- search_knowledge_base() tool — real Bedrock KB retrieval
- Agent decides which tool to call based on question

### How agents work
User asks question

→ Claude thinks → decides tool needed

→ returns stop_reason: "tool_use"

→ your code calls the tool

→ result sent back to Claude

→ Claude thinks again

→ returns stop_reason: "end_turn"

→ final answer

### Key concepts learned
- Agent = LLM + tools it can call at runtime
- stop_reason = "tool_use" → agent needs a tool
- stop_reason = "end_turn" → agent has final answer
- while True loop → keeps going until end_turn
- toolConfig → defines available tools to Claude
- retrieve() vs retrieve_and_generate() → retrieve gives raw chunks, more control
- Agent can chain tools — search KB then calculate

### Chatbot vs Agent
Chatbot  → fixed pipeline, one answer path

Agent    → flexible, chooses tools, chains actions

### Real world agent tools you can build
- check_ec2_status() → describe EC2 instances
- send_slack_alert() → post to Slack webhook
- run_kubectl() → execute Kubernetes commands
- query_cloudwatch() → get metrics and logs
- create_jira_ticket() → incident management

### Key insight
LLM never executes code directly.
It says "call this tool with these inputs."
Your Python function runs the tool.
Result goes back to LLM for final answer.
Claude = orchestrator, tools = workers. ✓

### Cost this session
Bedrock Converse API → ~$0.001 per agent run

Bedrock retrieve()   → ~$0.0001 per search

Total session        → ~$0.05 ✓

## Week 09 — Session 2 — 19 June 2026

### What was built
- agent_aws.py — agent with real AWS tool calls
- check_lambda_status() — queries actual Lambda function via boto3
- get_recent_logs() — fetches CloudWatch logs for any Lambda
- Combined KB search + AWS tools in one agent

### Key concepts learned
- bedrock-runtime → talk to LLM directly (converse, invoke_model)
- bedrock-agent-runtime → talk to managed AWS services (retrieve, retrieve_and_generate)
- get_function() → correct boto3 method for Lambda status
- boto3 naming pattern: get_ or describe_ never just the resource name
- Tool descriptions matter — better description = better tool selection
- One question can trigger multiple tools — agent chains them automatically
- Token discipline — one well-crafted question tests more than three separate ones

### Real AWS tools added
```python
check_lambda_status()  → lambda_client.get_function()
get_recent_logs()      → logs_client.filter_log_events()
```

### boto3 client reference
```python
bedrock-runtime        → converse(), invoke_model()
bedrock-agent-runtime  → retrieve(), retrieve_and_generate()
lambda                 → get_function(), list_functions()
logs                   → filter_log_events()
```

### Key insight
Agent = Claude (orchestrator) + your Python functions (workers)
Claude never executes code — it decides WHAT to call and WHEN
Your code does the actual work and returns results to Claude
Tool description quality directly determines tool selection accuracy