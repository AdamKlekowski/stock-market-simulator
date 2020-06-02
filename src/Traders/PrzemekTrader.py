from Traders.Trader import Trader
from Books.Order import Order
import tensorflow as tf
import numpy as np


class PrzemekTrader(Trader):
    def __init__(self, threadID, cb, orderBook, delay, money, portfolio):
        Trader.__init__(self, threadID, cb, orderBook, delay, money, portfolio)
        self.model = tf.keras.models.load_model('data/' + str(threadID)+'.h5')
        self.wariat = np.max([0.9, np.abs(np.random.normal(0, 0.1))])

    def playOnStock(self):
        self.cb.lock.acquire()
        try:
            self.prIBM = self.cb.stock_exchange_listing['IBM'][-1]
            self.x=[]
            for i in range(3,0,-1):
                self.x.append(self.cb.stock_exchange_listing['IBM'][-i])
                self.x.append(self.cb.oil_prices[self.cb.time-i])
            self.x=np.array(self.x)/500
            self.x=self.x.reshape((1,1,-1))
            self.valIBM=500*self.model.predict(self.x)[0,0]
            if self.valIBM>self.prIBM:
                toBuy=int(self.valIBM-self.prIBM)
                self.price=self.prIBM+(np.random.normal(-0.2, 0.2))
                #self.amount=int(np.min([self.money/self.price*self.wariat,toBuy]))
                self.amount=int(np.min([self.money/self.price,toBuy]))
                if self.amount>0 and self.price>0:
                    #print("Buy "+str(self.price)+' '+str(self.amount))
                    order = Order(self.threadID, self.threadID, self.amount, self.price, self.cb.time)
                    self.orderBook["IBM"].addOrder("BID", order)
                    self.money-=self.amount*self.price
            elif self.portfolio['IBM']>0:
                self.amount= int(np.min([self.portfolio['IBM']*self.wariat,self.wariat*(-self.valIBM+self.prIBM)]))
                self.price=self.prIBM+(np.random.normal(0.2, 0.2))
                if self.amount>0 and self.price>0:
                    #print("Sell "+str(self.price)+' '+str(self.amount))
                    order = Order(self.threadID, self.threadID, self.amount, self.price, self.cb.time)
                    self.orderBook["IBM"].addOrder("ASK", order)
        finally:
            self.cb.lock.release()
