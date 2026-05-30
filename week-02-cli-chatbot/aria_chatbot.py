import ollama
import json
from datetime import datetime

history = [
    {"role": "system", "content": """You are Aria, an AWS and DevOps specialist.
Only answer AWS and DevOps questions.
Always answer in this exact format:

Example question: What is S3?
Example answer:
- What: Object storage service on AWS
- Use case: Store static files, backups, ML datasets
- Key fact: 99.999999999% durability

Now follow this exact format for every answer.
Format:
- What: [one line explanation]
- Use case: [one line]
- Key fact: [one line]"""}
]

def ask(prompt, history):
    if len(prompt) > 500:
        return "Please keep your question under 500 characters."
    
    history.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    if len(history) > 11:
        history = [history[0]] + history[-10:]
    
    response = ollama.chat(
        model="mistral",
        messages=history,
        options={"num_predict": 100}  # limit to 100 tokens
    )
    
    history.append({
        "role": "assistant",
        "content": response.message.content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    return response.message.content

if __name__ == "__main__":
    print("Aria — AWS & DevOps Assistant. Type 'exit' to quit.\n")
    while True:
        user_input = input("Rajat: ")
        if user_input.lower() == "exit":
            with open("conversation.json", "w") as f:
                json.dump(history, f, indent=2)
            print("Conversation saved to conversation.json")
            break
        response = ask(user_input, history)
        print(f"\nAria: {response}\n")