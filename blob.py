import random

import vector
from abstract_blob import AbstractBlob
from bullet_blob import BulletBlob


class Blob(AbstractBlob):
    INIT_WEIGHT = 16

    def __init__(self, model, position, player_id, blob_family, force=(0,0)):
        super().__init__(model, position, player_id, self.INIT_WEIGHT, force)
        self.blob_family = blob_family
        self.proxy = BlobProxy(self)

    def get_together(self, center):
        difference = vector.multiply(vector.substract(center, self.position), 0.015)
        self.force = vector.add(self.force, difference)

    def repel_from_each_other(self, blob):
        difference = vector.substract(blob.get_position(), self.position)
        distance = vector.norm(difference)
        strength = distance - self.radius - blob.get_radius()

        self.force = vector.add(self.force, vector.multiply(difference,  0.1*strength/distance - 0.01))
        blob.force = vector.add(blob.force, vector.multiply(difference, -0.1*strength/distance + 0.01))

    def explode(self):
        self.set_weight(int(self.get_weight() * 0.9 + 0.5))
        has_divided = False

        while self.get_weight() >= 2*self.INIT_WEIGHT and self.blob_family.number_of_blobs() < self.blob_family.MAX_NUM_BLOBS:
            self.add_weight(-self.INIT_WEIGHT)
            direction = vector.random_direction()
            position = vector.add(self.get_position(), vector.multiply(direction, self.get_radius()))

            shoot = random.randint(0,2) == 0

            if shoot:
                bullet_blob = BulletBlob(self.model, position, self.player_id, vector.multiply(direction, 200))
                self.model.add_bullet_blob(bullet_blob)
            else:
                new_blob = Blob(self.model, position, self.player_id, self.blob_family, vector.multiply(direction, 50))
                self.blob_family.blobs.append(new_blob)
                self.model.add_blob(new_blob)
                has_divided = True

        if has_divided: self.blob_family.divide_countdown = max(20, self.blob_family.get_total_cell_radius() * 0.2)

    def set_weight(self, weight):
        old_weight = self.weight
        super().set_weight(weight)

        if weight > old_weight:
            if weight > self.blob_family.main_blob.get_weight():
                self.blob_family.main_blob = self
        elif self is self.blob_family.main_blob:
            self.blob_family.select_main_blob()

    def get_blob_family(self):
        return self.blob_family

    def remove_from_family(self):
        self.blob_family.remove(self)

    def get_proxy(self):
        return self.proxy

# read-only wrapper around Blob
class BlobProxy():
    def __init__(self, blob):
        self.__blob = blob

    def get_position(self):
        return self.__blob.get_position()

    def get_weight(self):
        return self.__blob.get_weight()