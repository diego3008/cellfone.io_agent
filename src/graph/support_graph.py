


from langgraph.graph import StateGraph

from state import StoreState


class SupportGraph():

    def __init__(self):
        workflow = StateGraph(StoreState)
        

        self.graph = workflow

support_graph = SupportGraph().graph
