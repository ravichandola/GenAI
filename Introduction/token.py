enc = tiktoken.get_encoding("cl100k_base")  # Updated to use the correct method
text = "Hello, world!"
tokens = enc.encode(text)
print("Tokens:", tokens)

detokenized_text = enc.decode(tokens)
print("Detokenized text:", detokenized_text)