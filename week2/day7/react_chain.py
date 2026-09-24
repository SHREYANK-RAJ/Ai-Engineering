import os
from dotenv import load_dotenv
from groq import Groq
from time import sleep
import re
# Load API Key from .env file
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API Key not found!")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"
# TOOLS
def detect_issue(text):
    if "laptop" in text.lower():
        return "Hardware Issue"

    elif "payment" in text.lower():
        return "Billing Issue"

    else:
        return "General Support"
def create_ticket(issue):

    return "TICKET-1025"
def assign_engineer(ticket_id):

    return "Rahul Sharma (Support Engineer)"
def notify_customer(ticket_id):

    return "Notification Sent Successfully"

# Tool Dictionary
tools = {

    "detect_issue": detect_issue,

    "create_ticket": create_ticket,

    "assign_engineer": assign_engineer,

    "notify_customer": notify_customer

}
# System Prompt
system_prompt = """
You are an AI Customer Support Agent.

Available Tools

detect_issue(text)

create_ticket(issue)

assign_engineer(ticket_id)

notify_customer(ticket_id)

Rules

1. Think carefully.
2. Use only ONE tool at a time.
3. After Action, STOP.
4. Wait for Observation.
5. Never guess tool output.
6. Continue until task finishes.

Format

Thought: ...

Action: tool(argument)

When everything is complete

Final Answer: ...
"""
def run_agent(question):

    messages = [

        {
            "role": "system",
            "content": system_prompt
        },

        {
            "role": "user",
            "content": question
        }

    ]

    for step in range(10):

        print("\n-------------------------")
        print("STEP", step + 1)
        print("-------------------------")

        response = client.chat.completions.create(

            model=model,

            messages=messages,

            temperature=0

        )

        answer = response.choices[0].message.content

        print(answer)
        # Agent Finished
        if "Final Answer:" in answer:
            break
        # Find Action
        match = re.search(

            r"Action:\s*(\w+)\((.*?)\)",

            answer

        )

        if match:

            tool_name = match.group(1)

            tool_input = match.group(2)

            tool_input = tool_input.strip()

            tool_input = tool_input.strip('"')

            # Execute Tool

            if tool_name in tools:

                tool = tools[tool_name]

                observation = tool(tool_input)

            else:

                observation = "Tool Not Found"

            print("\nObservation:", observation)

            # Save Assistant Message

            messages.append({
                "role": "assistant",
                "content": answer

            })
            # Give Observation
            messages.append({
                "role": "user",
                "content": "Observation: " + str(observation)

            })
            sleep(2)

# User Question
prompt = """
My laptop is not starting after the latest software update.
Please help me.
"""
run_agent(prompt)