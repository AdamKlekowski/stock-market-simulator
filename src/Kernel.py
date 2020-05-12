import random
import time
import numpy
import NoisyTrader
import PrzemekTrader
from MarketOrderBook import MarketOrderBook


NUM_NOISY_TRADER = 1400
NUM_PRZEMEK_TRADER = 1
NUM_OF_AGENTS = NUM_NOISY_TRADER + NUM_PRZEMEK_TRADER
NUM_OF_ITERATIONS = 10

class Kernel:
    def __init__(self, cb):
        self.cb = cb
        self.threads = []

        self.orderBook = {
            "IBM": MarketOrderBook(),
            "ABB": MarketOrderBook()
        }
        for i,j in zip([122.78,122.78,122.77,122.65,122.77],[117.76,117.78,117.81,117.79,117.81]):
            self.cb.addAveragePrice('IBM', i)
            self.cb.addAveragePrice('ABB', j)
        for i in range(0, NUM_PRZEMEK_TRADER):
            self.threads.append(PrzemekTrader.PrzemekTrader(i, self.cb, self.orderBook, random.choice([1, 2, 3]), random.choice([10000, 20000])))

        for i in range(NUM_PRZEMEK_TRADER, NUM_NOISY_TRADER+NUM_PRZEMEK_TRADER):
            self.threads.append(NoisyTrader.NoisyTrader(i, self.cb, self.orderBook, random.choice([1, 1]), random.choice([1000, 2000])))

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

        #for t in self.threads:
        #    print(t)

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
                    if (not bids) or (not asks):                                                                        #nie ma wystarczacej ilosci bidow albo askow
                        break
                    elif bids[0].getPrice() < asks[0].getPrice():                                                       #cena kupujacych jest mniejsza od ceny sprzedajacych
                        break
                    else:
                        if bids[0].getQuantity() < asks[0].getQuantity():                                               #sprzedajacy ma więcej akcji od kupujacego
                            self.cb.addMessage(bids[0].getOrderID(), "BUY:" + name + ":" + str(bids[0].getQuantity()))
                            self.cb.addMessage(asks[0].getOrderID(), "SELL:" + str(int(asks[0].getPrice() * bids[0].getQuantity())))
                            sumQuantity += bids[0].getQuantity()
                            sumPrice += asks[0].price * bids[0].getQuantity()
                            market.changeQuantityASK(asks[0].getQuantity() - bids[0].getQuantity())
                            market.removeBID(market.getBID()[0])

                        elif bids[0].getQuantity() > asks[0].getQuantity():                                             #kupujacy ma wiecej akcji od sprzedajacego
                            self.cb.addMessage(bids[0].getOrderID(), "BUY:" + name + ":" + str(asks[0].getQuantity()))
                            self.cb.addMessage(asks[0].getOrderID(), "SELL:" + str(int(asks[0].getPrice()) * asks[0].getQuantity()))
                            sumQuantity += asks[0].getQuantity()
                            sumPrice += asks[0].price * asks[0].getQuantity()
                            market.changeQuantityBID(bids[0].getQuantity() - asks[0].getQuantity())
                            market.removeASK(asks[0])
                        else:                                                                                           #oboje kupujacy i sprzedajacy maja tyle samo akcji
                            self.cb.addMessage(bids[0].getOrderID(), "BUY:" + name + ":" + str(bids[0].getQuantity()))
                            self.cb.addMessage(asks[0].getOrderID(), "SELL:" + str(int(asks[0].getPrice()) * bids[0].getQuantity()))
                            sumQuantity += bids[0].getQuantity()
                            sumPrice += asks[0].price * bids[0].getQuantity()
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
