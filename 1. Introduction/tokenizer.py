import tiktoken

# Create a simple text to tokenize
text = "Hello, world!"

# Initialize the tokenizer
try:
    enc = tiktoken.get_encoding("cl100k_base")

    # Tokenize the text
    tokens = enc.encode(text)

    # Print the tokens
    print("Tokens:", tokens)

    # Convert tokens back to text
    decoded_text = enc.decode(tokens)
    print("Decoded text:", decoded_text)

except Exception as e:
    print("Error:", e)
    print("\nMake sure you have installed the tiktoken package using:")
    print("pip install tiktoken")
    print("\nAlso ensure you're running this script from the command line/terminal")
    print("and not just saving the file. Use:")
    print("python Introduction/token.py")