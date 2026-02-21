from langgraph.graph import StateGraph
from ..state import StoreState

class StoreGraph():

    def __init__(self):
        self.workflow = StateGraph(StoreState)
        self.workflow.add_node("message_categorizer", )

        self.graph = self.workflow.compile()

store_graph = StoreGraph().graph