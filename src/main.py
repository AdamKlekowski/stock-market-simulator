import time
from CommunicationBox import CommunicationBox
from Kernel import Kernel
from Plot.Plot import Plot
from ModelChecker import ModelChecker


if __name__ == "__main__":
    i=0
    f=open('./results/main.csv','w+')
    for startIndex in [100,200]:#range(0,2500,100):
        for num in [98,99]:#range(0,800,50):
            time_begin = time.time()
            cb = CommunicationBox(startIndex)
            kernel = Kernel(cb,startIndex,num)
            time_end = time.time()
            #Plot.displayPlot(cb)
            filename='./results/'+str(i)+'.csv'
            cb.saveToFile(kernel,filename)
            print(time_end - time_begin)
            ModelChecker.check_model(startIndex,cb,40,num,filename,f,startIndex)
            del(kernel,cb)
            i+=1
    f.close()
