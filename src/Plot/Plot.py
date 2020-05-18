import matplotlib.pyplot as plt


class Plot:
    @staticmethod
    def displayPlot(cb):
        for name in ["IBM", "ABB"]:
            plt.plot(cb.getPriceListing(name))
        plt.title("Stock prices")
        plt.legend(["IBM", "ABB"])
        plt.ylabel("Price [$]")
        plt.xlabel("Time [s]")
        plt.savefig("Plot/all_stock.png")
