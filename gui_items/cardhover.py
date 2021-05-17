import pygame as pg
import os


class CardZone:
    SPACE_MARGIN = 15

    def __init__(self, coor, num_cards):
        self.origin = coor
        self.card_spaces = []
        for i in range(num_cards):
            card_x = ((self.SPACE_MARGIN + CardHover.CARD_WIDTH) * i) + coor[0]
            new_card = CardHover((card_x, coor[1]))
            self.card_spaces.append(new_card)

    def check_mouse(self, mouse_coor):
        for card in self.card_spaces:
            card.check_mouse(mouse_coor)

    def draw(self, surf):
        for card in self.card_spaces:
            card.draw(surf)


class DropZone(CardZone):
    def __init__(self, coor):
        super(DropZone, self).__init__(coor, num_cards=3)


class HandZone(CardZone):
    def __init__(self, coor):
        super(HandZone, self).__init__(coor, num_cards=4)


class BasicCard:
    CARD_WIDTH = 130
    CARD_HEIGHT = 200

    def __init__(self, coor):
        self.rect = pg.Rect(coor[0], coor[1], self.CARD_WIDTH, self.CARD_HEIGHT)
        self.hover = False
        self.graphic = pg.image.load(os.path.join('cards', 'test_card.jpg'))

    def check_mouse(self, mouse_coor):
        if self.rect.collidepoint(mouse_coor):
            self.hover = True
        else:
            self.hover = False

    def draw(self, surf: pg.Surface):
        if self.hover:
            pg.draw.rect(surf, (0, 0, 0), self.rect, width=0, border_radius=5)
            surf.blit(self.graphic, self.rect)
            pg.draw.rect(surf, (255, 255, 255), self.rect, width=3, border_radius=5)


class CardHover(BasicCard):
    def __init__(self, coor):
        super().__init__(coor)
        self.card = MoveableCard(coor)

    def draw(self, surf: pg.Surface):
        if self.card:
            self.card.draw(surf)

        if self.hover:
            pg.draw.rect(surf, (255, 255, 255), self.rect, width=3, border_radius=5)


class MoveableCard(BasicCard):
    def __init__(self, coor):
        super(MoveableCard, self).__init__(coor)
        self.graphic = pg.image.load(os.path.join('cards', 'test_card.jpg'))
        self.clicked = False

    def check_mouse(self, mouse_coor):
        if not self.clicked:
            super().check_mouse(mouse_coor)
        else:
            self.rect.topleft = mouse_coor

    def try_click(self):
        if self.hover and not self.clicked:
            self.clicked = True
        elif not self.clicked:
            self.clicked = False

    def draw(self, surf: pg.Surface):
        pg.draw.rect(surf, (0, 0, 0), self.rect, width=0, border_radius=5)
        surf.blit(self.graphic, self.rect)

