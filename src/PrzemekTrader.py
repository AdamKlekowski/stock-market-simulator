import time

from Trader import Trader
from Order import Order
import random
import logging
from Kernel import Kernel
from CommunicationBox import CommunicationBox

class PrzemekTrader(Trader):
    def playOnStock(self):
        self.cb.lock.acquire()
        try:
            #logging.debug("playing")
            order = Order(self.threadID, self.threadID, random.choice([1, 2, 3]), random.choice([100, 110, 120, 130]))
            self.orderBook[random.choice(["ABB", "IBM"])].addOrder(random.choice(["ASK", "BID"]), order)
        finally:
            self.cb.lock.release()
