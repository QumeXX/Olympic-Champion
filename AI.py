from openai import OpenAI
from Data import API_KEY

def AI_func(msg):
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
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
