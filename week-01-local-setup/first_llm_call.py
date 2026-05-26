import ollama

history = []

def ask(prompt, history):
    history.append({"role": "user", "content": prompt})
    
    response = ollama.chat(
        model="mistral",
        messages=history
    )
    
    history.append({"role": "assistant", "content": response.message.content})
    
    return response.message.content

if __name__ == "__main__":
    while True:
        user_input = input("Ask anything: ")
        if user_input == "exit":
            break
        response = ask(user_input, history)
        print(response)