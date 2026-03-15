from .message_cleanup import message_cleanup_node
from .message_listener import message_listener_node
from .message_categorizer import message_categoryzer_node
from .orders_nodes import build_orders_node, process_tools_results
NODES = {
    "message_listener": message_listener_node,
    "message_categoryzer": message_categoryzer_node,
    "orders":  build_orders_node,
    "process_tools_results": process_tools_results,
    "cleanup": message_cleanup_node
}