import ollama

def ask(prompt):
    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.message.content

if __name__ == "__main__":
    while True:
        user_input = input("Ask anything: ")
        if user_input == "exit":
            break
        response = ask(user_input)
        print(response)