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

