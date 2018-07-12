import vector
from abstract_controller import AbstractController

from large_pellet import LargePelletProxy
from pellet import PelletProxy

class stupid_hungry_ai_controller(AbstractController):
    # AI that hunts the closest thing
    def update(self):
        if not self.manipulator.is_alive(): return

        main_blob = self.manipulator.get_largest_blob()

        others = self.manipulator.get_other_items()
        closest = None

        for item in others:
            if isinstance(item, PelletProxy) or isinstance(item, LargePelletProxy):
                distance = vector.squared_distance(main_blob.get_position(), item.get_position())
                if closest is None or distance < closest[1]:
                    closest = (item.get_position(), distance)

        if closest is None:
            position = self.manipulator.get_largest_blob().get_position()
            middle = vector.divide(self.manipulator.get_board_size(), 2)
            self.manipulator.set_velocity(vector.substract(middle, position))
        else:
            self.manipulator.set_velocity(vector.normalize(vector.substract(closest[0], main_blob.get_position())))