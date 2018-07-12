import vector
from controllers.abstract_controller import AbstractController

# AI that just goes to the middle
class middle_ai_controller(AbstractController):
    def update(self):
        if not self.manipulator.is_alive(): return

        position = self.manipulator.get_largest_blob().get_position()
        middle = vector.divide(self.manipulator.get_board_size(), 2)

        self.manipulator.set_velocity(vector.substract(middle, position))
