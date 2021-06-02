from pyo import *
from .dx7 import DX7Poly
from .audio_cards import ALL_CARDS, AudioCard
from time import time
from random import uniform
import os
from numpy import mean


class AudioManager:
    def __init__(self):
        self.server = Server().boot()
        self.server.start()
        self.zones = (ZoneOne(), ZoneTwo(), ZoneThree())
        self.added_gaps = False
        for zone in self.zones:
            #zone.dx7.randomize_all()
            for i in range(6):
                zone.dx7.set_level(i, uniform(0, .4))

    def input(self, msg):
        # Messages should be a tuple of three tuples, each inner tuple providing three elements of instructions ((1, 2, 3), (None, 5, 8), (2, 5, 8))
        for i, zone in enumerate(self.zones):
            zone.input(msg[i])

        # special cards affecting all zones
        for zone_msg in msg:
            if 21 in zone_msg:
                self.randomize_all()
            elif 22 in zone_msg:
                self.make_tonal_all()
            if 26 in zone_msg:
                self.add_gaps()
            else:
                self.remove_gaps()

        self.check_status()

    def randomize_all(self):
        for zone in self.zones:
            zone.dx7.randomize_all()
            zone.pattern.time = uniform(.2, 1.5)

    def make_tonal_all(self):
        for zone in self.zones:
            orig_ratios = [zone.dx7.get_ratio(i) for i in range(6)]
            for i, ratio in enumerate(orig_ratios):
                new_rat = int(ratio)
                zone.dx7.set_ratio(i, new_rat)

    def add_gaps(self):
        if not self.added_gaps:
            for _ in range(3):
                for loc in (1, 5, 6, 8):
                    Zone.glob_pattern.insert(loc, None)
            self.added_gaps = True

    def remove_gaps(self):
        if self.added_gaps:
            Zone.glob_pattern = [48, 51, 55, 56, 51, 58]
            self.added_gaps = False

    def check_status(self):
        for zone in self.zones:
            print(zone.check_status())


    def test_lag(self):
        pass

    def close(self):
        self.server.stop()



class Zone:
    glob_pattern = [48, 51, 55, 56, 51, 58]
    glob_pat_count = 0
    # shared global pattern that the three zones will loop through together

    def __init__(self):
        self.dx7 = DX7Poly(4)
        self.trans = 0
        self.count = 0
        self.pattern_count = 0
        self.pattern = Pattern(self.play, 1)
        self.card_nums = []
        self.applied_cards = []
        self.notes = (48, 51, 55, 56, 51, 58)
        self.last_time = time()
        self.card_callback = None
        self.callbacks = []

    def input(self, msg):
        for card_num in msg:
            if card_num or card_num == 0:
                self.apply_card(card_num)
        for card in self.applied_cards:
            if card.index not in msg:
                self.remove_card(card)
        if self.applied_cards and not self.pattern.isPlaying():
            self.pattern.play()
        elif not self.applied_cards and self.pattern.isPlaying():
            self.pattern.stop()

    def apply_card(self, card_num):
        # check if the card is not yet accounted for in the hand and then apply it
        if ALL_CARDS[card_num] not in self.applied_cards:
            new_card = ALL_CARDS[card_num]
            self.applied_cards.append(new_card)
            new_card.apply(self.dx7, self.pattern)

            if new_card.cb:
                self.callbacks.append(new_card.cb)

    def remove_card(self, card: AudioCard):
        card.remove(self.dx7, self.pattern)
        if card.cb in self.callbacks:
            self.callbacks.remove(card.cb)

        self.applied_cards.remove(card)

    def play(self):
        # print(self.last_time - time())
        if self.callbacks:
            for cb in self.callbacks:
                cb(self.dx7, self.pattern)
        self.last_time = time()

        if Zone.glob_pat_count >= len(Zone.glob_pattern):
            Zone.glob_pat_count = 0
        if self.glob_pattern[Zone.glob_pat_count]:
            freq = note_to_freq(self.glob_pattern[Zone.glob_pat_count])
            self.dx7.noteon(freq, 1)
        Zone.glob_pat_count += 1

    def load(self, filename):
        path = os.path.join("audio/settings", filename)
        file = open(path)
        self.dx7.load(file)

    def check_status(self):
        if self.pattern.isPlaying():
            msg = [self.check_atonal(), self.check_levels(), self.check_register()]
            return msg

    def check_atonal(self):
        ratios = [self.dx7.get_ratio(i) for i in range(6)]
        total_offset = 0
        for r in ratios:
            offset = (r * 2) - (round(r * 2))
            total_offset += offset

        if total_offset > .3:
            return "atonal"
        if total_offset == 0:
            return "tonal"

    def check_register(self):
        ratios = [self.dx7.get_ratio(i) for i in range(6)]
        avg_rat = mean(ratios)
        if avg_rat > 10:
            return "high"
        elif avg_rat < 1:
            return "low"

    def check_levels(self):
        levels = [self.dx7.get_level(i) for i in range(6)]
        if mean(levels) > 0.6:
            return "static"
        elif mean(levels) < 0.1:
            return "quiet"



class ZoneOne(Zone):
    def __init__(self):
        super().__init__()
        self.load("soft_steel_perc.json")



class ZoneTwo(Zone):
    def __init__(self):
        super().__init__()
        self.load("organ_bell.json")
        self.pattern.time = .75


class ZoneThree(Zone):
    def __init__(self):
        super().__init__()
        self.load("harmonica.json")
        self.pattern.time = 1.5


class Node:
    pass


def note_to_freq(pitch):
    a = 440
    return (a / 32) * (2 ** ((pitch - 9) / 12))