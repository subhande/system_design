from enum import Enum
from decimal import Decimal
from abc import ABC, abstractmethod
from copy import deepcopy

# TODO: Add LFU implementation

class Storage:
    def __init__(self, capacity: int):
        self.storage: dict = deepcopy({})
        self.capacity: int = capacity

    def add(self, key: str, value: str):
        if self.isStorageFull():
            print("Storage is full")
            return
        self.storage[key] = value
        

    def remove(self, key: str):
        if key not in self.storage:
            print("Key not found")
            return
        # del self.storage[key]
        self.storage.pop(key)

    def get(self, key: str) -> str:
        return self.storage.get(key)

    def isStorageFull(self) -> bool:
        return len(self.storage) == self.capacity
    
class DLLNode:
    def __init__(self, key: str, value: str) -> None:
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class DLL:
    def __init__(self) -> None:
        self.head = None
        self.tail = None

    def addNode(self, node: DLLNode):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    def removeNode(self, node: DLLNode):
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

    def moveNodeToTail(self, node: DLLNode):
        self.removeNode(node)
        self.addNode(node)


class EvictionPolicy(ABC):
    def __init__(self) -> None:
        self.dll = DLL()
        self.mapper = deepcopy({})

    @abstractmethod
    def keyAccessed(self, key: str):
        pass

    @abstractmethod
    def evictKey(self) -> str:
        pass


class LRUEP(EvictionPolicy):
    # Least Recently Used
    def keyAccessed(self, key: str):
        if key in self.mapper:
            self.dll.moveNodeToTail(self.mapper[key])
        else:
            node = DLLNode(key, None)
            self.dll.addNode(node)
            self.mapper[key] = node

    def evictKey(self) -> str:
        node = self.dll.head
        self.dll.removeNode(node)
        self.mapper.pop(node.key)
        return node.key
    

class FIFOEP(EvictionPolicy):
    # First In First Out
    def keyAccessed(self, key: str):
        if key not in self.mapper:
            node = DLLNode(key, None)
            self.dll.addNode(node)
            self.mapper[key] = node

    def evictKey(self) -> str:
        node = self.dll.head
        self.dll.removeNode(node)
        self.mapper.pop(node.key)
        return node.key


class LIFOEP(EvictionPolicy):
    # Last In First Out
    def keyAccessed(self, key: str):
        if key not in self.mapper:
            node = DLLNode(key, None)
            self.dll.addNode(node)
            self.mapper[key] = node

    def evictKey(self) -> str:
        node = self.dll.tail
        self.dll.removeNode(node)
        self.mapper.pop(node.key)
        return node.key



class LFUEP(EvictionPolicy):
    # TODO: Add LFU implementation
    pass
    

class GetEvictionPolicyFactory:
    
    def getEvictionPolicy(self, evictionPolicyName: str) -> EvictionPolicy:
        if evictionPolicyName == "LRU":
            return LRUEP()
        elif evictionPolicyName == "FIFO":
            return FIFOEP()
        elif evictionPolicyName == "LIFO":
            return LIFOEP()
        elif evictionPolicyName == "LFU":
            return LFUEP()
        else:
            return None
        
class Cache:
    def __init__(self, capacity: int, evictionPolicyName: str) -> None:
        self.storage: Storage = Storage(capacity)
        self.evictionPolicy: EvictionPolicy = GetEvictionPolicyFactory().getEvictionPolicy(evictionPolicyName)

    def get(self, key: str) -> str:
        self.evictionPolicy.keyAccessed(key)
        return self.storage.get(key)

    def put(self, key: str, value: str):
        if self.storage.isStorageFull():
            self.storage.remove(self.evictionPolicy.evictKey())
        self.storage.add(key, value)
        self.evictionPolicy.keyAccessed(key)

    def remove(self, key: str):
        self.storage.remove(key)
        self.evictionPolicy.keyAccessed(key)

    def isFull(self) -> bool:
        return self.storage.isStorageFull()

    def printCache(self):
        print(self.storage.storage)


if __name__ == "__main__":

    cache = Cache(3, "LRU")
    cache.put("a", "1")
    cache.put("b", "2")
    cache.put("c", "3")
    cache.printCache()
    cache.get("b")
    cache.printCache()
    cache.put("d", "4")
    cache.printCache()
    cache.put("e", "5")
    cache.printCache()
    cache.put("f", "6")
    cache.printCache()
    cache.get("a")
    cache.printCache()
    cache.put("g", "7")
    cache.printCache()
    cache.put("h", "8")
    cache.printCache()
    cache.put("i", "9")
    cache.printCache()
    cache.put("j", "10")
    cache.printCache()
    cache.put("k", "11")
    cache.printCache()
    cache.put("l", "12")
    cache.printCache()
    cache.put("m", "13")
    cache.printCache()

    