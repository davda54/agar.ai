from functools import reduce

import vector
from blob import Blob


# contains all blobs that makes up a player and manipulates them
class BlobFamily():
    def __init__(self, model, blob, player_id):
        self.model = model
        self.blobs = [blob] # better use some heap to quickly get the largest blob
        self.main_blob = blob
        self.player_id = player_id
        self.velocity = (0,0)
        self.shoot_now = False
        self.divide_now = False

    def update(self, dt):
        if self.divide_now:
            self.__divide()

        center = self.get_average_position()

        for blob in self.blobs:
            blob.move(self.velocity, dt)
            blob.get_together(center)
            blob.bounce_from_boundaries(self.model.get_board_size())

        self.shoot_now = self.divide_now = False

    def set_velocity(self, v):
        self.velocity = v

    def shoot(self):
        self.shoot_now = True

    def __divide(self):
        if self.main_blob.get_weight() >= 32:
            self.main_blob.set_weight(int(self.main_blob.get_weight() / 2))
            blob = Blob(self.main_blob.get_position(), self.player_id)
            blob.set_weight(self.main_blob.get_weight())
            self.blobs.append(blob)
            self.model.blobs.append(blob)
            blob.force = vector.multiply(vector.normalize(self.velocity), 150)

    def divide(self):
        self.divide_now = True

    def get_blobs(self):
        return self.blobs

    def get_largest_blob(self):
        return self.main_blob.get_proxy()

    def get_average_position(self):
        position_sum = reduce(lambda x, y: vector.add(x, y), [vector.multiply(blob.get_position(), blob.get_weight()) for blob in self.blobs])
        return vector.divide(position_sum, sum([blob.get_weight() for blob in self.blobs]))

    def get_total_cell_radius(self):
        return sum([blob.get_radius() for blob in self.blobs])
