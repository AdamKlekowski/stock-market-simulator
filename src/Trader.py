class Trader():
    def __init__(self,_TraderID,_Portfolio,_Money):
        if type(_TraderID)!=str:
            raise TypeError("TraderID is a string, different type given")
        if type(_Portfolio):
            pass
        if type(_Money)!=float:
            raise TypeError("Money is a float, different type given")
        self.__TraderID__ = _TraderID
        self.__Portfolio__ = _Portfolio
        self.__Money__ = _Money
    def getMoney(self):
        return self.__Money__
    def getTraderID(self):
        return self.__TraderID__
    def getPortfolio(self):
        return self.__Portfolio__
a=Trader('aa',2,5.34)
print(a.__Money__)