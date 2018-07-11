import vector
from abstract_moving_item import AbstractMovingItem

class LargePellet(AbstractMovingItem):
    WEIGHT = 100
    RADIUS = 25
    SPEED = 250

    def __init__(self, model, position):
        super().__init__(model, position, self.RADIUS, self.SPEED, (0,0))
        self.proxy = LargePelletProxy(self)

    def push(self, bullet_blob):
        direction = vector.normalize(vector.substract(self.position, bullet_blob.get_position()))
        bullet_force = bullet_blob.get_force()

        pellet_force_strength = vector.dot_product(direction, bullet_force)
        self.force = vector.multiply(direction, pellet_force_strength)
        bullet_blob.set_force(vector.substract(bullet_force, self.force))

    def add_force(self, force):
        self.force = vector.add(self.force, force)

    def affect(self, blob):
        blob.add_weight(self.WEIGHT)

    def get_bonus_weight(self):
        return self.WEIGHT

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