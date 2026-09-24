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
prompt1="hi!"
prompt2="explain the difference between a cat and a dog."
prompt3=" write 100 words essay about the importance of exercise."
prompt4="write a short poem about the beauty of nature."
prompts=[prompt1,prompt2,prompt3,prompt4]
for prompt in prompts:
    message = {"role": role, "content": prompt}
    message = [message]
    response = client.chat.completions.create(model=model, messages=message,max_tokens=100000)
    usage = response.usage
    print(f"Prompt: {prompt} -->your tokens: {usage.prompt_tokens} completion_tokens: {usage.completion_tokens} total tokens: {usage.total_tokens}  Finish Reason: {response.choices[0].finish_reason}")
    answer = response.choices[0].message.content 
    print(answer)
#message = {"role": role, "content": prompt}
#message = [message]
#response = client.chat.completions.create(model=model, messages=message)
#print(response)
#answer = response.choices[0].message.content 
#print(answer)