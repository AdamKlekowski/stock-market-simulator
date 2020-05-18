from Traders.Trader import Trader
from Books.Order import Order
import random


class NoisyTrader(Trader):
    def playOnStock(self):
        self.cb.lock.acquire()
        try:
            if random.choice(["ASK", "BID"]) == "ASK":
                stock_name = random.choice(["ABB", "IBM"])
                quantity = random.choice([1])
                if stock_name in self.portfolio and self.portfolio[stock_name] > quantity:
                    last_price = self.cb.stock_exchange_listing[stock_name][-1]

                    oil_diff = self.cb.oil_prices[self.cb.time+1] - self.cb.oil_prices[self.cb.time]
                    if oil_diff > 0:
                        price = random.choice([last_price * 1.10, last_price * 1.0])
                    else:
                        price = random.choice([last_price * 1.05, last_price * 1.0, last_price * 0.95])

                    min_price, max_price = self.cb.min_max[stock_name]
                    if price > max_price:
                        price = max_price
                    elif price < min_price:
                        price = min_price

                    order = Order(self.threadID, self.threadID, quantity, price, self.cb.time)
                    self.orderBook[stock_name].addOrder("ASK", order)
            else:
                stock_name = random.choice(["ABB", "IBM"])
                last_price = self.cb.stock_exchange_listing[stock_name][-1]

                oil_diff = self.cb.oil_prices[self.cb.time + 1] - self.cb.oil_prices[self.cb.time]
                if oil_diff > 0:
                    price = random.choice([last_price * 1.20, last_price * 1.1])
                else:
                    price = random.choice([last_price * 1.05, last_price * 1.0, last_price * 0.95])

                min_price, max_price = self.cb.min_max[stock_name]
                if price > max_price:
                    price = max_price
                elif price < min_price:
                    price = min_price

                quantity = random.choice([1])
                if quantity*price < self.money:
                    order = Order(self.threadID, self.threadID, quantity, price, self.cb.time)
                    self.orderBook[stock_name].addOrder("BID", order)
                    self.money -= price*quantity
        finally:
            self.cb.lock.release()
