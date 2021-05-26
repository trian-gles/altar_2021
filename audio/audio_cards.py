from pyo import *
from .dx7 import DX7Poly
from random import uniform, choice, getrandbits

ALL_CARDS = []


class AudioCard:
    def __init__(self):
        ALL_CARDS.append(self)
        self.index = ALL_CARDS.index(self)
        self.orig_param = None
        self.cb = self.callback
        self.levels = None
        self.ratios = None
        self.algo = None

    def apply(self, dx7: DX7Poly, pat: Pattern):
        pass

    def remove(self, dx7: DX7Poly, pat: Pattern):
        pass

    def callback(self, dx7: DX7Poly, pat: Pattern):
        pass

    def set_levels(self, dx7: DX7Poly):
        for i, level in enumerate(self.levels):
            dx7.set_level(i, level)

    def set_ratios(self, dx7: DX7Poly):
        for i, ratio in enumerate(self.ratios):
            dx7.set_ratio(i, ratio)

    def set_algo(self, dx7: DX7Poly):
        dx7.set_algo(self.algo)

    def __repr__(self):
        return f"<Card Num {self.index}>"


class Card0(AudioCard):
    # standard arp pattern
    pass


class Card1(AudioCard):
    # double speed arp pattern
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_param = pat.time
        pat.time = pat.time / 2


class Card2(AudioCard):
    # stuttering times
    def __init__(self):
        super(Card2, self).__init__()
        self.cb = self.callback

    def callback(self, dx7: DX7Poly, pat: Pattern):
        print("Calling card 2 callback")
        pat.time = uniform(0, 1)


class Card3(AudioCard):
    # soft swelling tones
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_attack = [dx7.get_attack(i) for i in range(6)]
        print(self.orig_attack)
        for i in range(6):
            dx7.set_attack(i, random.uniform(1, 2))
        for i in range(6):
            dx7.set_level(i, random.uniform(0, .2))


class Card4(AudioCard):
    # soft percussion
    rhythm_pattern = (0.14, 0.14, 0.7)

    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_level = [dx7.get_attack(i) for i in range(6)]

        for i in range(6):
            dx7.set_attack(i, random.uniform(0.001, 0.01))
        for i in range(6):
            dx7.set_level(i, random.uniform(0, .4))

    def callback(self, dx7: DX7Poly, pat: Pattern):
        pat.time = random.choice(self.rhythm_pattern)


class Card5(AudioCard):
    # octave doubler
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]
        print(self.orig_ratios)

        for i, ratio in enumerate(self.orig_ratios):
            dx7.set_ratio(i, ratio * 2)


class Card6(AudioCard):
    # round ratios
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]
        print(self.orig_ratios)

        for i, ratio in enumerate(self.orig_ratios):
            dx7.set_ratio(i, int(ratio))


class Card6B(AudioCard):
    # round some ratios
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]
        print(self.orig_ratios)

        for i, ratio in enumerate(self.orig_ratios):
            if getrandbits(1):
                dx7.set_ratio(i, int(ratio))


class Card7(AudioCard):
    # round ratios to .5
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]
        print(self.orig_ratios)

        for i, ratio in enumerate(self.orig_ratios):
            new_rat = int(ratio * 2) / 2
            dx7.set_ratio(i, new_rat)


class Card7B(AudioCard):
    # round some ratios to .5
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]
        print(self.orig_ratios)

        for i, ratio in enumerate(self.orig_ratios):
            new_rat = int(ratio * 2) / 2
            if getrandbits(1):
                dx7.set_ratio(i, new_rat)


class Card8(AudioCard):
    # completely destroy ratios
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]
        print(self.orig_ratios)

        for i, ratio in enumerate(self.orig_ratios):
            new_rat = ratio + uniform(-.5, .5)
            dx7.set_ratio(i, new_rat)


class Card8B(AudioCard):
    # completely destroy some ratios
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]
        print(self.orig_ratios)

        for i, ratio in enumerate(self.orig_ratios):
            new_rat = ratio + uniform(-.5, .5)
            dx7.set_ratio(i, new_rat)


class Card9(AudioCard):
    # static card
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.levels = (.13, .9, .93, .8, .87, .16)
        self.ratios = (1.3, 1.2, 5.6, 1.1, 6.1, 6.1)
        self.algo = 2
        self.set_levels(dx7)
        self.set_ratios(dx7)
        self.set_algo(dx7)


audio_cards = [AudioCard(), Card9(), Card6(), Card8(), Card7(), Card6(), Card5(), Card3(), Card1(), Card2(), Card4()]