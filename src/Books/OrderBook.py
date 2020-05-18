class OrderBook:
    def __init__(self):
        self.BID = []
        self.ASK = []

    def addOrder(self, _type, _order):
        raise NotImplementedError()

    def getBID(self):
        return self.BID

    def getASK(self):
        return self.ASK

    def removeBID(self, _order):
        self.BID.remove(_order)

    def removeASK(self, _order):
        self.ASK.remove(_order)

    def changeQuantityBID(self, newQuantity):
        self.BID[0].changeQuantity(newQuantity)
        #TODO dopytać jak działa giełda
        #for bid in self.BID:
        #    if bid.getStock() == order.getStock():
        #       bid.changeQuantity(newQuantity)

    def changeQuantityASK(self, newQuantity):
        self.ASK[0].changeQuantity(newQuantity)

    def drawOrderBook(self):
        print("ASKS:")
        for i in range(0, len(self.ASK)):
            print(str(i) + ". " + str(self.ASK[i].price) + "  " + str(self.ASK[i].traderID))
        print("BIDS:")
        for i in range(0, len(self.BID)):
            print(str(i) + ". " + str(self.BID[i].price) + "  " + str(self.BID[i].traderID))
