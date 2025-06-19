from models.state import State
from agents.classifier import classify_query, route_query
from agents.coding_agent import coding_agent
from agents.general_agent import general_agent
from agents.validate_query import validate_query
from langgraph.graph import StateGraph, START, END


def build_graph() :
    graph_builder = StateGraph(State)
    # Add nodes to the graph
    graph_builder.add_node("classify_query", classify_query)
    graph_builder.add_node("route_query", route_query)
    graph_builder.add_node("coding_agent", coding_agent)
    graph_builder.add_node("general_agent", general_agent)
    graph_builder.add_node("validate_query", validate_query)
    
    # Add edges to the graph
    graph_builder.add_edge(START, "classify_query")
    graph_builder.add_conditional_edges("classify_query", route_query)

    graph_builder.add_edge("general_agent", END)

    graph_builder.add_edge("coding_agent", "validate_query")
    graph_builder.add_edge("validate_query", END)

    # Compile the graph to execute it 
    return graph_builder.compile()
    
    
    