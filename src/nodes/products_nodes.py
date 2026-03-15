import json
from langchain_core.messages import ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI

from ..state import StoreState
from ..prompts import PRODUCTS_AGENT_PROMPT
from dotenv import load_dotenv
from .tools.products_tools import tools
load_dotenv()


def build_products_node(state: StoreState) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini")
    llm_with_tools = llm.bind_tools(tools)
    messages = [SystemMessage(content=PRODUCTS_AGENT_PROMPT)] + state["messages"]
    result = llm_with_tools.invoke(messages)
    return {"messages": [result]}


def process_products_results(state: StoreState) -> dict:
    last_tool_message = next(
        m for m in reversed(state["messages"])
        if isinstance(m, ToolMessage)
    )

    match last_tool_message.name:
        case "get_products":
            return {"products": json.loads(last_tool_message.content)}
        case "get_product":
            return {"products": [json.loads(last_tool_message.content)]}
        case _:
            return {}
