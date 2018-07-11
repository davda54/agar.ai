import vector
from abstract_item import AbstractItem
from parameters import *


class AbstractMovingItem(AbstractItem):
    def __init__(self, model, position, radius, force):
        super().__init__(position, radius)

        self.model = model
        self.force = force
        self.speed = self.__get_speed_from_radius(radius)

    def update(self, dt, global_velocity=(0,0)):
        velocity = vector.add(global_velocity, vector.multiply(self.force, dt))
        self.force = vector.multiply(self.force, FORCE_DRAG)
        self.position = vector.add(self.position, vector.multiply(velocity, dt * self.speed))

        self.bounce_from_boundaries()

    def push(self, bullet_blob, strength):
        direction = vector.normalize(vector.substract(self.position, bullet_blob.get_position()))
        bullet_force = bullet_blob.get_force()

        self_force_strength = vector.dot_product(direction, bullet_force)*strength
        self.add_force(vector.multiply(direction, self_force_strength))
        bullet_blob.set_force(vector.substract(bullet_force, self.force))

    def bounce_from_boundaries(self):
        board_size = self.model.get_board_size()

        if self.position[0] < self.radius: x = self.radius - self.position[0] + BOUNCE_BASE_VALUE
        elif self.position[0] > board_size[0] - self.radius: x = board_size[0] - self.radius - self.position[0] - BOUNCE_BASE_VALUE
        else: x = 0

        if self.position[1] < self.radius: y =  self.radius - self.position[1] + BOUNCE_BASE_VALUE
        elif self.position[1] > board_size[1] - self.radius: y = board_size[1] - self.radius - self.position[1] - BOUNCE_BASE_VALUE
        else: y = 0

        self.add_force((BOUNCE_STRENGTH*x, BOUNCE_STRENGTH*y))

    def add_force(self, force):
        self.force = vector.add(self.force, force)

    def set_radius(self, radius):
        self.radius = radius
        self.speed = self.__get_speed_from_radius(self.radius)

    def __get_speed_from_radius(self, radius):
        return BASE_SPEED * ((radius*2) ** -0.439)