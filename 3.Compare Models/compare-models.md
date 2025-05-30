# AI Response Comparison Project

## Overview

This project compares responses from two AI models (OpenAI and Gemini) for the same question, analyzing their similarity and numerical answers.

## Components

### 1. Question Setup

```python
question = "If there are 3 apples and you take away 2, how many do you have?"

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"Q: {question}\nLet's think step by step."}
]
```

### 2. AI Model Integration

The project uses two AI models:

- OpenAI's model (via `get_openai_response`)
- Google's Gemini model (via `get_gemini_response`)

```python
# OpenAI API Call
openai_result = get_openai_response(messages[-1]["content"])

# Gemini API Call
gemini_result = get_gemini_response(messages)
```

Note: Currently, there's an implementation issue where the full messages array is being sent to Gemini instead of just the user message.

### 3. Response Comparison

#### Similarity Analysis

The project includes a function to calculate the similarity between responses using the Jaccard similarity coefficient:

```python
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
```

#### Numerical Answer Comparison

The code also extracts and compares numerical answers from both AI responses:

```python
# Extract numbers from responses
openai_answer = [int(word) for word in openai_result.split() if word.isdigit()]
gemini_answer = [int(word) for word in gemini_result.split() if word.isdigit()]

# Compare final answers
if len(openai_answer) > 0 and len(gemini_answer) > 0:
    if openai_answer[-1] == gemini_answer[-1]:
        print("Both AIs gave the same final number!")
    else:
        print("The AIs gave different final numbers")
```

## Output Format

The program outputs:

1. OpenAI's response
2. Gemini's response
3. Similarity percentage between responses
4. Whether the numerical answers match

## Inside .env

1. OPENAI_API_KEY
2. GEMINI_API_KEY
3. OPENAI_MODEL
4. GEMINI_MODEL
5. PROMPT_QUESTION

## Dependencies

- OpenAI API
- Google Gemini API
- Custom models module with:
  - `get_openai_response()`
  - `get_gemini_response()`

## Note

The implementation assumes the existence of a separate `models.py` file containing the API integration code for both AI models.
