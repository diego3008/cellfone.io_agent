from .message_listener import message_listener_node
from .message_categorizer import message_categoryzer_node
from .orders_nodes import build_orders_node
NODES = {
    "message_listener": message_listener_node,
    "message_categoryzer": message_categoryzer_node,
    "orders":  build_orders_node
}