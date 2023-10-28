from models.Amount import Amount


class BalanceMap:
    def __init__(self, resultBalances: dict[str, Amount] = {}):
        self.balances = resultBalances

    def getBalances(self) -> dict[str, Amount]:
        return self.balances

    def __str__(self):
        str__ = "BalanceMap(balances="
        for k, v in self.balances.items():
            str__ += f"{k}: {v} "
        str__ += ")"
        return str__
