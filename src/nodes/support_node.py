


from state import StoreState


def build_support_node(state: StoreState) -> any:

    message = state["last_message"]
    if not message:
        state["support_answer"] = "Can't resolve at the moment."
        return state
    