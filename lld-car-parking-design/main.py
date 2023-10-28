from __future__ import annotations
from enum import Enum
from decimal import Decimal
from abc import ABC, abstractmethod
from copy import deepcopy
import uuid
from typing import List, Dict
import time

class CarParking2Main(Enum):
    car: str = "car"
    truck: str = "truck"
    van: str = "van"
    electric: str = "electric"
    motorbike: str = "motorbike"

class ParkingSpotType(Enum):
    Handicapped: str = "Handicapped"
    Compact: str = "Compact"
    Large: str = "Large"
    Electric: str = "Electric"

class Account(ABC):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Admin(Account):
    
    def addParkingFloor(self, p: ParkingLot, floor: ParkingFloor) -> bool:
        p.addFloor(floor)

    def addParkingSpot(self, floor: ParkingFloor, spot: ParkingSpot) -> bool:
        pass

    def addParkingDisplayBoard(self, floor: ParkingFloor, displayBoard: ParkingDisplayBoard) -> bool:
        pass

    def addEntrancePanel(self, floor: ParkingFloor, entrancePanel: EntrancePanel) -> bool:
        pass

    def addExitPanel(self, floor: ParkingFloor, exitPanel: ExitPanel) -> bool:
        pass

class ParkingAttendant(Account):
    def processTicket(self, ticket: ParkingTicket) -> bool:
        pass


class ParkingLot:
    def __init__(self, name: str, entrances: Dict[str, EntrancePanel], exits: Dict[str, ExitPanel], parkingFloors: Dict[str, ParkingFloor], globalDisplayBoard: ParkingDisplayBoard):
        self.parkingFloors = parkingFloors
        self.entrances = entrances
        self.exits = exits
        self.globalDisplayBoard = globalDisplayBoard
        self.name = name
    @classmethod
    def getInstance(self) -> ParkingLot:
        return ParkingLot("ParkingLot", [], [], [], ParkingDisplayBoard())
    
    def addEtrancePanel(self, entrancePanel: EntrancePanel):
        entrancePanel.setParkingDisplayBoard(self.globalDisplayBoard)
        self.entrances[entrancePanel.getId()] = entrancePanel
        return True
    
    def addExit(self, exitPanel: ExitPanel):
        exitPanel[exitPanel.getId()] = exitPanel
        return True
    
    def addFloor(self, floor: ParkingFloor):
        self.parkingFloors[floor.getId()] = floor
        return True


class ParkingTicket:
    def __init__(self, number):
        self.numberPlate = number
        self.timestamp = time.time()


class Vehicle:
    def __init__(self, numberPlate: str, type: CarParking2Main):
        self.numberPlate = numberPlate
        self.type = type
        self.parkingTicket = None

    def assignTicket(self, ticket: ParkingTicket) -> bool:
        self.parkingTicket = ticket
        return True

    def getNumberPlate(self) -> str:
        return self.numberPlate  

class Car(Vehicle):
    def __init__(self, numberPlate: str):
        super().__init__(numberPlate, CarParking2Main.car)

class Truck(Vehicle):
    def __init__(self, numberPlate: str):
        super().__init__(numberPlate, CarParking2Main.truck)


class EntrancePanel:
    def __init__(self, id: str):
        self.id = id
        self.parkingDisplayBoard = None

    def checkSpotAvailability(self, vehicle: Vehicle) -> bool:
        pass

    def issueParkingTicket(self, vehicle: Vehicle) -> ParkingTicket:
        if self.checkSpotAvailability(vehicle):
            return vehicle.issueParkingTicket(ParkingTicket(vehicle.getNumberPlate()))
        else:
            print("There is no available spot for your vehicle")

    def setGlobalDisplayBoard(self, globalDisplayBoard: ParkingDisplayBoard):
        self.parkingDisplayBoard = globalDisplayBoard



class ExitPanel:
    def __init__(self, id: str):
        self.id = id

    def acceptPayment(self, ticket: ParkingTicket) -> bool:
        pass

class ParkingFloor:
    def __init__(self, id: str, parkingSpots: Dict[str, ParkingSpot], parkingDisplayBoard: ParkingDisplayBoard, globalParkingDisplayBoard: ParkingDisplayBoard):
        self.id = id
        self.parkingSpots: Dict[str, ParkingSpot] = parkingSpots
        self.globalParkingDisplayBoard = globalParkingDisplayBoard
        self.parkingBoard = parkingDisplayBoard

    def addParkingSpot(self, parkingSpot: ParkingSpot) -> bool:
        self.parkingSpots[parkingSpot.getid()] = parkingSpot
        return True

    def getParkingBoard(self) -> ParkingDisplayBoard:
        return self.parkingBoard

    def getGlobalParkingBoard(self) -> ParkingDisplayBoard:
        return self.globalParkingDisplayBoard

    def getId(self) -> str:
        return self.id
    

class ParkingSpot:
    def __init__(self, id: str, floor: ParkingFloor, type: ParkingSpotType):
        self.id = id
        self.type = type
        self.isAvailable = True
        self.vehicle = None
        self.floor = floor

    def getid(self) -> str:
        return self.id

    def getSpotType(self) -> ParkingSpotType:
        return self.type

    def isFree(self) -> bool:
        return self.isAvailable

    def assignVehicle(self, vehicle: Vehicle) -> bool:
        self.isAvailable = False
        self.vehicle = vehicle
        self.floor.getParkingBoard().chnageCount(self.type, -1)
        self.floor.getGlobalParkingBoard().chnageCount(self.type, -1)
        return True

    def removeVehicle(self, vehicle: Vehicle) -> bool:
        self.isAvailable = True
        self.vehicle = None
        self.floor.getParkingBoard().chnageCount(self.type, 1)
        self.floor.getGlobalParkingBoard().chnageCount(self.type, 1)
        return True
    
class HandicappedSpot(ParkingSpot):
    def __init__(self, id: str, floor: ParkingFloor):
        super().__init__(id, floor, ParkingSpotType.Handicapped)

class CompactSpot(ParkingSpot):
    def __init__(self, id: str, floor: ParkingFloor):
        super().__init__(id, floor, ParkingSpotType.Compact)


class ElectricSpot(ParkingSpot):
    def __init__(self, id: str, floor: ParkingFloor):
        super().__init__(id, floor, ParkingSpotType.Electric)

    def acceptPayment(self) -> bool:
        pass

class ParkingDisplayBoard:
    def __init__(self, id: str, countParkingSpots: Dict[ParkingSpotType, int]):
        self.id = id
        self.countParkingSpots = countParkingSpots

    def changeCount(self, type: ParkingSpotType, count: int) -> bool:
        self.countParkingSpots[type] += count
        return True
    

