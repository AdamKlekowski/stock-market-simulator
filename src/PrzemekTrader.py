from Trader import Trader


class PrzemekTrader(Trader):
    def playOnStock(self):
        self.lock.acquire()
        try:
            pass
        finally:
            self.lock.release()
