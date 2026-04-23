import ollama

messages = [
    {"role": "system", "content": "必ず日本語で返答してください。"}
]

while True:
    user_input = input("あなた: ")
    
    if user_input == "/bye":
        break
    
    messages.append({"role": "user", "content": user_input})
    
    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=messages
    )
    
    reply = response["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    
    print(f"AI: {reply}\n")