import pygame as pg
import os
from random import shuffle
from typing import Tuple, Optional, List, Callable
from .basic_card import MoveableCard, BasicCard

# type aliases
Vector2 = Tuple[int, int]

# Spaces containing multiple cards

TOTAL_CARDS = 29


class CardZone:
    """Base class for an area with multiple card spaces"""
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

    def try_click(self) -> Optional[MoveableCard]:
        for space in self.card_spaces:
            # check if the selected space is highlighted and has a card, then return it
            result = space.try_click()
            if result:
                return result

    def super_try_right_click(self, callback: Callable = None) -> Optional[int]:
        """Check if any of the contained spaces are highlighted and contain a card.
        The callback can be used to provide a function to perform on the indicated card
        """
        for space in self.card_spaces:
            result = space.try_right_click()
            if result:
                if callback:
                    callback(space.card)
                return result

    def super_drop_card(self, card: MoveableCard, callback: Callable = None) -> bool:
        """Try to move the held card to all contained spaces, return results.
        The callback can be used to provide a function to perform on the indicated card
        """
        for space in self.card_spaces:
            result = space.drop_card(card)
            if result:
                if callback:
                    callback(space.card)
                return True
        else:
            return False
            
    def set_help(self, new_help: bool):
        for space in self.card_spaces:
            space.help = new_help

    def draw(self, surf: pg.Surface):
        for card in self.card_spaces:
            card.draw(surf)


class DropZone(CardZone):
    """Three card area of the main game board"""
    def __init__(self, coor: Vector2, font: pg.font.Font):
        super(DropZone, self).__init__(coor, num_cards=3)
        self.font = font
        self.text = font.render("  ", False, (255, 255, 255))
        self.alpha = 255
        self.update_text_offset = 0

    def set_text(self, new_text: str):
        self.text = self.font.render(new_text, False, (255, 255, 255))
        self.alpha = 255

    def return_content(self) -> Tuple[Optional[int]]:
        return tuple([space.return_content() for space in self.card_spaces])

    def set_content(self, card_nums, username: str):
        """Set the content of each card space, fade in the card if it is new and display the user that dropped it"""
        for i, card_num in enumerate(card_nums):
            print(f"Previous card = {self.card_spaces[i].card}/"
                  f"New card = {card_num}")
            fade_in = False


            if card_num:
                if not self.card_spaces[i].card:
                    fade_in = True
                elif self.card_spaces[i].card:
                    if self.card_spaces[i].card.id_num != card_num:
                        fade_in = True

            self.card_spaces[i].set_content(card_num)
            if fade_in:
                self.update_text_offset = i * 147
                print(f"Fading in card {card_num}")
                self.set_text(username)
                self.card_spaces[i].card.start_fade()

    def fade_in_card(self, card: MoveableCard):
        card.start_fade()

    def fade_in_card_num(self, card_num: int):
        if self.card_spaces:
            for space in self.card_spaces:
                if not space.card:
                    continue
                if space.card.id_num == card_num:
                    space.card.start_fade()

    def try_right_click(self) -> Optional[int]:
        return self.super_try_right_click(self.fade_in_card)

    def drop_card(self, card: MoveableCard) -> bool:
        return self.super_drop_card(card, self.fade_in_card)

    def draw(self, surf: pg.Surface):
        super(DropZone, self).draw(surf)
        if self.alpha > 0:
            self.alpha -= 1
            self.text.set_alpha(self.alpha)
        surf.blit(self.text, (self.origin[0] + self.update_text_offset, self.origin[1] - 50))


class HandZone(CardZone):
    """Four card area for the player's hand"""
    def __init__(self, coor: Vector2):
        super(HandZone, self).__init__(coor, num_cards=4)

    # all these methods should have no effect
    def return_content(self) -> None:
        pass

    def set_content(self, card_nums):
        pass

    def try_right_click(self) -> None:
        pass

    def drop_card(self, card: MoveableCard) -> bool:
        return self.super_drop_card(card, None)
    
    def draw(self, surf: pg.Surface):
        for card_space in self.card_spaces:
            pg.draw.rect(surf, (60, 60, 60), card_space.rect, width=3, border_radius=5)
        super(HandZone, self).draw(surf)


