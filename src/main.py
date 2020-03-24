from Kernel import *
from Trader import *
import random

available_stock = [("IBM", 100), ("ABB", 100), ("Comarch", 100)]


def main():
    kernel = Kernel()
    for i in range(10):
        Trader(i, available_stock, round(random.uniform(1000, 10000), 2), kernel.getOrderBook()).start()

    for _ in range(1):
        for element in kernel.getOrderBook().getASK():
            print(element)
        for element in kernel.getOrderBook().getBID():
            print(element)


if __name__ == "__main__":
    main()
