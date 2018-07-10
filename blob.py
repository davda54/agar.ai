import vector
from abstract_blob import AbstractBlob


class Blob(AbstractBlob):
    INIT_WEIGHT = 20

    def __init__(self, model, position, player_id, blob_family, force=(0,0)):
        super().__init__(model, position, player_id, self.INIT_WEIGHT, force)
        self.blob_family = blob_family

    def get_together(self, center):
        difference = vector.multiply(vector.substract(center, self.position), 0.015)
        self.force = vector.add(self.force, difference)

    def repel_from_each_other(self, blob):
        difference = vector.substract(blob.get_position(), self.position)
        distance = vector.norm(difference)
        strength = distance - self.radius - blob.get_radius()

        self.force = vector.add(self.force, vector.multiply(difference,  0.1*strength/distance - 0.01))
        blob.force = vector.add(blob.force, vector.multiply(difference, -0.1*strength/distance + 0.01))

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