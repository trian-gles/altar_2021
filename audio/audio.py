from pyo import *
from .dx7 import DX7Poly
from .audio_cards import ALL_CARDS



class AudioManager:
    def __init__(self):
        self.server = Server().boot()
        self.server.start()
        self.zones = (ZoneOne(), ZoneTwo(), ZoneThree())

    def input(self, msg):
        # Messages should be a tuple of three tuples, each inner tuple providing three elements of instructions ((1, 2, 3), (None, 5, 8), (2, 5, 8))
        for i, zone in enumerate(self.zones):
            zone.input(msg[i])

    def close(self):
        self.server.stop()


class Zone:
    def __init__(self):
        self.dx7 = DX7Poly(8)
        self.trans = 0
        self.count = 0
        self.pattern_count = 0
        self.pattern = Pattern(self.play, 0.2)
        self.applied_cards = []
        self.notes = (48, 51, 55, 56, 51, 58)

    def input(self, msg):
        for card_num in msg:
            if card_num or card_num == 0:
                self.apply_card(card_num)

    def apply_card(self, card_num):
        self.applied_cards.append(ALL_CARDS[card_num])
        print(self.applied_cards)
        if self.applied_cards and not self.pattern.isPlaying():
            print("Playing zone")
            self.pattern.play()

    def play(self):
        self.dx7.randomize_all()
        self.dx7.noteon(220, 1)



class ZoneOne(Zone):
    pass


class ZoneTwo(Zone):
    pass


class ZoneThree(Zone):
    pass


class Node:
    pass
