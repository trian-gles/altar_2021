from pyo import *
import random
import math


s = Server().boot()


class DXSineModule:
    env = None

    def __init__(self, ratio=1.0, level=1.0):
        self.ratio = Sig(ratio)
        self.ratio.ctrl([SLMap(0, 8.0, 'lin', 'value', ratio)])
        self.phasor = Phasor(200, mul=math.pi*2)
        self.level = Sig(level)
        self.cos = Cos(input=self.phasor, mul=self.env)
        self.output = self.level + self.cos
        self.calldecay = None

    def modulate_phase(self, modulating_sig):
        self.cos.input += modulating_sig

    def change_pitch(self, freq):
        self.phasor.freq = freq * self.ratio

    def out(self, level):
        self.mixed = self.output.mix(2) * level * 0.3
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

        self.routes = {}
        in_mod_count = 1
        for modding in self.all_mods:
            out_mod_count = 1
            for modded in self.all_mods:
                ctrl_sig = Sig(0)
                title = f"{in_mod_count}{out_mod_count}"
                self.routes[title] = ctrl_sig

                #ctrl_sig.ctrl([SLMap(0, 8.0, 'lin', 'value', 0)], title=title + " route control")

                if in_mod_count == out_mod_count:
                    feed_title = f"{in_mod_count} feedback"
                    feed_sig = Sig(0)
                    self.routes[feed_title] = feed_sig
                    #self.routes[feed_title].ctrl([SLMap(0, 8.0, 'lin', 'value', 0)], title=feed_title + " control")
                    modded.modulate_phase(modding.output * ctrl_sig * feed_sig)

                else:
                    modded.modulate_phase(modding.output * ctrl_sig)

                out_mod_count += 1
            out_sig = Sig(0)
            self.routes[f"{in_mod_count}out"] = out_sig
            modding.out(out_sig)
            #out_sig.ctrl([SLMap(0, 1.0, 'lin', 'value', 0)], title=f"{in_mod_count} output control")
            in_mod_count += 1

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