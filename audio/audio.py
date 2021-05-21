from pyo import *
from .dx7 import DX7Poly
from .audio_cards import ALL_CARDS


class AudioManager:
    def __init__(self):
        self.zones = (ZoneOne(), ZoneTwo(), ZoneThree())

    def input(self, msg):
        # Messages should be a tuple of three tuples, each inner tuple providing three elements of instructions ((1, 2, 3), (None, 5, 8), (2, 5, 8))
        for i, zone in enumerate(self.zones):
            zone.input(msg[i])


class Zone:
    def __init__(self):
        self.dx7 = DX7Poly(8)

    def input(self, msg):
        for card_num in msg:
            if card_num:
                self.apply_card(card_num)

    def apply_card(self, card_num):
        print(ALL_CARDS[card_num])


class ZoneOne(Zone):
    pass


class ZoneTwo(Zone):
    pass


class ZoneThree(Zone):
    pass


class Node:
    pass
