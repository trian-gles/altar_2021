import pygame as pg
from random import randrange
from .gfx_base import GfxBase


class DustManager(GfxBase):
    def __init__(self, x_min, x_max, y_min, y_max):
        super(DustManager, self).__init__(x_min, x_max, y_min, y_max)

    def update(self):
        # check to see if to add a new particle or to remove an old one
        if randrange(0, 4) == 0:
            if self.parts:
                self.parts.pop(0)
        elif randrange(0, 4) in (1, 2):
            if (len(self.parts) < 40) and self.run:
                self.spawn_part(DustPart)


class DustPart:
    def __init__(self, coor):
        self.vel = pg.math.Vector2((0, -1))
        self.vel.rotate_ip(randrange(-20, 20))
        self.coor = pg.math.Vector2(coor)

    def move(self):
        self.coor += self.vel

    def draw(self, surf: pg.Surface):
        self.move()
        pg.draw.circle(surf, (255, 255, 255), self.coor, 1)


if __name__ == "__main__":
    import gfx_tester
    dm = DustManager(0, 200, 300, 350)
    dm.start()
    gfx_tester.main(dm)
