import logging
import threading
import time
import Trader
import PrzemekTrader


NUM_OF_AGENTS = 3
NUM_OF_ITERATIONS = 1


class Kernel:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s (%(threadName)-2s) %(message)s',
                            datefmt="%H:%M:%S")

        logging.debug("the begin of simulation")
        logging.debug("numbers of traders: " + str(NUM_OF_AGENTS))
        logging.debug("numbers of iterations: " + str(NUM_OF_ITERATIONS))
        self.progress = 0
        time.sleep(0.5)

        self.time_begin = time.time()
        self.condition = threading.Condition()
        self.threads = []
        for i in range(0, NUM_OF_AGENTS):
            self.threads.append(PrzemekTrader.PrzemekTrader(i, self.condition))

        for t in self.threads:
            t.start()

        for i in range(0, NUM_OF_ITERATIONS):
            self.wakeUpAll(i)
            time.sleep(0.005)
        self.endSimulation()

    def wakeUpAll(self, i):
        with self.condition:
            #logging.debug('New turn: ' + str(i))
            self.condition.notifyAll()

            if i/NUM_OF_ITERATIONS >= 0.25 and self.progress == 0:
                logging.debug("25% of simulation")
                self.progress += 1
            elif i/NUM_OF_ITERATIONS >= 0.50 and self.progress == 1:
                logging.debug("50% of simulation")
                self.progress += 1
            elif i / NUM_OF_ITERATIONS >= 0.75 and self.progress == 2:
                logging.debug("75% of simulation")
                self.progress += 1

    def endSimulation(self):
        time_end = time.time()
        logging.debug("time of simulation: " + str(time_end - self.time_begin))

        for t in self.threads:
            t.stop()
        self.wakeUpAll(9999)
        for t in self.threads:
            t.join()
        logging.debug("the end of simulation")


if __name__ == "__main__":
    kernel = Kernel()