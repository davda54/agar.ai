import math

from abstract_bonus_item import AbstractBonusItem


class WeightBonusItem(AbstractBonusItem):
    SMALL_BONUS_WEIGHT = 10
    LARGE_BONUS_WEIGHT = 200

    def __init__(self, position, weight):
        super().__init__(position, math.sqrt(weight))
        self.weight = weight
        self.proxy = WeightBonusItemProxy(self)

    def affect(self, blob):
        blob.set_weight(blob.get_weight() + self.weight)

    def get_bonus_weight(self):
        return self.weight

    def get_proxy(self):
        return self.proxy


# read-only wrapper around WeightBonusItem
class WeightBonusItemProxy():
    def __init__(self, item):
        self.__item = item

    def get_position(self):
        return self.__item.get_position()

    def get_bonus_weight(self):
        return self.__item.get_bonus_weight()