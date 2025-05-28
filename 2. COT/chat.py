from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
# Make sure to create a .env file with:
# OPENAI_API_KEY=your-api-key-here
load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello, world!"}],
)

print(response.choices[0].message.content)