import pygame
from pygame import gfxdraw

import vector
from entities.abstract_blob import AbstractBlob
from entities.blob import Blob
from entities.large_pellet import LargePellet
from entities.pellet import Pellet
from parameters import *


class AbstractView:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        self.font = pygame.font.SysFont('Consolas Bold', 32)
        self.id_to_col = {}

    def render(self):
        self.screen.lock()

        self.screen.fill(VIEW_BACKGROUND_COLOR)
        self._draw_rect((0,0), self.model.get_board_size(), VIEW_BORDER_COLOR)

        for item in self.model.get_items():
            if isinstance(item, AbstractBlob): self._draw_blob(item)
            elif isinstance(item, Pellet) or isinstance(item, LargePellet): self._draw_pellet(item)

        self.screen.unlock()

        self._render_text()

    def _render_text(self):
        for item in self.model.get_items():
            if isinstance(item, Blob): self._draw_weight(item)

    def _draw_blob(self, blob):
        if not self._fits_on_screen(blob): return

        color = self._get_unique_color(blob.get_player_id())
        self._draw_circle(blob.get_position(), blob.get_radius(), color)


    def _draw_pellet(self, pellet):
        if not self._fits_on_screen(pellet): return

        if isinstance(pellet, LargePellet):
            self._draw_circle(pellet.get_position(), pellet.get_radius(), VIEW_LARGE_PELLET_COLOR)
        else:
            self._draw_circle(pellet.get_position(), pellet.get_radius(), VIEW_SMALL_PELLET_COLOR)

    def _draw_weight(self, blob):
        if blob.is_main_blob():
            col = (255,255,255)
        else:
            col = self._get_unique_color(blob.get_player_id())
            col = col + pygame.Color(160,160,160,255)

        self._draw_centered_text(str(blob.get_weight()), blob.get_position(), col)

    def _draw_centered_text(self, text, pos, col):
        textsurface = self.font.render(text, ANTIALIASING, col)

        size = vector.divide(self.font.size(text), 2)
        mapped_pos = vector.substract(self._map_coord_to_screen(pos), size)

        x = int(mapped_pos[0] + 1 + 0.5)
        y = int(mapped_pos[1] + 1 + 0.5)

        self.screen.blit(textsurface, (x,y))

    # draw circle in the board coordinates onto the screen coordinates
    def _draw_circle(self, pos, r, col):
        mapped_pos = self._map_coord_to_screen(pos)

        x = int(mapped_pos[0] + 0.5)
        y = int(mapped_pos[1] + 0.5)
        r = int(r*self._get_resize_ratio() + 0.5)

        if ANTIALIASING: pygame.gfxdraw.aacircle(self.screen, x, y, r, col)
        pygame.gfxdraw.filled_circle(self.screen, x, y, r, col)

    # draw rectangle edge in the board coordinates onto the screen coordinates
    def _draw_rect(self, pos, size, col):
        mapped_pos = self._map_coord_to_screen(pos)
        mapped_size = (size[0]*self._get_resize_ratio(), size[1]*self._get_resize_ratio())

        l = int(mapped_pos[0] + 0.5)
        r = int(mapped_pos[1] + 0.5)
        w = int(mapped_size[0] + 0.5)
        h = int(mapped_size[1] + 0.5)

        pygame.gfxdraw.rectangle(self.screen, pygame.Rect(l,r,w,h), col)

    def _map_coord_to_screen(self, coord):
        return vector.add(vector.multiply(coord, self._get_resize_ratio()), self._get_resize_offset())

    def _get_resize_ratio(self):
        raise NotImplementedError('subclasses must override _get_resize_ratio()!')

    def _get_resize_offset(self):
        raise NotImplementedError('subclasses must override _get_resize_offset()!')

    def _fits_on_screen(self, item):
        raise NotImplementedError('subclasses must override _fits_on_screen()!')

    # uses golden angle to return the most distant hues for different consecutive ns
    def _get_unique_color(self, n):
        if n in self.id_to_col:
            return self.id_to_col[n]

        hue = n*137.5077640500378546463487 #phi

        color = pygame.Color(0,0,0,0)
        color.hsva = (hue % 360.0, 100, 100, 90)
        self.id_to_col[n] = color
        return color