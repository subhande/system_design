from decimal import Decimal

class Amount:

    def __init__(self, amount: Decimal, currency: str):
        self.amount = amount
        self.currency = currency

    def __add__(self, amount: any) -> any:
        if not isinstance(amount, Amount):
            raise Exception("Not an Amount")
        if self.currency != amount.currency:
            raise Exception("Currencies don't match")
        return Amount(amount=self.amount + amount.amount, currency=self.currency)
    
    def getCurrency(self) -> str:
        return self.currency
    
    def getAmount(self) -> float:
        return self.amount

    def __str__(self) -> str:
        return f"Amount({self.amount} {self.currency})"
    


