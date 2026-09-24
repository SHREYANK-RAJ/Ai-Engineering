import os 
from pathlib import Path
from dotenv import load_dotenv # type: ignore 
 
from groq import Groq          # type: ignore 

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"
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
Return ONLY JSON matching this schema.
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
#print(answer)

import json
raw_json=answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)



print(ticket.name)
print(ticket.email)
print(ticket.issue)




#prompt = "Write a short poem about the beauty of nature."
#message = {"role": role, "content": prompt}
#message = [message]
#response = client.chat.completions.create(model=model, messages=message)
#print(response)
#answer = response.choices[0].message.content 
#print(answer)