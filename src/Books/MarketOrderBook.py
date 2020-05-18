from Books.OrderBook import OrderBook


class MarketOrderBook(OrderBook):

    def addOrder(self, _type, _order):
        if type(_type) != str:
            raise TypeError("Type is a string, different type given")

        if _type == "BID":
            index = 0
            for i in range(len(self.BID)):
                try:
                    if _order.price > self.BID[i].price:
                        break
                except:
                    pass
                index += 1
            self.BID.insert(index, _order)
            # TODO bisect.insort(self.BID, index)

        elif _type == "ASK":
            index = 0
            for i in range(len(self.ASK)):
                try:
                    if _order.price < self.ASK[i].price:
                        break
                except:
                    pass
                index += 1
            self.ASK.insert(index, _order)
            # TODO bisect.insort(self.ASK, index)

        else:
            raise ValueError("Type should be equal BID or ASK, different type given")
