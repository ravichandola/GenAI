# user ki query ko judge karega ki coding related hai ya nahi
# agar coding related hai to isCoding ko true karega

import json
from openai import OpenAI
from typing import Literal
from models.state import State
from utils.client import client

def classify_query(state: State) :
    print("⚠️ classify_query")
    query = state['user_query']
    SYSTEM_PROMPT = """
    You are a helpful assistant that classifies user queries into two categories:
    - Coding related queries
    - Non-coding related queries
    
    Please respond with a JSON object containing a boolean field "isCoding":
    - Set "isCoding" to true if the query is related to programming, coding, software development, algorithms, etc.
    - Set "isCoding" to false if the query is about general topics, non-technical subjects, etc.
    """
    
    response = client.chat.completions.create(    
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        response_format={"type": "json_object"},
    )
    
    response_content = json.loads(response.choices[0].message.content)
    state['isCoding'] = response_content['isCoding']
    return state



def route_query(state: State) -> Literal["general_agent", "coding_agent"]:
    print("⚠️ route_query")
    return "coding_agent" if state["isCoding"] else "general_agent"




