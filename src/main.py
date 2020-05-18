from CommunicationBox import CommunicationBox
from Kernel import Kernel
from Plot import Plot

if __name__ == "__main__":
    cb = CommunicationBox()
    kernel = Kernel(cb)
    Plot.displayPlot(cb)
    print(cb.stock_exchange_listing)
