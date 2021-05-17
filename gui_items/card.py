import pygame as pg


class CardZone:
    SPACE_MARGIN = 15

    def __init__(self, coor, num_cards):
        self.origin = coor
        self.cards = []
        for i in range(num_cards):
            card_x = ((self.SPACE_MARGIN + Card.CARD_WIDTH) * i) + coor[0]
            new_card = Card((card_x, coor[1]))
            self.cards.append(new_card)

    def check_mouse(self, mouse_coor):
        for card in self.cards:
            card.check_mouse(mouse_coor)

    def draw(self, surf):
        for card in self.cards:
            card.draw(surf)


class DropZone(CardZone):
    def __init__(self, coor):
        super(DropZone, self).__init__(coor, num_cards=3)


class HandZone(CardZone):
    def __init__(self, coor):
        super(HandZone, self).__init__(coor, num_cards=4)

class Card:
    CARD_WIDTH = 130
    CARD_HEIGHT = 200

    def __init__(self, coor):
        self.rect = pg.Rect(coor[0], coor[1], self.CARD_WIDTH, self.CARD_HEIGHT)
        self.hover = False

    def check_mouse(self, mouse_coor):
        if self.rect.collidepoint(mouse_coor):
            self.hover = True
        else:
            self.hover = False

    def draw(self, surf):
       # if self.hover:
            pg.draw.rect(surf, (0, 0, 0), self.rect, width=0, border_radius=5)
            pg.draw.rect(surf, (255, 255, 255), self.rect, width=3, border_radius=5)
