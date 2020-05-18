from Traders.Trader import Trader
from Books.Order import Order
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class PrzemekTrader(Trader):
    def __init__(self, threadID, cb, orderBook, delay, money):
        Trader.__init__(self, threadID, cb, orderBook, delay, money)

        self.model = tf.keras.models.load_model('data/mod.h5')
        self.aapl = np.genfromtxt('data/AAPL.csv', delimiter=',')
        self.aapl = self.aapl[1:, 1:]
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaler.fit(np.reshape(self.aapl[:, 3], (-1, 1)))

    def playOnStock(self):
        self.cb.lock.acquire()
        try:
            self.prIBM = self.cb.stock_exchange_listing['IBM'][-1]
            self.x = []
            for i in range(5, 0, -1):
                self.x.append(self.cb.stock_exchange_listing['IBM'][-i])
            self.x = [self.scaler.transform([[i]]) for i in self.x]
            self.x = np.array(self.x)
            self.x = self.x.reshape((1,1,-1))
            self.valIBM = self.scaler.inverse_transform(self.model.predict(self.x))[0,0]
            if self.valIBM > self.prIBM:
                order = Order(self.threadID, self.threadID, 4, self.prIBM+np.random.normal(0,0.1))
                self.orderBook["IBM"].addOrder("BID", order)
            else:
                order = Order(self.threadID, self.threadID, 4, self.prIBM+np.random.normal(0,0.1))
                self.orderBook["IBM"].addOrder("ASK", order)
        finally:
            self.cb.lock.release()
