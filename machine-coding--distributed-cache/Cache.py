
from asyncio import Future
from model import *
THRESHOLD_SIZE = 10
from queue import PriorityQueue

class Cache:
    def __init__(self, dataSource: dict, map: dict, fetchAlgorithm: FetchAlgorithm, evictionAlgorithm: EvictionAlgorithm) -> None:
        self.dataSource = dataSource
        self.map = map
        self.fetchAlgorithm = fetchAlgorithm
        self.evictionAlgorithm = evictionAlgorithm
        self.expiryTime = 1000
        self.expiryQueue = PriorityQueue()
        self.priorityQueue = PriorityQueue()
    def get(self, key: any) -> Records:
        if key in self.map and map[key].getAccessTimeStamp() - Timer.getTime() < self.expiryTime:
            return self.map[key].getValue()
        return self.dataSource.get(key)
    def set(self, key: any, value: Records) -> Records:
        if key in self.map:
            if self.fetchAlgorithm == FetchAlgorithm.WRITE_THROUGH:
                self.dataSource[key] = value
                # after update in datasource
                self.map[key] = value
                # Update immediately
            elif self.fetchAlgorithm == FetchAlgorithm.WRITE_BACK:
                self.map[key] = value
                # Update on datasource eventually
                self.dataSource[key] = value
            
        else:
            if len(list(self.map.keys())) >= THRESHOLD_SIZE:
                # Evict: LRU, LFU
                pass
                
    
