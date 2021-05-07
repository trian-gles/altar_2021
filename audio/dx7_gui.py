import pygame as pg
from dx7 import DX7Poly
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
FONT = pg.font.Font('../resources/JetBrainsMono-Medium.ttf', 16)
pg.display.set_caption("DX7 testing GUI")


class Slider:
    dimensions = (100, 20)
    cursor = (10, 20)

    def __init__(self, coor, callback, min=0, max=1.0, init=1.0):
        self.rect = pg.Rect(coor, self.dimensions)
        self.cursor_rect = pg.Rect(coor, self.cursor)

        self.callback = callback
        self.min = min
        self.max = max
        self.value = init

    def draw(self, surf):
        value_frac = ((self.value - self.min) / (self.max - self.min))
        self.cursor_rect.centerx = (value_frac * self.dimensions[0]) + self.rect.x
        pg.draw.rect(surf, WHITE, self.rect)
        pg.draw.rect(surf, LIGHT_GREY, self.cursor_rect)

    def change_value(self, new_val):
        self.value = new_val
        self.callback(new_val)

    def check_mouse(self, mouse_coor):
        if self.rect.collidepoint(mouse_coor):
            value_frac = (mouse_coor[0] - self.rect.left) / self.rect.width
            new_val = (value_frac * (self.max - self.min)) + self.min
            self.change_value(new_val)


def test_call(value):
    print(f"Test call called with {value}")


def main():
    run = True
    clock = pg.time.Clock()
    sliders = (Slider((20, 20), test_call),)
    gui_items = sliders

    while run:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                for slider in sliders:
                    slider.check_mouse(mouse_pos)
        screen.fill(BLACK)
        for item in gui_items:
            item.draw(screen)
        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()