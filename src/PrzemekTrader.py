from Trader import Trader
from Order import Order
import random

class PrzemekTrader(Trader):
    def playOnStock(self):
        self.cb.lock.acquire()
        try:
            order = Order(self.threadID, self.threadID, random.choice([1, 2, 3, 4]), random.choice([100, 110, 120, 130]))
            self.orderBook[random.choice(["ABB", "IBM"])].addOrder(random.choice(["ASK", "BID"]), order)
        finally:
            self.cb.lock.release()
