import vector

# wrapper used by controllers to manipulate a family of blobs according to the state of the environment
class Manipulator:
    def __init__(self, blob_family, model):
        self.blob_family = blob_family
        self.model = model

    def set_velocity(self, v):
        if vector.squared_norm(v) > 1:
            v = vector.normalize(v)

        self.blob_family.set_velocity(v)

    def shoot(self):
        self.blob_family.shoot()

    def divide(self):
        self.blob_family.divide()

    def get_other_items(self):
        blobs_in_family = self.blob_family.get_blobs()
        position = self.blob_family.get_average_position()
        radius = self.blob_family.get_total_cell_radius()

        return [i.get_proxy() for i in self.model.get_items() if i not in blobs_in_family and vector.squared_distance(position, i.get_position()) < (13*radius)**2]

    def get_blob_family_positions_and_weights(self):
        return [(b.get_position(), b.get_weight()) for b in self.blob_family.get_blobs()]

    def get_largest_blob(self):
        return self.blob_family.get_largest_blob()

    def get_board_size(self):
        return self.model.get_board_size()

    def is_alive(self):
        return self.blob_family.is_alive()