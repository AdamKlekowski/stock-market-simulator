import Trader
from Order import Order


class RandomTrader(Trader):
    def playOnStockMarket(self):  # TODO to develop !
        order = Order(0, self.__traderID__, "IBM", 100, 1000)
        if self.__money__ > 1000:
            self.__public_order_book__.addOrder("ASK", order)
        else:
            self.__public_order_book__.addOrder("BID", order)

    def run(self):
        print(str(self.__traderID__) + " working and has " + str(self.__money__))  # TODO to delete
        for _ in range(1000):
            self.playOnStockMarket()