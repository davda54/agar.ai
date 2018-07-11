import random

import vector
from abstract_blob import AbstractBlob
from bullet_blob import BulletBlob
from parameters import *


class Blob(AbstractBlob):
    def __init__(self, model, position, player_id, blob_family, force=(0,0), weight=BLOB_INIT_WEIGHT):
        super().__init__(model, position, player_id, weight, force)
        self.blob_family = blob_family
        self.proxy = BlobProxy(self)

    def update(self, dt, global_velocity=(0, 0)):
        super().update(dt, global_velocity)
        self.weight -= self.weight * BLOB_WEIGHT_LOSE_PER_SECOND * dt

    def get_together(self, center):
        difference = vector.substract(center, self.position)
        self.add_force(vector.multiply(difference, BLOB_GRAVITATION))

    def repel_from_each_other(self, blob):
        difference = vector.substract(blob.get_position(), self.position)
        distance = vector.norm(difference)
        strength = distance - self.radius - blob.get_radius()

        self.add_force(vector.multiply(difference,  BLOB_REPEL_STRENGTH*strength/distance - BLOB_REPEL_BASE_STRENGTH))
        blob.add_force(vector.multiply(difference, -BLOB_REPEL_STRENGTH*strength/distance + BLOB_REPEL_BASE_STRENGTH))

    def explode(self):
        self.set_weight(int(self.get_weight() * BLOB_EXPLOSION_SHRINK + 0.5))
        has_divided = False

        while self.get_weight() >= 2*BLOB_INIT_WEIGHT and self.blob_family.number_of_blobs() < BLOB_MAX_NUM:
            direction = vector.random_direction()
            position = vector.add(self.get_position(), vector.multiply(direction, self.get_radius()))

            shoot = random.randint(0, BLOB_EXPLOSION_SHOOT_CHANCE) == 0

            if shoot:
                self.add_weight(-BULLET_WEIGHT)
                bullet_blob = BulletBlob(self.model, position, self.player_id, vector.multiply(direction, BLOB_SHOOT_STRENGTH))
                self.model.add_bullet_blob(bullet_blob)
            else:
                weight = min(random.randint(BLOB_INIT_WEIGHT, max(BLOB_INIT_WEIGHT, int(self.get_weight()/4))), self.get_weight() - BLOB_INIT_WEIGHT)
                self.add_weight(-weight)
                new_blob = Blob(self.model, position, self.player_id, self.blob_family, (0,0), weight)

                self.blob_family.add_blob(new_blob)
                self.model.add_blob(new_blob)
                has_divided = True

        if has_divided: self.blob_family.set_countdown()

    def can_eat(self, other_blob):
        return self.weight * BLOB_WEIGHT_RATIO_TO_EAT > other_blob.get_weight()

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

    def is_main_blob(self):
        return self.blob_family.main_blob is self

# read-only wrapper around Blob
class BlobProxy():
    def __init__(self, blob):
        self.__blob = blob

    def get_position(self):
        return self.__blob.get_position()

    def get_weight(self):
        return self.__blob.get_weight()