from langgraph.graph import END, START, StateGraph
from src.state import StoreState
from src.nodes import NODES
import os
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

class StoreGraph():

    def __init__(self):
        workflow = StateGraph(StoreState)
        workflow.add_node("message_listener", NODES["message_listener"])
        workflow.add_node("message_categoryzer", NODES["message_categoryzer"])
        workflow.add_edge(START, "message_listener")
        workflow.add_edge("message_listener", "message_categoryzer")
        workflow.add_edge("message_categoryzer", END)

        

        self.graph = workflow.compile()

store_graph = StoreGraph().graph