import unittest


from pyo import *
from audio.dx7 import DX7Poly, DX7Mono, DXSineModule
from audio.audiomanager import Zone, AudioManager
from audio.audio_cards import ALL_CARDS


class AudioTest(unittest.TestCase):
    s = None

    @classmethod
    def setUpClass(cls):
        cls.s = Server().boot()

    @classmethod
    def tearDownClass(cls):
        cls.s.shutdown()


class TestDX7Poly(AudioTest):
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

    def test_poly(self):
        self.synth.noteon(40, 1)
        self.assertEqual(self.synth.active_voice, self.synth.voices[1])


class TestDX7Mono(AudioTest):
    def setUp(self):
        self.synth = DX7Mono()

    def test_algo(self):
        self.synth.set_algo(5)
        self.assertEqual(self.synth.algo_num, 5)


class TestDX7Sine(AudioTest):
    def setUp(self):
        self.synth = DXSineModule(0)


class TestZone(AudioTest):
    def setUp(self):
        self.zone = Zone(0)

    def test_input(self):
        self.zone.input((0, 1, 2))
        self.assertTrue(self.zone.pattern.isPlaying())
        self.assertEqual(self.zone.applied_cards, [ALL_CARDS[i] for i in range(3)])
        self.zone.input((0, 1, 2))
        self.assertEqual(self.zone.applied_cards, [ALL_CARDS[i] for i in range(3)])

    def test_remove(self):
        self.zone.input((0, 1, None))
        self.assertEqual(self.zone.applied_cards, [ALL_CARDS[i] for i in range(2)])
        self.zone.input((None, None, None))
        self.assertEqual(self.zone.applied_cards, [])
        self.assertFalse(self.zone.pattern.isPlaying())

    def test_status(self):
        self.zone.input((12, None, None))
        self.assertEqual(self.zone.check_status()[0:2], ('atonal', 'static'))
        self.zone.input((19, None, None))
        self.assertEqual(self.zone.check_status()[1], 'quiet')


class TestAM(AudioTest):
    basic_hand = (0, None, None)

    def setUp(self):
        self.am = AudioManager()

    def test_random_and_tonal(self):
        self.am.input(((21, None, None), self.basic_hand, self.basic_hand))
        self.am.input(((22, None, None), self.basic_hand, self.basic_hand))
        for tup in self.am.check_status():
            self.assertEqual(tup[0], "tonal")

    def test_tree_card(self):
        self.am.input(((26, None, None), self.basic_hand, self.basic_hand))
        desired_pat = [48, None, None, None, 51, None, None, 55, None, None, None, 56, None, None, None, 51, None, 58]
        self.assertEqual(self.am.zones[0].glob_pattern, desired_pat)


if __name__ == "__main__":
    unittest.main()