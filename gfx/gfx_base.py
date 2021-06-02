import pygame as pg
from random import randrange


class GfxBase:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.parts = []
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def spawn_part(self, part: type):
        x = randrange(self.x_min, self.x_max)
        y = randrange(self.y_min, self.y_max)
        self.parts.append(part((x, y)))

    def update(self):
        pass

    def draw(self, surf: pg.Surface):
        self.update()
        for part in self.parts:
            part.draw(surf)