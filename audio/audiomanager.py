from pyo import *
from .dx7_gradual import DX7Poly
from .audio_cards import ALL_CARDS, AudioCard
from time import time
from random import uniform, choice
import os
from numpy import mean
from typing import Tuple, Optional, List
from itertools import cycle

# type aliases
DropZoneContent = Tuple[Optional[int], Optional[int], Optional[int]]
AudioZoneStatus = Tuple[Optional[str], Optional[str], Optional[str]]


class AudioManager:
    def __init__(self):
        self.zones = (ZoneOne(), ZoneTwo(), ZoneThree())

        # prevent global colored cards from reapplying every turn
        self.added_gaps = False
        self.randomized_all = False
        self.all_tonal = False
        self.GLOB_PATTERNS = cycle(([48, 51, 55, 56, 51, 58],
                                    [48, 51, 55, 56, 51, 59],
                                    [49, 51, 55, 56, 51, 58]))
        Zone.glob_pattern = next(self.GLOB_PATTERNS)
        self.current_pat_num = 0
        print(Zone.glob_pattern)

        for zone in self.zones:
            # zone.dx7.randomize_all()
            for i in range(6):
                zone.dx7.set_level(i, uniform(0, .4))

    def input(self, msg: Tuple[DropZoneContent, DropZoneContent, DropZoneContent]):

        # special cards affecting all zones, checked before normal card applications
        full_msg = msg[0] + msg[1] + msg[2]
        if 21 in full_msg:
            if not self.randomized_all:
                self.randomize_all()
        else:
            self.randomized_all = False
        if 22 in full_msg:
            if not self.all_tonal:
                self.make_tonal_all()
        else:
            self.all_tonal = False

        # this needs work
        if 26 in full_msg:
            if not self.added_gaps:
                self.added_gaps = True
                self.add_gaps(Zone.glob_pattern)
        else:
            self.remove_pat_gaps()

        for i, zone in enumerate(self.zones):
            zone.input(msg[i])
        self.check_all_acted_on()

    def force_input(self, card_num: int, zone_num: int):
        # forces the selected card to have its effect on the indicated zone
        self.zones[zone_num].force_apply(card_num)

        if card_num == 21:
            self.randomize_all()
        elif card_num == 22:
            self.make_tonal_all()
        elif card_num == 26:
            self.add_gaps(Zone.glob_pattern)

        self.check_all_acted_on()

    def randomize_all(self):
        for zone in self.zones:
            zone.dx7.randomize_all()
            zone.pattern.time = uniform(.2, 1.5)
        self.randomized_all = True
        self.advance_pattern()

    def make_tonal_all(self):
        for zone in self.zones:
            orig_ratios = [zone.dx7.get_ratio(i) for i in range(6)]
            for i, ratio in enumerate(orig_ratios):
                new_rat = int(ratio)
                zone.dx7.set_ratio(i, new_rat)
        self.all_tonal = True

        self.advance_pattern()

    def add_gaps(self, p: list):
        for _ in range(3):
            for loc in (1, 5, 6, 8):
                p.insert(loc, None)

    def remove_pat_gaps(self):
        if self.added_gaps:
            Zone.glob_pattern = list(filter(lambda note: note, Zone.glob_pattern))
            self.added_gaps = False

    def check_status(self) -> Tuple[AudioZoneStatus, AudioZoneStatus, AudioZoneStatus]:
        """Get info on each zone for the GFX manager"""
        return tuple([zone.check_status() for zone in self.zones])

    def advance_pattern(self):
        """Next melodic pattern"""
        Zone.glob_pattern = next(self.GLOB_PATTERNS)
        for z in self.zones:
            z.acted_on = False

        # space out the notes if the tree card is still active
        if self.added_gaps:
            self.add_gaps(Zone.glob_pattern)

        self.current_pat_num = (self.current_pat_num + 1) % 3

    def check_all_acted_on(self):
        """Go to the next melodic pattern if all zones have been acted on"""
        acted_tups = map(lambda zone: zone.acted_on, self.zones)
        if all(acted_tups):
            self.advance_pattern()


    def test_lag(self):
        pass


