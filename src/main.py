import time
from CommunicationBox import CommunicationBox
from Kernel import Kernel
from Plot.Plot import Plot
import numpy as np


if __name__ == "__main__":
    time_begin = time.time()
    cb = CommunicationBox()
    kernel = Kernel(cb)
    time_end = time.time()
    Plot.displayPlot(cb)
    cb.saveToFile()
    print(time_end - time_begin)
