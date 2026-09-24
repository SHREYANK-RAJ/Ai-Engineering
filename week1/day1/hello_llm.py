import os 
from pathlib import Path
from dotenv import load_dotenv # type: ignore # Load .env file variables
from groq import Groq          # type: ignore # Import Groq client

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"
role= "user"
prompt = "Write a short poem about the beauty of nature."
message = {"role": role, "content": prompt}
message = [message]
response = client.chat.completions.create(model=model, messages=message)
#print(response)
answer = response.choices[0].message.content 
print(answer)