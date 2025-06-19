from models.state import State
from utils.client import client


def coding_agent(state: State) :
    print("⚠️ coding_agent")
    #state persist karna hai
    user_query = state["user_query"]

    SYSTEM_PROMPT = """
    You are a expert in coding and you are given a user query and you need to help the user with their coding related queries.
    """
    
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ],
    )
    state['llm_result'] = response.choices[0].message.content
    return state