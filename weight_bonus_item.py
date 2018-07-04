from abstract_bonus_item import AbstractBonusItem

class WeightBonusItem(AbstractBonusItem):
    INIT_SIZE = 2

    def __init__(self, position):
        super().__init__(position, self.INIT_SIZE)
        self.proxy = WeightBonusItem(self)

    def affect(self, blob):
        pass

    def get_bonus_weight(self):
        pass

    def get_proxy(self):
        return self.proxy


# read-only wrapper around WeightBonusItem
class WeightBonusItemProxy():
    def __init__(self, bonus):
        self.__bonus = bonus

    def get_position(self):
        return self.__bonus.get_position()

    def get_bonus_weight(self):
        return self.__bonus.get_bonus_weight()