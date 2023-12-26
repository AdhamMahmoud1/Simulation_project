class Car:
    def __init__(self):
        self.__netProfit = 10000
        self.__holdinCost = 1000
        self.__shortageCost = 500

    def getNetProfit(self):
        return self.__netProfit

    def getHoldinCost(self):
        return self.__holdinCost

    def getShortageCost(self):
        return self.__shortageCost
