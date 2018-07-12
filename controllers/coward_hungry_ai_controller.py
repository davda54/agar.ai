import vector
from abstract_controller import AbstractController
from blob import BlobProxy
from bullet_blob import BulletBlobProxy
from large_pellet import LargePelletProxy
from parameters import *
from pellet import PelletProxy


# AI that hunts the closest thing
class coward_hungry_ai_controller(AbstractController):
    def update(self):
        if not self.manipulator.is_alive(): return

        blob = self.manipulator.get_largest_blob()

        others = self.manipulator.get_other_items()

        best_target = None

        for item in others:
            distance = vector.squared_distance(blob.get_position(), item.get_position())

            if isinstance(item, PelletProxy) or isinstance(item, LargePelletProxy):
                value = item.get_bonus_weight()**2 / distance
                run_away = False
            elif isinstance(item, BlobProxy) or isinstance(item, BulletBlobProxy):
                if item.get_weight()*(BLOB_WEIGHT_RATIO_TO_EAT*1.1) > blob.get_weight():
                    value = item.get_weight()**2 / distance
                    run_away = True
                elif blob.get_weight()*BLOB_WEIGHT_RATIO_TO_EAT > item.get_weight():
                    value = item.get_weight()**2 / distance
                    run_away = False
                else:
                    continue
            else:
                continue

            if best_target is None or value > best_target[1]:
                best_target = (item, value, run_away)

        if best_target is None:
            position = self.manipulator.get_blob_family_positions_and_weights()[0][0]
            middle = vector.divide(self.manipulator.get_board_size(), 2)
            self.manipulator.set_velocity(vector.substract(middle, position))
        elif best_target[2]:
            self.manipulator.set_velocity(vector.normalize(vector.substract(blob.get_position(), best_target[0].get_position())))
        else:
            self.manipulator.set_velocity(vector.normalize(vector.substract(best_target[0].get_position(), blob.get_position())))