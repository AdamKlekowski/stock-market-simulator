import Trader
from Order import Order


class PrzemekTrader(Trader):
    def playOnStockMarket(self):  # TODO to develop !
        order = Order(0, self.__traderID__, "IBM", 100, 1000)
        pass

    def run(self):
        print(str(self.__traderID__) + " working and has " + str(self.__money__))  # TODO to delete
        for _ in range(1000):
            self.playOnStockMarket()