class Zone:
    glob_pattern: List[Optional[int]] = [48, 51, 55, 56, 51, 58]
    glob_pat_count = 0
    # shared global pattern that the three zones will loop through together

    def __init__(self, pan: float, zone_num: int):
        self.dx7 = DX7Poly(4, pan=pan)
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
        self.trans_cb = None
        self.zone_num = zone_num
        self.acted_on = False

    def input(self, msg: Tuple[Optional[int], Optional[int], Optional[int]]):

        active_nums = [card_num for card_num in msg if card_num is not None]
        for card_num in active_nums:
            self.try_apply(card_num)

        remove_cards = list(filter(lambda card: card.index not in msg, self.applied_cards))
        for card in remove_cards:
            self.remove_card(card)

        if self.applied_cards and not self.pattern.isPlaying():
            self.pattern.play()
        elif not self.applied_cards and self.pattern.isPlaying():
            self.pattern.stop()

    def try_apply(self, card_num: int):
        # check if the card is not yet accounted for in the hand and then apply it
        if ALL_CARDS[card_num] not in self.applied_cards:
            new_card = ALL_CARDS[card_num]
            self.applied_cards.append(new_card)
            new_card.apply(self.dx7, self.pattern)
            self.callbacks.append(new_card.callback)
            if new_card.trans_cb:
                self.trans_cb = new_card.trans_cb

            # mark this zone as recently updated
            print(f"Applying card {card_num} to zone {self.zone_num}")
            self.acted_on = True

    def force_apply(self, card_num: int):
        card = ALL_CARDS[card_num]
        card.apply(self.dx7, self.pattern)

        # mark this zone as recently updated
        print(f"Reactivating {card_num} on zone {self.zone_num}")
        self.acted_on = True

    def remove_card(self, card: AudioCard):
        card.remove(self.dx7, self.pattern)
        if card.callback in self.callbacks:
            self.callbacks.remove(card.callback)

        if card.trans_cb and (card.trans_cb == self.trans_cb):
            self.trans_cb = None

        self.applied_cards.remove(card)

    def play(self):
        if self.callbacks:
            for cb in self.callbacks:
                cb(self.dx7, self.pattern)

        if self.trans_cb:
            self.trans = self.trans_cb()

        if Zone.glob_pat_count >= len(Zone.glob_pattern):
            Zone.glob_pat_count = 0
        if self.glob_pattern[Zone.glob_pat_count]:
            freq = note_to_freq(self.glob_pattern[Zone.glob_pat_count] + self.trans)
            self.dx7.noteon(freq, 1)
        Zone.glob_pat_count += 1

    def load(self, filename: str):
        path = os.path.join("resources/settings", filename)
        file = open(path)
        self.dx7.load(file)

    def check_status(self) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        if self.pattern.isPlaying():
            msg = (self.check_atonal(), self.check_levels(), self.check_register())
            return msg
        else:
            return tuple((None, None, None))

    def check_atonal(self) -> Optional[str]:
        ratios = [self.dx7.get_ratio(i) for i in range(6)]
        total_offset = 0
        for r in ratios:
            offset = (r * 2) - (round(r * 2))
            total_offset += offset

        if total_offset > .3:
            return "atonal"
        if total_offset == 0:
            return "tonal"

    def check_register(self) -> Optional[str]:
        ratios = [self.dx7.get_ratio(i) for i in range(6)]
        avg_rat = mean(ratios)
        if avg_rat > 10:
            return "high"
        elif avg_rat < 1:
            return "low"

    def check_levels(self) -> Optional[str]:
        levels = [self.dx7.get_level(i) for i in range(6)]
        if mean(levels) > 0.6:
            return "static"
        elif mean(levels) < 0.1:
            return "quiet"


class ZoneOne(Zone):
    def __init__(self):
        super().__init__(0.5, 0)
        self.load("soft_steel_perc.json")


class ZoneTwo(Zone):
    def __init__(self):
        super().__init__(0.3, 1)
        self.load("organ_bell.json")
        self.pattern.time = .75


class ZoneThree(Zone):
    def __init__(self):
        super().__init__(0.8, 2)
        self.load("harmonica.json")
        self.pattern.time = 1.5


def note_to_freq(pitch: float) -> float:
    a = 440
    return (a / 32) * (2 ** ((pitch - 9) / 12))
