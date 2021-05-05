from pyo import *
import random
import math


s = Server().boot()


all_sines = []


class DXSineModule:
    def __init__(self, ratio=1.0, attack=.005, decay=.5, sustain=.5, release=1.0):
        self.ratio = Sig(ratio)
        self.ratio.ctrl([SLMap(0, 8.0, 'lin', 'value', ratio)])
        self.phasor = Phasor(200, mul=math.pi*2)
        self.vel = Sig(0)
        self.env = MidiAdsr(self.vel, attack, decay, sustain, release)
        self.cos = Cos(input=self.phasor, mul=self.env)
        self.calldecay = None

        all_sines.append(self)

    def modulate_phase(self, modulating_sig):
        self.cos.input += modulating_sig

    def modulate_sine(self, mod_sine):
        self.scaling = Sig(1)
        mod_sine.modulate_phase(self.cos * self.scaling)
        self.scaling.ctrl([SLMap(0, 8, 'lin', 'value', 1)], title="Scaling")

    def noteon(self, freq, vel):
        print("calling noteon")
        self.phasor.freq = freq * self.ratio
        self.vel.value = vel

    def noteoff(self):
        self.vel.value = 0

    def out(self):
        self.mixed = self.cos.mix(2) * 0.3
        self.mixed.out()



c = None


def all_noteoff():
    for sine in all_sines:
        sine.noteoff()


def note():
    global c
    freq = note_to_freq(random.randrange(12, 84))
    for sine in all_sines:
        sine.noteon(freq, 1)
    c = CallAfter(all_noteoff, 1)


def note_to_freq(pitch):
    a = 440
    return (a / 32) * (2 ** ((pitch - 9) / 12))


module_1 = DXSineModule(ratio=.5)
module_2 = DXSineModule(ratio=.5)
module_3 = DXSineModule(ratio=.5)
module_4 = DXSineModule(ratio=.5)
module_5 = DXSineModule(ratio=.5)
module_6 = DXSineModule(ratio=.5)

module_2.modulate_sine(module_1)
module_1.out()

module_6.modulate_sine(module_6)
module_6.modulate_sine(module_5)
module_5.modulate_sine(module_4)
module_4.modulate_sine(module_3)
module_3.out()


p = Pattern(note, 2)
p.play()
