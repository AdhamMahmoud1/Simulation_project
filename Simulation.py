import CarDealer
import Order
import Car
import random
class Simulation:
    def __init__(self):
        self.__carDealer = CarDealer.CarDealer()
        self.__demand = 0
        self.__demandList = list()
        self.__soldCars = 0
        self.__shortageDays = 0
        self.__shortageDaysList = list()
        self.__profitList = list()
        self.__inventory = list()
        self.__showRoom = list()
        self.__orders = list()

    def getCarDealer(self):
        return self.__carDealer

    def getSold(self):
        return self.__soldCars

    def getShortageDays(self):
        return self.__shortageDays
    
    def getShortageDaysList(self):
        return self.__shortageDaysList

    def getProfitList(self):
        return self.__profitList

    def getInventory(self):
        return self.__inventory

    def getShowRoom(self):
        return self.__showRoom

    def setSold(self, sold):
        self.__soldCars = sold

    def setShortageDays(self, shortageDays):
        self.__shortageDays = shortageDays

    def setInventory(self, inventory):
        self.__inventory = inventory

    def setShowRoom(self, showRoom):
        self.__showRoom = showRoom

    def generateDemand(self):
        randomProp = random.uniform(0, 1)
        if randomProp >= 0 and randomProp < 0.2:
            return 0
        elif randomProp >= 0.2 and randomProp < 0.54:
            return 1
        elif randomProp >= 0.54 and randomProp < 0.9:
            return 2
        else:
            return 3

    def setDemand(self):
        self.__demand = self.generateDemand()

    def getDemand(self):
        return self.__demand

    def getDemandList(self):
        return self.__demandList

    def run(self):
        for i in range(1000):
            self.__carDealer = CarDealer.CarDealer()
            self.__orders.append(Order.Order(5, 2))
            profit = 0
            shortageDays = 0
            for day in range(1, 31):
                o = 0
                while len(self.__orders) > 0 and o < len(self.__orders):
                    if self.__orders[o].getLeadTime() == 0:
                        if (self.__orders[o].getQuantity() + self.__carDealer.getShowRoomCapacity()) <= 5:
                            self.__carDealer.setShowRoomCapacity(self.__carDealer.getShowRoomCapacity() + self.__orders[o].getQuantity())
                        else:
                            self.__orders[o].setQuantity(self.__orders[o].getQuantity() - (5 - self.__carDealer.getShowRoomCapacity()))
                            self.__carDealer.setShowRoomCapacity(5)
                            self.__carDealer.setInventory(self.__carDealer.getInventory() + self.__orders[o].getQuantity()) 

                        self.__orders.remove(self.__orders[o])
                    else:
                        self.__orders[o].setLeadTime(self.__orders[o].getLeadTime() - 1)

                
                    o += 1
                    

                self.setDemand()
                self.__demandList.append(self.getDemand())
                if self.__demand <= self.__carDealer.getInventory():
                    self.__carDealer.setInventory(
                        self.__carDealer.getInventory() - self.__demand
                    )
                    self.__soldCars += self.__demand
                else:
                    self.__soldCars += self.__carDealer.getInventory()
                    self.__shortageDays += 1
                    self.__carDealer.setInventory(0)

                if self.__carDealer.getShowRoomCapacity() >= self.__demand:
                    self.__carDealer.setShowRoomCapacity(self.__carDealer.getShowRoomCapacity() - self.__demand)
                    self.__soldCars += self.__demand
                else:
                    self.__soldCars += self.__carDealer.getShowRoomCapacity()
                    self.__carDealer.setShowRoomCapacity(0)

                order = Order.Order(0,0)
                order.setQuantity(15 - self.__carDealer.getInventory() - self.__carDealer.getShowRoomCapacity())
                order.setNewLeadTime()
                self.__orders.append(order)
                profit = self.__soldCars * Car.Car().getNetProfit()

                if (self.__carDealer.getInventory() + self.__carDealer.getShowRoomCapacity() == 0):
                    shortageDays += 1

            self.__profitList.append(profit)
            self.__shortageDaysList.append(shortageDays)
            self.__inventory.append(self.__carDealer.getInventory())
            self.__showRoom.append(self.__carDealer.getShowRoomCapacity())
            self.__soldCars = 0
            self.__orders.clear()


