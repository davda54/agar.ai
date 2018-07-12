import math

from entities.abstract_moving_item import AbstractMovingItem


class AbstractBlob(AbstractMovingItem):

    def __init__(self, model, position, player_id, weight, force):
        self.weight = weight
        super().__init__(model, position, self.__get_radius_from_weight(weight), force)

        self.player_id = player_id

    def get_weight(self):
        return int(self.weight + 0.5)

    def add_weight(self, weight):
        self.set_weight(self.weight + weight)

    def set_weight(self, weight):
        self.weight = weight
        self.set_radius(self.__get_radius_from_weight(self.weight))

    def get_player_id(self):
        return self.player_id

    def __get_radius_from_weight(self, weight):
        return math.sqrt(weight)

    def __get_weight_from_radius(self, radius):
        return radius*radius