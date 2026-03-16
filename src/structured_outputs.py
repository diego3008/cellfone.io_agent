from pydantic import BaseModel, Field

from src.state import MessageCategory


class CategorizerMessageOutput(BaseModel):
    categories: list[MessageCategory] = Field(..., description="One or more categories assigned to the message. Assign multiple if the message clearly involves more than one intent (e.g. asking about both an order and a product).")