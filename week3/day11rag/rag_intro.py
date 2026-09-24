import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"


# step 1
knowledge_base = {
    "company": "TechNova was founded in 2020.",
    "employees": "TechNova has 150 employees.",
    "product": "TechNova develops AI-powered software.",
    "location": "TechNova is headquartered in Bangalore."
}

# step 2 retreieval
def retrieve_info(question):
    question=question.lower()
    if "company" in question:
        return knowledge_base["company"]
    elif "employees" in question:
        return knowledge_base["employees"]
    elif "product" in question:
        return knowledge_base["product"]
    elif "location" in question:
        return knowledge_base["location"]
    else:
        return None
def ask_llm(question):
    context=retrieve_info(question)

    sys_prompt=f"""answer in one line only. Answer only based on this context. do not hallucinate. Context: {context}"""
    system_message={
        "role": "system",
        "content": sys_prompt

    }
    message={
        "role": "user",
        "content": question
    }
    messages=[system_message, message]
    response=client.chat.completions.create(model=model, messages=messages)
    answer=response.choices[0].message.content
    return answer


question = "When was company founded?"
print(ask_llm(question))