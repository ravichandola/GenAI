import os
from dotenv import load_dotenv
from clients import get_openai_client, get_gemini_client
import google.generativeai as genai

load_dotenv()

PROVIDER = os.getenv('PROVIDER', 'openai').lower()
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
GEMINI_MODEL = os.getenv('GEMINI_MODEL')
PROMPT_FILE = os.getenv('PROMPT_FILE')

def load_prompt():
    """
    Loads the prompt content from the file path specified in the PROMPT_FILE environment variable.
    Supports .txt (plain text) and .py (Python file with a variable named 'prompt' or ending with '_prompt').
    """
    if not PROMPT_FILE:
        raise Exception("PROMPT_FILE environment variable not set.")

    prompt_path = os.path.join(os.path.dirname(__file__), PROMPT_FILE)
    if not os.path.exists(prompt_path):
        raise Exception(f"Prompt file '{PROMPT_FILE}' not found at '{prompt_path}'.")
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt = f.read()
        print(f"Loaded prompt: {prompt}")
        return prompt
    
    
    
def get_response(messages):
    provider = PROVIDER
    if provider == 'openai':
        client = get_openai_client()
        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI Error: {e}")
    elif provider == 'gemini':
        genai_module = get_gemini_client()
        try:
            prompt = ""
            for msg in messages:
                prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
            model = genai_module.GenerativeModel(GEMINI_MODEL)  # e.g., 'gemini-pro'
            response = model.generate_content(prompt.strip())
            return response.text if response.text else "No response"
        except Exception as e:
            raise RuntimeError(f"Gemini Error: {e}")

    else:
        raise ValueError(f"Unsupported provider: {provider}")
    
    