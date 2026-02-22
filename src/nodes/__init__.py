from .message_listener import message_listener_node
from .message_categorizer import message_categoryzer_node

NODES = {
    "message_listener": message_listener_node,
    "message_categoryzer": message_categoryzer_node
}