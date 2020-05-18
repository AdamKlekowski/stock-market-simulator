import matplotlib.pyplot as plt


class Plot:
    @staticmethod
    def displayPlot(cb):
        for name in ["IBM", "ABB"]:
            Plot.oneStockOnePlot(cb, name)
        Plot.allStockOnePlot(cb)

    @staticmethod
    def allStockOnePlot(cb):
        plt.clf()
        for name in ["IBM", "ABB"]:
            plt.plot(cb.getPriceListing(name))
        plt.title("Stock prices")
        plt.legend(["IBM", "ABB"])
        plt.ylabel("Price [$]")
        plt.xlabel("Time [s]")
        plt.savefig("Plot/all_stock.png")

    @staticmethod
    def oneStockOnePlot(cb, stock_name):
        plt.clf()
        plt.plot(cb.getPriceListing(stock_name))
        plt.title("Stock prices for " + str(stock_name))
        plt.legend([stock_name])
        plt.ylabel("Price [$]")
        plt.xlabel("Time [s]")
        plt.savefig("Plot/" + str(stock_name) + ".png")

