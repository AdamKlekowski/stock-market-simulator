import random
import time
import numpy
import NoisyTrader
import PrzemekTrader
from MarketOrderBook import MarketOrderBook


NUM_NOISY_TRADER = 100
NUM_PRZEMEK_TRADER = 100
NUM_OF_AGENTS = NUM_NOISY_TRADER + NUM_PRZEMEK_TRADER
NUM_OF_ITERATIONS = 50



class Kernel:
    def __init__(self, cb):
        self.cb = cb
        self.threads = []

        self.orderBook = {
            "IBM": MarketOrderBook(),
            "ABB": MarketOrderBook()
        }

        for i in range(0, NUM_PRZEMEK_TRADER):
            self.threads.append(PrzemekTrader.PrzemekTrader(i, self.cb, self.orderBook, random.choice([1, 2, 3]), random.choice([10000, 20000])))

        for i in range(NUM_PRZEMEK_TRADER, NUM_NOISY_TRADER+NUM_PRZEMEK_TRADER):
            self.threads.append(NoisyTrader.NoisyTrader(i, self.cb, self.orderBook, random.choice([4, 5]), random.choice([1000, 2000])))

        for t in self.threads:
            t.start()

        for i in range(0, NUM_OF_ITERATIONS):
            self.cb.clear_counter()
            self.cb.wakeUpAll()
            isWait = True
            while isWait:
                if self.cb.attendance_counter == NUM_OF_AGENTS:
                    self.transations()
                    isWait = False
                time.sleep(0.001)
        self.endSimulation()

        for t in self.threads:
            print(t)

    def endSimulation(self):
        for t in self.threads:
            t.stop()
        self.cb.wakeUpAll()
        for t in self.threads:
            t.join()

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
                            #print("firma " + str(bids[0].getOrderID()) + " kupuje " + str(bids[0].getQuantity()) + " od firmy " + str(asks[0].getOrderID()))
                            market.removeBID(market.getBID()[0])
                            market.changeQuantityASK(asks[0].getQuantity() - bids[0].getQuantity())

                        elif bids[0].getQuantity() > asks[0].getQuantity():  # aks<bid
                            #print("firma " + str(bids[0].getOrderID()) + " kupuje " + str(asks[0].getQuantity()) + " od firmy " + str(asks[0].getOrderID()))
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
