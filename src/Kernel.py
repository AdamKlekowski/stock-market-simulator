import random
import time
import Traders.NoisyTrader as NoisyTrader
import Traders.PrzemekTrader as PrzemekTrader
from Books.MarketOrderBook import MarketOrderBook

NUM_NOISY_TRADER = 1000
NUM_PRZEMEK_TRADER = 0
NUM_OF_AGENTS = NUM_NOISY_TRADER + NUM_PRZEMEK_TRADER
NUM_OF_ITERATIONS = 250


class Kernel:
    def __init__(self, cb):
        self.cb = cb
        self.threads = []

        self.orderBook = {
            "IBM": MarketOrderBook(),
            "ABB": MarketOrderBook()
        }
        for i, j in zip([122.78, 122.78, 122.77, 122.65, 122.77], [117.76, 117.78, 117.81, 117.79, 117.81]):
            self.cb.addAveragePrice('IBM', i)
            self.cb.addAveragePrice('ABB', j)

        for i in range(0, NUM_PRZEMEK_TRADER):
            portfolio = {random.choice(["IBM", "ABB"]): random.choice([20, 30])}
            self.threads.append(PrzemekTrader.PrzemekTrader(i, self.cb, self.orderBook, random.choice([2, 3, 5]), random.choice([10000, 20000]), portfolio))

        for i in range(NUM_PRZEMEK_TRADER, NUM_NOISY_TRADER + NUM_PRZEMEK_TRADER):
            portfolio = {random.choice(["IBM", "ABB"]): random.choice([10, 20, 40])}
            self.threads.append(NoisyTrader.NoisyTrader(i, self.cb, self.orderBook, random.choice([1, 2]), random.choice([1000, 2000, 5000]), portfolio))

        for t in self.threads:
            t.start()

        progress = list("[__________]")

        for i in range(0, NUM_OF_ITERATIONS):
            self.cb.clear_counter()
            self.cb.wakeUpAll()
            is_wait = True
            while is_wait:
                if self.cb.attendance_counter == NUM_OF_AGENTS:
                    self.transations()
                    is_wait = False
                time.sleep(0.001)
            self.clearOrders()
            progress[int(i / NUM_OF_ITERATIONS * 10) + 1] = '*'
            print('\r' + "".join(progress), end='')
        print("")
        self.endSimulation()

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
                if (not bids) or (not asks):  # nie ma wystarczacej ilosci bidow albo askow
                    break
                elif bids[0].getPrice() < asks[0].getPrice():  # cena kupujacych jest mniejsza od ceny sprzedajacych
                    break
                else:
                    if bids[0].getQuantity() < asks[0].getQuantity():  # sprzedajacy ma więcej akcji od kupujacego
                        self.cb.addMessage(bids[0].getOrderID(), "BUY:" + name + ":" + str(bids[0].getQuantity()))
                        self.cb.addMessage(asks[0].getOrderID(),
                                           "SELL:" + str(int(asks[0].getPrice() * bids[0].getQuantity())))
                        sumQuantity += bids[0].getQuantity()
                        sumPrice += asks[0].price * bids[0].getQuantity()
                        market.changeQuantityASK(asks[0].getQuantity() - bids[0].getQuantity())
                        market.removeBID(market.getBID()[0])

                    elif bids[0].getQuantity() > asks[0].getQuantity():  # kupujacy ma wiecej akcji od sprzedajacego
                        self.cb.addMessage(bids[0].getOrderID(), "BUY:" + name + ":" + str(asks[0].getQuantity()))
                        self.cb.addMessage(asks[0].getOrderID(),
                                           "SELL:" + str(int(asks[0].getPrice()) * asks[0].getQuantity()))
                        sumQuantity += asks[0].getQuantity()
                        sumPrice += asks[0].price * asks[0].getQuantity()
                        market.changeQuantityBID(bids[0].getQuantity() - asks[0].getQuantity())
                        market.removeASK(asks[0])
                    else:  # oboje kupujacy i sprzedajacy maja tyle samo akcji
                        self.cb.addMessage(bids[0].getOrderID(), "BUY:" + name + ":" + str(bids[0].getQuantity()))
                        self.cb.addMessage(asks[0].getOrderID(),
                                           "SELL:" + str(int(asks[0].getPrice()) * bids[0].getQuantity()))
                        sumQuantity += bids[0].getQuantity()
                        sumPrice += asks[0].price * bids[0].getQuantity()
                        market.removeBID(market.getBID()[0])
                        market.removeASK(market.getASK()[0])
            if sumQuantity:
                self.cb.addAveragePrice(str(name), round(sumPrice / sumQuantity, 2))
            else:
                pass
                # self.cb.addAveragePrice(str(name), numpy.nan)

    def clearOrders(self):
        for name, market in self.orderBook.items():
            bids = market.getBID()
            asks = market.getASK()

            for order in bids:
                if abs(order.timestamp-self.cb.time) > 5:
                    self.cb.addMessage(order.traderID, "SELL:" + str(order.price*order.quantity))
                    bids.remove(order)

            for order in asks:
                if abs(order.timestamp-self.cb.time) > 5:
                    self.cb.addMessage(order.traderID, "BUY:" + str(name) + ":" + str(order.quantity))
                    asks.remove(order)

    def drawMarket(self):
        for name, market in self.orderBook.items():
            market.drawOrderBook()
