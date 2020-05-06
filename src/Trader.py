import threading
import logging
import MarketOrderBook


class Trader(threading.Thread):
    def __init__(self, threadID, orderBook, condition):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.threadID = threadID
        self.cond = condition
        self.isStop = False
        self.money = 0
        self.portfolio = {}
        self.orderBook = orderBook

    def stop(self):
        self.isStop = True

    def run(self):
        while True:
            with self.cond:
                self.cond.wait()
                if self.isStop:
                    break
                # work here
                self.playOnStock()

    def playOnStock(self):
        raise NotImplementedError()
