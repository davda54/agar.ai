import random
import time

from blob import Blob
from blob_family import BlobFamily
from double_linked_list import DoubleLinkedList
from manipulator import Manipulator
from weight_bonus_item import WeightBonusItem


# implements the game logic and moves the environment
class Model:
    WIDTH = 1000
    HEIGHT = 1000
    NUM_OF_PELLETS = 500

    def __init__(self):
        self.pellets = DoubleLinkedList()
        for _ in range(self.NUM_OF_PELLETS): self.__generate_pellet()

        self.blob_families = []
        self.blobs = DoubleLinkedList()
        self.controllers = []
        self.lastime = time.time()
        self.num_players = 0

    def update(self):
        currentTime = time.time()
        dt = currentTime - self.lastime
        self.lastime = currentTime

        for controller in self.controllers:
            controller.update()

        for family in self.blob_families:
            family.update(dt)

        self.__resolve_collisions()

    def get_board_size(self):
        return (self.WIDTH, self.HEIGHT)

    def get_items(self):
        return [pellet.get() for pellet in self.pellets] + [blob.get() for blob in self.blobs]

    def register_controller(self, controller):
        blob = Blob(self.__random_position(50), self.num_players)
        blob_family = BlobFamily(blob, self.num_players)
        controller.set_manipulator(Manipulator(blob_family, self))

        self.num_players += 1

        self.controllers.append(controller)
        self.blobs.append(blob)
        self.blob_families.append(blob_family)

    def __random_position(self, offset):
        return (random.randint(offset, self.WIDTH - offset), random.randint(offset, self.HEIGHT - offset))

    def __resolve_collisions(self):
        blob_a = self.blobs.get_first_iterator()
        while blob_a is not None:

            pellet = self.pellets.get_first_iterator()
            while pellet is not None:
                if blob_a.get().collides(pellet.get()):
                    pellet.get().affect(blob_a.get())
                    tmp = pellet.get_next()
                    self.pellets.delete(pellet)
                    self.__generate_pellet()
                    pellet = tmp
                else:
                    pellet = pellet.get_next()

            blob_b = blob_a.get_next()
            while blob_b is not None:
                if blob_b.get().player_id != blob_b.get().player_id and blob_a.get().collides(blob_b.get()):
                    blob_b = blob_b.get_next()
                else:
                    blob_b = blob_b.get_next()

            blob_a = blob_a.get_next()

    def __generate_pellet(self):
        pellet = WeightBonusItem(self.__random_position(5), 5)
        self.pellets.append(pellet)
