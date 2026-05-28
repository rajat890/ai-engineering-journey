# Learning Log

## Week 01 — 24 May 2026
- Set up Ollama to run LLMs locally on M2
- Pulled and ran Mistral model via terminal
- Built first Python script to call LLM programmatically
- Learned: prompts need to be specific — "LLM" returned law degree answer
- Key analogy: Ollama = Docker for AI models, prompt = API request payload

## Week 01 — Session 2 — 25 May 2026
- Added while True loop for continuous conversation
- Learned: break exits a loop, same as Ctrl+C on a process
- Learned: functions make LLM calls reusable — import ask() anywhere
- Learned: vague prompts = unpredictable responses (prompt engineering preview)
- Key analogy: ask() function = Terraform module — write once, call everywhere

## Week 01 — Session 3 — 26 May 2026
- Added conversation memory using a history list
- Learned: state must live outside functions, not inside them
- Learned: return sends the result back to the caller — without it, None is returned
- Learned: role: assistant is how you feed Mistral its own previous replies
- Key analogy: stateless Lambda vs Lambda with DynamoDB — same concept

## Week 02 — Session 1 — 27 May 2026

### What was built
- Aria chatbot with system prompt and context window management
- Tested 4 system prompt variations: bullet points, simplified language, strict refusal, few-shot format
- Proved few-shot prompting enforces format but not restrictions

### Concepts learned
- System prompt = userdata for LLMs — sets behaviour before first message
- Tokens matter in production — cost, latency, context window all affected
- History trimming = log rotation — keep system prompt always, rotate old messages
- LLMs follow format instructions well, restriction instructions poorly
- Bedrock Guardrails = WAF for LLM — hard enforcement outside the model
- Few-shot prompting = giving examples inside the prompt for consistent output format

### Key insight
Same model + different system prompt = completely different product.
Multi-tenant AI = one model, one system prompt per customer.

## Week 02 — Session 2 — 28 May 2026

### What was built
- Added timestamps to every message in conversation history
- Saved full conversation to conversation.json on exit
- Added max token limit to prevent response drift
- Proved JSON is the right format — maps directly to DynamoDB structure in Week 7

### Concepts learned
- json.dump() serialises Python objects to disk — like writing Terraform state
- "w" mode creates file if not exists, overwrites if it does — like bash tee
- Timestamps reveal latency — short answers ~2s, long answers ~9s
- Hallucination drift — model over-generates when pattern matching kicks in
- num_predict limits tokens — first step toward cost and quality control

### Key insight
conversation.json structure today = DynamoDB item structure in Week 7.
No transformation needed when we move to AWS.
