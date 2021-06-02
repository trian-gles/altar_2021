import pygame as pg
from random import randrange


class DiamondManager:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.diamonds = []
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def spawn_part(self):
        x = randrange(self.x_min, self.x_max)
        y = randrange(self.y_min, self.y_max)
        self.diamonds.append(Diamond((x, y)))

    def reprocess(self):
        # check to see if to add a new particle or to remove an old one
        if randrange(0, 4) == 0:
            if self.diamonds:
                self.diamonds.pop(0)
        elif randrange(0, 4) in (1, 2):
            if len(self.diamonds) < 40:
                self.spawn_part()

    def draw(self, surf: pg.Surface):
        self.reprocess()
        for d in self.diamonds:
            d.draw(surf)


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
