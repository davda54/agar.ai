import vector
from abstract_view import AbstractView


class PlayerView(AbstractView):
    def __init__(self, screen, model, blob_family, player_radius):
        super().__init__(screen, model)
        self.center_blob_family = blob_family
        self.player_radius = player_radius

    def render(self):
        self.__set_resize_ratio()
        self.__set_resize_offset()

        super().render()

    def _get_resize_ratio(self):
        return self.resize_ratio

    def _get_resize_offset(self):
        return self.resize_offset

    def __set_resize_ratio(self):
        self.resize_ratio = self.player_radius/self.center_blob_family.get_total_cell_radius()

    def __set_resize_offset(self):
        screen_center = vector.divide(self.screen.get_size(), 2)
        scale_position = vector.multiply(self.center_blob_family.get_average_position(), self._get_resize_ratio())
        self.resize_offset = vector.substract(screen_center, scale_position)

    def _fits_on_screen(self, item):
        return True