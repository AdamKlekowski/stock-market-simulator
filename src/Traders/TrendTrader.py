from Traders.Trader import Trader
from Books.Order import Order
import numpy as np
import random


class TrendTrader(Trader):
    def playOnStock(self):
        self.cb.lock.acquire()
        try:
            predicted_prices = {}

            for stock_name in ["ABB", "IBM"]:
                data = self.cb.stock_exchange_listing(stock_name)[-3:]
                x = np.arange(0, len(data))
                y = np.array(data)
                z = np.polyfit(x, y, 1)
                a = "{0}".format(*z)
                b = "{1}".format(*z)
                predicted_prices[stock_name] = a, b

            stock_name = random.choice(["ABB", "IBM"])
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

                order = Order(self.threadID, self.threadID, quantity, price, self.cb.time)
                self.orderBook[stock_name].addOrder("ASK", order)

            stock_name = random.choice(["ABB", "IBM"])
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
                order = Order(self.threadID, self.threadID, quantity, price, self.cb.time)
                self.orderBook[stock_name].addOrder("BID", order)
                self.money -= price * quantity
        finally:
            self.cb.lock.release()
