
from models.state import State
from utils.client import client


def general_agent(state: State) :
    
    print("⚠️ general_agent")
    #state persist karna hai
    user_query = state["user_query"]

    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": user_query}
        ],
    )
    state['llm_result'] = response.choices[0].message.content
    return state