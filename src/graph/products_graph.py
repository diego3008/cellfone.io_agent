from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from src.state import StoreState
from src.nodes import NODES
from src.nodes.tools.products_tools import tools


class ProductsGraph():

    def __init__(self):
        workflow = StateGraph(StoreState)
        workflow.add_node("fetch_products", NODES["products"])
        workflow.add_node("tools", ToolNode(tools))
        workflow.add_node("process_results", NODES["process_products_results"])

        workflow.add_edge(START, "fetch_products")
        workflow.add_edge("tools", "process_results")
        workflow.add_edge("process_results", "fetch_products")
        workflow.add_conditional_edges(
            "fetch_products",
            tools_condition
        )
        self.graph = workflow


graph = ProductsGraph().graph
