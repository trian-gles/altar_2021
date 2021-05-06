from pyo import *
import random
import math


s = Server().boot()


class DXSineModule:
    env = None

    def __init__(self, ratio=1.0):
        self.ratio = Sig(ratio)
        self.ratio.ctrl([SLMap(0, 8.0, 'lin', 'value', ratio)])
        self.phasor = Phasor(200, mul=math.pi*2)

        self.cos = Cos(input=self.phasor, mul=self.env)
        self.calldecay = None

    def modulate_phase(self, modulating_sig):
        self.cos.input += modulating_sig

    def modulate_sine(self, mod_sine):
        self.scaling = Sig(1)
        mod_sine.modulate_phase(self.cos * self.scaling)
        self.scaling.ctrl([SLMap(0, 8, 'lin', 'value', 1)], title="Scaling")

    def change_pitch(self, freq):
        self.phasor.freq = freq * self.ratio

    def out(self):
        self.mixed = self.cos.mix(2) * 0.3
        self.mixed.out()


class DX7:
    def __init__(self, attack=.005, decay=.5, sustain=.5, release=1.0):
        self.vel = Sig(0)
        DXSineModule.env = MidiAdsr(self.vel, attack, decay, sustain, release)
        DXSineModule.env.ctrl()
        self.module_1 = DXSineModule(ratio=.5)
        self.module_2 = DXSineModule(ratio=.5)
        self.module_3 = DXSineModule(ratio=.5)
        self.module_4 = DXSineModule(ratio=.5)
        self.module_5 = DXSineModule(ratio=.5)
        self.module_6 = DXSineModule(ratio=.5)
        self.all_mods = (self.module_1, self.module_2, self.module_4, self.module_3, self.module_5, self.module_6)

        self.module_2.modulate_sine(self.module_1)
        self.module_1.out()

        self.module_6.modulate_sine(self.module_6)
        self.module_6.modulate_sine(self.module_5)
        self.module_5.modulate_sine(self.module_4)
        self.module_4.modulate_sine(self.module_3)
        self.module_3.out()

    def noteon(self, freq, vel):
        self.vel.value = vel
        for module in self.all_mods:
            module.change_pitch(freq)

    def noteoff(self):
        self.vel.value = 0


c = None

synth = DX7()


def note():
    global c
    freq = note_to_freq(random.randrange(12, 84))
    synth.noteon(freq, 1)
    c = CallAfter(synth.noteoff, 1)


def note_to_freq(pitch):
    a = 440
    return (a / 32) * (2 ** ((pitch - 9) / 12))


p = Pattern(note, 2)
p.play()


s.gui(locals())