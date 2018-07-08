import math

import vector
from abstract_item import AbstractItem


class Blob(AbstractItem):
    INIT_RADIUS = 20
    BASE_SPEED = 50000

    def __init__(self, position, player_id):
        super().__init__(position, self.INIT_RADIUS)

        self.player_id = player_id
        self.__set_weight_from_radius()
        self.__set_speed_from_weight()
        self.proxy = BlobProxy(self)

    def update(self):
        pass

    def move(self, velocity, dt):
        self.position = vector.add(self.position, vector.multiply(velocity, dt*self.speed))

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight
        self.__set_radius_from_weight()
        self.__set_speed_from_weight()

    def get_proxy(self):
        return self.proxy

    def __set_radius_from_weight(self):
        self.radius = math.sqrt(self.weight)

    def __set_weight_from_radius(self):
        self.weight = self.radius*self.radius

    def __set_speed_from_weight(self):
        self.speed = self.BASE_SPEED / self.weight

# read-only wrapper around Blob
class BlobProxy():
    def __init__(self, blob):
        self.__blob = blob

    def get_position(self):
        return self.__blob.get_position()

    def get_weight(self):
        return self.__blob.get_weight()