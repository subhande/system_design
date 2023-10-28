from enum import Enum
from decimal import Decimal
from abc import ABC, abstractmethod
from copy import deepcopy

class PaymentGateway:
    pass

class Account:
    pass

class StateName(Enum):
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"

class StrategyName(Enum):
    CASH = "CASH"
    CROSS_COUNTRY = "CROSS_COUNTRY"
    ONLINE = "ONLINE"

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    INR = "INR"

class PaymentMethod(Enum):
    CARD = "CARD"
    UPI = "UPI"
    BANK_TRANSFER = "BANK_TRANSFER"
    GIFT = "GIFT"

class Amount:
    def __init__(self, amount: Decimal, currency: Currency):
        self.amount = amount
        self.currency = currency

class Status(ABC):
    def __init__(self, name: StateName) -> None:
        self.name = name
    @abstractmethod
    def notifyUsers(self, senderAccount: Account, receiverAccount: Account):
        pass

class Transaction:
    def __init__(self, status: Status, _id: str, amount: Amount, senderAccount: Account, receiverAccount: Account, description: str, paymentMethod: PaymentMethod):
        self.status = status
        self._id = _id
        self.amount = amount
        self.senderAccount = senderAccount
        self.receiverAccount = receiverAccount
        self.description = description
        self.paymentMethod = paymentMethod
       

    def changeState(self, newState: Status):
        oldState: Status = deepcopy(self.status)
        self.status = newState
        self.state.notifyUsers(self.senderAccount, self.receiverAccount, oldState)

class Strategy(ABC):
    def __init__(self, strategyName: StrategyName) -> None:
        self.strategyName = strategyName

    @abstractmethod
    def validate(self, t: Transaction) -> bool:
        pass

class CashStrategy(Strategy):
    def __init__(self) -> None:
        super().__init__(StrategyName.CASH)

    def validate(self, t: Transaction) -> bool:
        return t.amount.value <= 100
    

class OnlineStrategy(Strategy):
    def __init__(self) -> None:
        super().__init__(StrategyName.ONLINE)

    def validate(self, t: Transaction) -> bool:
        return t.amount.value <= 1000



class RuleEngine:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def setStrategy(self, strategy: Strategy):
        self.strategy = strategy

    def validate(self, t: Transaction) -> bool:
        return self.strategy.validate(t)

    def isFraud(self, t: Transaction) -> bool:
        return False


class Bank:
    def __init__(self, _id: str, name: str, metaData: str):
        self._id = _id
        self.name = name
        self.metaData = metaData


class User:
    def __init__(self, _id):
        self._id = _id

    def create(self, t: Transaction):
        pass

class Account:
    def __init__(self, bank: Bank, user: User, _id: str) -> None:
        self.bank = bank
        self.user = user
        self._id = _id



class SuccessfulTransaction(Status):
    def notifyUsers(self, senderAccount: Account, receiverAccount: Account, oldState: Status):
        if oldState.name == StateName.IN_PROGRESS:
            # Notify sccessful transaction to sender and receiver through email
            pass
        elif oldState.name == StateName.ON_HOLD:
            # Notify sccessful transaction to sender and receiver through email and sms
            pass


class FailedTransaction(Status):
    def notifyUsers(self, senderAccount: Account, receiverAccount: Account, oldState: Status):
        if oldState.name == StateName.IN_PROGRESS:
            # Notify failed transaction to sender and receiver through email
            pass
        elif oldState.name == StateName.ON_HOLD:
            # Notify failed transaction to sender and receiver through email and sms
            pass

    



