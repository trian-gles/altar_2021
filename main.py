import sys
import os
from typing import Tuple, Optional, cast
import argparse
from random import randrange, seed

import pygame as pg
from pyo import Server

from gui_items import (DiscardSpace, DropZone, HandZone, DrawSpace,
                       MessageButton, CenterText, HelpHandler)
from gfx import ScreenFlasher, GfxManager, EyeAnimation, EndAnimation
from pg_menu import run_menu
from socks import Client, ProjectClient


pg.init()
# set up some type aliases
GetsetItems = Tuple[DropZone, DropZone, DropZone, DrawSpace]
DropZoneContent = Tuple[Optional[int], Optional[int], Optional[int]]
GuiContent = Tuple[DropZoneContent, DropZoneContent, DropZoneContent, Tuple[int]]
EMPTY_TUP = (None, None, None)
EMPTY_CONTENT = (EMPTY_TUP, EMPTY_TUP, EMPTY_TUP, None)


parser = argparse.ArgumentParser(description='Main script for piece')
parser.add_argument('-name', help='username for debug and logging purposes', default=f"USER {randrange(0, 100000)}")
parser.add_argument('--local', action='store_true',
                    help='run the gui in single player setup')
parser.add_argument('--ip', default="127.0.0.1")
parser.add_argument('--fullscreen', action='store_true', help='run the gui in a fullscreen display')
parser.add_argument('--audio', action='store_true', help='connect the audio engine to this client instance')
parser.add_argument('--admin', action='store_true',
                    help="When the player designated as 'ADMIN' exits, the server will restart")
parser.add_argument('--project', help="Run a projector for the audience", action='store_true')
parser.add_argument('--nogui', action='store_true')

args = parser.parse_args()

USERNAME = args.name
AUDIO = args.audio
LOCAL = args.local
ADMIN = args.admin
PROJECT = args.project
FULLSCREEN = args.fullscreen
IP = args.ip
GFX = True
DOWNSCALED = False

if not args.nogui:
    menu_opts = run_menu()

    USERNAME = menu_opts["username"]
    AUDIO = menu_opts["audio"]
    LOCAL = menu_opts["local"]
    ADMIN = menu_opts["admin"]
    PROJECT = menu_opts["project"]
    GFX = menu_opts["GFX"]
    FULLSCREEN = menu_opts["fullscreen"]
    IP = menu_opts["ip"]
    DOWNSCALED = menu_opts["downscale"]


if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass  # Windows XP doesn't support monitor scaling, so just do nothing.

if not LOCAL:
    if PROJECT:
        client = ProjectClient(USERNAME, ip=IP)
    else:
        client = Client(USERNAME, ip=IP)
else:
    AUDIO = True
    ADMIN = False

if AUDIO:
    from audio import AudioManager
    s = Server().boot()
    s.start()

WIDTH = 1920
HEIGHT = 1080

ZONE_COORS = ((750, 245), (175, 665), (1330, 665))

TWINK_LOCS = ((380, 120), (380, 450), (961, 630), (961, 960), (1537, 450), (1537, 120))

BLACK = (55, 55, 55)
WHITE = (255, 255, 255)
LIGHT_GREY = (191, 191, 191)
RED = (255, 0, 0)




def load_resource(filename: str) -> str:
    return os.path.join('resources', filename)


def load_image(filename: str) -> pg.image:
    return pg.image.load(load_resource(filename))


def get_content(items: GetsetItems) -> GuiContent:
    content = cast(GuiContent, tuple([item.return_content() for item in items]))
    return content


def set_content(items: GetsetItems, content: GuiContent, gfxman: GfxManager):
    if AUDIO:
        audio.input(content[0:3])
        audio_status = audio.check_status()  # will this be called twice for the user who sends a card?
        if GFX:
            gfxman.input(audio_status)
            gfxman.set_pattern_num(audio.current_pat_num)
        if not LOCAL:
            client.send_pattern_num(audio.current_pat_num)
            client.gfx_update(audio_status)
    for i, item in enumerate(items):
        item.set_content(content[i])


def end_turn_update(items: GetsetItems, gfxman: GfxManager):
    # updates the audio manager when cards are dropped
    content = get_content(items)
    if AUDIO:
        audio.input(content[0:3])
        audio_status = audio.check_status()
        if GFX:
            gfxman.input(audio_status)
            gfxman.set_pattern_num(audio.current_pat_num)
        if not LOCAL:
            client.send_pattern_num(audio.current_pat_num)
            if GFX:
                client.gfx_update(audio_status)
    if not LOCAL:
        client.end_turn(content)


def end_turn_reactivate(reac_card: int, zone_num: int, gfxman: GfxManager):
    # reactivate the selected card
    if AUDIO:
        audio.force_input(reac_card, zone_num)
        audio_status = audio.check_status()
        if GFX:
            gfxman.input(audio.check_status())

            gfxman.set_pattern_num(audio.current_pat_num)
        if not LOCAL:
            client.send_pattern_num(audio.current_pat_num)
            client.gfx_update(audio_status)
    if not LOCAL:
        client.end_turn_reactivate(reac_card, zone_num)


def check_screen_flash(card_num: int, sf: ScreenFlasher, sender=True):
    if not GFX:
        return
    if card_num == 26:
        sf.init_color((11, 82, 3))
    elif card_num == 22:
        sf.init_color((141, 252, 243))
    elif card_num == 21:
        sf.init_color((166, 0, 0))
    else:
        return
    if sender and not LOCAL:
        client.send_screen_flash(card_num)


def quit_all():
    if AUDIO:
        s.shutdown()
    quit()

scaling_factor = 1
if DOWNSCALED:
    scaling_factor = 2
