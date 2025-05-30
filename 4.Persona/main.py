import json
import os
from dotenv import load_dotenv
from models import load_prompt, get_response

# Load .env from current directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

def main():
    system_prompt = load_prompt()

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    print("Assistant is ready! Type your message below (type 'exit' to quit):")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit","bye","see you later"]:
            print("Exiting chat. Goodbye!")
            break
        messages.append({"role": "user", "content": user_input})

        try:
            raw_response = get_response(messages)
            # Try to parse as JSON
            try:
                parsed_response = json.loads(raw_response)
                step = parsed_response.get("step")
                content = parsed_response.get("content")

                if step == "think":
                    print("          🧠:", content)
                    messages.append({"role": "assistant", "content": raw_response})
                    continue
                elif step != "result":
                    print("          🧠:", content)
                    messages.append({"role": "assistant", "content": raw_response})
                    continue
                else:
                    print("🤖:", content)
                    messages.append({"role": "assistant", "content": raw_response})
            except json.JSONDecodeError:
                # If not JSON, just print the raw response
                print("🤖 (raw):", raw_response)
                messages.append({"role": "assistant", "content": raw_response})

        except Exception as e:
            print(f"Error: {str(e)}")
            break

if __name__ == "__main__":
    main()

