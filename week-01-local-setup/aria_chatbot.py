import ollama

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
    
    history.append({"role": "user", "content": prompt})
    
    if len(history) > 11:
        history = [history[0]] + history[-10:]
    
    response = ollama.chat(
        model="mistral",
        messages=history
    )
    
    history.append({"role": "assistant", "content": response.message.content})
    
    return response.message.content

if __name__ == "__main__":
    print("Aria — AWS & DevOps Assistant. Type 'exit' to quit.\n")
    while True:
        user_input = input("Rajat: ")
        if user_input == "exit":
            break
        response = ask(user_input, history)
        print(f"\nAria: {response}\n")