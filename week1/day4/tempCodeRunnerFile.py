import os 
from pathlib import Path
from groq import Groq          # type: ignore 

def load_dotenv(path=".env"):
    env_path = Path(path)
    if not env_path.exists():
        return
    with env_path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
client = Groq(api_key=my_api_key)
model = "llama-3.1-8b-instant"
role= "user"
 
from pydantic import BaseModel # type: ignore
class Ticket (BaseModel):
    name:str
    email:str
    issue:str
schema = Ticket.model_json_schema()
response_format={
    "type": "json_object"
}
system_prompt=f"""
Extract the personal information from the ticket strictly based on this schema and give a json output.
{schema}
"""
message_system={
    "role": "system",
    "content": system_prompt
}


text = "hello my name is John Doe, my email is john.doe@example.com, and I am having trouble logging into my account.my address is 123 Main St, Anytown, USA."
prompt=f"""
Extract the personal information from the following ticket text and give a json output.
{text}
"""
message_user = {"role": "user", "content": prompt}
messages=[message_system,message_user]
response = client.chat.completions.create(model=model, messages=messages,response_format=response_format) # type: ignore
answer = response.choices[0].message.content 
print(answer)

#prompt = "Write a short poem about the beauty of nature."
#message = {"role": role, "content": prompt}
#message = [message]
#response = client.chat.completions.create(model=model, messages=message)
#print(response)
#answer = response.choices[0].message.content 
#print(answer)