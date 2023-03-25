from models.BalanceMap import BalanceMap


class Expense:
    def __init__(
        self,
        userBalances: BalanceMap,
        title: str,
        imageUrl: str,
        description: str,
        groupId: str,
    ):
        self.userBalances = userBalances
        self.title = title
        self.imageUrl = imageUrl
        self.description = description
        self.groupId = groupId

    def getUserBalances(self) -> BalanceMap:
        return self.userBalances

    def getGroupId(self) -> str:
        return self.groupId

    def __str__(self):
        return f"Expense(userBalances={self.userBalances}, title={self.title})"
