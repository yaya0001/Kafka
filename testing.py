import ollama
messages=[{
        "role": "user",
        "content": "You are a helpful assistant."
    }]
while True:
  prompt=input("you: ")
  messages.append({"role": "user", "content": prompt})
  res=ollama.chat(model="llama3:8b",
        messages=messages)
  reply = res["message"]["content"]
  print("Bot:", reply)

  messages.append({"role": "assistant", "content": reply})

