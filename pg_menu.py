import pygame
import pygame_menu as pgm
from random import randrange

pygame.init()
surface = pygame.display.set_mode((600, 500))
audio = False

results = {}
results["username"] = str(randrange(0, 100000))
results["local"] = True
results["ip"] = "192.168.1.1"
results["audio"] = True
results["fullscreen"] = False
results["project"] = False
results["admin"] = True


def set_username(value: str):
    results["username"] = value


def set_ip(value: str):
    results["ip"] = value


def set_network(value, n_status):
    results["local"] = n_status
    if n_status:
        username_widget.hide()
        ip_widget.hide()
        admin_widget.hide()
        projector_widget.hide()
        audio_widget.hide()
    else:
        username_widget.show()
        ip_widget.show()
        admin_widget.show()
        projector_widget.show()
        audio_widget.show()


def set_audio(value, audio_status):
    results["audio"] = audio_status


def set_fullscreen(value, f_status):
    results["fullscreen"] = f_status


def set_projector(value, p_status):
    results["project"] = p_status
    if p_status:
        admin_widget.hide()
        username_widget.hide()
    else:
        admin_widget.show()
        username_widget.show()


def set_admin(value, a_status):
    results["admin"] = a_status


def quit_menu():
    exit()

menu = pgm.Menu('ALTAR config', 600, 500,
                theme=pgm.themes.THEME_DARK, onclose=pgm.events.CLOSE)

menu.add.selector('Network Config :', [('SINGLE PLAYER', True), ('MULTIPLAYER', False)], onchange=set_network)

username_widget = menu.add.text_input('Username :', default=results["username"], onchange=set_username)
ip_widget = menu.add.text_input('IP :', default=results["ip"], onchange=set_ip)
projector_widget = menu.add.selector('Projector Mode :', [('Off', False), ('On', True)], onchange=set_projector)
admin_widget = menu.add.selector('Admin :', [('On', True), ('Off', False)], onchange=set_admin)
audio_widget = menu.add.selector('Audio :', [('On', True), ('Off', False)], onchange=set_audio)
menu.add.selector('Fullscreen :', [('Off', False), ('On', True)], onchange=set_fullscreen)
menu.add.button('Play', menu.close)
menu.add.button('Quit', quit_menu)


def run_menu() -> dict:
    username_widget.hide()
    ip_widget.hide()
    admin_widget.hide()
    projector_widget.hide()
    audio_widget.hide()
    menu.mainloop(surface)
    return results


if __name__ == "__main__":
    run_menu()



