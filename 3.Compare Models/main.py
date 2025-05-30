from models import get_openai_response, get_gemini_response  # assuming you've split them
import os
from dotenv import load_dotenv

load_dotenv()


# Define a sample question
question = os.getenv("PROMPT_QUESTION")

# Define messages in OpenAI-style format
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"Q: {question}\nLet's think step by step."}
]

# Call OpenAI
openai_result = get_openai_response(messages[-1]["content"])  # Only send user message to OpenAI
print("OpenAI response:")
print(openai_result)
print("\n")

# Call Gemini
gemini_result = get_gemini_response(messages)  # This is incorrect - we're sending the full messages array
print("Gemini response:")
print(gemini_result)


# Function to calculate similarity score between two strings
def calculate_similarity(text1, text2):
    # Convert to lowercase and split into words
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    # Calculate intersection and union
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    # Calculate Jaccard similarity
    similarity = len(intersection) / len(union)
    return similarity

# Calculate similarity between OpenAI and Gemini responses
similarity = calculate_similarity(openai_result, gemini_result)
print("\nHow similar are the responses?")
print(f"They are {similarity * 100:.0f}% similar")

# Try to find numbers in both responses
try:
    # Get all numbers from OpenAI response
    openai_answer = []
    for word in openai_result.split():
        if word.isdigit():
            openai_answer.append(int(word))
    
    # Get all numbers from Gemini response  
    gemini_answer = []
    for word in gemini_result.split():
        if word.isdigit():
            gemini_answer.append(int(word))
    
    # Check if both have numbers and compare last ones
    if len(openai_answer) > 0 and len(gemini_answer) > 0:
        if openai_answer[-1] == gemini_answer[-1]:
            print("\nBoth AIs gave the same final number!")
        else:
            print("\nThe AIs gave different final numbers")
except:
    print("\nSorry, couldn't find numbers to compare")
