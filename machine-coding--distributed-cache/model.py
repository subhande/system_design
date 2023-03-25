from enum import Enum
import time



class EvictionAlgorithm(Enum):
    LRU = 1
    LFU = 2


class FetchAlgorithm(Enum):
    WRITE_THROUGH = 1
    WRITE_BACK = 2


class AccessDetails:
    def __init__(self, lastAccessTime) -> None:
        self.accessCount = 0
        self.lastAccessTime = lastAccessTime

    def getLastAccessTime(self):
        return self.lastAccessTime

    def getAccessCount(self):
        return self.accessCount

    def update(self, lastAccessTime):
        accessDetails = AccessDetails(lastAccessTime)
        accessDetails.accessCount = self.accessCount + 1
        return accessDetails

    def __eq__(self, __o: object) -> bool:
        assert __o is not None and isinstance(__o, AccessDetails)
        return (
            self.accessCount == __o.accessCount
            and self.lastAccessTime == __o.lastAccessTime
        )

    def __hash__(self) -> int:
        return hash((self.accessCount, self.lastAccessTime))

    def __str__(self) -> str:
        return f"AccessDetails(accessCount={self.accessCount}, lastAccessTime={self.lastAccessTime})"


class Records:
    def __init__(self, key: any, value: any, insertionTime: int) -> None:
        self.key = key
        self.value = value
        self.insertionTime = insertionTime
        self.accessDetails = AccessDetails(insertionTime)

    def getKey(self):
        return self.key

    def getValue(self):
        return self.value

    def getInsertionTime(self):
        return self.insertionTime

    def getAccessDetails(self):
        return self.accessDetails

    def setAccessDetails(self, accessDetails: AccessDetails):
        self.accessDetails = accessDetails

    def __str__(self) -> str:
        return f"Records(key={self.key}, value={self.value}, insertionTime={self.insertionTime}, accessDetails={self.accessDetails})"


class Timer:
    @classmethod
    def getCurrentTime(cls):
        return int(time.time() * 1000)