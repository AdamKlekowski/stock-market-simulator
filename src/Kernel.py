from typing import List, Any

from OrderBook import *


class Kernel:
    __order_book__ = OrderBook()

    def getOrderBook(self):
        return self.__order_book__

    def auction(self, stock):
        stockBid: List[Any] = []
        stockAsk: List[Any] = []
        for bid in self.__order_book__.getBID():
            print(bid)
            if bid.getStock() == stock:                                                     # wybiera tylko wybrana forme
                if not stockBid:                                                            # spr czy lista jest pusta
                    stockBid.append(bid)                                                    # dodaje
                else:                                                                       # przeszukuje liste by zajac odpowiedni priorytet
                    place = 0
                    for bidFromStockBid in stockBid:
                        if bidFromStockBid.getPriceRange() < bid.getPriceRange():           # bid jest najlepsze jak jest najwieksze
                            break
                        place += 1
                    stockBid.insert(place, bid)

        for ask in self.__order_book__.getASK():                                            # robi to samo tylko dla ask
            print(ask)
            if ask.getStock() == stock:
                if not stockAsk:
                    stockAsk.append(ask)
                else:
                    place = 0
                    for askFromStockAsk in stockAsk:
                        if askFromStockAsk.getPriceRange() > ask.getPriceRange():           #ask jest najlepsze jak jest najmniejsze
                            break
                        place += 1
                    stockAsk.insert(place, ask)
        while True:                                                                         #porownywanie najwyzej priorytetowanych

            if (not stockBid) and (not stockAsk):                                           #spr czy zostaly jeszcze jakies bid albo ask
                print("not enough offers")
                break
            elif stockBid[0].getPriceRange() < stockAsk[0].getPriceRange():                   #zaden bid nie odpowiada najnizszemu askowi
                print("the spread of " + stock + " is " + str(stockAsk[0].getPriceRange()-stockBid[0].getPriceRange()))
                break

            else:
                if stockBid[0].getQuantity() < stockAsk[0].getQuantity():                    #bid<ask
                    print("firma " + stockBid[0].getOrderID() + " kupuje " + str(stockBid[0].getQuantity())
                          + " od firmy " + stockAsk[0].getOrderID())
                    self.__order_book__.removeBID(stockBid[0])                               #bid usuwany, ask aktualizowany
                    self.__order_book__.changeQuantityASK(stockBid[0], stockAsk[0].getQuantity() - stockBid[0].getQuantity())
                    stockBid.pop(0)

                elif stockBid[0].getQuantity() > stockAsk[0].getQuantity():                  #aks<bid
                    print("firma " + stockBid[0].getOrderID() + " kupuje " + str(stockAsk[0].getQuantity())
                          + " od firmy " + stockAsk[0].getOrderID())
                    self.__order_book__.removeASK(stockAsk[0])                               #bid aktualizwoany, ask usuwany
                    self.__order_book__.changeQuantityBID(stockBid[0] ,stockBid[0].getQuantity() - stockAsk[0].getQuantity())
                    stockAsk.pop(0)

                else:                                                                        #bid=ask
                    print("firma " + stockBid[0].getOrderID() + " kupuje " + str(stockBid[0].getQuantity())
                          + " od firmy " + stockAsk[0].getOrderID())
                    self.__order_book__.removeBID(stockBid[0])                               #bid usuwany, aks usuwany
                    self.__order_book__.removeASK(stockAsk[0])
                    stockBid.pop(0)
                    stockAsk.pop(0)