temp_screen = pg.Surface((WIDTH, HEIGHT))
scaled_size = (WIDTH // scaling_factor, HEIGHT // scaling_factor)

if FULLSCREEN:
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN | pg.SCALED)

elif sys.platform == "darwin":
    screen = pg.display.set_mode(scaled_size)
else:
    screen = pg.display.set_mode(scaled_size, pg.RESIZABLE | pg.SCALED)


FONT = pg.font.Font(load_resource("JetBrainsMono-Medium.ttf"), 16)
BACKGROUND = pg.image.load(load_resource("gameboard.jpg")).convert()
pg.display.set_caption(f"ALTAR CLIENT username = {USERNAME}")

if AUDIO:
    audio = AudioManager()


def main():
    print("Configuring clock")
    clock = pg.time.Clock()

    ###########
    # GUI ITEMS
    ###########

    print("Setting up dropzones")
    drop_c = DropZone(ZONE_COORS[0])
    drop_r = DropZone(ZONE_COORS[1])
    drop_l = DropZone(ZONE_COORS[2])
    hand = HandZone((685, 850))
    discard = DiscardSpace((50, 50))
    draw = DrawSpace((WIDTH - 150, 50))
    debug_text = CenterText("Please wait for the ADMIN player to initiate the piece", (960, 50), FONT)

    # HelpHandler
    help_handle = HelpHandler(debug_text, [drop_c, drop_r, drop_l], hand, draw, discard)

    # GUI items that have get and set methods
    getset_items = (drop_c, drop_r, drop_l, draw)

    # All items that track mouse movement
    hover_items = (discard, hand) + getset_items
    # All GUI items
    if PROJECT:
        gui_items = getset_items[0:3]
    else:
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
    screen_flasher = ScreenFlasher(temp_screen)
    eye_anim = EyeAnimation()
    end_anim = EndAnimation(quit_all)

    gfx_man = GfxManager(ZONE_COORS, TWINK_LOCS)
    gfx_gens = (gfx_man, screen_flasher, eye_anim, end_anim)
    gui_items += gfx_gens




    held_card = None

    # wait for the server to send the start message
    piece_started = False

    run = True

    if LOCAL:
        debug_text.change_msg("Press H for help, R to restart")
        piece_started = True
        eye_anim.play()

    ###############
    # MAIN GAME LOOP
    ###############

    while run:

        #################
        # MOUSE POSITION CHECKS
        #################

        mouse_pos = tuple(dimension * scaling_factor for dimension in pg.mouse.get_pos())
        for item in hover_items:
            item.check_mouse(mouse_pos)
            if ADMIN:
                for btn in admin_btns:
                    btn.check_mouse(mouse_pos)
        if held_card:
            held_card.check_mouse(mouse_pos)

        #############
        # KEY INPUTS
        #############

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_all()
            if not PROJECT:
                # the projector can't move cards
                if event.type == pg.MOUSEBUTTONDOWN:
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

                                        if get_content(getset_items) == EMPTY_CONTENT:
                                            end_anim.play()
                                        break
                    elif (event.button == 3) and not held_card:  # right click
                        for i, item in enumerate(getset_items):
                            active_card = item.try_right_click()
                            if active_card:
                                check_screen_flash(active_card, screen_flasher)
                                end_turn_reactivate(active_card, i, gfx_man)
                elif event.type == pg.KEYDOWN and LOCAL:
                    if event.scancode == 11:
                        print("Show help menu")
                        help_handle.advance()
                    elif event.scancode == 21:
                        audio.reset()
                        return # restart via the for look

        #################
        # SERVER MESSAGES
        #################

        if not LOCAL:
            client_msg = client.listen()
            if client_msg:

                if client_msg["method"] == 'update':
                    if not piece_started:
                        piece_started = True
                        eye_anim.play()
                    set_content(getset_items, client_msg["content"], gfx_man)
                    print(f"Server message content: {client_msg['content']}")
                    print(f"Current get content : {get_content(getset_items)}")
                    if get_content(getset_items) == EMPTY_CONTENT:
                        end_anim.play()

                elif client_msg["method"] == 'new_turn':
                    debug_text.change_msg(client_msg['current_player'] + "'s turn")

                elif client_msg["method"] == "reactivate":
                    debug_text.change_msg(client_msg['current_player'] + "'s turn")
                    card_num = client_msg["content"][0]
                    zone_num = client_msg['content'][1]
                    reac_zone = getset_items[zone_num]
                    reac_zone.fade_in_card_num(card_num)
                    if AUDIO:
                        audio.force_input(card_num, zone_num)
                        if GFX:
                            gfx_man.input(audio.check_status())

                elif (client_msg["method"] == "new_user") and ADMIN:
                    debug_text.append(f"  New user {client_msg['name']}")

                elif (client_msg["method"] == "gfx_update") and not AUDIO:
                    print(f"Gfx update message: {client_msg}")
                    if GFX:
                        gfx_man.input(client_msg["content"])

                elif client_msg["method"] == "seed":
                    seed(client_msg["seed"])

                elif client_msg["method"] == "screen_flash":
                    check_screen_flash(client_msg["card_num"], screen_flasher, sender=False)

                elif client_msg["method"] == "pattern_num":
                    if GFX:
                        gfx_man.set_pattern_num(client_msg["pat_num"])
                    print("Updating pattern num via remote call")

                elif client_msg["method"] == 'quit':
                    quit_all()

        #################
        # DRAW AND FINISH
        #################
        temp_screen.blit(BACKGROUND, (0, 0))
        for item in gui_items:
            item.draw(temp_screen)
        if held_card:
            held_card.draw(temp_screen)
        resized_screen = pg.transform.scale(temp_screen, scaled_size)
        screen.blit(resized_screen, (0, 0))
        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    while True:
        main()
        print("restarting")
    print("finished loop")
