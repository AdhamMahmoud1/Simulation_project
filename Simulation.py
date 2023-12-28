import CarDealer
import Order

import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

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
        self.__lossDaysList = list()
        self.__profitdaysList = list()

    def getCarDealer(self):
        return self.__carDealer

    def setDemand(self):
        randomProp = random.uniform(0, 1)
        if randomProp >= 0 and randomProp < 0.2:
            self.__demand = 0
        elif randomProp >= 0.2 and randomProp < 0.54:
            self.__demand = 1
        elif randomProp >= 0.54 and randomProp < 0.9:
            self._demand = 2
        else:
            self.__demand = 3

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
            orderList = list()
            leadTimes = list()
            orderList.append(Order.Order(5, 2))
            self.__shortageDays = 0
            self.__soldCars = 0
            demandList = list()
            profitList = list()
            inventory = list()
            showRoom = list()
            holdingcost = 0
            loss = 0
            profit = 0
            # simulating for 10 days
            for day in range(1, 11):
                # check if there is any order to be delivered
                if len(orderList) > 0:
                    for order in orderList:
                        if order.getLeadTime() == 0:
                            # deliver the order
                            if (
                                order.getQuantity()
                                + self.getCarDealer().getShowRoomCapacity()
                                > 5
                            ):
                                self.getCarDealer().setShowRoomCapacity(5)
                                order.setQuantity(
                                    order.getQuantity()
                                    - (5 - self.getCarDealer().getShowRoomCapacity())
                                )
                                self.getCarDealer().setInventoryCapacity(
                                    self.getCarDealer().getInventoryCapacity()
                                    + order.getQuantity()
                                )
                            else:
                                self.getCarDealer().setShowRoomCapacity(
                                    order.getQuantity()
                                    + self.getCarDealer().getShowRoomCapacity()
                                )
                        else:
                            # reduce the lead time
                            order.setLeadTime(order.getLeadTime() - 1)
                    # remove the delivered orders from the list
                    for order in orderList:
                        if order.getLeadTime() == 0:
                            orderList.remove(order)

                self.setDemand()
                demandList.append(self.getDemand())

                if (
                    self.getCarDealer().getInventoryCapacity()
                    + self.getCarDealer().getShowRoomCapacity()
                    == 0
                ):
                    self.__shortageDays += 1
                elif self.getDemand() <= self.getCarDealer().getInventoryCapacity():
                    self.getCarDealer().setInventoryCapacity(
                        self.getCarDealer().getInventoryCapacity() - self.getDemand()
                    )
                    self.__soldCars += self.getDemand()
                elif self.getDemand() > self.getCarDealer().getInventoryCapacity():
                    self.__demand -= self.getCarDealer().getInventoryCapacity()
                    self.getCarDealer().setInventoryCapacity(0)
                    if self.getDemand() <= self.getCarDealer().getShowRoomCapacity():
                        self.getCarDealer().setShowRoomCapacity(
                            self.getCarDealer().getShowRoomCapacity() - self.getDemand()
                        )
                        self.__soldCars += self.getDemand()

                # calculate the holding cost
                holdingcost += self.getCarDealer().getInventoryCapacity() * HOLDING_COST

                # check if the review period is over
                flag = 0
                if day % REVIEW_PERIOD == 0:
                    order = Order.Order(0, 0)
                    order.setQuantity(
                        15
                        - self.getCarDealer().getInventoryCapacity()
                        - self.getCarDealer().getShowRoomCapacity()
                    )
                    order.setNewLeadTime()
                    leadTimes.append(order.getLeadTime())
                    orderList.append(order)
                    flag = 1

                if (
                    (self.__soldCars * NET_PROFIT_PER_CAR)
                    - (holdingcost)
                    - (ORDER_COST * flag)
                ) < 0:
                    loss += 1
                else:
                    profit += 1
                profitList.append(
                    (self.__soldCars * NET_PROFIT_PER_CAR)
                    - (holdingcost)
                    - (ORDER_COST * flag)
                )
                inventory.append(self.getCarDealer().getInventoryCapacity())
                showRoom.append(self.getCarDealer().getShowRoomCapacity())

            self.__demandList.append(self.calculateAverage(demandList))
            self.__profitList.append(self.calculateAverage(profitList))
            self.__shortageDaysList.append(self.__shortageDays)
            self.__inventory.append(self.calculateAverage(inventory))
            self.__showRoom.append(self.calculateAverage(showRoom))
            self.__leadTimes.append(self.calculateAverage(leadTimes))
            self.__lossDaysList.append(loss)
            self.__profitdaysList.append(profit)

    def theoricalAveargeDemand(self):
        theoricalAverage = (0 * 0.2) + (1 * 0.34) + (2 * 0.36) + (3 * 0.1)
        percentError = (
            abs(theoricalAverage - self.calculateAverage(self.__demandList))
            / theoricalAverage
        ) * 100
        return percentError

    def theoricalAveargeLeadTime(self):
        theoricalAverage = (1 * 0.4) + (2 * 0.35) + (3 * 0.25)
        percentError = (
            abs(theoricalAverage - self.calculateAverage(self.__leadTimes))
            / theoricalAverage
        ) * 100
        return percentError

    def printResults(self):
        print("Average demand: ", self.calculateAverage(self.__demandList))
        print("Average profit: ", self.calculateAverage(self.__profitList))
        print("Average shortage days: ", self.calculateAverage(self.__shortageDaysList))
        print("Average inventory: ", self.calculateAverage(self.__inventory))
        print("Average show room: ", self.calculateAverage(self.__showRoom))
        print("Average lead times: ", self.calculateAverage(self.__leadTimes))
        print(
            "Percentage of Profit: ", self.calculateAverage(self.__profitdaysList) / 10
        )
        print("Percentage of Loss: ", self.calculateAverage(self.__lossDaysList) / 10)
        print("Theorical Average Demand: ", self.theoricalAveargeDemand())
        print("Theorical Average Lead Time: ", self.theoricalAveargeLeadTime())

    def printHistoGrams(self):
        plt.hist(self.__demandList, bins=20)
        plt.xlabel("Values of Demand")
        plt.ylabel("Frequency of Demand")
        plt.title("Histogram of Demand")
        plt.show()

        plt.hist(self.__leadTimes, bins=10)
        plt.xlabel("Values of Lead Times")
        plt.ylabel("Frequency of Lead Times")
        plt.title("Histogram of Lead Times")
        plt.show()

        plt.hist(self.__profitList, bins=10)
        plt.xlabel("Values of Profit")
        plt.ylabel("frequency of Profit")
        plt.title("Histogram of Profit")
        plt.show()

        plt.hist(self.__shortageDaysList, bins=10)
        plt.xlabel("Values of Shortage Days")
        plt.ylabel("frequency of Shortage Days")
        plt.title("Histogram of Shortage Days")
        plt.show()

        plt.hist(self.__inventory, bins=10)
        plt.xlabel("Values of Inventory")
        plt.ylabel("frequency of Inventory")
        plt.title("Histogram of Inventory")
        plt.show()

        plt.hist(self.__showRoom, bins=10)
        plt.xlabel("Values of Show Room")
        plt.ylabel("frequency of Show Room")
        plt.title("Histogram of Show Room")
        plt.show()

    def display_simulation_results(self):
        root = tk.Tk()
        tree = ttk.Treeview(root)
        tree["columns"] = (
            "Average Demand",
            "Average Profit",
            "Average Shortage Days",
            "Average Inventory",
            "Average Show Room",
            "Average Lead Times",
            "Percentage of Profit",
            "Percentage of Loss",
        )
        for column in tree["columns"]:
            tree.heading(column, text=column)

        for i in range(10):
            tree.insert(
                "",
                "end",
                text=f"Simulation {i+1}",
                values=(
                    self.getDemandList()[i],
                    self.getProfitList()[i],
                    self.getShortageDaysList()[i],
                    self.getInventoryCapacity()[i],
                    self.getShowRoomCapacity()[i],
                    self.calculateAverage(self.__leadTimes),
                    self.calculateAverage(self.__profitdaysList) / 10,
                    self.calculateAverage(self.__lossDaysList) / 10,
                ),
            )

        tree.pack()
        root.mainloop()


# Usage:
# simulation = Simulation()
# simulation.run()
