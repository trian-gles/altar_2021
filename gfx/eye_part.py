from .gfx_base import GfxBase
import pygame as pg
from random import randrange
import cProfile as profile


class EyeManager(GfxBase):
    def __init__(self, x_min, x_max, y_min, y_max):
        super().__init__(x_min, x_max, y_min, y_max)

    def update(self):
        # check to see if to add a new particle or to remove an old one
        if randrange(0, 4) == 0:
            if self.parts:
                self.parts.pop(0)
        elif randrange(0, 4) in (1, 2):
            if len(self.parts) < 10 and self.run:
                self.spawn_part(EyePart)


class EyePart:
    img = pg.image.load("particles/eye_part.png")

    def __init__(self, coor):
        self.vel = pg.math.Vector2((0, -1))
        self.coor = pg.math.Vector2(coor)
        self.alpha = 255

    def update(self):
        self.coor += self.vel
        self.alpha -= 2
        if self.alpha > 1:
            self.img.set_alpha(self.alpha)

    def draw(self, surf: pg.Surface):
        if self.alpha > 1:
            self.update()
            surf.blit(self.img, (self.coor.x, self.coor.y))


if __name__ == "__main__":
    import gfx_tester
    def main():
        dm = EyeManager(0, 200, 300, 350)
        dm.start()
        gfx_tester.main(dm)

    profile.run('main()')
