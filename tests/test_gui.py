import unittest
from gui_items.basic_card import BasicCard, MoveableCard
from gui_items.cardspace import CardSpace
import pygame as pg


class TestBasicCard(unittest.TestCase):
    def setUp(self):
        self.card = BasicCard((0, 0))

    def test_hover(self):
        self.card.check_mouse((50, 50))
        self.assertTrue(self.card.hover)
        self.card.check_mouse((300, 300))
        self.assertFalse(self.card.hover)


class TestMoveCard(unittest.TestCase):
    def setUp(self):
        self.move_card = MoveableCard((0, 0))

    def test_hover(self):
        self.move_card.check_mouse((20, 20))
        self.assertTrue(self.move_card.hover)

    def test_drop(self):
        self.move_card.flip()
        self.move_card.drop((500, 500))
        self.assertFalse(self.move_card.flipped)
        self.move_card.check_mouse((520, 520))
        self.assertTrue(self.move_card.hover)


class TestCardSpace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        cls.screen = pg.display.set_mode((1, 1))

    def setUp(self):
        self.card_space = CardSpace((0, 0))

    def test_drop(self):
        self.card_space.check_mouse((0, 0))
        self.assertTrue(self.card_space.hover)
        drop_result = self.card_space.drop_card(MoveableCard((0, 0)))
        self.assertTrue(drop_result)
