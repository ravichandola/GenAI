from dotenv import load_dotenv
from openai import OpenAI
import json
import os
from prompts import SYSTEM_PROMPT

# Load environment variables from .env file
load_dotenv()

# Get model name from environment variable, default to gpt-3.5-turbo
MODEL_NAME = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo') 

client = OpenAI()

messages=[
    {"role": "system", "content": SYSTEM_PROMPT},
]

while True:
    user_input = input("Enter your query: ")
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )    
        raw_response = response.choices[0].message.content
        print("Debug - Raw response:", raw_response)  # Debug print
        
        messages.append(response.choices[0].message)
        parsed_response = json.loads(raw_response)
        
        if parsed_response.get("step") == "think":
            messages.append({ "role": "assistant", "content": "<>" })
            continue

        if parsed_response.get("step") != "result":
            print("          🧠:", parsed_response.get("content"))
            continue

        print("🤖:", parsed_response.get("content"))
        break
    except json.JSONDecodeError as e:
        print("Error: Invalid JSON response from API")
        print("Response received:", raw_response)
        print("JSON Error:", str(e))
        break
    except Exception as e:
        print(f"Error: {str(e)}")
        break
