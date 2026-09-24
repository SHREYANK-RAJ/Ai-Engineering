import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)

model = SentenceTransformer("all-MiniLM-L6-v2") #384
groqmodel="openai/gpt-oss-120b"

documents = [
    "Customers can request a replacement for damaged products within 15 days of delivery.",
    "Orders above Rs 5000 qualify for free standard shipping.",
    "Customers receive a tracking link within 24 hours after their order is dispatched.",
    "Refunds are processed within 5 to 7 business days after the returned product is approved.",
    "Customers can change their delivery address before the order is shipped.",
    "Support tickets submitted through email are usually answered within one business day."

]

document_embeddings = model.encode(documents)

def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

def retrieve(qembedding):
    scores = []  # 0.4 
    for i, document in  enumerate(document_embeddings):
        score=cosine_similarity(qembedding,document )
        scores.append((score,documents[i]))
    scores.sort(reverse=True)
    return scores[0]  #line#0.9

def ask_llm(question,context):
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
    response=client.chat.completions.create(model=groqmodel, messages=messages)
    answer=response.choices[0].message.content
    return answer

query = "When can the customers change the delivery address?"
qembedding=model.encode(query)
score,context=retrieve(qembedding)
answer=ask_llm(query,context)
print(answer)