from pyo import *
import random
import math
import json


s = Server()


class DXSineModule:
    def __init__(self, master: PyoObject, name: int, ratio: float = 1.0, level: float = 1.0, pan: float = 0.5):
        self.env = Adsr(dur=2)

        self.name = name
        self.ratio = SigTo(ratio, time=1)
        # self.ratio.ctrl([SLMap(0, 8.0, 'lin', 'value', ratio)], title=f"{name} ratio")
        self.phasor = Phasor(200)
        self.level = SigTo(level, time=2)
        # self.level.ctrl([SLMapMul(init=level)], title=f"{name} level")
        self.cos = Cos(input=self.phasor, mul=self.env)
        self.output = self.level * self.cos
        self.pan = Pan(self.output, pan=pan, mul=.3)
        self.inputs = [self.phasor]
        self.final_output = self.pan * master

    def patch(self, modding: PyoObject):
        self.inputs += modding

    def configure_input(self):

        for i in self.inputs:
            self.cos.input += i

        self.cos.input *= math.pi * 2

    def reset(self):
        self.inputs = [self.phasor]
        self.cos.input = self.phasor
        self.final_output.stop()

    def change_pitch(self, freq: float):
        self.phasor.freq = freq * self.ratio
        self.env.play()

    def out(self):
        self.final_output.out()


