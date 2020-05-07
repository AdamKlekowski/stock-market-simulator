import time

from Trader import Trader
from Order import Order
import random


class NoisyTrader(Trader):
    def playOnStock(self):
        self.cb.lock.acquire()
        try:
            if random.choice(["ASK", "BID"]) == "ASK":
                stock_name = random.choice(["ABB", "IBM"])
                quantity = random.choice([1, 2])
                if stock_name in self.portfolio and self.portfolio[stock_name] > quantity:
                    order = Order(self.threadID, self.threadID, quantity, random.choice([100, 110, 120]))
                    self.orderBook[stock_name].addOrder("ASK", order)

            else:
                price = random.choice([100, 110, 120])
                if price < self.money:
                    order = Order(self.threadID, self.threadID, random.choice([1]), price)
                    self.orderBook[random.choice(["ABB", "IBM"])].addOrder("BID", order)
                    self.money -= price
        finally:
            self.cb.lock.release()
