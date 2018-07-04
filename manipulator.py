# wrapper used by controllers to manipulate a family of blobs according to the state of the environment
class Manipulator:
    def __init__(self, blob_family, model):
        self.blob_family = blob_family
        self.model = model

    def set_velocity(self, v_x, v_y):
        self.blob_family.set_velocity(v_x, v_y)

    def shoot(self):
        self.blob_family.shoot()

    def divide(self):
        self.blob_family.divide()

    def get_other_items(self):
        blobs_in_family = self.blob_family.get_blobs()
        return [i.get_proxy() for i in self.model.get_items() if i not in blobs_in_family]

    def get_blob_positions_and_weights(self):
        return [(b.get_position(), b.get_weight()) for b in self.blob_family.get_blobs()]

    def get_board_size(self):
        return self.model.get_board_size()