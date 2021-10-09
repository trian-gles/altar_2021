import pygame as pg
import os
from typing import Tuple

# type aliases
Vector2 = Tuple[int, int]

TOTAL_CARDS = 29
# Consider not placing this in both files


class BasicCard:
    CARD_WIDTH = 130
    CARD_HEIGHT = 200

    def __init__(self, coor: Vector2):
        self.rect = pg.Rect(coor[0], coor[1], self.CARD_WIDTH, self.CARD_HEIGHT)
        self.hover = False
        self.graphic = None

    def check_mouse(self, mouse_coor: Vector2):
        if self.rect.collidepoint(mouse_coor):
            self.hover = True
        else:
            self.hover = False

    def draw(self, surf: pg.Surface):
        if self.hover:
            pg.draw.rect(surf, (0, 0, 0), self.rect, width=0, border_radius=5)
            surf.blit(self.graphic, self.rect)
            pg.draw.rect(surf, (255, 255, 255), self.rect, width=3, border_radius=5)


image_list = ["half_speed", "double_speed", "random_speeds", "long_sustain", "short_attacks", "octave_up", "int_ratios",
                  "some_int_ratios", "5_ratios", "some_5_ratios", "rand_ratios", "some_rand_ratios", "white_noise_card",
                  "random", "octave_down", "normal_speed", "many_octaves_up", "many_octaves_down", "quiet", "silence",
                  "random_every_cycle", "moon_card", "sunrise_card", "change_algo", "algo_every_cycle", "sharp_attacks",
                  "tree_card", "transp_changes", "transp_changes_many"]


class MoveableCard(BasicCard):
    flip_graphic = pg.image.load(os.path.join('resources/cards', 'flip_card.jpg'))
    imgs = [pg.image.load(os.path.join('resources/cards',
                                       image_list[id_num] + '.PNG')) for id_num in range(TOTAL_CARDS)]

    bkg_color = (0, 0, 0)
    border_color = (55, 55, 55)

    def __init__(self, coor: Vector2, id_num: int = 0, flip=False):
        super(MoveableCard, self).__init__(coor)
        self.graphic = self.imgs[id_num]
        self._id_num = id_num
        self.clicked = False
        self.flipped = flip
        self.alpha = 255
        if image_list[id_num] == "moon_card":
            self.bkg_color = (173, 35, 0)
        elif image_list[id_num] == "sunrise_card":
            self.bkg_color = (105, 233, 240)
        elif image_list[id_num] == "tree_card":
            self.bkg_color = (0, 74, 35)

    @property
    def id_num(self) -> int:
        return self._id_num

    @classmethod
    def convert_imgs(cls):
        cls.imgs = [img.convert_alpha() for img in cls.imgs]
        cls.flip_graphic = cls.flip_graphic.convert_alpha()

    def check_mouse(self, mouse_coor: Vector2):
        if not self.clicked:
            super().check_mouse(mouse_coor)
        else:
            self.rect.center = mouse_coor
            self.flip()

    def start_fade(self):
        self.alpha = 0

    def _fade_in(self):
        if self.alpha > 255:
            return
        self.alpha += 2
        self.graphic.set_alpha(self.alpha)

    def drop(self, coor: Vector2):
        self.rect.topleft = coor
        self.clicked = False
        if self.flipped:
            self.flip()

    def flip(self):
        self.flipped = False

    def draw(self, surf: pg.Surface):
        self._fade_in()
        if self.flipped:
            pg.draw.rect(surf, (0, 0, 0), self.rect, width=0, border_radius=5)
            surf.blit(self.flip_graphic, self.rect)
        else:
            pg.draw.rect(surf, self.bkg_color, self.rect, width=0, border_radius=5)
            surf.blit(self.graphic, self.rect)
        pg.draw.rect(surf, (55, 55, 55), self.rect, width=3, border_radius=5)
