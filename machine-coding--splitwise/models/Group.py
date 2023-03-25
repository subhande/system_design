
from typing import List
class Group:
    def __init__(self, name: str, desc: str, imageUrl: str, userList: List[str]):
        self.name = name
        self.desc = desc
        self.imageUrl = imageUrl
        self.userList = userList

    def getUsers(self) -> List[str]:
        return self.userList

    