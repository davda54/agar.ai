import pygame

import vector
from abstract_controller import AbstractController


# controls a blob family according to a mouse movemnt
class MouseController(AbstractController):

    def __init__(self, view_size, player_radius):
        self.view_center = vector.divide(view_size, 2)
        self.player_radius = player_radius

    def update(self):
        mouse_position = pygame.mouse.get_pos()
        direction = vector.substract(mouse_position, self.view_center)
        direction = vector.divide(direction, self.player_radius)
        self.manipulator.set_velocity(direction)