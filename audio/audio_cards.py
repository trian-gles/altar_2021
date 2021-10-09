from pyo import *
from .dx7_gradual import DX7Poly
from random import uniform, getrandbits, randrange
from itertools import cycle

ALL_CARDS = []


class AudioCard:
    def __init__(self):
        ALL_CARDS.append(self)
        self.index = ALL_CARDS.index(self)
        self.orig_param = None
        self.levels = None # use these, they are useful!!!
        self.ratios = None
        self.algo = None
        self.trans_cb = None

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

    def load(self, filename, dx7: DX7Poly):
        path = os.path.join("audio/settings", filename)
        file = open(path)
        dx7.load(file)

    def __repr__(self):
        return f"<Card Num {self.index}>"


class Card0(AudioCard):
    # half speed arp pattern
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_param = pat.time
        pat.time = pat.time * 2


class Card1(AudioCard):
    # double speed arp pattern
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_param = pat.time
        pat.time = pat.time / 2


class Card2(AudioCard):
    # stuttering times
    def __init__(self):
        super(Card2, self).__init__()

    def callback(self, dx7: DX7Poly, pat: Pattern):
        pat.time = uniform(0, 1)


class Card3(AudioCard):
    # soft swelling tones
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_attack = [dx7.get_attack(i) for i in range(6)]
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
    # octave up NEEDS IMAGE
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]

        for i, ratio in enumerate(self.orig_ratios):
            dx7.set_ratio(i, ratio * 2)


class Card6(AudioCard):
    # round ratios
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]

        for i, ratio in enumerate(self.orig_ratios):
            dx7.set_ratio(i, int(ratio))


class Card7(AudioCard):
    # round some ratios
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]
        print(self.orig_ratios)

        for i, ratio in enumerate(self.orig_ratios):
            if getrandbits(1):
                dx7.set_ratio(i, int(ratio))


class Card8(AudioCard):
    # round ratios to .5
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]

        for i, ratio in enumerate(self.orig_ratios):
            new_rat = (int(ratio * 2) + randrange(-1, 1)) / 2
            dx7.set_ratio(i, new_rat)


class Card9(AudioCard):
    # round some ratios to .5
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]
        print(self.orig_ratios)

        for i, ratio in enumerate(self.orig_ratios):
            new_rat = (int(ratio * 2) + randrange(-1, 1)) / 2
            if getrandbits(1):
                dx7.set_ratio(i, new_rat)


class Card10(AudioCard):
    # completely destroy ratios
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]

        for i, ratio in enumerate(self.orig_ratios):
            new_rat = ratio + uniform(-.5, .5)
            dx7.set_ratio(i, new_rat)


class Card11(AudioCard):
    # completely destroy some ratios
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]

        for i, ratio in enumerate(self.orig_ratios):
            new_rat = ratio + uniform(-.5, .5)
            dx7.set_ratio(i, new_rat)


class Card12(AudioCard):
    # static card
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.levels = (.13, .9, .93, .8, .87, .16)
        self.ratios = (1.3, 1.2, 5.6, 1.1, 6.1, 6.1)
        self.algo = 2
        self.set_levels(dx7)
        self.set_ratios(dx7)
        self.set_algo(dx7)


class Card13(AudioCard):
    # random card
    def apply(self, dx7: DX7Poly, pat: Pattern):
        dx7.randomize_all()
        pat.time = uniform(0, 1)


class Card14(AudioCard):
    # octave down
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]
        for i, ratio in enumerate(self.orig_ratios):
            dx7.set_ratio(i, ratio / 2)


class Card15(AudioCard):
    # normal speed
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_param = pat.time
        pat.time = 1


class Card16(AudioCard):
    # many octaves up
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]

        for i, ratio in enumerate(self.orig_ratios):
            dx7.set_ratio(i, ratio * 8)


class Card17(AudioCard):
    # many octaves down
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_ratios = [dx7.get_ratio(i) for i in range(6)]

        for i, ratio in enumerate(self.orig_ratios):
            dx7.set_ratio(i, ratio / 8)


class Card18(AudioCard):
    # quiet
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_levs = [dx7.get_level(i) for i in range(6)]

        for i, lev in enumerate(self.orig_levs):
            new_lev = lev / 4
            dx7.set_level(i, new_lev)


class Card19(AudioCard):
    # silence
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_levs = [dx7.get_level(i) for i in range(6)]

        for i, lev in enumerate(self.orig_levs):
            new_lev = lev / 10
            dx7.set_level(i, new_lev)

#    def remove(self, dx7: DX7Poly, pat: Pattern):
#        for i, lev in enumerate(self.orig_levs):
#            dx7.set_level(i, lev)


class Card20(AudioCard):
    # randomizes every note
    def __init__(self):
        super().__init__()

    def callback(self, dx7: DX7Poly, pat: Pattern):
        if getrandbits(1):
            dx7.randomize_all()


class Card21(AudioCard):
    # moon card
    pass


class Card22(AudioCard):
    # sun card
    pass


class Card23(AudioCard):
    # change algo
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.orig_algo = dx7.get_algo()
        new_algo = (self.orig_algo + 5) % 11
        dx7.set_algo(new_algo)


class Card24(AudioCard):
    # algo every cycle
    def __init__(self):
        super().__init__()
        self.count = 0

    def callback(self, dx7: DX7Poly, pat: Pattern):
        self.count = (self.count + 1) % 4
        if self.count == 0:
            self.orig_algo = dx7.get_algo()
            new_algo = (self.orig_algo + 5) % 11
            dx7.set_algo(new_algo)


class Card25(AudioCard):
    # sharp attacks card
    def apply(self, dx7: DX7Poly, pat: Pattern):
        self.load("sharp_attacks.json", dx7)

class Card26(AudioCard):
    # tree card
    pass


class Card27(AudioCard):
    # moderate transposition card
    def __init__(self):
        super(Card27, self).__init__()
        self.trans_vals = cycle((12, 0, -12, 0))
        self.trans_cb = self.cb
        self.trans_return = 0

    def cb(self):
        if getrandbits(1):
            self.trans_return = next(self.trans_vals)

        return self.trans_return


class Card28(Card27):
    # crazy transposition card
    def __init__(self):
        super().__init__()
        self.trans_vals = cycle((12, 0, 7, 24, -12, 0, -7, 7))


audio_cards = [Card0(), Card1(), Card2(), Card3(), Card4(), Card5(), Card6(), Card7(), Card8(), Card9(), Card10(),
               Card11(), Card12(), Card13(), Card14(), Card15(), Card16(), Card17(), Card18(), Card19(), Card20(),
               Card21(), Card22(), Card23(), Card24(), Card25(), Card26(), Card27(), Card28()]
