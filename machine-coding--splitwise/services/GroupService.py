from decimal import Decimal
from typing import List
from models.PaymentGraph import PaymentGraph
from models.Expense import Expense
from models.Group import Group
from models.BalanceMap import BalanceMap
from models.Amount import Amount
from services.ExpenseService import ExpenseService


class GroupService:

    def __init__(self, expenseService: ExpenseService, groups: dict[str, Group]):
        self.expenseService = expenseService
        self.groups = groups
    
    def getGroupPaymentGraph(self, groupId: str, userId: str) -> PaymentGraph:
        return self.expenseService.getPaymentGraph(self.getBalances(groupId, userId))
    
    def sumExpenses(self, groupExpenses: List[Expense]) -> BalanceMap:
        resultBalances: dict[str, Amount] = {}
        for expense in groupExpenses:
            for user, amount in expense.getUserBalances().getBalances().items():
                if user in resultBalances:
                    resultBalances[user] += amount
                else:
                    resultBalances[user] = amount
        return BalanceMap(resultBalances)
    
    def getBalances(self, groupId: str, userId: str) -> BalanceMap:
        if userId not in self.groups.get(groupId).getUsers():
            raise Exception("User not in group")
        groupExpenses: List[Expense] = self.expenseService.getGroupExpenses(groupId)
        resultExpense = self.sumExpenses(groupExpenses)
        return resultExpense