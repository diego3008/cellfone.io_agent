from langgraph.graph import END, START, StateGraph
import os
from src.graph.orders_graph import graph as order_graph
from src.graph.products_graph import graph as products_graph
from src.nodes import NODES
from src.state import StoreState
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

class StoreGraph():

    def __init__(self):
        workflow = StateGraph(StoreState)
        workflow.add_node("msg_cleanup", NODES["cleanup"])
        workflow.add_node("message_listener", NODES["message_listener"])
        workflow.add_node("message_categoryzer", NODES["message_categoryzer"])

        #Subgraphs
        workflow.add_node("orders_subgraph", order_graph.compile())
        workflow.add_node("products_subgraph", products_graph.compile())

        
        workflow.add_edge(START, "msg_cleanup")
        workflow.add_edge("msg_cleanup", "message_listener")
        workflow.add_edge("message_listener", "message_categoryzer")


        # Conditional routing based on category
        workflow.add_conditional_edges(
            "message_categoryzer",
            self.route_by_category,
            {
                "order_inquiry": "orders_subgraph",
                "product_inquiry": "products_subgraph",
                "complaint": END,
                "policy_question": END,
                "other": END,
            }
        )

        # All subgraphs lead to END
        workflow.add_edge("orders_subgraph", END)
        workflow.add_edge("products_subgraph", END)

        self.graph = workflow.compile()

    def route_by_category(self, state: StoreState) -> str:
        """Reads the category set by the categorizer node and returns the route."""
        category = state["message_category"]
        return category


store_graph = StoreGraph().graph
