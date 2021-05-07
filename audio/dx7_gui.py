import pygame as pg
from dx7 import DX7Poly, s
from random import uniform
import pyautogui


WIDTH = 1920
HEIGHT = 1080

# colors need work to match pallete
BLACK = (55, 55, 55)
WHITE = (255, 255, 255)
LIGHT_GREY = (191, 191, 191)
RED = (255, 0, 0)

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
FONT = pg.font.Font('../resources/JetBrainsMono-Medium.ttf', 12)
pg.display.set_caption("DX7 testing GUI")


class Slider:
    dimensions = (100, 20)
    cursor = (10, 20)

    def __init__(self, name, coor, callback, mod_num, min=0, max=1.0, init=1.0, step=None):
        self.rect = pg.Rect(coor, self.dimensions)
        self.cursor_rect = pg.Rect(coor, self.cursor)
        self.name = FONT.render(name, False, WHITE)
        self.name_loc = (self.rect.topleft[0], self.rect.topleft[1] - 20)

        self.value_loc = (self.rect.topright[0], self.rect.topright[1] - 20)
        self.callback = callback
        self.mod_num = mod_num
        self.min = min
        self.max = max
        self.step = step
        self.change_value(init)

    def draw(self, surf):
        value_frac = ((self.value - self.min) / (self.max - self.min))
        self.cursor_rect.centerx = (value_frac * self.dimensions[0]) + self.rect.x

        surf.blit(self.display_val, self.value_loc)
        surf.blit(self.name, self.name_loc)
        pg.draw.rect(surf, WHITE, self.rect)
        pg.draw.rect(surf, LIGHT_GREY, self.cursor_rect)

    def change_value(self, new_val):
        if not self.step:
            self.value = new_val
        else:
            self.value = self.step * round(new_val/self.step)
        self.callback(self.mod_num, new_val)
        self.display_val = FONT.render(str(self.value)[0:4], False, WHITE)

    def randomize(self):
        self.change_value(uniform(self.min, self.max))

    def check_mouse(self, mouse_coor):
        if self.rect.collidepoint(mouse_coor):
            value_frac = (mouse_coor[0] - self.rect.left) / self.rect.width
            new_val = (value_frac * (self.max - self.min)) + self.min
            self.change_value(new_val)


class Module:
    spacing = 40

    def __init__(self, coor: tuple, mod_num: int, synth: DX7Poly):
        self.coor = coor

        self.level = Slider("Level", (coor[0], coor[1]), synth.set_level, mod_num)
        self.ratio = Slider("Ratio", (coor[0], coor[1] + self.spacing), synth.set_ratio, mod_num)
        self.attack = Slider("Attack", (coor[0], coor[1] + self.spacing * 3), synth.set_attack, mod_num)
        self.decay = Slider("Decay", (coor[0], coor[1] + self.spacing * 4), synth.set_decay, mod_num)
        self.sustain = Slider("Sustain", (coor[0], coor[1] + self.spacing * 5), synth.set_sustain, mod_num)
        self.release = Slider("Release", (coor[0], coor[1] + self.spacing * 6), synth.set_release, mod_num)

        self.sliders = (self.level, self.ratio, self.attack, self.decay, self.sustain, self.release)

    def check_mouse(self, mouse_coor):
        for slider in self.sliders:
            slider.check_mouse(mouse_coor)

    def draw(self, surf):
        for slider in self.sliders:
            slider.draw(surf)

    def randomize(self):
        for slider in self.sliders:
            slider.randomize()


def main():
    run = True
    clock = pg.time.Clock()
    synth = DX7Poly(4)
    modules = [Module(((mod_num * 200) + 20, 20), mod_num, synth) for mod_num in range(6)]


    other_gui = []
    gui_items = modules + other_gui
    s.start()

    while run:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                s.stop()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                for module in modules:
                    module.check_mouse(mouse_pos)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    for module in modules:
                        module.randomize()
                if event.key == pg.K_SPACE:
                    synth.noteon(220, 1)
        screen.fill(BLACK)
        for item in gui_items:
            item.draw(screen)
        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()