

from langchain_core.messages import RemoveMessage

from src.state import StoreState


def message_cleanup_node(state: StoreState):
    messages = state["messages"]
    
    # Define your threshold
    MAX_MESSAGES = 10
    
    if len(messages) > MAX_MESSAGES:
        # Get the messages to delete (oldest ones)
        messages_to_delete = messages[:-MAX_MESSAGES]  # keep only the last N
        
        return {"messages": [RemoveMessage(id=m.id) for m in messages_to_delete]}
    
    return {}