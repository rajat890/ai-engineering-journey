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


