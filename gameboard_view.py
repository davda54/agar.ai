import vector
from abstract_view import AbstractView


# renders the environment
class GameboardView(AbstractView):
    def __init__(self, screen, model):
        super().__init__(screen, model)
        self.__set_resize_ratios()

    def __set_resize_ratios(self):
        board_size = self.model.get_board_size()
        screen_size = self.screen.get_size()

        width_ratio = screen_size[0] / board_size[0]
        height_ratio = screen_size[1] / board_size[1]

        if width_ratio < height_ratio:
            self.resize_ratio = width_ratio
            self.resize_offset = (0, (screen_size[1] - board_size[1]*self.resize_ratio) * 0.5)
        else:
            self.resize_ratio = height_ratio
            self.resize_offset = ((screen_size[0] - board_size[0]*self.resize_ratio) * 0.5, 0)

    def _draw_weight(self, blob):
        self._draw_centered_text(str(blob.get_weight()), vector.add(blob.get_position(), (0, -2*blob.get_radius())))

    def _get_resize_ratio(self):
        return self.resize_ratio

    def _get_resize_offset(self):
        return self.resize_offset

    def _fits_on_screen(self, item):
        return True

