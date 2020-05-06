import logging
import threading
import time
import Trader
import PrzemekTrader
from MarketOrderBook import MarketOrderBook

NUM_OF_AGENTS = 3
NUM_OF_ITERATIONS = 3


class Kernel:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s (%(threadName)-2s) %(message)s',
                            datefmt="%H:%M:%S")

        logging.debug("the begin of simulation")
        logging.debug("numbers of traders: " + str(NUM_OF_AGENTS))
        logging.debug("numbers of iterations: " + str(NUM_OF_ITERATIONS))
        self.progress = 0
        time.sleep(0.5)

        # markets
        self.orderBook = {
            "IBM": MarketOrderBook()
        }

        self.time_begin = time.time()
        self.condition = threading.Condition()
        self.threads = []
        for i in range(0, NUM_OF_AGENTS):
            self.threads.append(PrzemekTrader.PrzemekTrader(i, self.orderBook, self.condition))

        for t in self.threads:
            t.start()

        for i in range(0, NUM_OF_ITERATIONS):
            self.wakeUpAll(i)
            time.sleep(1)
            self.transations()

        self.endSimulation()

    def wakeUpAll(self, i):
        with self.condition:
            # logging.debug('New turn: ' + str(i))
            self.condition.notifyAll()

            if i / NUM_OF_ITERATIONS >= 0.25 and self.progress == 0:
                logging.debug("25% of simulation")
                self.progress += 1
            elif i / NUM_OF_ITERATIONS >= 0.50 and self.progress == 1:
                logging.debug("50% of simulation")
                self.progress += 1
            elif i / NUM_OF_ITERATIONS >= 0.75 and self.progress == 2:
                logging.debug("75% of simulation")
                self.progress += 1

    def endSimulation(self):
        time_end = time.time()
        logging.debug("time of simulation: " + str(time_end - self.time_begin))

        for t in self.threads:
            t.stop()
        self.wakeUpAll(9999)
        for t in self.threads:
            t.join()
        logging.debug("the end of simulation")

    def transations(self):
        for name, market in self.orderBook.items():
            bids = market.getBID()
            asks = market.getASK()
            while True:
                    if (not bids) or (not asks):
                        #print("not enough offers - " + str(name) )
                        break

                    elif bids[0].getPrice() < asks[0].getPrice():
                        #print("the spread of " + str(name) + " is " + str(market.getASK()[0].getPrice() - market.getBID()[0].getPrice()))
                        break
                    else:
                        if bids[0].getQuantity() < asks[0].getQuantity():
                            #print("firma " + str(bids[0].getOrderID()) + " kupuje " + str(bids[0].getQuantity()) + " od firmy " + str(asks[0].getOrderID()))
                            market.removeBID(market.getBID()[0])
                            market.changeQuantityASK(asks[0].getQuantity() - bids[0].getQuantity())

                        elif bids[0].getQuantity() > asks[0].getQuantity():  # aks<bid
                            #print("firma " + bids[0].getOrderID() + " kupuje " + str(asks[0].getQuantity()) + " od firmy " + asks[0].getOrderID())
                            market.removeASK(asks[0])
                            market.changeQuantityBID(bids[0].getQuantity() - bids[0].getQuantity())

                        else:
                            #print("firma " + str(bids[0].getOrderID()) + " kupuje " + str(bids[0].getQuantity()) + " od firmy " + str(asks[0].getOrderID()))
                            market.removeBID(market.getBID()[0])
                            market.removeASK(market.getASK()[0])
                        #TODO wysyłanie traderom komunikatu

    """test"""
    def drawMarket(self):
        for name, market in self.orderBook.items():
            market.drawOrderBook()


if __name__ == "__main__":
    kernel = Kernel()
