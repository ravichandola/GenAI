from client import call_openai
from model import build_messages
from utils import parse_code_blocks, save_files, setup_and_run_app

def main():
    print("📝 Describe the React app you want to generate:")
    user_prompt = input("> ")
    
    print("🤖 Contacting GPT-4...")
    messages = build_messages(user_prompt)
    response = call_openai(messages)
    
    print("📁 Parsing and saving files...")
    code_blocks = parse_code_blocks(response)
    save_files(code_blocks)
    
    print("\n🚀 Setting up and running the app...")
    setup_and_run_app()

if __name__ == "__main__":
    main()
