from entities.abstract_moving_item import AbstractMovingItem
from parameters import *


class LargePellet(AbstractMovingItem):

    def __init__(self, model, position):
        super().__init__(model, position, LARGE_PELLET_RADIUS, (0,0))
        self.proxy = LargePelletProxy(self)

    def affect(self, blob):
        if blob.get_weight() > BLOB_MINIMAL_WEIGHT_TO_EXPLODE:
            blob.explode()
        else:
            blob.add_weight(LARGE_PELLET_WEIGHT)

    def get_bonus_weight(self):
        return LARGE_PELLET_WEIGHT

    def get_proxy(self):
        return self.proxy


# read-only wrapper around WeightBonusItem
class LargePelletProxy():
    def __init__(self, item):
        self.__item = item

    def get_position(self):
        return self.__item.get_position()

    def get_bonus_weight(self):
        return self.__item.get_bonus_weight()