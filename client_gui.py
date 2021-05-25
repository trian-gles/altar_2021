import pygame as pg
import pyautogui
import os
from gui_items import DiscardSpace, DropZone, HandZone, DrawSpace, MessageButton
import argparse
from random import randrange
from socks import Client


parser = argparse.ArgumentParser(description='Main script for piece')
parser.add_argument('-name', help='username for debug and logging purposes', default=f"USER {randrange(0, 100000)}")
parser.add_argument('--local', action='store_true',
                    help='run the gui in single player setup')
parser.add_argument('--fullscreen', action='store_true', help='run the gui in a fullscreen display')
parser.add_argument('--audio', action='store_true', help='connect the audio engine to this client instance')
parser.add_argument('--admin', action='store_true',
                    help="When the player designated as 'ADMIN' exits, the server will restart")

args = parser.parse_args()

USERNAME = args.name
AUDIO = args.audio
LOCAL = args.local
ADMIN = args.admin
FULLSCREEN = args.fullscreen

if not LOCAL:
    client = Client(USERNAME)

if AUDIO:
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
    return content


def set_content(items, content: tuple):
    if AUDIO:
        audio.input(content[0:3])
    for i, item in enumerate(items):
        item.set_content(content[i])


def end_turn(gui_items):
    # updates the audio manager when cards are dropped
    content = get_content(gui_items)
    if AUDIO:
        audio.input(content[0:3])
    if not LOCAL:
        client.end_turn(content)


def quit_all():
    if AUDIO:
        audio.close()
    if ADMIN and not LOCAL:
        client.send_quit()
    quit()


if FULLSCREEN:
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
else:
    screen = pg.display.set_mode((WIDTH, HEIGHT))


FONT = pg.font.Font(load_resource("JetBrainsMono-Medium.ttf"), 12)
BACKGROUND = pg.image.load(load_resource("gameboard.jpg"))
pg.display.set_caption(f"ALTAR CLIENT username = {USERNAME}")

if AUDIO:
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

    # GUI items that have get and set methods
    getset_items = (drop_c, drop_r, drop_l, draw)

    # All items that track mouse movement
    hover_items = (discard, hand) + getset_items

    if ADMIN:
        # buttons only viewable by those with admin designation
        quit_btn = MessageButton("QUIT", (50, 350), quit_all, FONT)
        start_btn = MessageButton("START", (50, 400), client.send_start, FONT)
        hover_items += (quit_btn, start_btn)

    # All GUI items
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
                quit_all()
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
                            end_turn(getset_items)
                            break

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    set_content(getset_items, ((3, None, 0), (None, None, 2), (None, 1, 4), (5, 6)))

        if not LOCAL:
            client_msg = client.listen()
            if client_msg:
                if client_msg["method"] == 'update':
                    print(client_msg['content'])
                    print(client_msg['current_player'])
                    set_content(getset_items, client_msg["content"])

        screen.blit(BACKGROUND, (0, 0))
        for item in gui_items:
            item.draw(screen)
        if held_card:
            held_card.draw(screen)
        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()





