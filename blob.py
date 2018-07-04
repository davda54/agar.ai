from abstract_item import AbstractItem

class Blob(AbstractItem):
    INIT_SIZE = 10

    def __init__(self, position):
        super().__init__(position, self.INIT_SIZE)
        self.proxy = BlobProxy(self)

    def get_weight(self):
        pass

    def update(self):
        pass

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