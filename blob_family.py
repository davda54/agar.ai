from functools import reduce

import vector


# contains all blobs that makes up a player and manipulates them
class BlobFamily():
    def __init__(self, model, blob, player_id):
        self.model = model
        self.blobs = [blob] # better use some heap to quickly get the largest blob
        self.main_blob = blob
        self.player_id = player_id
        self.velocity = (0,0)
        self.shoot = False
        self.divide = False

    def update(self, dt):
        for blob in self.blobs:
            blob.move(self.velocity, dt)
            blob.bounce_from_boundaries(self.model.get_board_size())

    def set_velocity(self, v):
        self.velocity = v

    def shoot(self):
        self.shoot = True

    def divide(self):
        self.divide = True

    def get_blobs(self):
        return self.blobs

    def get_largest_blob(self):
        return self.main_blob.get_proxy()

    def get_average_position(self):
        sum = reduce(lambda x, y: vector.add(x, y), [blob.get_position() for blob in self.blobs])
        return vector.divide(sum, len(self.blobs))

    def get_total_cell_radius(self):
        return sum([blob.get_radius() for blob in self.blobs])
