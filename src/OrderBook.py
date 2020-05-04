from Order import Order


class OrderBook:
    def __init__(self):
        BID = []
        ASK = []
        # dodane do testkow kernela
        BID = [Order("b1", "1", "IBM", 1, 150), Order("b2", "2", "IBM", 2, 140), Order("b3", "3", "IBM", 2, 170)]
        ASK = [Order("a1", "4", "IBM", 1, 140), Order("a2", "5", "IBM", 3, 130), Order("a3", "6", "IBM", 1, 170)]

    def addOrder(self, _type, _order):
        if type(_type) != str:
            raise TypeError("Type is a string, different type given")

        if _type == "BID":
            self.BID.append(_order)
        elif _type == "ASK":
            self.ASK.append(_order)
        else:
            raise ValueError("Type should be equal BID or ASK, different type given")

    def getBID(self):
        return self.BID

    def getASK(self):
        return self.ASK

    # dodal Dominik
    def removeBID(self, _order):
        self.BID.remove(_order)

    def removeASK(self, _order):
        self.ASK.remove(_order)

    def changeQuantityBID(self, order, newQuantity):
        for bid in self.BID:
            if bid.getStock() == order.getStock():
                bid.changeQuantity(newQuantity)

    def changeQuantityASK(self, order, newQuantity):
        for ask in self.ASK:
            if ask.getStock() == order.getStock():
                ask.changeQuantity(newQuantity)
