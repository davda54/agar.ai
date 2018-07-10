from abstract_blob import AbstractBlob


class BulletBlob(AbstractBlob):
    INIT_WEIGHT = 14

    def __init__(self, model, position, player_id, force):
        super().__init__(model, position, player_id, self.INIT_WEIGHT, force)
        self.proxy = BulletBlobProxy(self)

    def get_proxy(self):
        return self.proxy


# read-only wrapper around Blob
class BulletBlobProxy():
    def __init__(self, blob):
        self.__blob = blob

    def get_position(self):
        return self.__blob.get_position()

    def get_weight(self):
        return self.__blob.get_weight()