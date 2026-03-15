from langgraph.graph import END, START, StateGraph
from src.state import StoreState
from src.nodes import NODES
import os
from src.graph.orders_graph import graph as order_graph  # ajusta según tu estructura
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

class StoreGraph():

    def __init__(self):
        workflow = StateGraph(StoreState)
        workflow.add_node("msg_cleanup", NODES["cleanup"])
        workflow.add_node("message_listener", NODES["message_listener"])
        workflow.add_node("message_categoryzer", NODES["message_categoryzer"])

        #Subgraphs
        workflow.add_node("orders_subgraph", order_graph.compile())

        
        workflow.add_edge(START, "msg_cleanup")
        workflow.add_edge("msg_cleanup", "message_listener")
        workflow.add_edge("message_listener", "message_categoryzer")


        # Conditional routing based on category
        workflow.add_conditional_edges(
            "message_categoryzer",
            self.route_by_category,  # routing function
            {
                "operation_request": "orders_subgraph",
                "unknown": END
            }
        )
        
        # All subgraphs lead to END
        workflow.add_edge("orders_subgraph", END)

        self.graph = workflow.compile()

    def route_by_category(self, state: StoreState) -> str:
        """Reads the category set by the categorizer node and returns the route."""
        category = state["message_category"]
        return category


store_graph = StoreGraph().graph