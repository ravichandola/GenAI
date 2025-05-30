# Import required libraries
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt import SYSTEM_PROMPT
import json

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize conversation with system prompt
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

# Main conversation loop
while True:
    # Get user input and add to messages
    user_input = input("Enter your query: ")
    messages.append({"role": "user", "content": user_input})
    
    # Make API call to OpenAI
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=messages,
    )
    
    # Extract response content
    response_content = response.choices[0].message.content
    
    # Add assistant's response to conversation history
    messages.append({"role": "assistant", "content": response_content})
    
    # Parse JSON response if applicable
    try:
        raw_response = response.choices[0].message.content
        print("Debug - Raw response:", raw_response)  # Debug print
        
        parsed_response = json.loads(raw_response)
        
        # Check if we've reached the final result
        if parsed_response.get("step") == "think":
            messages.append({"role": "assistant", "content": "<>"})
            continue

        if parsed_response.get("step") != "result":
            print("          🧠:", parsed_response.get("content"))
            continue

        print("🤖:", parsed_response.get("content"))
        break
    except json.JSONDecodeError:
        print("Failed to parse JSON response")
        continue