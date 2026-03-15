from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class StoreState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    last_message: str
    message_category: str
    last_checked_order: list[dict[str, Any]]
    orders: list[dict[str, Any]]    # replaced on each write
    products: list[dict[str, Any]] 
    support_anwer: str


class MessageCategory(str, Enum):
    ORDER_INQUIRY = "order_inquiry"      # any order-related request: check status, list orders, get order by ID
    PRODUCT_INQUIRY = "product_inquiry"  # browse catalog, get product details, check availability or pricing
    COMPLAINT = "complaint"              # user expresses dissatisfaction or reports a problem
    POLICY_QUESTION = "policy_question"  # questions about returns, warranties, shipping, or store policies
    OTHER = "other"                      # anything that does not fit the above