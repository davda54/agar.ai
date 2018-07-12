from entities.abstract_blob import AbstractBlob
from parameters import *


class BulletBlob(AbstractBlob):
    def __init__(self, model, position, player_id, force):
        super().__init__(model, position, player_id, BULLET_WEIGHT, force)
        self.proxy = BulletBlobProxy(self)

    def get_proxy(self):
        return self.proxy

    def get_force(self):
        return self.force

    def set_force(self, force):
        self.force = force

# read-only wrapper around Blob
class BulletBlobProxy():
    def __init__(self, blob):
        self.__blob = blob

    def get_position(self):
        return self.__blob.get_position()

    def get_weight(self):
        return self.__blob.get_weight()