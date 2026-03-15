from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from src.state import StoreState
from src.nodes import NODES
from src.nodes.tools.orders_tools import tools
import os

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

class OrdersGraph():



    def __init__(self):
        workflow = StateGraph(StoreState)
        workflow.add_node("fetch_orders", NODES["orders"])
        workflow.add_node("tools", ToolNode(tools))
        workflow.add_node("process_results", NODES["process_tools_results"])  # 👈 new node

        workflow.add_edge(START, "fetch_orders")
        workflow.add_edge("tools", "process_results")    # 👈 tools → process
        workflow.add_edge("process_results", "fetch_orders")     # 👈 process → back to agent
        workflow.add_conditional_edges(
            "fetch_orders",
            tools_condition                                          # decide si llamar tool o terminar
        )
        self.graph = workflow

graph = OrdersGraph().graph