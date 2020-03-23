class Order:
    orderID = 0
    traderID = 0
    stock = ""
    quantity = 0
    priceRange = (0,0)

    def __init__(self, orderID, traderID, stock, quantity, priceRange):
        self.orderID = orderID
        self.traderID = traderID
        self.stock = stock
        self.quantity = quantity
        self.priceRange = priceRange