import pygame as pg
import pyautogui
import os
from gui_items import Card, DropZone, HandZone

WIDTH = 1920
HEIGHT = 1080

BLACK = (55, 55, 55)
WHITE = (255, 255, 255)
LIGHT_GREY = (191, 191, 191)
RED = (255, 0, 0)

pg.init()


def load_resource(filename):
    return os.path.join('resources', filename)


def load_image(filename):
    return pg.image.load(load_resource(filename))


screen = pg.display.set_mode((WIDTH, HEIGHT))
FONT = pg.font.Font(load_resource("JetBrainsMono-Medium.ttf"), 12)
BACKGROUND = pg.image.load(load_resource("gameboard.jpg"))
pg.display.set_caption("DX7 testing GUI")


def main():
    run = True
    clock = pg.time.Clock()
    drop_c = DropZone((750, 245))
    drop_r = DropZone((175, 665))
    drop_l = DropZone((1330, 665))
    hand = HandZone((685, 850))
    hover_items = (drop_c, drop_r, drop_l, hand)
    gui_items = hover_items

    while run:
        # check the mouse position for all hoverable items
        mouse_pos = pg.mouse.get_pos()
        for item in hover_items:
            item.check_mouse(mouse_pos)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

        screen.blit(BACKGROUND, (0, 0))
        for item in gui_items:
            item.draw(screen)
        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()





