import vector
from abstract_controller import AbstractController

# AI that hunts the closest thing
class StupidHungryAIController(AbstractController):
    def update(self):
        position = self.manipulator.get_blob_family_positions_and_weights()[0][0]

        others = self.manipulator.get_other_items()
        closest = None

        for item in others:
            distance = vector.squared_distance(position, item.get_position())
            if closest is None or distance < closest[1]:
                closest = (item.get_position(), distance)

        self.manipulator.set_velocity(vector.normalize(vector.substract(closest[0], position)))