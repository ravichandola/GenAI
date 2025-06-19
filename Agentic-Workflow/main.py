from graph_builder import build_graph
from models.state import State

def main():
    user = input("> ")

    _state: State = {
        "user_query": user,
        "accuracy_score": None,
        "isCoding": False,
        "llm_result": None
    }

    graph = build_graph()
    response = graph.invoke(_state)

    print(response)



main()
