import pygame as pg
import os
from random import shuffle
from typing import Tuple
from .basic_card import MoveableCard, BasicCard

# type aliases
Vector2 = Tuple[int, int]

# Spaces containing multiple cards

TOTAL_CARDS = 29

class CardZone:
    SPACE_MARGIN = 15

    def __init__(self, coor: Vector2, num_cards: int):
        self.origin = coor
        self.card_spaces = []
        for i in range(num_cards):
            card_x = ((self.SPACE_MARGIN + CardSpace.CARD_WIDTH) * i) + coor[0]
            new_card = CardSpace((card_x, coor[1]))
            self.card_spaces.append(new_card)

    def check_mouse(self, mouse_coor: Vector2):
        for card in self.card_spaces:
            card.check_mouse(mouse_coor)

    def try_click(self):
        for space in self.card_spaces:
            # check if the selected space is highlighted and has a card, then return it
            result = space.try_click()
            if result:
                return result

    def try_right_click(self):
        for space in self.card_spaces:
            # check if the selected space is highlighted and has a card, then return it
            result = space.try_right_click()
            if result:
                return result

    def drop_card(self, card):
        for space in self.card_spaces:
            # check if the drop was successful
            result = space.drop_card(card)
            if result:
                return True

    def draw(self, surf: pg.Surface):
        for card in self.card_spaces:
            card.draw(surf)


class DropZone(CardZone):
    def __init__(self, coor: Vector2):
        super(DropZone, self).__init__(coor, num_cards=3)
        print(self.card_spaces[0].rect.topleft)
        print(self.card_spaces[2].rect.bottomright)

    def return_content(self) -> tuple:
        map_obj = map(lambda space: space.return_content(), self.card_spaces)
        return tuple(map_obj)

    def set_content(self, card_nums):
        for i, card_num in enumerate(card_nums):
            self.card_spaces[i].set_content(card_num)


class HandZone(CardZone):
    def __init__(self, coor: Vector2):
        super(HandZone, self).__init__(coor, num_cards=4)

    # all these methods should have no effect
    def return_content(self):
        pass

    def set_content(self, card_nums):
        pass

    def try_right_click(self):
        pass
    
    def draw(self, surf):
        for card_space in self.card_spaces:
            pg.draw.rect(surf, (60, 60, 60), card_space.rect, width=3, border_radius=5)
        super(HandZone, self).draw(surf)





class CardSpace(BasicCard):
    def __init__(self, coor: Vector2):
        super().__init__(coor)
        self.card = None
        MoveableCard.convert_imgs()

    def check_mouse(self, mouse_coor: Vector2):
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
            print("Calling pickup card")
            return picked_card

    def try_click(self):
        if self.card:
            if self.hover and not self.card.clicked:
                self.card.clicked = True
                picked_card = self.card
                self.card = None
                return picked_card
            elif not self.card.clicked:
                self.card.clicked = False

    def try_right_click(self):
        if self.hover:
            return self.return_content()

    def return_content(self):
        if self.card:
            return self.card.id_num
        else:
            return None

    def set_content(self, card_num):
        if card_num or card_num == 0:
            self.card = MoveableCard(self.rect.topleft, card_num)
        else:
            self.card = None

    def draw(self, surf: pg.Surface):
        if self.card:
            self.card.draw(surf)

        if self.hover:
            pg.draw.rect(surf, (255, 255, 255), self.rect, width=3, border_radius=5)


class DiscardSpace(CardSpace):
    def __init__(self, coor: Vector2):
        super(DiscardSpace, self).__init__(coor)
        self.graphic = pg.image.load(os.path.join('resources/cards', 'discard.png')).convert_alpha()

    def draw(self, surf: pg.Surface):
        surf.blit(self.graphic, self.rect)
        if self.hover:
            pg.draw.rect(surf, (255, 255, 255), self.rect, width=3, border_radius=5)
        else:
            pg.draw.rect(surf, (55, 55, 55), self.rect, width=3, border_radius=5)

    def pickup_card(self):
        pass

    def try_click(self):
        pass

    def try_right_click(self):
        pass

    def drop_card(self, card):
        if self.hover:
            self.card = card
            card.drop(self.rect.topleft)
            card.flip()
            return True


class DrawSpace(BasicCard):
    def __init__(self, coor: Vector2):
        super(DrawSpace, self).__init__(coor)
        self.cards = [MoveableCard(coor, i, True) for i in range(TOTAL_CARDS)]
        shuffle(self.cards)

    def check_mouse(self, mouse_coor: Vector2):
        super().check_mouse(mouse_coor)
        if self.cards:
            self.cards[0].check_mouse(mouse_coor)

    def pickup_card(self):
        if self.hover and self.cards:
            picked_card = self.cards.pop()
            print(self.cards)
            return picked_card

    def try_click(self):
        if self.cards:
            if self.hover and not self.cards[0].clicked:
                self.cards[0].clicked = True
                picked_card = self.cards.pop(0)
                return picked_card
            elif not self.cards[0].clicked:
                self.cards[0].clicked = False

    def try_right_click(self):
        pass

    def draw(self, surf: pg.Surface):
        if self.cards:
            self.cards[0].draw(surf)

        if self.hover:
            pg.draw.rect(surf, (255, 255, 255), self.rect, width=3, border_radius=5)

    def drop_card(self, card):
        pass

    def return_content(self):
        if self.cards:
            return tuple(map(lambda card: card.id_num, self.cards))
        else:
            return None

    def set_content(self, card_nums):
        if card_nums:
            self.cards = [MoveableCard(self.rect.topleft, card_num, True) for card_num in card_nums]







#    3744    0.008    0.000   10.763    0.003 cardspace.py:37(draw) # maybe the hand should only appear on mouseover?

