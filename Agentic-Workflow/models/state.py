from typing import TypedDict

class State(TypedDict):
    user_query: str
    llm_result : str|None
    accuracy_score : str|None
    isCoding : bool
    


    