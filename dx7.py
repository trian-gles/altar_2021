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
        self.calldecay = None
        self.mixed = None

    def modulate_phase(self, modding, ctrl):
        print(f"modulating phase of {self.name} by {modding.name}")
        self.cos.input += (modding.output * ctrl)

    def change_pitch(self, freq):
        self.phasor.freq = freq * self.ratio

    def out(self, out_ctrl):
        self.mixed = self.output.mix(2) * out_ctrl * 0.3
        self.mixed.out()


class DX7:
    def __init__(self, attack=.005, decay=.5, sustain=.5, release=1.0):
        self.vel = Sig(0)
        DXSineModule.env = MidiAdsr(self.vel, attack, decay, sustain, release)
        DXSineModule.env.ctrl()
        self.module_1 = DXSineModule("1", ratio=.5)
        self.module_2 = DXSineModule("2", ratio=.5)
        self.module_3 = DXSineModule("3", ratio=.5)
        self.module_4 = DXSineModule("4", ratio=.5)
        self.module_5 = DXSineModule("5", ratio=.5)
        self.module_6 = DXSineModule("6", ratio=.5)
        self.all_mods = (self.module_1, self.module_2, self.module_4, self.module_3, self.module_5, self.module_6)
        self.master_feedback = Sig(1.0)
        self.master_feedback.ctrl([SLMap(0, 8.0, 'lin', 'value', 1)], title="Master Feedback")

        # Store Sig() objects to set each module connection in a dictionary
        self.routes = {}
        for modding in self.all_mods:
            for modded in self.all_mods:
                ctrl_sig = Sig(0)
                title = f"{modding.name}{modded.name}"
                print(f"Storing route {title}")
                self.routes[title] = ctrl_sig

                # ctrl_sig.ctrl([SLMap(0, 8.0, 'lin', 'value', 0)], title=title + " route control")

                if modding.name == modded.name:
                    # Modules that feedback into themselves are multiplied by a master feedback control
                    modded.modulate_phase(modded, self.routes[title] * self.master_feedback)
                    print(f"Route {title} gets attached to master feedback")

                else:
                    modded.modulate_phase(modding, self.routes[title])

            out_sig = Sig(0)
            title = f"{modding.name}out"
            self.routes[title] = out_sig
            print(f"Storing route {title}")
            modding.out(out_sig)
            # out_sig.ctrl([SLMap(0, 1.0, 'lin', 'value', 0)], title=f"{in_mod_count} output control")

        # Module connections are shown for each algorithm
        self.ALGORITHMS = (
            ('1out', '21', '66', '65', '54', '43', '3out'),
            ('11', '1out'),
            (),
            ()
        )

        self.set_algo(1)
        print(self.routes)

    def set_algo(self, algo_num):
        self.reset_routes()
        print(f"Switching to algorithm {algo_num}")
        for route in self.ALGORITHMS[algo_num]:
            print(f"Activating route {route}")
            self.routes[route].value = 1.0



    def reset_routes(self):
        print("Resetting all routes")
        for route in self.routes.values():
            route.value = 0

    def noteon(self, freq, vel):
        self.vel.value = vel
        for module in self.all_mods:
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