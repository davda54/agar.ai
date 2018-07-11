from abstract_bonus_item import AbstractBonusItem
from parameters import *

class Pellet(AbstractBonusItem):
    def __init__(self, position, weight):
        super().__init__(position, SMALL_PELLET_RADIUS)
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