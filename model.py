import random
import time

from blob import Blob
from blob_family import BlobFamily
from double_linked_list import DoubleLinkedList
from large_pellet import LargePellet
from manipulator import Manipulator
from parameters import *
from pellet import Pellet


# implements the game logic and moves the environment
class Model:
    def __init__(self):
        self.pellets = DoubleLinkedList()

        for _ in range(SMALL_PELLET_NUM): self.__generate_pellet()

        for _ in range(LARGE_PELLET_NUM): self.__generate_large_pellet()

        self.blob_families = []
        self.blobs = DoubleLinkedList()
        self.bullet_blobs = DoubleLinkedList()
        self.controllers = []
        self.lastime = time.time()

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

    #TODO: What the actual fuck? Have to simplify this!
    def __resolve_collisions(self):
        blob_a = self.blobs.get_first_iterator()
        while blob_a is not None:

            pellet = self.pellets.get_first_iterator()
            while pellet is not None:
                if blob_a.get().collides(pellet.get()):
                    pellet.get().affect(blob_a.get())

                    if isinstance(pellet.get(), LargePellet): self.__generate_large_pellet()
                    else: self.__generate_pellet()

                    tmp = pellet.get_next()
                    self.pellets.delete(pellet)
                    pellet = tmp

                else:
                    pellet = pellet.get_next()

            blob_b = blob_a.get_next()
            while blob_b is not None:
                if blob_a.get().player_id != blob_b.get().player_id:
                    if blob_a.get().collides(blob_b.get()):
                        if blob_a.get().can_eat(blob_b.get()):
                            blob_a.get().add_weight(blob_b.get().get_weight())
                            tmp = blob_b.get_next()
                            self.blobs.delete(blob_b)
                            blob_b.get().remove_from_family()
                            blob_b = tmp

                        elif blob_b.get().can_eat(blob_a.get()):
                            blob_b.get().add_weight(blob_a.get().get_weight())
                            tmp = blob_a.get_next()
                            self.blobs.delete(blob_a)
                            blob_a.get().remove_from_family()
                            blob_a = tmp
                            break
                        else:
                            blob_b = blob_b.get_next()
                    else:
                        blob_b = blob_b.get_next()

                else:
                    if blob_a.get().get_blob_family().should_stay_divided():
                        if blob_a.get().touches(blob_b.get()):
                            blob_a.get().repel_from_each_other(blob_b.get())
                        blob_b = blob_b.get_next()

                    elif blob_a.get().collides(blob_b.get()):
                        if blob_a.get().get_weight() >= blob_b.get().get_weight():
                            blob_a.get().add_weight(blob_b.get().get_weight())
                            tmp = blob_b.get_next()
                            self.blobs.delete(blob_b)
                            blob_b.get().remove_from_family()
                            blob_b = tmp
                        else:
                            blob_b.get().add_weight(blob_a.get().get_weight())
                            tmp = blob_a.get_next()
                            self.blobs.delete(blob_a)
                            blob_a.get().remove_from_family()
                            blob_a = tmp
                            break
                    else:
                        blob_b = blob_b.get_next()

            blob_a = blob_a.get_next()

        bullet_blob = self.bullet_blobs.get_first_iterator()
        while bullet_blob is not None:

            for blob in self.blobs:
                if bullet_blob.get().collides(blob.get()):
                    blob.get().push(bullet_blob.get())
                    blob.get().add_weight(int(BULLET_EAT_RATIO*bullet_blob.get().get_weight() + 0.5))

                    tmp = bullet_blob.get_next()
                    self.bullet_blobs.delete(bullet_blob)
                    bullet_blob = tmp
                    break
            else:

                for pellet in self.pellets:
                    if isinstance(pellet.get(), LargePellet) and pellet.get().touches(bullet_blob.get()):
                        pellet.get().push(bullet_blob.get())

                        tmp = bullet_blob.get_next()
                        self.bullet_blobs.delete(bullet_blob)
                        bullet_blob = tmp
                        break
                else:
                    bullet_blob = bullet_blob.get_next()


    # TODO: dont generate on active cell
    def __generate_pellet(self):
        weight = random.randint(1, 5)
        pellet = Pellet(self.__random_position(10), weight)
        self.pellets.append(pellet)

    # TODO: dont generate on active cell
    def __generate_large_pellet(self):
        pellet = LargePellet(self, self.__random_position(50))
        self.pellets.append(pellet)