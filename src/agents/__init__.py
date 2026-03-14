from .message_categorizer import categorize_message
from .support_clerk import solve_user_issue

AGENT_REGISTRY = {
    "message_categorizer": categorize_message(),
    "support_clerk": solve_user_issue()
}