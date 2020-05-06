import logging
import random
import threading
import time

import numpy

import PrzemekTrader
from CommunicationBox import CommunicationBox
from MarketOrderBook import MarketOrderBook
import matplotlib.pyplot as plt

NUM_OF_AGENTS = 100
NUM_OF_ITERATIONS = 50


class Kernel:
    def __init__(self):
        self.cb = CommunicationBox()
        self.threads = []

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s (%(threadName)-2s) %(message)s',
                            datefmt="%H:%M:%S")

        logging.debug("the begin of simulation")
        logging.debug("numbers of traders: " + str(NUM_OF_AGENTS))
        logging.debug("numbers of iterations: " + str(NUM_OF_ITERATIONS))
        self.progress = 0
        # markets
        self.orderBook = {
            "IBM": MarketOrderBook(),
            "ABB": MarketOrderBook()
        }

        self.time_begin = time.time()

        for i in range(0, NUM_OF_AGENTS):
            self.threads.append(PrzemekTrader.PrzemekTrader(i, self.cb, self.orderBook, random.choice([1, 2, 3, 4, 5])))

        for t in self.threads:
            t.start()

        for i in range(0, NUM_OF_ITERATIONS):
            #logging.debug("New turn: " + str(i))
            self.cb.clear_counter()
            self.cb.wakeUpAll()
            isWait = True
            while isWait:
                if self.cb.attendance_counter == NUM_OF_AGENTS:
                    self.transations()
                    isWait = False
                time.sleep(0.001)
            #logging.debug(self.cb.attendance_counter)

        self.endSimulation()

        # for t in self.threads:
        #     print(t)

        # for s in self.cb.getPriceListing("IBM"):
        #     print(s, end=", ")
        #
        # for name in self.orderBook:
        #     plt.plot(self.cb.getPriceListing(name))
        # plt.show()

    # def wakeUpAll(self, i):
    #     if i / NUM_OF_ITERATIONS >= 0.25 and self.progress == 0:
    #         logging.debug("25% of simulation")
    #         self.progress += 1
    #     elif i / NUM_OF_ITERATIONS >= 0.50 and self.progress == 1:
    #         logging.debug("50% of simulation")
    #         self.progress += 1
    #     elif i / NUM_OF_ITERATIONS >= 0.75 and self.progress == 2:
    #         logging.debug("75% of simulation")
    #         self.progress += 1

    def endSimulation(self):
        time_end = time.time()
        logging.debug("time of simulation: " + str(time_end - self.time_begin))

        for t in self.threads:
            t.stop()
        self.cb.wakeUpAll()
        for t in self.threads:
            t.join()
        logging.debug("the end of simulation")

    def transations(self):
        for name, market in self.orderBook.items():
            bids = market.getBID()
            asks = market.getASK()

            sumQuantity = 0
            sumPrice = 0
            while True:
                    if (not bids) or (not asks):
                        #print("not enough offers - " + str(name) )
                        break
                    elif bids[0].getPrice() < asks[0].getPrice():
                        #print("the spread of " + str(name) + " is " + str(market.getASK()[0].getPrice() - market.getBID()[0].getPrice()))
                        break
                    else:
                        if bids[0].getQuantity() < asks[0].getQuantity():
                            print("firma " + str(bids[0].getOrderID()) + " kupuje " + str(bids[0].getQuantity()) + " od firmy " + str(asks[0].getOrderID()))
                            market.removeBID(market.getBID()[0])
                            market.changeQuantityASK(asks[0].getQuantity() - bids[0].getQuantity())

                        elif bids[0].getQuantity() > asks[0].getQuantity():  # aks<bid
                            print("firma " + str(bids[0].getOrderID()) + " kupuje " + str(asks[0].getQuantity()) + " od firmy " + str(asks[0].getOrderID()))
                            market.removeASK(asks[0])
                            market.changeQuantityBID(bids[0].getQuantity() - asks[0].getQuantity())
                        else:
                            self.cb.addMessage(bids[0].getOrderID(), "BUY:" + name + ":" + str(bids[0].getQuantity()))
                            self.cb.addMessage(asks[0].getOrderID(), "SELL:" + str(asks[0].price))
                            sumPrice += asks[0].price
                            sumQuantity += bids[0].getQuantity()
                            #print("firma " + str(bids[0].getOrderID()) + " kupuje " + str(bids[0].getQuantity()) + " od firmy " + str(asks[0].getOrderID()))
                            market.removeBID(market.getBID()[0])
                            market.removeASK(market.getASK()[0])
            if sumQuantity:
                self.cb.addAveragePrice(str(name), round(sumPrice/sumQuantity, 2))
            else:
                self.cb.addAveragePrice(str(name), numpy.nan)

    """test"""
    def drawMarket(self):
        for name, market in self.orderBook.items():
            market.drawOrderBook()


if __name__ == "__main__":
    kernel = Kernel()
