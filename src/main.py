import time
from CommunicationBox import CommunicationBox
from Kernel import Kernel
from Plot.Plot import Plot
from ModelChecker import ModelChecker


if __name__ == "__main__":
    startIndex=1700;
    time_begin = time.time()
    cb = CommunicationBox(startIndex)
    kernel = Kernel(cb,startIndex)
    time_end = time.time()
    Plot.displayPlot(cb)
    filename='symulation_data'+str(int(time.time()))+'.csv'
    cb.saveToFile(kernel,filename)
    print(time_end - time_begin)
    ModelChecker.check_model(startIndex,cb,int(kernel.returnParams().split('NUM_OF_ITERATIONS:')[1]),kernel.returnParams(),filename)
