import math

from abstract_moving_item import AbstractMovingItem


class AbstractBlob(AbstractMovingItem):

    BASE_SPEED = 250

    def __init__(self, model, position, player_id, weight, force):
        self.weight = weight
        radius = self.__get_radius_from_weight(weight)
        speed = self.__get_speed_from_radius(radius)
        super().__init__(model, position, radius, speed, force)

        self.player_id = player_id

    def get_weight(self):
        return self.weight

    def add_weight(self, weight):
        self.set_weight(self.weight + weight)

    def set_weight(self, weight):
        self.weight = weight
        self.radius = self.__get_radius_from_weight(self.weight)
        self.speed = self.__get_speed_from_radius(self.radius)

    def get_player_id(self):
        return self.player_id

    def __get_radius_from_weight(self, weight):
        return math.sqrt(weight*5)

    def __get_weight_from_radius(self, radius):
        return radius*radius / 5

    def __get_speed_from_radius(self, radius):
        return self.BASE_SPEED*2.2*(radius**-0.439)