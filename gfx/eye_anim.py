import pygame as pg
import os


class EyeAnimation:
    filenames = ["eye_" + str(i + 1) + ".png" for i in range(4)]
    frames = [pg.image.load(os.path.join('eye_anims', filename)) for filename in filenames]

    def __init__(self):
        self.alpha = 255
        self.run = False
        self.framenum = 0
        self.frame = self.frames[0]

    def play(self):
        self.run = True
        self.alpha = 255
        self.framenum = 0
        self.frame = self.frames[0]

    def update(self):
        if self.framenum == 5:
            self.frame = self.frames[1]

        elif self.framenum == 11:
            self.frame = self.frames[2]

        elif self.framenum == 17:
            self.frame = self.frames[3]

        elif self.framenum > 20:
            if self.alpha > 2:
                self.alpha -= 5
            else:
                self.alpha = 0
            self.frame.set_alpha(self.alpha)

        self.framenum += 1

    def draw(self, surf: pg.Surface):
        if self.run:
            self.update()
            surf.blit(self.frame, (0, 0))


if __name__ == "__main__":
    import gfx_tester

    ea = EyeAnimation()
    ea.play()
    gfx_tester.main(ea)