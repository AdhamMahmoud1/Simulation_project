
class CarDealer:
    def __init__(self):
        # intial case
        self.__inventoryCapacity = 3
        self.__showRoomCapacity = 4

    def getInventoryCapacity(self):
        return self.__inventoryCapacity

    def getShowRoomCapacity(self):
        return self.__showRoomCapacity

    def setInventoryCapacity(self, inventory):
        self.__inventoryCapacity = inventory

    def setShowRoomCapacity(self, showRoomCapacity):
        self.__showRoomCapacity = showRoomCapacity

