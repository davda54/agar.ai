import vector
from abstract_controller import AbstractController

# AI that just goes to the middle
class MiddleAIController(AbstractController):
    def update(self):
        position = self.manipulator.get_blob_family_positions_and_weights()[0][0]
        middle = vector.divide(self.manipulator.get_board_size(), 2)

        self.manipulator.set_velocity(vector.substract(middle, position))
