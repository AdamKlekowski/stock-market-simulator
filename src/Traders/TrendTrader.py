from Traders.Trader import Trader
from Books.Order import Order
import numpy as np
import random


class TrendTrader(Trader):
    def playOnStock(self):
            data = self.cb.stock_exchange_listing("IBM")[-5:]
            x = np.arange(0, len(data))
            y = np.array(data)
            z = np.polyfit(x, y, 1)
            a = "{0}".format(*z)
            b = "{1}".format(*z)
            predicted_price_val = a*8 + b

            stock_name = random.choice("IBM")
            quantity = random.choice([1])

            last_price = self.cb.stock_exchange_listing[stock_name][-1]

            if predicted_price_val > last_price:
                price = last_price + abs(last_price - predicted_price_val)*0.1

                min_price, max_price = self.cb.min_max[stock_name]
                if price > max_price:
                    price = max_price
                elif price < min_price:
                    price = min_price

                if quantity * price < self.money:
                    order = Order(self.threadID, self.threadID, quantity, price, self.cb.time)
                    self.cb.lock.acquire()
                    try:
                        self.orderBook[stock_name].addOrder("BID", order)
                        self.money -= price * quantity
                    finally:
                        self.cb.lock.release()
            else:
                if stock_name in self.portfolio and self.portfolio[stock_name] > quantity:
                    price = last_price - abs(last_price - predicted_price_val) * 0.1

                    min_price, max_price = self.cb.min_max[stock_name]
                    if price > max_price:
                        price = max_price
                    elif price < min_price:
                        price = min_price

                    order = Order(self.threadID, self.threadID, quantity, price, self.cb.time)

                    try:
                        self.orderBook[stock_name].addOrder("ASK", order)
                        self.portfolio[stock_name] -= quantity
                    finally:
                        self.cb.lock.release()
