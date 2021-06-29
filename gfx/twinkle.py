import pygame as pg
from typing import Tuple


class TwinklePoint:
    def __init__(self, coor: Tuple[int, int], direction: Tuple[int, int]):
        self.origin = pg.math.Vector2(coor)
        self.point = pg.math.Vector2(coor)
        self.direction = pg.math.Vector2(direction).normalize()
        self.max = 50
        self.step = 2

    def move(self):
        self.point += self.direction * self.step

        length = self.origin.distance_to(self.point)
        if (length < self.step) or (length > self.max):
            self.direction.rotate_ip(180)

    def draw(self, surf: pg.Surface):
        self.move()
        pg.draw.circle(surf, (255, 255, 255), self.point, 1)
        pg.draw.line(surf, (255, 255, 255), self.point, self.origin, 1)


class TwinkleStar:
    def __init__(self, coor: Tuple[int, int]):
        point_directions = ((1, 0), (0, 1), (-1, 0), (0, -1),
                            (1, 1), (1, -1), (-1, -1), (-1, 1))
        self.points = [TwinklePoint(coor, direc) for direc in point_directions]

    def draw(self, surf: pg.Surface):
        for point in self.points:
            point.draw(surf)







