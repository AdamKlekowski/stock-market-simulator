import threading
from Order import *
from OrderBook import *


class Trader(threading.Thread):
    __public_order_book__ = []

    def __init__(self, _traderID, _portfolio, _money, _order_book=OrderBook):
        threading.Thread.__init__(self)
        if type(_traderID) != int:
            raise TypeError("TraderID is a integer, different type given")
        if type(_portfolio):
            pass
        if type(_money) != float:
            raise TypeError("Money is a float, different type given")
        self.__traderID__ = _traderID
        self.__portfolio__ = _portfolio
        self.__money__ = _money
        self.__public_order_book__ = []
        self.__public_order_book__ = _order_book

    def getMoney(self):
        return self.__money__

    def getTraderID(self):
        return self.__traderID__

    def getPortfolio(self):
        return self.__portfolio__

    def playOnStockMarket(self):  # TODO to develop !
        order = Order(0, self.__traderID__, "IBM", 100, 1000)
        if self.__money__ > 1000:
            self.__public_order_book__.addOrder("ASK", order)
        else:
            self.__public_order_book__.addOrder("BID", order)

    def run(self):
        print(str(self.__traderID__) + " working and has " + str(self.__money__))  # TODO to delete
        for _ in range(1000):
            self.playOnStockMarket()
