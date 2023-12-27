import CarDealer
import Order

import random

HOLDING_COST = 1000
NET_PROFIT_PER_CAR = 10000
REVIEW_PERIOD = 3
ORDER_COST = 20000

class Simulation:
    def __init__(self):
        self.__carDealer = CarDealer.CarDealer()
        self.__demand = 0
        self.__demandList = list()
        self.__soldCars = 0
        self.__shortageDays = 0
        self.__shortageDaysList = list()
        self.__leadTimes = list()
        self.__profitList = list()
        self.__inventory = list()
        self.__showRoom = list()
        
    def getCarDealer(self):
        return self.__carDealer
    
    def setDemand(self):
        randomProp = random.uniform(0, 1)
        if randomProp >= 0 and randomProp < 0.2:
            self.__demand = 0
        elif randomProp >= 0.2 and randomProp < 0.54:
            self.__demand =  1
        elif randomProp >= 0.54 and randomProp < 0.9:
            self._demand =  2
        else:
            self.__demand =  3

    def getDemand(self):
        return self.__demand
    
    def getDemandList(self):
        return self.__demandList
    
    def getShortageDaysList(self):
        return self.__shortageDaysList          
    
    def getProfitList(self):
        return self.__profitList
    
    def getInventoryCapacity(self):
        return self.__inventory
    
    def getShowRoomCapacity(self):
        return self.__showRoom
    
    def calculateAverage(self, list):
        return sum(list) / len(list)
    
    def run(self):
        for i in range(1000):
            self.__carDealer = CarDealer.CarDealer()
            orderList =  list()
            leadTimes = list()
            orderList.append(Order.Order(5, 2))
            self.__shortageDays = 0
            self.__soldCars = 0
            demandList = list()
            profitList = list()
            inventory = list()
            showRoom = list()
            holdingcost =  0
            # simulating for 10 days
            for day in range(1, 10):
                # check if there is any order to be delivered
                if len(orderList) > 0:
                    for order in orderList:
                        if order.getLeadTime() == 0:
                            # deliver the order
                            if order.getQuantity() + self.getCarDealer().getShowRoomCapacity() > 5 :
                                self.getCarDealer().setShowRoomCapacity(5)
                                order.setQuantity(order.getQuantity() - (5 - self.getCarDealer().getShowRoomCapacity()))
                                self.getCarDealer().setInventoryCapacity(self.getCarDealer().getInventoryCapacity() + order.getQuantity())
                            else:
                                self.getCarDealer().setShowRoomCapacity(order.getQuantity() + self.getCarDealer().getShowRoomCapacity())
                        else:
                            # reduce the lead time
                            order.setLeadTime(order.getLeadTime() - 1)
                    # remove the delivered orders from the list
                    for order in orderList:
                        if order.getLeadTime() == 0:
                            orderList.remove(order)

                self.setDemand()
                demandList.append(self.getDemand())

                if self.getDemand() <= self.getCarDealer().getInventoryCapacity():
                    self.getCarDealer().setInventoryCapacity(self.getCarDealer().getInventoryCapacity() - self.getDemand())
                    self.__soldCars += self.getDemand()
                elif self.getDemand() > self.getCarDealer().getInventoryCapacity():
                    self.__demand -= self.getCarDealer().getInventoryCapacity()
                    self.getCarDealer().setInventoryCapacity(0)
                    if self.getDemand() <= self.getCarDealer().getShowRoomCapacity():
                        self.getCarDealer().setShowRoomCapacity(self.getCarDealer().getShowRoomCapacity() - self.getDemand())
                        self.__soldCars += self.getDemand()
                elif (self.getCarDealer().getInventoryCapacity() + self.getCarDealer().getShowRoomCapacity() == 0):
                    self.__shortageDays += 1
                

                holdingcost += self.getCarDealer().getInventoryCapacity() * HOLDING_COST

                # check if the review period is over
                flag = 0
                if (day % REVIEW_PERIOD == 0):
                    order = Order.Order(0,0)
                    order.setQuantity(15 - self.getCarDealer().getInventoryCapacity() - self.getCarDealer().getShowRoomCapacity())
                    order.setNewLeadTime()
                    leadTimes.append(order.getLeadTime())
                    orderList.append(order)
                    flag = 1
                
                profitList.append((self.__soldCars * NET_PROFIT_PER_CAR) - ( holdingcost * self.getCarDealer().getInventoryCapacity()) - (ORDER_COST * flag))
                inventory.append(self.getCarDealer().getInventoryCapacity())
                showRoom.append(self.getCarDealer().getShowRoomCapacity())

            
            self.__demandList.append(self.calculateAverage(demandList))
            self.__profitList.append(self.calculateAverage(profitList))
            self.__shortageDaysList.append(self.__shortageDays)
            self.__inventory.append(self.calculateAverage(inventory))
            self.__showRoom.append(self.calculateAverage(showRoom))
            self.__leadTimes.append(self.calculateAverage(leadTimes))
            

    def printResults(self):
        print("Average demand: ", self.calculateAverage(self.__demandList))
        print("Average profit: ", self.calculateAverage(self.__profitList))
        print("Average shortage days: ", self.calculateAverage(self.__shortageDaysList))
        print("Average inventory: ", self.calculateAverage(self.__inventory))
        print("Average show room: ", self.calculateAverage(self.__showRoom))
        print("Average lead times: ", self.calculateAverage(self.__leadTimes))



                    
                

                
                    
                