from Trader import Trader
from Order import Order
import random
import time
import logging

class PrzemekTrader(Trader):
    def playOnStock(self):
        self.lock.acquire()
        try:
            logging.debug("playing")
            order = Order(self.threadID, self.threadID, 1, random.choice([100, 110, 120, 130]))
            self.orderBook["IBM"].addOrder(random.choice(["ASK", "BID"]), order)
        finally:
            self.lock.release()
