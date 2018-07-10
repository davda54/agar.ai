import math
from functools import reduce

import vector
from blob import Blob


# contains all blobs that makes up a player and manipulates them
class BlobFamily():
    def __init__(self, model, player_id):
        self.model = model
        self.blobs = [] # better use some heap to quickly get the largest blob
        self.main_blob = None
        self.player_id = player_id
        self.velocity = (0,0)
        self.shoot_now = False
        self.divide_now = False
        self.divide_countdown = 0

    def update(self, dt):
        if not self.is_alive(): return

        if self.divide_now:
            self.__divide()

        if self.should_stay_divided():
            self.divide_countdown -= dt

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

    def add_blob(self, blob):
        self.blobs.append(blob)
        self.select_main_blob()

    def select_main_blob(self):
        if len(self.blobs) == 0: self.main_blob = None
        else: self.main_blob = max(self.blobs, key=lambda blob: blob.get_weight())

    def remove(self, blob):
        self.blobs.remove(blob)
        if blob is self.main_blob:
            self.select_main_blob()

    def __divide(self):
        has_divided = False
        for blob in self.blobs[:]:
            if blob.get_weight() >= 32 and len(self.blobs) < 16:
                blob.set_weight(int(blob.get_weight() / 2))
                position = vector.add(blob.get_position(), vector.multiply(self.velocity, blob.get_radius()*2))
                new_blob = Blob(position, self.player_id, self)
                new_blob.set_weight(blob.get_weight())
                self.blobs.append(new_blob)
                self.model.blobs.append(new_blob)
                new_blob.force = vector.multiply(vector.normalize(self.velocity), 200)

                has_divided = True

        if has_divided: self.divide_countdown = max(20, self.get_total_cell_radius() * 0.2)

    def divide(self):
        self.divide_now = True

    def should_stay_divided(self):
        return self.divide_countdown > 0

    def get_blobs(self):
        return self.blobs

    def get_largest_blob(self):
        if self.main_blob is None: return None
        else: return self.main_blob.get_proxy()

    def get_average_position(self):
        position_sum = reduce(lambda x, y: vector.add(x, y), [vector.multiply(blob.get_position(), blob.get_weight()) for blob in self.blobs])
        return vector.divide(position_sum, sum([blob.get_weight() for blob in self.blobs]))

    def get_total_cell_radius(self):
        return sum([blob.get_radius() for blob in self.blobs]) / math.sqrt(len(self.blobs))

    def is_alive(self):
        return len(self.blobs) > 0