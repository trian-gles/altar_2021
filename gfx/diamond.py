import pygame as pg
from random import randrange
from .gfx_base import GfxBase


class DiamondManager(GfxBase):
    def __init__(self, x_min, x_max, y_min, y_max):
        super(DiamondManager, self).__init__(x_min, x_max, y_min, y_max)

    def update(self):
        # check to see if to add a new particle or to remove an old one
        if randrange(0, 4) == 0:
            if self.parts:
                self.parts.pop(0)
        elif randrange(0, 4) in (1, 2):
            if len(self.parts) < 40:
                self.spawn_part(Diamond)


class Diamond:
    def __init__(self, coor):
        self.size = 10
        self.coor = coor
        self.points = ()

    def compute_points(self):
        left = (self.coor[0] - self.size, self.coor[1])
        right = (self.coor[0] + self.size, self.coor[1])

        vert = self.size * 1.5
        top = (self.coor[0], self.coor[1] - vert)
        bottom = (self.coor[0], self.coor[1] + vert)
        self.points = (left, top, right, bottom)

    def update(self):
        if self.size > 0:
            self.size -= .5
        self.compute_points()

    def draw(self, surf: pg.Surface):
        self.update()
        if self.size > 0:
            pg.draw.polygon(surf, (255, 255, 255), self.points)


if __name__ == "__main__":
    import gfx_tester
    dm = DiamondManager(0, 200, 300, 350)
    gfx_tester.main(dm)
