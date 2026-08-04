import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not found")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"
prompt = ("Explain how the process of a FIFA selection works.Also explain how the selection process is different for men and u17")
message={
    "role" : "user",
    "content" : prompt
}
messages=[message]
#response1=client.chat.completions.create(model=model, messages=messages)
# # print(response1)
#answer=response1.choices[0].message.content
#print(answer)


stream=client.chat.completions.create(model=model, messages=messages,stream=True,temperature=2)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
       print(content, end="", flush=True)