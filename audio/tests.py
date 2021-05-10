import unittest
from pyo import *
from dx7 import DX7Poly

s = Server().boot()


class TestDX7(unittest.TestCase):
    def setUp(self):
        self.synth = DX7Poly(4)

    def test_algo(self):
        self.synth.set_algo(5)
        self.assertEqual(5, self.synth.get_algo())

    def test_level(self):
        self.synth.set_level(2, .7)
        self.assertEqual(.7, self.synth.get_level(2))

    def test_attack(self):
        self.synth.set_attack(4, .2)
        self.assertEqual(.2, self.synth.get_attack(4))

if __name__ == "__main__":
    unittest.main()