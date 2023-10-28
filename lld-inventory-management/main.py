from __future__ import annotations
from enum import Enum
from decimal import Decimal
from abc import ABC, abstractmethod
from copy import deepcopy
import uuid
from typing import List, Dict
import time


class InventoryManagement:
    productList: Dict[str, Product] = {}
    locationMap: Dict[Location, Unit] = {}

    def addProduct(self, p: Product) -> bool:
        self.productList.append(p)
    
    def getProduct(self, pid) -> Product:
        return self.productList.get(pid)

    def placeUnit(unit: Unit):
        unit.locationId = ""

    def getShelvesStatus(self):
        return self.locationMap
    
    def updateStatus(self, unit: Unit, status: Status):
        unit.status = status



class Order:
    productCount: Dict[Product, int] = {}

    
class User:
    def addProduct():
        InventoryManagement.addProduct(Product())
    

class Unit:
    id: str
    product_id: str
    locationId: str
    status: Status

class Product:
    id: int
    price: Decimal
    description: str
    weight: Decimal
    size: SIZE

class Location:
    id: str
    type: SIZE


class SIZE(Enum):
    SMALL: str = "SMALL"
    MEDIUM: str = "MEDIUM"
    LARGE: str = "LARGE"


class Status(Enum):
    INVENTORY: str = "inventory"
    TRANSIT: str = 'transit'
    DELIVERY: str = 'delivery'