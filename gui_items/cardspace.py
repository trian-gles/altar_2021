import pygame as pg
import os
from random import shuffle

# Spaces containing multiple cards

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
            # check if the selected space is highlighted and has a card, then return it
            result = space.try_click()
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
        print(self.card_spaces[0].rect.topleft)
        print(self.card_spaces[2].rect.bottomright)

    def return_content(self):
        map_obj = map(lambda space: space.return_content(), self.card_spaces)
        return tuple(map_obj)

    def set_content(self, card_nums):
        for i, card_num in enumerate(card_nums):
            self.card_spaces[i].set_content(card_num)


class HandZone(CardZone):
    def __init__(self, coor):
        super(HandZone, self).__init__(coor, num_cards=4)

    def return_content(self):
        pass

    def set_content(self, card_nums):
        pass
    
    def draw(self, surf):
        for card_space in self.card_spaces:
            pg.draw.rect(surf, (60, 60, 60), card_space.rect, width=3, border_radius=5)
        super(HandZone, self).draw(surf)


# Smaller card units


class BasicCard:
    CARD_WIDTH = 130
    CARD_HEIGHT = 200

    def __init__(self, coor):
        self.rect = pg.Rect(coor[0], coor[1], self.CARD_WIDTH, self.CARD_HEIGHT)
        self.hover = False
        self.graphic = None

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
        self.card = None
        MoveableCard.convert_imgs()

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
    def __init__(self, coor):
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

    def drop_card(self, card):
        if self.hover:
            self.card = card
            card.drop(self.rect.topleft)
            card.flip()
            return True


class DrawSpace(BasicCard):
    def __init__(self, coor):
        super(DrawSpace, self).__init__(coor)
        self.cards = [MoveableCard(coor, i, True) for i in range(27)]
        shuffle(self.cards)

    def check_mouse(self, mouse_coor):
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


image_list = ["half_speed", "double_speed", "random_speeds", "long_sustain", "short_attacks", "octave_up", "int_ratios",
                  "some_int_ratios", "5_ratios", "some_5_ratios", "rand_ratios", "some_rand_ratios", "white_noise_card",
                  "random", "octave_down", "normal_speed", "many_octaves_up", "many_octaves_down", "quiet", "silence",
                  "random_every_cycle", "moon_card", "sunrise_card", "change_algo", "algo_every_cycle", "sharp_attacks",
                  "tree_card"]


class MoveableCard(BasicCard):
    flip_graphic = pg.image.load(os.path.join('resources/cards', 'flip_card.jpg'))
    imgs = [pg.image.load(os.path.join('resources/cards', image_list[id_num] + '.PNG')) for id_num in range(27)]

    bkg_color = (0, 0, 0)
    border_color = (55, 55, 55)

    def __init__(self, coor, id_num=0, flip=False):
        super(MoveableCard, self).__init__(coor)
        self.graphic = self.imgs[id_num]
        self.id_num = id_num
        self.clicked = False
        self.flipped = flip
        if image_list[id_num] == "moon_card":
            self.bkg_color = (173, 35, 0)
        elif image_list[id_num] == "sunrise_card":
            self.bkg_color = (105, 233, 240)
        elif image_list[id_num] == "tree_card":
            self.bkg_color = (0, 74, 35)

    @classmethod
    def convert_imgs(cls):
        cls.imgs = [img.convert_alpha() for img in cls.imgs]
        cls.flip_graphic = cls.flip_graphic.convert_alpha()

    def check_mouse(self, mouse_coor):
        if not self.clicked:
            super().check_mouse(mouse_coor)
        else:
            self.rect.center = mouse_coor

    def drop(self, coor):
        self.rect.topleft = coor
        self.clicked = False
        if self.flipped:
            self.flip()

    def flip(self):
        self.flipped = not self.flipped

    def draw(self, surf: pg.Surface):

        if self.flipped:
            pg.draw.rect(surf, (0, 0, 0), self.rect, width=0, border_radius=5)
            surf.blit(self.flip_graphic, self.rect)
        else:
            pg.draw.rect(surf, self.bkg_color, self.rect, width=0, border_radius=5)
            surf.blit(self.graphic, self.rect)
        pg.draw.rect(surf, (55, 55, 55), self.rect, width=3, border_radius=5)

#    3744    0.008    0.000   10.763    0.003 cardspace.py:37(draw) # maybe the hand should only appear on mouseover?

