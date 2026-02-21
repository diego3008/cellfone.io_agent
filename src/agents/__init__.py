from .message_categorizer import categorize_message

AGENT_REGISTRY = {
    "message_categorizer": categorize_message
}