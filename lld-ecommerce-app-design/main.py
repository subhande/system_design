from __future__ import annotations
from enum import Enum
from decimal import Decimal
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List
from uuid import uuid4



class Customer:
    def __init__(self, name: str, email: str, phone: str, address: List[Address], cart: Cart):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.cart = cart

    def returnItem(self, items: List[Item]) -> ReturnOrder:
        return ReturnOrder(items, self, Order.AMAZON_ADDRESS, self.address[0])

    def addToCart(self, item: Item):
       self.cart.addItem(item)

    def viewItems(self) -> List[Item]:
        return self.cart.getItemsList()

    def checkOut(self) -> Order:
        return Order(self.cart.getItemsList(), self, self.address[0], Order.AMAZON_ADDRESS)

class Item:
    def __init__(self, name: str, price: Decimal, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    def getAmount(self) -> Decimal:
        return self.price * self.quantity

class Cart:
    def __init__(self, items: List[Item]):
        self.items = items

    def getItemsList(self):
        return self.items

    def addItem(self, item: Item):
        self.items.append(item)

class Address:
    def __init__(self, addressLine1: str, addressLine2: str, city: str, state: str, pincode: str):
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.city = city
        self.state = state
        self.pincode = pincode

class Order:
    AMAZON_ADDRESS = Address("Amazon", "Amazon", "Amazon", "Amazon", "Amazon")
    def __init__(self, itemsList: List[Item], customer: Customer, payment: Payment, destinationAddress: Address, sourceAddress: Address):
        self.itemsList = itemsList
        self._id = str(uuid4())
        self.customer = customer
        self.amount = sum([item.getAmount() for item in itemsList])
        self.payment = payment
        self.destinationAddress = destinationAddress
        self.sourceAddress = sourceAddress

    def statusChange(self, orderStatus: OrderStatus):
        if orderStatus == OrderStatus.PAYMENT_COMPLETE:
            self.delivery = Delivery(self, "Initiated", self.itemsList, "Initiated")
        if orderStatus == OrderStatus.COMPLETED:
            [Invoice(self, item, item.price, item.price * 0.18) for item in self.itemsList]


class ReturnOrder:
    def __init__(self, items: List[Item], destinationAddress: Address, sourceAddress: Address):
        self.items = items
        self.amountToRefund =  sum([item.getAmount() for item in items])
        self.destinationAddress = destinationAddress
        self.sourceAddress = sourceAddress
        self._id = str(uuid4())
        self.orderDetails = OrderDetails(str(uuid4()), self.destinationAddress, self.sourceAddress)

class OrderDetails:
    def __init__(self, _id, destication: Address, source: Address):
        self.destinationAddress = destication
        self.sourceAddress = source
        self._id = _id

class Payment:
    def __init__(self, id_: str, paymentMethod: PaymentMethod, status: str):
        self.id_ = id_
        self.paymentMethod = paymentMethod
        self.status = status


class PaymentMethod(Enum):
    CREDIT_CARD = 1
    DEBIT_CARD = 2
    NET_BANKING = 3
    UPI = 4
    CASH_ON_DELIVERY = 5


class Product:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._id = str(uuid4())

class Delivery:
    def __init__(self, order: Order, status: str, itesmList: List[Item], deliveryUpdates: str):
        self.id_ = str(uuid4())
        self.order = order
        self.status = status
        self.itemsList = itesmList
        self.deliveryUpdates = deliveryUpdates


class OrderStatus(Enum):
    CHECKOUT = 1
    PAYMENT = 2
    PAYMENT_COMPLETE = 3
    INCOMPLETE = 4
    IN_FLIGHT = 5
    COMPLETED = 6


class Invoice:
    def __init__(self, order: Order, iem: Item, invoiceDetails: str, price: Decimal, taxes: Decimal):
        self.order = order
        self.item = iem
        self.invoiceDetails = invoiceDetails
        self.price = price
        self.taxes = taxes
