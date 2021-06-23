import pygame as pg
import os


class BaseEye:
    filenames = ["eye_" + str(i + 1) + ".png" for i in range(4)]
    frames = [pg.image.load(os.path.join('resources/eye_anims', filename)) for filename in filenames]

    def __init__(self):
        self.run = False
        self.framenum = 0
        self.frame = self.frames[0]

    def play(self):
        self.run = True
        self.framenum = 0
        self.frame = self.frames[0]

    def update(self):
        if self.framenum == 5:
            self.frame = self.frames[1]

        elif self.framenum == 11:
            self.frame = self.frames[2]

        elif self.framenum >= 17:
            self.frame = self.frames[3]

        self.framenum += 1

    def draw(self, surf: pg.Surface):
        if self.run:
            self.update()
            surf.blit(self.frame, (0, 0))


class EyeAnimation(BaseEye):
    def __init__(self):
        super().__init__()
        self.alpha = 255

    def play(self):
        super().play()
        self.alpha = 255

    def update(self):
        if self.framenum > 20:
            if self.alpha > 2:
                self.alpha -= 5
            else:
                self.alpha = 255
                self.run = False
            self.frame.set_alpha(self.alpha)
        super().update()


class EndAnimation(BaseEye):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def update(self):
        if self.framenum == 120:
            self.callback()
            self.run = False
        super().update()


if __name__ == "__main__":
    import gfx_tester

    ea = EyeAnimation()
    ea.play()
    gfx_tester.main(ea)