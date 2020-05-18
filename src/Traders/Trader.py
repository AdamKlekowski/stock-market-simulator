import threading


class Trader(threading.Thread):
    def __init__(self, threadID, cb, orderBook, delay, money, portfolio):
        threading.Thread.__init__(self)
        self.cb = cb
        self.threadID = threadID
        self.time_delay = delay
        self.isStop = False
        self.money = money
        self.portfolio = portfolio
        self.orderBook = orderBook

    def stop(self):
        self.isStop = True

    def run(self):
        while True:
            with self.cb.condition:
                self.cb.condition.wait()
                self.parseMsg()
                if self.isStop:
                    break
                if self.cb.time % self.time_delay == 0:
                    self.playOnStock()
                self.cb.mark_attendance_counter()

    def playOnStock(self):
        raise NotImplementedError()

    def addStock(self, name, quantity):
        if name in self.portfolio:
            self.portfolio[name] += quantity
        else:
            self.portfolio[name] = quantity

    def parseMsg(self):
        messages = self.cb.getMessage(self.threadID)
        if messages:
            for m in messages:
                content = m.split(":")

                if content[0] == "BUY":
                    self.addStock(str(content[1]), float(content[2]))
                elif content[0] == "SELL":
                    self.money += float(content[1])

    def __str__(self):
        return str(self.threadID) + " : " + str(self.money) + " : " + str(self.portfolio)
