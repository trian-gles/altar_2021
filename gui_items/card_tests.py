import unittest
from cardspace import MoveableCard, CardSpace


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
    def setUp(self):
        self.card_space = CardSpace((0, 0))

    def test_drop(self):
        self.card_space.check_mouse((0, 0))
        self.assertTrue(self.card_space.hover)
        drop_result = self.card_space.drop_card(MoveableCard((0, 0)))
        self.assertTrue(drop_result)


if __name__ == '__main__':
    unittest.main()
