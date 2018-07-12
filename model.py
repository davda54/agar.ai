import random
import time

from double_linked_list import DoubleLinkedList
from entities.blob import Blob
from entities.blob_family import BlobFamily
from entities.large_pellet import LargePellet
from entities.pellet import Pellet
from manipulator import Manipulator
from parameters import *


# implements the game logic and moves the environment
class Model:
    def __init__(self):
        self.pellets = DoubleLinkedList()
        self.blobs = DoubleLinkedList()
        self.bullet_blobs = DoubleLinkedList()
        self.blob_families = []
        self.controllers = []
        self.lastime = time.time()

        for _ in range(SMALL_PELLET_NUM): self.__generate_pellet()

        for _ in range(LARGE_PELLET_NUM): self.__generate_large_pellet()

    def update(self):
        dt = self.__get_dt()
        self.__move(dt)
        self.__resolve_collisions()

    def get_board_size(self):
        return (BOARD_WIDTH, BOARD_HEIGHT)

    def get_items(self):
        return [pellet.get() for pellet in self.pellets] + [bullet_blob.get() for bullet_blob in self.bullet_blobs] + [blob.get() for blob in self.blobs]

    def register_controller(self, controller):
        blob_family = BlobFamily(self, len(self.controllers))
        blob = Blob(self, self.__random_position(100), len(self.controllers), blob_family)
        blob_family.add_blob(blob)
        controller.set_manipulator(Manipulator(blob_family, self))

        self.controllers.append(controller)
        self.blobs.append(blob)
        self.blob_families.append(blob_family)

    def add_blob(self, blob):
        self.blobs.append(blob)

    def add_bullet_blob(self, bullet_blob):
        self.bullet_blobs.append(bullet_blob)

    def __move(self, dt):
        for controller in self.controllers:
            controller.update()
        for family in self.blob_families:
            family.update(dt)
        for bullet_blob in self.bullet_blobs:
            bullet_blob.get().update(dt)
        for pellet in self.pellets:
            if isinstance(pellet.get(), LargePellet): pellet.get().update(dt)

    def __get_dt(self):
        currentTime = time.time()
        dt = currentTime - self.lastime
        self.lastime = currentTime
        return dt

    def __random_position(self, offset):
        return (random.randint(offset, BOARD_WIDTH - offset), random.randint(offset, BOARD_HEIGHT - offset))

    def __resolve_collisions(self):
        blob_iter = self.blobs.get_first_iterator()
        while blob_iter is not None:

            self.__resolve_collisions_blob_pellets(blob_iter.get())

            if self.__resolve_collisions_blob_other_blobs(blob_iter):
                tmp = blob_iter.get_next()
                self.blobs.delete(blob_iter)
                blob_iter.get().remove_from_family()
                blob_iter = tmp
                continue

            blob_iter = blob_iter.get_next()

        bullet_blob = self.bullet_blobs.get_first_iterator()
        while bullet_blob is not None:

            if self.__resolve_collisions_bullet_blobs(bullet_blob.get()) or self.__resolve_collisions_bullet_pellets(bullet_blob.get()):
                tmp = bullet_blob.get_next()
                self.bullet_blobs.delete(bullet_blob)
                bullet_blob = tmp
            else:
                bullet_blob = bullet_blob.get_next()

    def __resolve_collisions_blob_pellets(self, blob):
        pellet = self.pellets.get_first_iterator()
        while pellet is not None:
            if blob.collides(pellet.get()):
                pellet.get().affect(blob)

                if isinstance(pellet.get(), LargePellet):
                    self.__generate_large_pellet()
                else:
                    self.__generate_pellet()

                tmp = pellet.get_next()
                self.pellets.delete(pellet)
                pellet = tmp

            else:
                pellet = pellet.get_next()

    def __resolve_collisions_blob_other_blobs(self, blob_iter_1):
        # returns true if blob_iter_1.get() should be deleted

        blob_1 = blob_iter_1.get()
        blob_iter_2 = blob_iter_1.get_next()

        can_merge = not blob_1.get_blob_family().should_stay_divided()

        while blob_iter_2 is not None:

            blob_2 = blob_iter_2.get()
            same_family = blob_1.get_blob_family() is blob_2.get_blob_family()

            if blob_1.collides(blob_2):
                if (not same_family and blob_1.can_eat(blob_2)) or (same_family and can_merge and blob_1.get_weight() >= blob_2.get_weight()):
                    blob_1.add_weight(blob_2.get_weight())
                    tmp = blob_iter_2.get_next()
                    self.blobs.delete(blob_iter_2)
                    blob_2.remove_from_family()
                    blob_iter_2 = tmp
                    continue

                elif (not same_family and blob_2.can_eat(blob_1)) or (same_family and can_merge and blob_1.get_weight() <= blob_2.get_weight()):
                    blob_2.add_weight(blob_1.get_weight())
                    return True

            if same_family and not can_merge and blob_1.touches(blob_2):
                blob_1.repel_from_each_other(blob_2)

            blob_iter_2 = blob_iter_2.get_next()

    def __resolve_collisions_bullet_blobs(self, bullet_blob):
        for blob in self.blobs:
            if bullet_blob.collides(blob.get()):
                blob.get().push(bullet_blob, BULLET_BLOB_STRENGTH)
                blob.get().add_weight(BULLET_EAT_RATIO * bullet_blob.get_weight())
                return True
        return False

    def __resolve_collisions_bullet_pellets(self, bullet_blob):
        for pellet in self.pellets:
            if isinstance(pellet.get(), LargePellet) and pellet.get().collides(bullet_blob):
                pellet.get().push(bullet_blob, BULLET_PELLET_STRENGTH)
                return True
        return False

    def __generate_pellet(self):
        weight = random.randint(1, 5)
        pellet = Pellet(self.__random_position(10), weight)

        while True:
            for blob in self.blobs:
                if blob.get().touches(pellet):
                    break
            else: break
            pellet.position = self.__random_position(50)

        self.pellets.append(pellet)

    def __generate_large_pellet(self):
        pellet = LargePellet(self, self.__random_position(50))

        while True:
            for blob in self.blobs:
                if blob.get().touches(pellet):
                    break
            else: break
            pellet.position = self.__random_position(50)

        self.pellets.append(pellet)