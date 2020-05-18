from Traders.Trader import Trader
from Books.Order import Order
import random


class NoisyTrader(Trader):
    def playOnStock(self):
        self.cb.lock.acquire()
        try:
            if random.choice(["ASK", "BID"]) == "ASK":
                stock_name = random.choice(["ABB", "IBM"])
                quantity = random.choice([1, 2])
                if stock_name in self.portfolio and self.portfolio[stock_name] > quantity:
                    last_price = self.cb.stock_exchange_listing[stock_name][-1]
                    price = random.choice([last_price*1.30, last_price * 1.10, last_price * 1.0, last_price * 0.95])
                    order = Order(self.threadID, self.threadID, quantity, price, self.cb.time)
                    self.orderBook[stock_name].addOrder("ASK", order)
            else:
                stock_name = random.choice(["ABB", "IBM"])
                last_price = self.cb.stock_exchange_listing[stock_name][-1]
                price = random.choice([last_price*1.30, last_price*1.10, last_price * 1.0, last_price * 0.95])
                if price < self.money:
                    order = Order(self.threadID, self.threadID, random.choice([1]), price, self.cb.time)
                    self.orderBook[stock_name].addOrder("BID", order)
                    self.money -= price
        finally:
            self.cb.lock.release()
