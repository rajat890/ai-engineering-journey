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
    user_input = input("Ask anything: ")
    print(ask(user_input))