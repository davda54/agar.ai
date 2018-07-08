import pygame
from pygame import gfxdraw

from blob import Blob
from pellet import Pellet


# renders the environment
class View:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model

        self.__set_resize_ratios()

    def render(self):
        self.screen.lock()

        self.screen.fill((0,0,0))
        self.__draw_rect((0,0), self.model.get_board_size(), (128,128,128))

        for item in self.model.get_items():
            if isinstance(item, Blob): self.__draw_blob(item)
            elif isinstance(item, Pellet): self.__draw_pellet(item)

        self.screen.unlock()

    def __draw_blob(self, blob):
        color = self.__get_unique_color(blob.get_player_id())
        self.__draw_circle(blob.get_position(), blob.get_radius(), color)

    def __draw_pellet(self, pellet):
        shade = 64 + pellet.get_bonus_weight()*32
        self.__draw_circle(pellet.get_position(), 2, (shade,shade,shade))

    # draw circle in the board coordinates onto the screen coordinates
    def __draw_circle(self, pos, r, col):
        mapped_pos = self.__map_coord_to_screen(pos)

        x = int(mapped_pos[0] + 0.5)
        y = int(mapped_pos[1] + 0.5)
        r = int(r + 0.5)

        pygame.gfxdraw.aacircle(self.screen, x, y, r, col)
        pygame.gfxdraw.filled_circle(self.screen, x, y, r, col)

    # draw rectangle edge in the board coordinates onto the screen coordinates
    def __draw_rect(self, pos, size, col):
        mapped_pos = self.__map_coord_to_screen(pos)
        mapped_size = (size[0]*self.resize_ratio, size[1]*self.resize_ratio)

        l = int(mapped_pos[0] + 0.5)
        r = int(mapped_pos[1] + 0.5)
        w = int(mapped_size[0] + 0.5)
        h = int(mapped_size[1] + 0.5)

        pygame.gfxdraw.rectangle(self.screen, pygame.Rect(l,r,w,h), col)

    def __map_coord_to_screen(self, coord):
        return (coord[0] * self.resize_ratio + self.resize_offset[0], coord[1] * self.resize_ratio + self.resize_offset[1])

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

    # uses golden angle to return the most distant hues for different consecutive ns
    def __get_unique_color(self, n):
        hue = n*137.5077640500378546463487

        color = pygame.Color(0,0,0,0)
        color.hsva = (hue % 360.0, 100, 100, 100)
        return color