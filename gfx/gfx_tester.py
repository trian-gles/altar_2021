import pygame as pg
import sys

if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass # Windows XP doesn't support monitor scaling, so just do nothing.

pg.init()
screen = pg.display.set_mode((1920, 1080))


def main(tested_item):
    step = 0
    while step < 200:
        clock = pg.time.Clock()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
        screen.fill((0, 0, 0))
        tested_item.draw(screen)
        pg.display.update()
        step += 1
        clock.tick(30)