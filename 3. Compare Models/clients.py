from openai import OpenAI
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    return OpenAI()



def get_gemini_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


