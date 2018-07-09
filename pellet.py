from abstract_bonus_item import AbstractBonusItem

class Pellet(AbstractBonusItem):

    LARGE_PELLET_WEIGHT = 100

    def __init__(self, position, weight, radius):
        super().__init__(position, radius)
        self.weight = weight
        self.proxy = PelletProxy(self)

    def affect(self, blob):
        blob.add_weight(self.weight)

    def get_bonus_weight(self):
        return self.weight

    def get_proxy(self):
        return self.proxy


# read-only wrapper around WeightBonusItem
class PelletProxy():
    def __init__(self, item):
        self.__item = item

    def get_position(self):
        return self.__item.get_position()

    def get_bonus_weight(self):
        return self.__item.get_bonus_weight()