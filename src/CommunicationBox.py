import threading
import pandas as pd


class CommunicationBox:
    def __init__(self):
        self.time = 0
        self.condition = threading.Condition()
        self.lock = threading.Lock()
        self.attendance_counter = 0
        self.messages = {}
        self.stock_exchange_listing = {}    # notowania giełdowe
        self.min_max = {
            'IBM': (105, 135),
            'ABB': (10, 25)
        }
        self.oil_prices = pd.read_csv("data/oil_prices.csv")["price"]

    def mark_attendance_counter(self):
        self.attendance_counter += 1

    def clear_counter(self):
        self.attendance_counter = 0
        self.time += 1

    def wakeUpAll(self):
        with self.condition:
            self.condition.notifyAll()

    def addMessage(self, receiver_id, msg):
        if receiver_id in self.messages:
            self.messages[receiver_id].append(msg)
        else:
            self.messages[receiver_id] = []
            self.messages[receiver_id].append(msg)

    def getMessage(self, trader_id):
        if trader_id in self.messages:
            return self.messages.pop(trader_id)
        else:
            return None

    def addAveragePrice(self, name, price):
        if name in self.stock_exchange_listing:
            self.stock_exchange_listing[name].append(price)
        else:
            self.stock_exchange_listing[name] = []
            self.stock_exchange_listing[name].append(price)

    def getPriceListing(self, name):
        if name in self.stock_exchange_listing:
            return self.stock_exchange_listing[name]
        else:
            return None
