import pygame as pg
import sys
import os
from gui_items import (DiscardSpace, DropZone, HandZone, DrawSpace,
                       MessageButton, CenterText)
from gfx import ScreenFlasher, GfxManager, EyeAnimation
import argparse
import menu
from random import randrange
from socks import Client
import cProfile as profile


parser = argparse.ArgumentParser(description='Main script for piece')
parser.add_argument('-name', help='username for debug and logging purposes', default=f"USER {randrange(0, 100000)}")
parser.add_argument('--local', action='store_true',
                    help='run the gui in single player setup')
parser.add_argument('--fullscreen', action='store_true', help='run the gui in a fullscreen display')
parser.add_argument('--audio', action='store_true', help='connect the audio engine to this client instance')
parser.add_argument('--admin', action='store_true',
                    help="When the player designated as 'ADMIN' exits, the server will restart")
parser.add_argument('--nogui', action='store_true')

args = parser.parse_args()

USERNAME = args.name
AUDIO = args.audio
LOCAL = args.local
ADMIN = args.admin
FULLSCREEN = args.fullscreen

if not args.nogui:
    menu_opts = menu.menu()

    USERNAME = menu_opts["username"]
    AUDIO = menu_opts["audio"]
    LOCAL = menu_opts["local"]
    ADMIN = menu_opts["admin"]
    FULLSCREEN = menu_opts["fullscreen"]

if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass  # Windows XP doesn't support monitor scaling, so just do nothing.

if not LOCAL:
#    client = Client(USERNAME, ip="172.104.21.51")
    client = Client(USERNAME, ip="127.0.0.1")

else:
    AUDIO = True

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


def set_content(items, content: tuple, gfxman: GfxManager):
    if AUDIO:
        audio.input(content[0:3])
        audio_status = audio.check_status()  # will this be called twice for the user who sends a card?
        gfxman.input(audio_status)
        if not LOCAL:
            client.gfx_update(audio_status)
    for i, item in enumerate(items):
        item.set_content(content[i])


def end_turn_update(gui_items, gfxman: GfxManager):
    # updates the audio manager when cards are dropped
    content = get_content(gui_items)
    if AUDIO:
        audio.input(content[0:3])
        audio_status = audio.check_status()
        gfxman.input(audio_status)
    if not LOCAL:
        client.end_turn(content)



def end_turn_reactivate(reac_card: int, zone_num: int, gfxman: GfxManager):
    # reactivate the selected card
    if AUDIO:
        audio.force_input(reac_card, zone_num)
        gfxman.input(audio.check_status())
    if not LOCAL:
        client.end_turn_reactivate(reac_card, zone_num)


def check_screen_flash(card_num: int, sf: ScreenFlasher):
    if card_num == 26:
        sf.init_color((11, 82, 3))
    elif card_num == 22:
        sf.init_color((141, 252, 243))
    elif card_num == 21:
        sf.init_color((166, 0, 0))


def quit_all():
    if AUDIO:
        audio.close()
    quit()


if FULLSCREEN:
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
else:
    screen = pg.display.set_mode((WIDTH, HEIGHT))


FONT = pg.font.Font(load_resource("JetBrainsMono-Medium.ttf"), 12)
BACKGROUND = pg.image.load(load_resource("gameboard.jpg")).convert()
pg.display.set_caption(f"ALTAR CLIENT username = {USERNAME}")

if AUDIO:
    audio = AudioManager()


def main():
    clock = pg.time.Clock()

    zone_coors = ((750, 245), (175, 665), (1330, 665))

    drop_c = DropZone(zone_coors[0])
    drop_r = DropZone(zone_coors[1])
    drop_l = DropZone(zone_coors[2])
    hand = HandZone((685, 850))
    discard = DiscardSpace((50, 50))
    draw = DrawSpace((WIDTH - 150, 50))
    debug_text = CenterText("Please wait for the ADMIN player to initiate the piece", (960, 50), FONT)

    # GUI items that have get and set methods
    getset_items = (drop_c, drop_r, drop_l, draw)

    # All items that track mouse movement
    hover_items = (discard, hand) + getset_items
    # All GUI items
    gui_items = hover_items + (debug_text,)

    admin_btns = None

    if ADMIN:
        # buttons only viewable by those with admin designation
        quit_btn = MessageButton("QUIT", (50, 400), client.send_quit, FONT)
        start_btn = MessageButton("START", (50, 350), client.send_start, FONT)
        admin_btns = (quit_btn, start_btn)
        gui_items += admin_btns

        debug_text.change_msg("Press START when all users have joined.")

    # GFX generators
    screen_flasher = ScreenFlasher(screen)
    eye_anim = EyeAnimation()
    if LOCAL:
        eye_anim.play()

    gfx_man = GfxManager(zone_coors)
    gfx_gens = (gfx_man, screen_flasher, eye_anim)

    gui_items += gfx_gens

    held_card = None

    # wait for the server to send the start message
    piece_started = False

    run = True

    if LOCAL:
        debug_text.change_msg("RUNNING IN LOCAL MODE")
        piece_started = True

    # MAIN GAMELOOP
    while run:

        # check the mouse position for all hoverable items
        mouse_pos = pg.mouse.get_pos()
        for item in hover_items:
            item.check_mouse(mouse_pos)
            if ADMIN:
                for btn in admin_btns:
                    btn.check_mouse(mouse_pos)
        if held_card:
            held_card.check_mouse(mouse_pos)

        # check for key inputs
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_all()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    if ADMIN:
                        for btn in admin_btns:
                            btn.try_click()
                    if piece_started:
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
                                # check if the card was successfully dropped
                                if result:
                                    # for certain cards, fill the screen
                                    if type(item) == DropZone:
                                        check_screen_flash(held_card.id_num, screen_flasher)
                                    held_card = None
                                    end_turn_update(getset_items, gfx_man)
                                    break
                elif (event.button == 3) and not held_card:  # right click
                    for i, item in enumerate(getset_items):
                        active_card = item.try_right_click()
                        if active_card:
                            check_screen_flash(active_card, screen_flasher)
                            end_turn_reactivate(active_card, i, gfx_man)

        # check for input from the server
        if not LOCAL:
            client_msg = client.listen()
            if client_msg:
                if client_msg["method"] == 'update':
                    if not piece_started:
                        piece_started = True
                        eye_anim.play()
                    debug_text.change_msg(client_msg['current_player'] + "'s turn")
                    set_content(getset_items, client_msg["content"], gfx_man)
                elif client_msg["method"] == "reactivate":
                    debug_text.change_msg(client_msg['current_player'] + "'s turn")
                    card_num = client_msg["content"][0]
                    zone_num = client_msg['content'][1]
                    if AUDIO:
                        audio.force_input(card_num, zone_num)
                        gfx_man.input(audio.check_status())
                elif (client_msg["method"] == "new_user") and ADMIN:
                    debug_text.append(f"  New user {client_msg['name']}")
                elif (client_msg["method"] == "gfx_update") and not AUDIO:
                    gfx_man.input(client_msg["content"])

                elif client_msg["method"] == 'quit':
                    quit_all()

        # draw everything and finish the loop
        screen.blit(BACKGROUND, (0, 0))
        for item in gui_items:
            item.draw(screen)
        if held_card:
            held_card.draw(screen)
        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    profile.run('main()')
