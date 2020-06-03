import time
from CommunicationBox import CommunicationBox
from Kernel import Kernel
from Plot.Plot import Plot
from ModelChecker import ModelChecker


if __name__ == "__main__":
    f=open('args','r')
    a=f.read()
    f.close()
    i,startIndex,num=[int(i) for i in a.split(',')]
    f=open('./results/main.csv','a+')
    time_begin = time.time()
    cb = CommunicationBox(startIndex)
    kernel = Kernel(cb,startIndex,num)
    time_end = time.time()
    #Plot.displayPlot(cb)
    filename='./results/'+str(i)+'.csv'
    cb.saveToFile(kernel,filename)
    print(time_end - time_begin)
    ModelChecker.check_model(startIndex,cb,40,num,filename,f,startIndex)
    f.flush()
    del(kernel,cb)
    i+=1
    f.close()


