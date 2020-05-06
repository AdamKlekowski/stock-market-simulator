class Order:
    def __init__(self, order_id, trader_id, quantity, price):
        self.orderID = order_id
        self.traderID = trader_id
        self.quantity = quantity
        self.price = price

    def getOrderID(self):
        return self.orderID

    def getQuantity(self):
        return self.quantity

    def changeQuantity(self, newQuantity):
        self.quantity = newQuantity

    def getPrice(self):
        return self.price
