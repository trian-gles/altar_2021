import pygame as pg
from .gfx_base import GfxBase
import os
from random import randrange, choice


class SmokeManager(GfxBase):
    def __init__(self, x_min, x_max, y_min, y_max):
        super().__init__(x_min, x_max, y_min, y_max)
        SmokePart.convert_imgs()

    def update(self):
        # check to see if to add a new particle or to remove an old one
        if randrange(0, 4) == 0:
            if self.parts:
                self.parts.pop(0)
        elif randrange(0, 4) in (1, 2):
            if len(self.parts) < 20 and self.run:
                self.spawn_part(SmokePart)


class SmokePart:
    filenames = ["smoke_" + str(i + 1) + ".PNG" for i in range(4)]
    file_obs = [pg.image.load(os.path.join('resources/particles/smoke_img', filename)) for filename in filenames]

    def __init__(self, coor):
        self.vel = pg.math.Vector2((0, -1))
        self.coor = pg.math.Vector2(coor)

        self.img = choice(self.file_obs)
        self.alpha = 255

    @classmethod
    def convert_imgs(cls):
        cls.file_obs = [img.convert_alpha() for img in cls.file_obs]

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
    import cProfile
    dm = SmokeManager(0, 200, 300, 350)
    dm.start()
    cProfile.run("gfx_tester.main(dm)")

# without : 2654    2.389    0.001    2.389    0.001 {method 'blit' of 'pygame.Surface' objects}
# with      2654    0.788    0.000    0.788    0.000 {method 'blit' of 'pygame.Surface' objects}