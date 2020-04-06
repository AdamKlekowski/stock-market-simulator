from Order import Order


class OrderBook:
    __BID__ = []
    __ASK__ = []

    # dodane do testkow kernela
    __BID__ = [Order("b1", "1", "IBM", 1, 150), Order("b2", "2", "IBM", 2, 140), Order("b3", "3", "IBM", 2, 170)]
    __ASK__ = [Order("a1", "4", "IBM", 1, 140), Order("a2", "5", "IBM", 3, 130), Order("a3", "6", "IBM", 1, 170)]

    def addOrder(self, _type, _order):
        if type(_type) != str:
            raise TypeError("Type is a string, different type given")

        if _type == "BID":
            self.__BID__.append(_order)
        elif _type == "ASK":
            self.__ASK__.append(_order)
        else:
            raise ValueError("Type should be equal BID or ASK, different type given")

    def getBID(self):
        return self.__BID__

    def getASK(self):
        return self.__ASK__

    # dodal Dominik
    def removeBID(self, _order):
        self.__BID__.remove(_order)

    def removeASK(self, _order):
        self.__ASK__.remove(_order)

    def changeQuantityBID(self, order, newQuantity):
        for bid in self.__BID__:
            if bid.getStock() == order.getStock():
                bid.changeQuantity(newQuantity)

    def changeQuantityASK(self, order, newQuantity):
        for ask in self.__ASK__:
            if ask.getStock() == order.getStock():
                ask.changeQuantity(newQuantity)
