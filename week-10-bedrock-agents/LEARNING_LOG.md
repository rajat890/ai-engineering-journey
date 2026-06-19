# Learning Log — Week 10

## Week 10 — Session 1 — 19 June 2026

### What was built
- aria-tool-lambda — Lambda function as Bedrock Agent tool
- Bedrock Agent (aria-agent) via Console
- Action Group: calculator tool → aria-tool-lambda
- Knowledge Base: aria-kb connected to agent
- test_agent.py — invokes agent from Python

### Architecture
test_agent.py

→ bedrock-agent-runtime.invoke_agent()

→ Bedrock Agent (aria-agent)

→ KB search (aria-kb) for company docs

→ Action Group → aria-tool-lambda for math

→ returns answer

### Key concepts learned
- Bedrock Agent = managed agent loop — no while True needed
- Action Group = collection of Lambda tools
- Lambda permission needed: lambda:InvokeFunction for bedrock.amazonaws.com
- TSTALIASID = default test alias for Console testing
- invoke_agent() returns streaming response — iterate completion events
- Agent instructions = system prompt for the agent
- KB description drives when agent searches KB vs uses tools

### Week 9 vs Week 10
Week 9  → you manage agent loop (~80 lines)

Week 10 → AWS manages agent loop (~20 lines)

Same result, different abstraction level

### Key insight
Bedrock Agent = managed orchestration layer
You define: tools (Lambda) + knowledge (KB) + instructions
AWS handles: tool calling, result routing, loop management
Same pattern as EKS vs self-managed Kubernetes ✓

### Cost this session
Bedrock Agent invocations → ~$0.001 per call

Lambda tool calls         → free tier

KB retrieval              → ~$0.0001 per search

Total                     → ~$0.05 ✓

### Next session — Week 11
- Observability — CloudWatch dashboards
- Cost monitoring per invocation
- Lambda performance metrics
- First production-grade monitoring setup