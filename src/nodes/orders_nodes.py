

import json
from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from ..state import StoreState
from dotenv import load_dotenv
from .tools.orders_tools import tools
load_dotenv()


def build_orders_node(state: StoreState) -> any:

    llm = ChatOpenAI(model="gpt-4o-mini")
    llm_with_tools = llm.bind_tools(tools)

    def assistant(state: StoreState):
        messages = state["messages"]
        result = llm_with_tools.invoke(messages)
        return {"messages": [result]}

    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_edge("tools", "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    return builder.compile()

def process_tools_results(state: StoreState) -> any:
    last_tool_message = next(
        m for m in reversed(state["messages"])
        if isinstance(m, ToolMessage)
    )

    match last_tool_message.name:
        case "get_orders":
            return {"orders": json.loads(last_tool_message.content)}
        case "get_products":
            return {"products": json.loads(last_tool_message.content)}
        case _:
            return {}


