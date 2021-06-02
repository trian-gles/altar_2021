import pygame as pg
import sys

if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass # Windows XP doesn't support monitor scaling, so just do nothing.


def main(tested_item):
    pg.init()
    screen = pg.display.set_mode((400, 400))
    while True:
        clock = pg.time.Clock()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
        screen.fill((0, 0, 0))
        tested_item.draw(screen)
        pg.display.update()
        clock.tick(30)