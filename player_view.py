import math

import vector
from abstract_view import AbstractView
from gameboard_view import GameboardView


class PlayerView(AbstractView):
    def __init__(self, screen, model, blob_family, player_radius):
        super().__init__(screen, model)
        self.center_blob_family = blob_family
        self.player_radius = player_radius

        self.backup_view = GameboardView(screen, model)

    def render(self):
        if not self.center_blob_family.is_alive():
            self.backup_view.render()
            return

        self.__set_resize_ratio()
        self.__set_resize_offset()

        super().render()

    def _get_resize_ratio(self):
        return self.resize_ratio

    def _get_resize_offset(self):
        return self.resize_offset

    def __set_resize_ratio(self):
        self.resize_ratio = self.player_radius/max(20, 7*math.pow(self.center_blob_family.get_total_cell_radius(), 0.4))

    def __set_resize_offset(self):
        screen_center = vector.divide(self.screen.get_size(), 2)
        scale_position = vector.multiply(self.center_blob_family.get_largest_blob().get_position(), self._get_resize_ratio())
        self.resize_offset = vector.substract(screen_center, scale_position)

    def _fits_on_screen(self, item):
        right, bottom = self._map_coord_to_screen(vector.add(item.get_position(), (item.get_radius(), item.get_radius())))
        left, top = self._map_coord_to_screen(vector.substract(item.get_position(), (item.get_radius(), item.get_radius())))
        screen_size = self.screen.get_size()

        return left >= 0 and top >= 0 and right >= screen_size[0] and bottom >= screen_size[1]