class CardSpace(BasicCard):
    """Space that may contain a MoveableCard"""
    def __init__(self, coor: Vector2):
        super().__init__(coor)
        self.card: Optional[MoveableCard] = None
        MoveableCard.convert_imgs()

    def check_mouse(self, mouse_coor: Vector2):
        super().check_mouse(mouse_coor)
        if self.card:
            self.card.check_mouse(mouse_coor)

    def drop_card(self, card) -> bool:
        if self.hover:
            self.card = card
            card.drop(self.rect.topleft)
            return True
        else:
            return False

    def pickup_card(self) -> Optional[MoveableCard]:
        if self.hover:
            picked_card = self.card
            self.card = None
            print("Calling pickup card")
            return picked_card

    def try_click(self) -> Optional[MoveableCard]:
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

    def return_content(self) -> Optional[int]:
        if self.card:
            return self.card.id_num
        else:
            return None

    def set_content(self, card_num: int):
        if card_num or card_num == 0:
            self.card = MoveableCard(self.rect.topleft, card_num)
        else:
            self.card = None

    def draw(self, surf: pg.Surface):
        if self.card:
            self.card.draw(surf)
            
        if self.help:
            pg.draw.rect(surf, (0, 255, 255), self.help_rect, width=2, border_radius=5)
        if self.hover:
            pg.draw.rect(surf, (255, 255, 255), self.rect, width=3, border_radius=5)


class DiscardSpace(CardSpace):
    def __init__(self, coor: Vector2):
        super(DiscardSpace, self).__init__(coor)
        self.graphic = pg.image.load(os.path.join('resources/cards', 'discard.png')).convert_alpha()

    def draw(self, surf: pg.Surface):
        surf.blit(self.graphic, self.rect)
        
        if self.help:
            pg.draw.rect(surf, (0, 255, 255), self.help_rect, width=2, border_radius=5)
        
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

    def drop_card(self, card: MoveableCard) -> bool:
        if self.hover:
            self.card = card
            card.drop(self.rect.topleft)
            card.flip()
            return True
        else:
            return False


class DrawSpace(BasicCard):
    def __init__(self, coor: Vector2):
        super(DrawSpace, self).__init__(coor)
        self.cards: List[MoveableCard] = [MoveableCard(coor, i, True) for i in range(TOTAL_CARDS)]
        shuffle(self.cards)

    def check_mouse(self, mouse_coor: Vector2):
        super().check_mouse(mouse_coor)
        if self.cards:
            self.cards[0].check_mouse(mouse_coor)

    def pickup_card(self) -> Optional[MoveableCard]:
        if self.hover and self.cards:
            picked_card = self.cards.pop()
            print(self.cards)
            return picked_card

    def try_click(self) -> Optional[MoveableCard]:
        if self.cards:
            if self.hover and not self.cards[0].clicked:
                self.cards[0].clicked = True
                picked_card = self.cards.pop(0)
                return picked_card
            elif not self.cards[0].clicked:
                self.cards[0].clicked = False

    def try_right_click(self) -> None:
        pass

    def draw(self, surf: pg.Surface):
        if self.cards:
            self.cards[0].draw(surf)
            
        if self.help:
            pg.draw.rect(surf, (0, 255, 255), self.help_rect, width=2, border_radius=5)

        if self.hover:
            pg.draw.rect(surf, (255, 255, 255), self.rect, width=3, border_radius=5)

    def drop_card(self, card: MoveableCard):
        pass

    def return_content(self) -> Optional[Tuple[int]]:
        if self.cards:

            return tuple([card.id_num for card in self.cards])
        else:
            return None

    def set_content(self, card_nums: Tuple[int], _: str):
        if card_nums:
            self.cards = [MoveableCard(self.rect.topleft, card_num, True) for card_num in card_nums]
        else:
            self.cards = []
            
    
