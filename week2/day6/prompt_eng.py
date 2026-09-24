import os 
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"

def llm_answer(prompt):
    message = {
        "role": "user",
        "content": prompt
    }
    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer

my_prompt="""
# ROLE
You are a professional travel planner.

# TASK
Recommend one travel destination based on the user's preferences.

# CONSTRAINT
- Recommend exactly ONE destination.
- Budget must be under ₹50,000.
- Trip duration should be 3-5 days.
- Give one famous attraction.

# OUTPUT FORMAT
Destination: <Place>
Budget: <Approx Budget>
Attraction: <Famous Place>

# EXAMPLE
User:
I love beaches and sunsets.


Output:
Destination: Goa
Budget: ₹30,000
Attraction: Baga Beach

# FALLBACK
If the preferences are unclear, respond exactly:
Destination: NONE
Budget: N/A
Attraction: N/A

User:
I enjoy staying at home not going anywhere. Give me a travel planner.
"""
print(llm_answer(my_prompt))

