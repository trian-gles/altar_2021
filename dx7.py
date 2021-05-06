from pyo import *
import math


s = Server().boot()


class DXSineModule:
    env = None

    def __init__(self, name, ratio=1.0, level=1.0):
        self.name = name
        self.ratio = Sig(ratio)
        self.ratio.ctrl([SLMap(0, 8.0, 'lin', 'value', ratio)], title=f"{name} ratio")
        self.phasor = Phasor(200, mul=math.pi*2)
        self.level = Sig(level)
        self.cos = Cos(input=self.phasor, mul=self.env)
        self.output = self.level * self.cos
        self.mixed = None
        self.inputs = [self.phasor]

    def patch(self, modding):
        self.inputs += modding

    def configure_input(self):
        self.cos.input = sum(self.inputs)

    def reset(self):
        self.inputs = [self.phasor]
        self.cos.input = self.phasor
        self.mixed = None

    def change_pitch(self, freq):
        self.phasor.freq = freq * self.ratio

    def out(self):
        self.mixed = self.output.mix(2) * 0.3
        self.mixed.out()


class DX7:
    def __init__(self, attack=.005, decay=.5, sustain=.5, release=1.0):
        self.vel = Sig(0)
        DXSineModule.env = MidiAdsr(self.vel, attack, decay, sustain, release)
        DXSineModule.env.ctrl()
        self.mod_dict = {}
        for mod_num in range(6):
            self.mod_dict[mod_num + 1] = DXSineModule(0.5)
        self.master_feedback = Sig(1.0)
        self.master_feedback.ctrl([SLMap(0, 8.0, 'lin', 'value', 1)], title="Master Feedback")

        # Module connections are shown for each algorithm
        self.ALGORITHMS = (
            ((1, 0), (2, 1), (6, 6), (6, 5), (5, 4), (4, 3), (3, 0)),
            ((1, 0), (2, 1), (2, 2), (6, 5), (5, 4), (4, 3), (3, 0)),
            ((3, 2), (2, 1), (1, 0), (6, 5), (5, 4), (4, 3))
        )

        self.set_algo(0)

    def set_algo(self, algo_num):
        self.reset_routes()
        print(f"Switching to algorithm {algo_num}")
        for route in self.ALGORITHMS[algo_num]:
            out_num = route[0]
            in_num = route[1]
            if in_num == 0:
                self.mod_dict[out_num].out()
            elif in_num == out_num:
                self.mod_dict[in_num].patch(self.mod_dict[out_num].output * self.master_feedback)
            else:
                self.mod_dict[in_num].patch(self.mod_dict[out_num].output)
        for mod in self.mod_dict.values():
            mod.configure_input()

    def reset_routes(self):
        for mod in self.mod_dict.values():
            mod.reset()

    def noteon(self, freq, vel):
        self.vel.value = vel
        for module in self.mod_dict.values():
            module.change_pitch(freq)

    def noteoff(self):
        self.vel.value = 0


c = None

synth = DX7()


pattern = (48, 51, 55, 56, 51, 58)
pattern_count = 0

def note():
    global c
    global pattern_count
    freq = note_to_freq(pattern[pattern_count] + 24)
    synth.noteon(freq, 1)
    c = CallAfter(synth.noteoff, 0.5)
    pattern_count = (pattern_count + 1) % 6


def note_to_freq(pitch):
    a = 440
    return (a / 32) * (2 ** ((pitch - 9) / 12))


p = Pattern(note, 1)
p.play()


s.gui(locals())