from src.graph.store_graph import StoreGraph

def main():
    print("Starting Langgraph Cellfone.io agent ...")
    initial_state = {
        "messages": ["I need all the orders made by users"],
        "message_category": "",
        "last_message": "",
        "last_checked_order": "",
        "orders": []
    }


    workflow = StoreGraph()
    graph = workflow.graph

    for output in graph.stream(initial_state):
        for node, state in output.items():
            print("Node:\n")
            print(f"{node}\n")
            print("State:\n")
            print(f"{state}\n")

if __name__ == "__main__":
    main()