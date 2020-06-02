import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
class ModelChecker():
    @staticmethod
    def check_model(index,cb,iterations,comm,fn,resFile,strind):
        y=np.array(cb.stock_exchange_listing["IBM"][5:])
        x=np.array(cb.aapl_prices[5:45])
        x=x.reshape(-1)
        corrPredToReal=np.corrcoef(x,y)
        o=np.array(cb.oil_prices[5:45])
        o=o.reshape(-1)
        corrOilToAppl=np.corrcoef(x,o)
        resFile.write(str(np.abs(corrPredToReal[0,1]))+', '+str(np.abs(corrOilToAppl[0,1]))+', '+str(comm)+', '+str(1200-comm)+', '+str(strind)+"\n")
        """print()
        plt.clf()
        plt.plot(x)
        plt.plot(y)
        plt.legend(('Real price', 'Predicted price'),loc='upper left')
        plt.title(comm.replace('NUM_NOISY_TRADER:','Noisy Trader: ').replace('NUM_PRZEMEK_TRADER:',", Przemek Trader: ").replace(
            'NUM_TREND_TRADER:','\nTrend Trader: ').replace('NUM_OF_ITERATIONS:',', Iterations: ')+', corr: '+str(c[1,0]))
        plt.savefig(fn.replace('.csv','.png'))
        plt.show()"""
