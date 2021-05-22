from pyo import *
from .dx7 import DX7Poly


ALL_CARDS = []


class AudioCard:
    def __init__(self):
        ALL_CARDS.append(self)
        self.index = ALL_CARDS.index(self)
        self.orig_param = None

    def apply(self, dx7: DX7Poly, pat: Pattern):
        pass

    def remove(self, dx7: DX7Poly, pat: Pattern):
        pass

    def __repr__(self):
        return f"<Card Num {self.index}>"


class Card0(AudioCard):
    pass


class Card1(AudioCard):
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_param = pat.time
        pat.time = pat.time / 2
        print("Calling card 1 apply function")

    def remove(self, dx7: DX7Poly, pat: Pattern):
        pat.time = self.orig_param


audio_cards = [Card0(), Card1()] + [AudioCard() for _ in range(50)]