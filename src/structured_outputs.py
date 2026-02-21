from pydantic import BaseModel, Field

from state import MessageCategory


class CategorizerMessageOutput(BaseModel):
    category: MessageCategory = Field(..., description="The category assigned to the message, indicating its type based on predefined rules.")