from ..state import StoreState

def message_listener_node(state: StoreState) -> StoreState:
    messages = state["messages"]

    last_message = messages[-1]
    state["last_message"] = last_message
    print(f"Content: {last_message}")
    return state  # or return modified state