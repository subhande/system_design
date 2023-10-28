from models.BalanceMap import BalanceMap
class PaymentGraph:
    def __init__(self, graph: dict[str, BalanceMap]):
        self.graph = graph

    def getGraph(self) -> dict[str, BalanceMap]:
        return self.graph