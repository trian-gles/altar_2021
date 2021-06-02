import pygame as pg
import sys
from random import randrange

if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass # Windows XP doesn't support monitor scaling, so just do nothing.


class DustPart:
    def __init__(self):
        self.vel = randrange(0, )

    def move(self):
        pass

    def draw(self, surf: pg.Surface):
        self.move()


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((200, 200))
    while True:
        clock = pg.time.Clock()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
        screen.fill((0, 0, 0))
        pg.display.update()
        clock.tick(30)