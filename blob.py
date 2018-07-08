import math

import vector
from abstract_item import AbstractItem


class Blob(AbstractItem):
    INIT_WEIGHT = 20
    BASE_SPEED = 100

    def __init__(self, position, player_id):
        self.weight = self.INIT_WEIGHT
        super().__init__(position, self.__get_radius_from_weight())

        self.player_id = player_id
        self.speed = self.__get_speed_from_radius()
        self.proxy = BlobProxy(self)

    def update(self):
        pass

    def move(self, velocity, dt):
        self.position = vector.add(self.position, vector.multiply(velocity, dt*self.speed))

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight
        self.radius = self.__get_radius_from_weight()
        self.speed = self.__get_speed_from_radius()

    def get_proxy(self):
        return self.proxy

    def get_player_id(self):
        return self.player_id

    def __get_radius_from_weight(self):
        return math.sqrt(self.weight*5)

    def __get_weight_from_radius(self):
        return self.radius*self.radius / 5

    def __get_speed_from_radius(self):
        return self.BASE_SPEED*2.2*(self.radius**-0.439)

# read-only wrapper around Blob
class BlobProxy():
    def __init__(self, blob):
        self.__blob = blob

    def get_position(self):
        return self.__blob.get_position()

    def get_weight(self):
        return self.__blob.get_weight()