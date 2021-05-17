import pygame as pg


class Card:
    CARD_WIDTH = 160
    CARD_HEIGHT = 240

    def __init__(self, coor):
        self.rect = pg.Rect(coor[0], coor[1], self.CARD_WIDTH, self.CARD_HEIGHT)
        self.hover = False

    def check_mouse(self, mouse_coor):
        if self.rect.collidepoint(mouse_coor):
            self.hover = True
        else:
            self.hover = False

    def draw(self, surf):
        if self.hover:
            pg.draw.rect(surf, (255, 255, 255), self.rect, width=3, border_radius=5)
