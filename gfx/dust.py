import pygame as pg
from random import randrange


class DustManager:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.dust = []
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        for _ in range(12):
            self.spawn_part()

    def spawn_part(self):
        x = randrange(self.x_min, self.x_max)
        y = randrange(self.y_min, self.y_max)
        self.dust.append(DustPart((x, y)))

    def reprocess(self):
        # check to see if to add a new particle or to remove an old one
        if randrange(0, 4) == 0:
            if self.dust:
                self.dust.pop(0)
        elif randrange(0, 4) in (1, 2):
            if len(self.dust) < 40:
                self.spawn_part()

    def draw(self, surf: pg.Surface):
        self.reprocess()
        for d in self.dust:
            d.draw(surf)


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
    gfx_tester.main(dm)
