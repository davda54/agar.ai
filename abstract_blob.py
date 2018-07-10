import math

import vector
from abstract_item import AbstractItem


class AbstractBlob(AbstractItem):

    BASE_SPEED = 250

    def __init__(self, model, position, player_id, weight, force):
        self.weight = weight
        super().__init__(position, self.__get_radius_from_weight())

        self.model = model
        self.player_id = player_id
        self.force = force
        self.proxy = BlobProxy(self)
        self.speed = self.__get_speed_from_radius()

    def update(self, dt, global_velocity=(0,0)):
        velocity = vector.add(global_velocity, vector.multiply(self.force, dt))
        self.force = vector.multiply(self.force, 0.95)
        self.position = vector.add(self.position, vector.multiply(velocity, dt * self.speed))

        self.bounce_from_boundaries()

    def bounce_from_boundaries(self):
        board_size = self.model.get_board_size()

        if self.position[0] < self.radius: x = self.radius - self.position[0] + 10
        elif self.position[0] > board_size[0] - self.radius: x = board_size[0] - self.radius - self.position[0] - 10
        else: x = 0

        if self.position[1] < self.radius: y =  self.radius - self.position[1] + 10
        elif self.position[1] > board_size[1] - self.radius: y = board_size[1] - self.radius - self.position[1] - 10
        else: y = 0

        self.force = vector.add(self.force, (x, y))

    def get_weight(self):
        return self.weight

    def add_weight(self, weight):
        self.set_weight(self.weight + weight)

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