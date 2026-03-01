from langgraph.graph import END, START, StateGraph
from src.state import StoreState
from src.nodes import NODES
import os

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

class OrdersGraph():



    def __init__(self):
        workflow = StateGraph(StoreState)
        workflow.add_node("fetch_orders", NODES["orders_nodes"])

        workflow.add_edge(START, "fetch_orders")
        workflow.add_edge("fetch_orders", END)

        self.graph = workflow.compile()

graph = OrdersGraph().graph