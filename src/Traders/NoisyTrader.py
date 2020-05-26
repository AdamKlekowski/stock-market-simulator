from Traders.Trader import Trader
from Books.Order import Order
import random


class NoisyTrader(Trader):
    def playOnStock(self):

        stock_name = "IBM"#random.choice(["ABB", "IBM"])
        quantity = random.choice([1])
        if stock_name in self.portfolio and self.portfolio[stock_name] > quantity:
            last_price = self.cb.stock_exchange_listing[stock_name][-1]

            oil_diff = self.cb.oil_prices[self.cb.time + 1] - self.cb.oil_prices[self.cb.time]
            if oil_diff > 5:
                price = last_price * random.choice([1.20, 1.15, 1.1])
            elif 0 < oil_diff < 5:
                price = last_price * random.choice([1.12, 1.1, 1.05, 1, 0.999])
            elif 0 > oil_diff > -5:
                price = last_price * random.choice([1.03, 1, 0.99])
            else:
                price = last_price * random.choice([0.99, 0.97, 0.9, 0.85])

            min_price, max_price = self.cb.min_max[stock_name]
            if price > max_price:
                price = max_price
            elif price < min_price:
                price = min_price

            self.cb.lock.acquire()
            try:
                order = Order(self.threadID, self.threadID, quantity, price, self.cb.time)
                self.orderBook[stock_name].addOrder("ASK", order)
            finally:
                self.cb.lock.release()

        stock_name = "IBM"#random.choice(["ABB", "IBM"])
        last_price = self.cb.stock_exchange_listing[stock_name][-1]

        oil_diff = self.cb.oil_prices[self.cb.time + 1] - self.cb.oil_prices[self.cb.time]
        if oil_diff > 5:
            price = last_price * random.choice([1.20, 1.15, 1.1])
        elif 0 < oil_diff < 5:
            price = last_price * random.choice([1.12, 1.1, 1.05, 1, 0.999])
        elif 0 > oil_diff > -5:
            price = last_price * random.choice([1.03, 1, 0.99])
        else:
            price = last_price * random.choice([0.99, 0.97, 0.9, 0.85])

        min_price, max_price = self.cb.min_max[stock_name]
        if price > max_price:
            price = max_price
        elif price < min_price:
            price = min_price

        quantity = random.choice([1])
        if quantity * price < self.money:
            self.cb.lock.acquire()
            try:
                order = Order(self.threadID, self.threadID, quantity, price, self.cb.time)
                self.orderBook[stock_name].addOrder("BID", order)
                self.money -= price * quantity
            finally:
                self.cb.lock.release()
