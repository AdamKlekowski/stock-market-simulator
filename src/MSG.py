class MSG:
    def __init__(self, _TraderID, _TypeofOrd, _Stock, _Quantity, _PriceMin, _PriceMax):
        if type(_TraderID) != str:
            raise TypeError("traderID is a string, different type given")
        if type(_TypeofOrd):
            pass
        if type(_Stock):
            pass
        if type(_Quantity) != int:
            raise TypeError("quantity is an integer, different type given")
        if type(_PriceMax) != float and type(_PriceMin) != float:
            raise TypeError("price is a float, different type given")
        self.__PriceMin__ = _PriceMin
        self.__PriceMax__ = _PriceMax
        self.__Quantity__ = _Quantity
        self.__Stock__ = _Stock
        self.__TraderID__ = _TraderID
        self.__TypeofOrd__ = _TypeofOrd

    def getPriceMin(self):
        return self.__PriceMin__

    def getPriceMax(self):
        return self.__PriceMax__

    def getStock(self):
        return self.__Stock__

    def getQuantity(self):
        return self.__Quantity__

    def getTypeofOrd(self):
        return self.__TypeofOrd__

    def getTraderID(self):
        return self.__TraderID__


a = MSG('123', 0, 0, 2, 1.1, 1.2)
print(a.getPriceMax())
