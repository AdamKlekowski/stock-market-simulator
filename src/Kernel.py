from OrderBook import *


class Kernel:
    __order_book__ = OrderBook()

    def getOrderBook(self):
        return self.__order_book__
