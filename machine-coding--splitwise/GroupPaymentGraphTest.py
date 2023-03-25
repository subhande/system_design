from decimal import Decimal

from models.Amount import Amount
from models.BalanceMap import BalanceMap
from models.Expense import Expense
from models.Group import Group
from models.PaymentGraph import PaymentGraph
from models.Currency import Currency
from models.User import User
from services.ExpenseService import ExpenseService
from services.GroupService import GroupService
from Splitwise import SplitWise


def constructExpenseService() -> ExpenseService:
    expenseService = ExpenseService(groupExpenses={})

    firstExpense = BalanceMap(resultBalances={})
    firstExpense.getBalances()["A"] = Amount(Decimal(10), Currency.USD)
    firstExpense.getBalances()["B"] = Amount(Decimal(20), Currency.USD)
    firstExpense.getBalances()["C"] = Amount(Decimal(-30), Currency.USD)
    expenseService.addExpense(
        Expense(firstExpense, "outing1", "www.interviewready.io", "outing 1", "123")
    )

    secondExpense = BalanceMap(resultBalances={})
    secondExpense.getBalances()["A"] = Amount(Decimal(-50), Currency.USD)
    secondExpense.getBalances()["B"] = Amount(Decimal(10), Currency.USD)
    secondExpense.getBalances()["C"] = Amount(Decimal(40), Currency.USD)
    expenseService.addExpense(
        Expense(secondExpense, "outing2", "www.interviewready.io", "outing 2", "123")
    )

    thirdExpense = BalanceMap(resultBalances={})
    thirdExpense.getBalances()["A"] = Amount(Decimal(90), Currency.USD)
    # thirdExpense.getBalances()["B"] = Amount(Decimal(0), Currency.USD)
    thirdExpense.getBalances()["C"] = Amount(Decimal(-90), Currency.USD)
    expenseService.addExpense(
        Expense(thirdExpense, "outing3", "www.interviewready.io", "outing 3", "123")
    )

    return expenseService


def constructExpenseService2() -> ExpenseService:
    expenseService = ExpenseService(groupExpenses={})

    firstExpense = BalanceMap(resultBalances={})
    firstExpense.getBalances()["A"] = Amount(Decimal(90), Currency.USD)
    firstExpense.getBalances()["B"] = Amount(Decimal(-70), Currency.USD)
    firstExpense.getBalances()["C"] = Amount(Decimal(-40), Currency.USD)
    firstExpense.getBalances()["D"] = Amount(Decimal(80), Currency.USD)
    firstExpense.getBalances()["E"] = Amount(Decimal(-100), Currency.USD)
    firstExpense.getBalances()["F"] = Amount(Decimal(40), Currency.USD)
    expenseService.addExpense(
        Expense(firstExpense, "outing1", "www.interviewready.io", "outing 1", "123")
    )
    return expenseService


def getGroups():
    groups: dict[str, Group] = {}
    userList: list[str] = ["A", "B", "C", "D", "E", "F"]
    groups["123"] = Group("Europe", "Euro trip", "www.interviewready.io", userList)
    return groups


def test_default_tests():
    expenseService: ExpenseService = constructExpenseService()
    groups: dict[str, Group] = getGroups()
    groupService: GroupService = GroupService(expenseService, groups)

    balances = groupService.getBalances("123", "A")
    balanceMap = balances.getBalances()

    assert balanceMap["A"].getAmount() == Decimal(
        50
    ), "A should have a balance of 50, but has a balance of " + str(
        balanceMap["A"].getAmount()
    )
    assert balanceMap["B"].getAmount() == Decimal(
        30
    ), "B should have a balance of 30, but has a balance of " + str(
        balanceMap["B"].getAmount()
    )
    assert balanceMap["C"].getAmount() == Decimal(
        -80
    ), "C should have a balance of 80, but has a balance of " + str(
        balanceMap["C"].getAmount()
    )


def test_default_tests2():
    expenseService: ExpenseService = constructExpenseService2()
    groups: dict[str, Group] = getGroups()
    groupService: GroupService = GroupService(expenseService, groups)

    balances = groupService.getGroupPaymentGraph("123", "A")
    graph = balances.getGraph()
    for k, v in graph.items():
        print(k, v)

    a = graph.get("A").getBalances().get("E").getAmount()
    assert a == Decimal(
        90
    ), "A should have a balance of 90, but has a balance of " + str(a)

    a = graph.get("D").getBalances().get("B").getAmount()
    assert a == Decimal(
        70
    ), "A should have a balance of 70, but has a balance of " + str(a)

    a = graph.get("F").getBalances().get("C").getAmount()
    assert a == Decimal(
        40
    ), "A should have a balance of 40, but has a balance of " + str(a)

    a = graph.get("D").getBalances().get("E").getAmount()
    assert a == Decimal(
        10
    ), "A should have a balance of 10, but has a balance of " + str(a)


# test_default_tests()
test_default_tests2()
