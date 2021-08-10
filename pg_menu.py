import pygame
import pygame_menu as pgm
from random import randrange

pygame.init()
surface = pygame.display.set_mode((600, 500))
audio = False

results = {}
results["username"] = str(randrange(0, 100000))
results["local"] = 0
results["audio"] = True
results["fullscreen"] = False
results["project"] = False
results["admin"] = True


def set_network(value, n_status):
    results["local"] = n_status


def set_audio(value, audio_status):
    results["audio"] = audio_status


def set_fullscreen(value, f_status):
    results["fullscreen"] = f_status


def set_projector(value, p_status):
    results["project"] = p_status


def set_admin(value, a_status):
    results["admin"] = a_status


def quit_menu():
    exit()

menu = pgm.Menu('ALTAR config', 600, 500,
                theme=pgm.themes.THEME_DARK, onclose=pgm.events.CLOSE)
menu.add.text_input('Username :', default=results["username"])
menu.add.selector('Network Config :', [('SINGLE PLAYER', 0), ('LAN', 1), ('REMOTE', 2)], onchange=set_audio)
menu.add.selector('Audio :', [('On', True), ('Off', False)], onchange=set_audio)
menu.add.selector('Projector Mode :', [('Off', False), ('On', True)], onchange=set_projector)
menu.add.selector('Fullscreen :', [('Off', False), ('On', True)], onchange=set_fullscreen)
menu.add.selector('Admin :', [('On', True), ('Off', False)], onchange=set_admin)
menu.add.button('Play', menu.close)
menu.add.button('Quit', quit_menu)


def run_menu() -> dict:
    menu.mainloop(surface)
    return results

if __name__ == "__main__":
    run_menu()



