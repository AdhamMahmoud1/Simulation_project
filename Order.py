import random
import CarDealer


class Order:
    def __init__(self, quantity, leadTime):
        self.__quantity = quantity
        self.__leadTime = leadTime
        self.__ORDER_COST  = 20000

    def generateLeadTime(self):
        randomProp = random.uniform(0, 1)
        if randomProp >= 0 and randomProp < 0.4:
            return 1
        elif randomProp >= 0.4 and randomProp < 0.75:
            return 2
        else:
            return 3


    def getQuantity(self):
        return self.__quantity

    def getLeadTime(self):
        return self.__leadTime

    def setQuantity(self, quantity):
        self.__quantity = quantity

    def getOrderCost(self):
        return self.__ORDER_COST

    def setNewLeadTime(self):
        self.__leadTime = self.generateLeadTime()

    def setLeadTime(self, time):
        self.__leadTime = time