class DX7Mono:
    # Module connections are shown for each algorithm.  0 indicates output
    ALGORITHMS = (
        ((1, 0), (2, 1), (6, 6), (6, 5), (5, 4), (4, 3), (3, 0)),
        ((1, 0), (2, 1), (2, 2), (6, 5), (5, 4), (4, 3), (3, 0)),
        ((3, 2), (2, 1), (1, 0), (6, 5), (5, 4), (4, 3), (6, 6)),
        ((3, 2), (2, 1), (1, 0), (6, 5), (5, 4), (4, 3), (6, 0)),
        ((2, 1), (1, 0), (4, 3), (3, 0), (6, 6), (6, 5), (5, 0)),
        ((2, 1), (1, 0), (4, 3), (3, 0), (6, 0), (6, 5), (5, 0)),
        ((2, 1), (1, 0), (4, 3), (3, 0), (6, 6), (6, 5), (5, 3)),
        ((2, 1), (1, 0), (4, 3), (3, 0), (4, 4), (6, 5), (5, 3)),
        ((2, 1), (1, 0), (4, 3), (3, 0), (2, 2), (6, 5), (5, 3)),
        ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 5), (6, 6)),
        ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (6, 6))
    )

    def __init__(self, master: PyoObject, pan: float = 0.5):
        self.vel = Sig(0)
        self.mod_dict = {}
        for mod_num in range(6):
            self.mod_dict[mod_num + 1] = DXSineModule(master, mod_num + 1, pan=pan)
        self.master_feedback = Sig(1.0)
        # self.master_feedback.ctrl([SLMap(0, 8.0, 'lin', 'value', 1)], title="Master Feedback")
        self.set_algo(0)

    def set_algo(self, algo_num: int):
        self.reset_routes()
        self.algo_num = algo_num
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
    def __init__(self, master: PyoObject, voices: int, rand_seed: int = 10, pan: float = 0.5):
        #random.seed(rand_seed)
        self.voices = [DX7Mono(master, pan) for _ in range(voices)]
        self.voice_num = voices
        self.active_voice_num = 0
        self.active_voice = self.voices[0]
        self.algo = 0

    def noteon(self, freq, vel):
        self.active_voice.noteon(freq, vel)
        self.active_voice_num = (self.active_voice_num + 1) % self.voice_num
        self.active_voice = self.voices[self.active_voice_num]

    def set_algo(self, algo_num):
        for voice in self.voices:
            voice.set_algo(algo_num)
        self.algo = algo_num

    def set_ratio(self, mod_num: int, new_val):
        for voice in self.voices:
            voice.mod_dict[mod_num + 1].ratio.value = new_val

    def set_attack(self, mod_num: int, new_val):
        for voice in self.voices:
            voice.mod_dict[mod_num + 1].env.attack = new_val

    def set_decay(self, mod_num: int, new_val):
        for voice in self.voices:
            voice.mod_dict[mod_num + 1].env.decay = new_val

    def set_sustain(self, mod_num: int, new_val):
        for voice in self.voices:
            voice.mod_dict[mod_num + 1].env.sustain = new_val

    def set_release(self, mod_num: int, new_val):
        for voice in self.voices:
            voice.mod_dict[mod_num + 1].env.release = new_val

    def set_level(self, mod_num: int, new_val):
        for voice in self.voices:
            voice.mod_dict[mod_num + 1].level.value = new_val

    def get_algo(self):
        return self.voices[0].algo_num

    def get_ratio(self, mod_num):
        return self.voices[0].mod_dict[mod_num + 1].ratio.value

    def get_attack(self, mod_num):
        return self.voices[0].mod_dict[mod_num + 1].env.attack

    def get_decay(self, mod_num):
        return self.voices[0].mod_dict[mod_num + 1].env.decay

    def get_sustain(self, mod_num):
        return self.voices[0].mod_dict[mod_num + 1].env.sustain

    def get_release(self, mod_num):
        return self.voices[0].mod_dict[mod_num + 1].env.release

    def get_level(self, mod_num):
        return self.voices[0].mod_dict[mod_num + 1].level.value

    def randomize_ratios(self):
        for mod_num in range(6):
            rand_ratio = (random.randrange(0, 6) / 2) + 0.5
            self.set_ratio(mod_num, rand_ratio)

    def randomize_ratios_bad(self):
        for mod_num in range(6):
            rand_ratio = (random.uniform(0, 3))
            self.set_ratio(mod_num, rand_ratio)

    def randomize_envs(self):
        for mod_num in range(6):
            self.set_attack(mod_num, random.uniform(0.002, 0.02))
            self.set_decay(mod_num, random.uniform(0.1, 0.5))
            self.set_sustain(mod_num, random.uniform(0.1, 0.9))
            self.set_release(mod_num, random.uniform(0.8, 1.4))

    def randomize_levels(self):
        for mod_num in range(6):
            self.set_level(mod_num, random.random())

    def randomize_all(self):
        self.randomize_levels()
        self.randomize_ratios_bad()
        self.randomize_envs()
        self.randomize_algo()

    def randomize_algo(self):
        self.set_algo(random.randrange(0, len(DX7Mono.ALGORITHMS)))

    def save(self, file):
        settings = {
            "algo": self.algo
        }
        for count, mod in enumerate(self.voices[0].mod_dict.values()):
            mod_settings = {
                "level": mod.level.value,
                "ratio": mod.ratio.value,
                "attack": mod.env.attack,
                "decay": mod.env.decay,
                "sustain": mod.env.sustain,
                "release": mod.env.release
            }
            settings[count] = mod_settings
        json.dump(settings, file)
        file.close()

    def load(self, file):
        settings = json.load(file)
        file.close()
        self.set_algo(settings["algo"])
        for count, mod in enumerate(self.voices[0].mod_dict.values()):
            count_str = str(count)
            self.set_level(count, settings[count_str]['level'])
            self.set_ratio(count, settings[count_str]['ratio'])
            self.set_attack(count, settings[count_str]['attack'])
            self.set_decay(count, settings[count_str]['decay'])
            self.set_sustain(count, settings[count_str]['sustain'])
            self.set_release(count, settings[count_str]['release'])



if __name__ == "__main__":
    s.boot()
    synth = DX7Poly(4, pan=0.5)
    synth.randomize_all()
    # synth.load()

    pattern = (48, 51, 55, 56, 51, 58)
    pattern_count = 0
    c = None
    trans = 0
    def note():
        global trans
        global c
        global pattern_count
        freq = note_to_freq(pattern[pattern_count] + 12 * trans)
        synth.noteon(freq, 1)
        pattern_count = (pattern_count + 1) % 6
        print(synth.get_attack(0))
        if pattern_count == 0:
            trans = (trans + 1) % 4
            synth.randomize_all()


    def note_to_freq(pitch):
        a = 440
        return (a / 32) * (2 ** ((pitch - 9) / 12))


    p = Pattern(note, 0.2)
    p.play()
    p.ctrl()

    s.gui(locals())