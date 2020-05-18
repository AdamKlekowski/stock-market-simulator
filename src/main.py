from CommunicationBox import CommunicationBox
from Kernel import Kernel
from Plot.Plot import Plot

if __name__ == "__main__":
    cb = CommunicationBox()
    kernel = Kernel(cb)
    Plot.displayPlot(cb)
