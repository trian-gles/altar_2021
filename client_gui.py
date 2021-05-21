import pygame as pg
import pyautogui
import os
from gui_items import DiscardSpace, DropZone, HandZone, DrawSpace
from audio import AudioManager

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


def get_content(items):
    content = tuple(map(lambda item: item.return_content(), items))
    audio.input(content[0:3])
    return content


def set_content(items, content: list):
    for i, item in enumerate(items):
        item.set_content(content[i])


screen = pg.display.set_mode((WIDTH, HEIGHT))
FONT = pg.font.Font(load_resource("JetBrainsMono-Medium.ttf"), 12)
BACKGROUND = pg.image.load(load_resource("gameboard.jpg"))
pg.display.set_caption("DX7 testing GUI")

audio = AudioManager()


def main():
    run = True
    clock = pg.time.Clock()
    drop_c = DropZone((750, 245))
    drop_r = DropZone((175, 665))
    drop_l = DropZone((1330, 665))
    hand = HandZone((685, 850))
    discard = DiscardSpace((50, 50))
    draw = DrawSpace((WIDTH - 150, 50))
    hover_items = (drop_c, drop_r, drop_l, discard, hand, draw)
    gui_items = hover_items
    held_card = None

    while run:
        # check the mouse position for all hoverable items
        mouse_pos = pg.mouse.get_pos()
        for item in hover_items:
            item.check_mouse(mouse_pos)
        if held_card:
            held_card.check_mouse(mouse_pos)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                # try to pick up a card
                if not held_card:
                    for item in hover_items:
                        new_card = item.try_click()
                        if new_card:
                            held_card = new_card
                # try to drop a card
                else:
                    for item in hover_items:
                        result = item.drop_card(held_card)
                        if result:
                            # check if the card was successfully dropped
                            held_card = None
                            break

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    get_content(gui_items)

        screen.blit(BACKGROUND, (0, 0))
        for item in gui_items:
            item.draw(screen)
        if held_card:
            held_card.draw(screen)
        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()





