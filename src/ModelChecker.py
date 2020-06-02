import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class ModelChecker:
    @staticmethod
    def check_model(index, cb, iterations, comm, fn):
        y = np.array(cb.stock_exchange_listing["IBM"][5:])
        x = pd.read_csv('data/AAPL.csv')['Close'][index+5:index+iterations+5].to_numpy()
        x = x.reshape(-1)
        c = np.corrcoef(x, y)
        print()
        plt.clf()
        plt.plot(x)
        plt.plot(y)
        plt.legend(('Real price', 'Predicted price'), loc='upper left')
        plt.title(comm.replace('NUM_NOISY_TRADER:', 'Noisy Trader: ').replace('NUM_PRZEMEK_TRADER:', ", Przemek Trader: ").replace(
            'NUM_TREND_TRADER:', '\nTrend Trader: ').replace('NUM_OF_ITERATIONS:', ', Iterations: ')+', corr: '+str(c[1, 0]))
        plt.savefig(fn.replace('.csv', '.png'))
        #plt.show()
