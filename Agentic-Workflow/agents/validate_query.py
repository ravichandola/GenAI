from models.response import CodeAccuracyResponse
from models.state import State
from utils.client import client

def validate_query(state: State) :
    print("⚠️ validate_query")
    #state persist karna hai
    user_query = state["user_query"]
    llm_result = state["llm_result"]

    SYSTEM_PROMPT = """
    You are expert in calculating accuracy of the code according to the question.
        Return the percentage of accuracy
        
        User Query: {user_query}
        Code: {llm_result}
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4.1-mini",
        response_format=CodeAccuracyResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"User Query: {user_query}\nCode: {llm_result}"}
        ],
    )
    state['accuracy_score'] = response.choices[0].message.parsed.accuracy_percentage
    return state