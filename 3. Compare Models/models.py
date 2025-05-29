from google import genai
from google.genai import types
from openai import OpenAI
import os
from dotenv import load_dotenv
from clients import get_gemini_client, get_openai_client

load_dotenv()




def get_openai_response(prompt):
    client = get_openai_client()    
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

def get_gemini_response(messages):
    client = get_gemini_client()
    
    # Get system message and latest user message
    system_message = ""
    user_message = ""
    
    for msg in messages:
        if msg["role"] == "system":
            system_message = msg["content"]
        elif msg["role"] == "user":
            user_message = msg["content"]
    
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        config=types.GenerateContentConfig(
            system_instruction=system_message
        ),
        contents=user_message  
    )
    return response.text
