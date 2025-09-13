from openai import OpenAI

def AI_func(msg):
  with open("Token.txt", "r") as f:
    TOKEN = f.read()
    f.close()

  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=TOKEN,
  )

  completion = client.chat.completions.create(
    model="deepseek/deepseek-chat-v3-0324:free",
    messages=[
      {
        "role": "user",
          "content": msg
      }
    ]
  )

  return completion.choices[0].message.content