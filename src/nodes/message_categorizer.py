from ..agents import AGENT_REGISTRY
from ..state import StoreState

def message_categoryzer_node(state: StoreState) -> StoreState:
    message = state["last_message"]

    if not message:
        state["message_category"] = "Not message"
        return state
    result = AGENT_REGISTRY["message_categorizer"].invoke({"message" : message})
    state["message_category"] = result.category.value
    return state