from typing import List
from queue import PriorityQueue
import copy
from decimal import Decimal
from models.Amount import Amount
from models.BalanceMap import BalanceMap
from models.Expense import Expense
from models.PaymentGraph import PaymentGraph

from models.Currency import Currency
from pydantic import BaseModel


class ExpenseService:
    def __init__(self, groupExpenses: dict[str, List[Expense]] = {}):
        self.groupExpenses = groupExpenses

    def addExpense(self, expense: Expense):
        groupId = expense.getGroupId()
        if groupId is not None:
            if groupId in self.groupExpenses:
                self.groupExpenses[groupId].append(expense)
            else:
                self.groupExpenses[groupId] = [expense]

    def getGroupExpenses(self, groupId: str) -> List[Expense]:
        if groupId in self.groupExpenses:
            return self.groupExpenses[groupId]
        else:
            return []

    def getPaymentGraph(self, groupBalances: BalanceMap) -> PaymentGraph:
        positiveAmounts = PriorityQueue()
        negativeAmounts = PriorityQueue()
        for user, amount in groupBalances.getBalances().items():
            if amount.getAmount() > 0:
                positiveAmounts.put((amount.getAmount() * Decimal(-1), user, amount))
            else:
                negativeAmounts.put((amount.getAmount() * Decimal(1), user, amount))
        graph: dict[str, BalanceMap] = {}
        while not positiveAmounts.empty():
            largestPositive = positiveAmounts.get()
            largestNegative = negativeAmounts.get()
            largestPositiveUser = largestPositive[1]
            largestNegativeUser = largestNegative[1]
            negativeAmount = largestNegative[2].getAmount() * Decimal(-1)
            positiveAmount = largestPositive[2].getAmount()
            currency = largestNegative[2].getCurrency()
            if largestPositiveUser not in graph:
                graph[largestPositiveUser] = BalanceMap(resultBalances={})
            graph.get(largestPositiveUser).getBalances()[largestNegativeUser] = Amount(
                min(positiveAmount, negativeAmount), currency
            )
            remaining = positiveAmount - negativeAmount
            if remaining > 0:
                positiveAmounts.put(
                    (
                        remaining * Decimal(-1),
                        largestPositiveUser,
                        Amount(remaining, currency),
                    ),
                )
            elif remaining < 0:
                negativeAmounts.put(
                    (
                        remaining * Decimal(-1),
                        largestNegativeUser,
                        Amount(remaining, currency),
                    ),
                )
        return PaymentGraph(graph)
