# Import required libraries
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt import SYSTEM_PROMPT
import json

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# TODO :Initialize conversation with system prompt
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

# Main conversation loop
while True:
    #TODO : Get user input and add to messages
    user_input = input("Enter your query: ")
    messages.append({"role": "user", "content": user_input})
    
    # TODO : Make API call to OpenAI
    response = client.chat.completions.create(
        # * Get model name from environment variable
        model=os.getenv("OPENAI_MODEL"),
        # * Pass messages to the model
        messages=messages,
    )
    
    # TODO : Extract response content
    response_content = response.choices[0].message.content
    
    # TODO : Add assistant's response to conversation history
    messages.append({"role": "assistant", "content": response_content})
    
    # TODO : Display raw response
    print(response_content)
    
    # TODO : Parse JSON response if applicable
    if response_content.startswith("{"):
        parsed_response = json.loads(response_content)
        print(parsed_response)
        
    if parsed_response.get("step") == "think":
        print("🧠 Thinking...")
        print("--------------------------------")
        continue
    
    # TODO : Check if we've reached the final result
    if parsed_response.get("step") != "result":
        print("          🧠:", parsed_response.get("content"))
        continue
    
    print("🤖:", parsed_response.get("content"))
    break
   
