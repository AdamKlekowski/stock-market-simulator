class Order:
    def __init__(self, order_id, trader_id, stock, quantity, price):
        self.orderID = order_id
        self.traderID = trader_id
        self.stock = stock
        self.quantity = quantity
        self.price = price
