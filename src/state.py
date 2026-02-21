from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class StoreState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    message_category: str

class MessageCategory(str, Enum):
    PRODUCT_INQUIRY = "product_inquiry"
    ORDER_STATUS = "order_status"
    POLICY_QUESTION = "policy_question"
    COMPLAINT = "complaint"
    OPERATION_REQUEST = "operation_request"  # new: triggers operations agent
    OTHER = "other"