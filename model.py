import random
import time

from blob import Blob
from blob_family import BlobFamily
from manipulator import Manipulator
from weight_bonus_item import WeightBonusItem


# implements the game logic and moves the environment
class Model:
    WIDTH = 1000
    HEIGHT = 1000
    NUM_OF_PELLETS = 100

    def __init__(self):
        self.pellets = [WeightBonusItem(self.__random_position(5), 5) for _ in range(self.NUM_OF_PELLETS)]
        self.blob_families = []
        self.controllers = []
        self.lastime = time.time()

    def update(self):
        currentTime = time.time()
        dt = currentTime - self.lastime
        self.lastime = currentTime

        for controller in self.controllers:
            controller.update()

        for family in self.blob_families:
            family.update(dt)

    def get_board_size(self):
        return (self.WIDTH, self.HEIGHT)

    def get_items(self):
        return self.pellets + [blob for family in self.blob_families for blob in family.get_blobs()]

    def register_controller(self, controller):
        blob_family = BlobFamily(Blob(self.__random_position(50)))
        controller.set_manipulator(Manipulator(blob_family, self))

        self.controllers.append(controller)
        self.blob_families.append(blob_family)

    def __random_position(self, offset):
        return (random.randint(offset, self.WIDTH - offset), random.randint(offset, self.HEIGHT - offset))