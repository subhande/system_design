from enum import Enum
from decimal import Decimal
from abc import ABC, abstractmethod
from copy import deepcopy
import uuid

class ThreadType(Enum):
    ONE_TO_ONE = "ONE_TO_ONE"
    GROUP = "GROUP"

class MessageStatus(Enum):
    RECEIVED = "RECEIVED"
    PARTIAL_RECEIVED = "PARTIAL_RECEIVED"

class ChatType(Enum):
    MESSAGE = "MESSAGE"
    REPLY = "REPLY"

class Attachment:
    def __init__(self, fileExtension: str, size: str):
        self.fileExtension = fileExtension
        self.size = size


class Group:
    def __init__(self, users: list[str], metaData: any) -> None:
        self._id = uuid.uuid1()
        self.users = users
        self.metaData = metaData

    def addMember(self, user: User, adder: User):
        if adder in self.users:
            self.users.append(user)
    def removeMember(self, user: User, remover: User):
        if remover in self.users and user in self.users:
            self.users.remove(user)

class Message:
    def __init__(
        self,
        _id: str,
        attachment: Attachment,
        body: str,
        sender: User,
        recived: Thread,
        status: MessageStatus,
        editatedAt: int,
        thread: str,
    ):
        self._id = _id
        self.attachment = attachment
        self.body = body
        self.sender = sender
        self.recived = recived
        self.status = status
        self.editatedAt = editatedAt
        self.thread = thread

    def status(self, status: MessageStatus):
        self.status = status

    def getThread(self) -> Thread:
        return self.thread

class Thread:
    def __init__(self, _id: str, threadType: any, messages: list[Message]):
        self._id = _id
        self.threadType = threadType
        self.messages = messages

    def type(self) -> ThreadType:
        return self.threadType

class Chat:
    def __init__(self, _id: str, _type: any):
        self._id = _id
        self._type = _type

class Reply:
    def __init__(self, _id: str, user: str, message: str, description: str):
        self.user = user
        self.message = message
        self.thread = description
        self._id = _id

class Reaction:
    def __init__(self, user: str, chat: Chat, description: str):
        self.user = user
        self.chat = Chat
        self.description = description


class User(ABC):
    def __init__(self, _id: str, lastActivityTime: int, status: str, messageQueue: MessageQueue):
        self._id = _id
        self.lastActivityTime = lastActivityTime
        self.status = status
        self.messageQueue = messageQueue

    def getPresence(self) -> int:
        return self.lastActivityTime

    def setStatus(self, status: str):
        self.status = status

    def send(self, message: Message):
        self.messageQueue.publish(message)

    def receive(self, message: Message):
        self.messageQueue.receivedMessage(message)

    def react(self, react: Reaction):
        self.messageQueue.publish(react)

    def edit(self, message: Message):
        self.messageQueue.publishEdit(message)

    def reply(self, reply: Reply):
        self.messageQueue.publish(reply)

    def createGroup(self, userList: list[str], metatData: any):
        Group(userList, metatData)

    def joinGroup(self, group: Group):
        group.addMember(self, self)

    def leaveGroup(self, group: Group):
        group.removeMember(self, self)

    def setStatus(self, status: str):
        pass


class MessageQueue:
    def publish(self, message: Message | Reply | Reaction):
        pass

    def publishedit(self, message: Message | Reply | Reaction):
        pass

    def receivedMessage(self, message: Message):
        if message.getThread().type() == ThreadType.ONE_TO_ONE:
            message.status(MessageStatus.RECEIVED)
        else:
            message.status(MessageStatus.PARTIAL_RECEIVED)

