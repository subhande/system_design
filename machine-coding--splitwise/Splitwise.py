from services.ExpenseService import ExpenseService
from services.GroupService import GroupService

class SplitWise:
    def __init__(self, groupService: GroupService, expenseService: ExpenseService):
        self.groupService = groupService
        self.expenseService = expenseService