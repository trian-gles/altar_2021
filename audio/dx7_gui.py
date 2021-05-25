import pygame as pg
from dx7 import DX7Poly, s
from random import uniform, randrange
from text import MessageButton
import pyautogui
from pyo import Pattern
from tkinter import filedialog as fd
from tkinter import Tk


WIDTH = 1920
HEIGHT = 1080

# colors need work to match pallete
BLACK = (55, 55, 55)
WHITE = (255, 255, 255)
LIGHT_GREY = (191, 191, 191)
RED = (255, 0, 0)

pg.init()
s.boot()

screen = pg.display.set_mode((WIDTH, HEIGHT))
FONT = pg.font.Font('../resources/JetBrainsMono-Medium.ttf', 12)
pg.display.set_caption("DX7 testing GUI")


def note_to_freq(pitch):
    a = 440
    return (a / 32) * (2 ** ((pitch - 9) / 12))



class Slider:
    dimensions = (100, 20)
    cursor = (10, 20)

    def __init__(self, name, coor, setter, callback_arg, getter, min=0.0, max=1.0, init=1.0, step=None):
        self.rect = pg.Rect(coor, self.dimensions)
        self.cursor_rect = pg.Rect(coor, self.cursor)
        self.name = FONT.render(name, False, WHITE)
        self.name_loc = (self.rect.topleft[0], self.rect.topleft[1] - 20)

        self.value_loc = (self.rect.topright[0], self.rect.topright[1] - 20)
        self.setter = setter
        self.callback_arg = callback_arg
        self.getter = getter
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

    def change_value(self, new_val: float):
        if not self.step:
            self.value = new_val
        else:
            self.value = self.step * round(new_val/self.step)
        self.setter(self.callback_arg, self.value)
        self.display_val = FONT.render(str(self.value)[0:4], False, WHITE)

    def load(self):
        self.change_value(self.getter(self.callback_arg))

    def randomize(self):
        self.change_value(uniform(self.min, self.max))

    def check_mouse(self, mouse_coor):
        if self.rect.collidepoint(mouse_coor):
            value_frac = (mouse_coor[0] - self.rect.left) / self.rect.width
            new_val = (value_frac * (self.max - self.min)) + self.min
            self.change_value(new_val)


class AlgoSlider(Slider):
    def __init__(self, coor, callback, getter):
        super().__init__("Algorithm", coor, callback, None, getter, 0, 10, 0, 1)

    def change_value(self, new_val):
        self.value = int(new_val + 0.5)
        self.setter(self.value)
        self.display_val = FONT.render(str(self.value), False, WHITE)

    def load(self):
        self.change_value(self.getter())


class Module:
    spacing = 40

    def __init__(self, coor: tuple, mod_num: int, synth: DX7Poly):
        self.coor = coor

        self.level = Slider("Level", (coor[0], coor[1]), synth.set_level, mod_num, synth.get_level)
        self.ratio = Slider("Ratio", (coor[0], coor[1] + self.spacing), synth.set_ratio,
                            mod_num, synth.get_ratio, .5, 6, 1, .5)
        self.attack = Slider("Attack", (coor[0], coor[1] + self.spacing * 3), synth.set_attack,
                             mod_num, synth.get_attack, 0, .1, .01)
        self.decay = Slider("Decay", (coor[0], coor[1] + self.spacing * 4), synth.set_decay,
                            mod_num, synth.get_decay, .1, .5, .2)
        self.sustain = Slider("Sustain", (coor[0], coor[1] + self.spacing * 5), synth.set_sustain,
                              mod_num, synth.get_sustain)
        self.release = Slider("Release", (coor[0], coor[1] + self.spacing * 6),
                              synth.set_release, mod_num, synth.get_release, .8, 1.4, 1)

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

    def load(self):
        for slider in self.sliders:
            slider.load()


pattern = (48, 51, 55, 56, 51, 58)
pattern_count = 0
c = None
trans = 0


def main():
    run = True
    clock = pg.time.Clock()

    synth = DX7Poly(8)
    synth.randomize_all()

    def note():
        global trans
        global c
        global pattern_count
        hold = False
        if randrange(6) == 1:
            hold = True
        p.time = 0.2
        if hold:
            p.time = 0.6
        freq = note_to_freq(pattern[pattern_count] + 12 * trans)
        synth.noteon(freq, 1)
        if not hold:
            pattern_count = (pattern_count + 1) % 6
        if pattern_count == 0:
            trans = (trans + 1) % 4

    def randomize():
        for module in modules:
            module.randomize()
        algo_slider.randomize()

    def load_all():
        root = Tk()
        file = fd.askopenfile()
        root.destroy()
        synth.load(file)
        for module in modules:
            module.load()
        algo_slider.load()

    def save_all():
        root = Tk()
        file = fd.asksaveasfile()
        root.destroy()
        synth.save(file)

    p = Pattern(note, 0.2)

    global playing
    playing = False

    def play():
        global playing
        if playing:
            print("stopping pattern")
            p.stop()
            playing = False
        else:
            print("playing pattern")
            p.play()
            playing = True

    modules = [Module(((mod_num * 200) + 20, 20), mod_num, synth) for mod_num in range(6)]
    algo_slider = AlgoSlider((20, 800), synth.set_algo, synth.get_algo)
    save_btn = MessageButton("Save", (20, 840), save_all, FONT)
    load_btn = MessageButton("Load", (20, 880), load_all, FONT)
    pattern_btn = MessageButton("Pattern", (20, 920), play, FONT)
    random_btn = MessageButton("Randomize", (20, 960), randomize, FONT)

    other_gui = [algo_slider, save_btn, load_btn, pattern_btn, random_btn]
    gui_items = modules + other_gui
    s.start()

    while run:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                s.stop()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                for item in gui_items:
                    item.check_mouse(mouse_pos)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    for module in modules:
                        module.randomize()
                    algo_slider.randomize()
                if event.key == pg.K_SPACE:
                    synth.noteon(220, 1)
        screen.fill(BLACK)
        for item in gui_items:
            item.draw(screen)
        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()