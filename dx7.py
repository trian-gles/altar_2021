from pyo import *
from random import randrange
import math


s = Server().boot()


class DXSineModule:

    def __init__(self, name, ratio=1.0, level=1.0):
        self.env = Adsr(dur=2)

        self.name = name
        self.ratio = Sig(ratio)
        # self.ratio.ctrl([SLMap(0, 8.0, 'lin', 'value', ratio)], title=f"{name} ratio")
        self.phasor = Phasor(200)
        self.level = Sig(level)
        # self.level.ctrl([SLMapMul(init=level)], title=f"{name} level")
        self.cos = Cos(input=self.phasor, mul=self.env)
        self.output = self.level * self.cos
        self.mixed = None
        self.inputs = [self.phasor]

    def patch(self, modding):
        self.inputs += modding

    def configure_input(self):
        self.cos.input = sum(self.inputs) * math.pi*2

    def reset(self):
        self.inputs = [self.phasor]
        self.cos.input = self.phasor
        self.mixed = None

    def change_pitch(self, freq):
        self.phasor.freq = freq * self.ratio
        self.env.play()

    def out(self):
        self.mixed = self.output.mix(2) * 0.3
        self.mixed.out()


class DX7Mono:
    # Module connections are shown for each algorithm.  0 indicates output
    ALGORITHMS = (
        ((1, 0), (2, 1), (6, 6), (6, 5), (5, 4), (4, 3), (3, 0)),
        ((1, 0), (2, 1), (2, 2), (6, 5), (5, 4), (4, 3), (3, 0)),
        ((3, 2), (2, 1), (1, 0), (6, 5), (5, 4), (4, 3), (6, 6)),
        ((3, 2), (2, 1), (1, 0), (6, 5), (5, 4), (4, 3), (6, 0))
    )

    def __init__(self):
        self.vel = Sig(0)
        self.mod_dict = {}
        for mod_num in range(6):
            self.mod_dict[mod_num + 1] = DXSineModule(mod_num + 1)
        self.master_feedback = Sig(1.0)
        # self.master_feedback.ctrl([SLMap(0, 8.0, 'lin', 'value', 1)], title="Master Feedback")
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


class DX7Poly:
    def __init__(self, voices):
        self.voices = [DX7Mono() for _ in range(voices)]
        self.voice_num = voices
        self.active_voice_num = 0
        self.active_voice = self.voices[0]

    def noteon(self, freq, vel):
        self.active_voice.noteon(freq, vel) # WTF IS WRONG HERE
        self.active_voice_num = (self.active_voice_num + 1) % self.voice_num
        self.active_voice = self.voices[self.active_voice_num]

    def set_algo(self, algo_num):
        for voice in self.voices:
            voice.set_algo(algo_num)

    def randomize_ratios(self):
        for mod_num in range(6):
            rand_ratio = (random.randrange(0, 6) / 2) + 0.5
            for voice in self.voices:
                voice.mod_dict[mod_num + 1].ratio.value = rand_ratio

    def randomize_envs(self):
        for mod_num in range(6):
            attack = random.uniform(0.002, 0.02)
            decay = random.uniform(0.1, 0.5)
            sustain = random.uniform(0.1, 0.9)
            release = random.uniform(0.8, 1.4)
            for voice in self.voices:
                env = voice.mod_dict[mod_num + 1].env
                env.attack, env.decay, env.sustain, env.release = attack, decay, sustain, release

    def randomize_levels(self):
        for mod_num in range(6):
            level = random.random()
            for voice in self.voices:
                voice.mod_dict[mod_num + 1].level.value = level

    def randomize_all(self):
        self.randomize_levels()
        self.randomize_ratios()
        self.randomize_envs()
        self.randomize_algo()

    def randomize_algo(self):
        self.set_algo(random.randrange(0, len(DX7Mono.ALGORITHMS)))


c = None

synth = DX7Poly(8)
synth.randomize_all()

pattern = (48, 51, 55, 56, 51, 58)
pattern_count = 0

def note():
    global c
    global pattern_count
    freq = note_to_freq(pattern[pattern_count] + 24)
    synth.noteon(freq, 1)
    pattern_count = (pattern_count + 1) % 6


def note_to_freq(pitch):
    a = 440
    return (a / 32) * (2 ** ((pitch - 9) / 12))


p = Pattern(note, 0.2)
p.play()
p.ctrl()


s.gui(locals())