import pygame as pg
from random import randrange, getrandbits
import sys

if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass # Windows XP doesn't support monitor scaling, so just do nothing.


class BoltManager:
    def __init__(self, bounds: pg.rect):
        self.bounds = bounds
        self.bolts = []
        for _ in range(12):
            self.new_bolt()

    def reprocess(self):
        # check to see if to add a new bolt or to remove an old one
        if randrange(0, 4) == 0:
            if self.bolts:
                self.bolts.pop(0)
        elif randrange(0, 4) in (1, 2):
            self.new_bolt()

    def new_bolt(self):
        if len(self.bolts) < 20:
            new_bolt = Bolt(*self.rand_points())
            self.bolts.append(new_bolt)

    def rand_points(self):
        x = randrange(self.bounds.left, self.bounds.left + self.bounds.width)
        y = randrange(self.bounds.top, self.bounds.top + self.bounds.height)
        point_1 = (x, y)

        x_length = randrange(1, 100)
        y_length = randrange(1, 100)
        if getrandbits(1):
            x_length *= -1
        if getrandbits(1):
            y_length *= -1

        point_2 = (x + x_length, y + y_length)

        return point_1, point_2

    def draw(self, surf: pg.Surface):
        self.reprocess()
        for bolt in self.bolts:
            bolt.draw(surf)


class Bolt:
    def __init__(self, start: tuple, finish: tuple):
        self.color = (255, 255, 255)
        self.segment_num = 6
        self.primary_points = self.return_points(start, finish)
        self.second_points = self.get_sec_points(start, finish)
        self.all_points = self.combine_points(self.primary_points, self.second_points)

    def get_sec_points(self, start: tuple, finish: tuple):
        x_trans = randrange(-20, 20)
        y_trans = randrange(-20, 20)
        second_start = (start[0] + x_trans, start[1] + y_trans)
        second_finish = (finish[0] + x_trans, finish[1] + y_trans)
        return self.return_points(second_start, second_finish)

    def return_points(self, start: tuple, finish: tuple):
        slope = (start[0] - finish[0]) / (start[1] - finish[1])
        y_inter = ((start[0] * finish[1]) - (start[1] * finish[0])) / (start[0] - finish[0])

        x_start = start[0]
        x_end = finish[0]
        x_length = x_end - x_start
        segment_len = x_length / self.segment_num

        x_coors = [x_start + (segment_len * i) for i in range(self.segment_num)] + [x_end]
        points = [(x, x * slope + y_inter) for x in x_coors]
        return points

    def combine_points(self, prim_points, sec_points):
        all_points = []
        for i in range(len(prim_points)):
            all_points.append(prim_points[i])
            all_points.append(sec_points[i])

        return all_points

    def draw(self, surf: pg.Surface):

        pg.draw.lines(surf, self.color, False, self.all_points)


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((500, 500))
    bm_bounds = screen.get_rect()
    bm = BoltManager(bm_bounds)
    while True:
        clock = pg.time.Clock()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
        screen.fill((0, 0, 0))
        bm.draw(screen)
        pg.display.update()
        clock.tick(30)