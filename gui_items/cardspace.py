import pygame as pg
import os


class CardZone:
    SPACE_MARGIN = 15

    def __init__(self, coor, num_cards):
        self.origin = coor
        self.card_spaces = []
        for i in range(num_cards):
            card_x = ((self.SPACE_MARGIN + CardSpace.CARD_WIDTH) * i) + coor[0]
            new_card = CardSpace((card_x, coor[1]))
            self.card_spaces.append(new_card)

    def check_mouse(self, mouse_coor):
        for card in self.card_spaces:
            card.check_mouse(mouse_coor)

    def try_click(self):
        for space in self.card_spaces:
            if space.card:
                # check if the selected space is highlighted and has a card, then return it
                result = space.card.try_click()
                if result:
                    return result

    def drop_card(self, card):
        for space in self.card_spaces:
            # check if the drop was successful
            result = space.drop_card(card)
            if result:
                return True

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


class CardSpace(BasicCard):
    def __init__(self, coor):
        super().__init__(coor)
        self.card = MoveableCard(coor)

    def check_mouse(self, mouse_coor):
        super().check_mouse(mouse_coor)
        if self.card:
            self.card.check_mouse(mouse_coor)

    def drop_card(self, card):
        if self.hover:
            self.card = card
            card.drop(self.rect.topleft)
            return True

    def pickup_card(self):
        if self.hover:
            picked_card = self.card
            self.card = None
            return picked_card

    def draw(self, surf: pg.Surface):
        if self.card:
            self.card.draw(surf)

        if self.hover:
            pg.draw.rect(surf, (255, 255, 255), self.rect, width=3, border_radius=5)


class DiscardSpace(CardSpace):
    def draw(self, surf: pg.Surface):
        if self.hover:
            pg.draw.rect(surf, (255, 255, 255), self.rect, width=3, border_radius=5)

    def pickup_card(self):
        pass

    def try_click(self):
        pass


class MoveableCard(BasicCard):
    def __init__(self, coor, id_num=0):
        super(MoveableCard, self).__init__(coor)
        self.graphic = pg.image.load(os.path.join('cards', 'test_card.jpg'))
        self.id_num = id_num
        self.clicked = False

    def check_mouse(self, mouse_coor):
        if not self.clicked:
            super().check_mouse(mouse_coor)
        else:
            self.rect.center = mouse_coor

    def drop(self, coor):
        self.rect.topleft = coor
        self.clicked = False

    def try_click(self):
        if self.hover and not self.clicked:
            self.clicked = True
            return self
        elif not self.clicked:
            self.clicked = False

    def draw(self, surf: pg.Surface):
        pg.draw.rect(surf, (0, 0, 0), self.rect, width=0, border_radius=5)
        surf.blit(self.graphic, self.rect)
        pg.draw.rect(surf, (55, 55, 55), self.rect, width=3, border_radius=5)

