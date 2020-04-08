class Order:
    def __init__(self, _orderID, _traderID, _stock, _quantity, _price):
        self.__orderID__ = _orderID
        self.__traderID__ = _traderID
        self.__stock__ = _stock
        self.__quantity__ = _quantity
        self.__price__ = _price

    def __str__(self):
        return str(self.__orderID__) + ":" + str(self.__traderID__) + ":" + str(self.__stock__) + ":" + str(self.__quantity__) + ":" + str(self.__price__)

    def getOrderID(self):
        return self.__orderID__

    def getTraderID(self):
        return self.__traderID__

    def getStock(self):
        return self.__stock__

    def getQuantity(self):
        return self.__quantity__

    def getPriceRange(self):
        return self.__price__

#dodal Dominik
    def changeQuantity(self, newQuantity):
        self.__quantity__ = newQuantity
