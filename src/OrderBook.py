class OrderBook:
    __BID__ = []
    __ASK__ = []

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
