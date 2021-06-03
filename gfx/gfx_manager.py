import pygame as pg
from gfx import DustManager, DiamondManager, SmokeManager, BoltSpots


class GfxZone:
    def __init__(self, x_min, x_max, y_min, y_max):
        bounds = (x_min, x_max, y_min, y_max)
        self.diamond = DiamondManager(*bounds)
        self.smoke = SmokeManager(*bounds)
        self.dust = DustManager(*bounds)
        self.bolt = BoltSpots(*bounds)

        self.all_managers = (self.diamond, self.smoke, self.dust, self.bolt)

    def start_all(self):
        for manager in self.all_managers:
            manager.start()

    def input(self, msg: list):
        if msg[0] == 'tonal':
            pass
        elif msg[0] == "atonal":
            pass
        else:
            pass

        if msg[1] == "quiet":
            self.dust.start()
            self.bolt.stop()
        elif msg[1] == "static":
            self.bolt.start()
            self.dust.start()

        if msg[2] == "high":
            self.diamond.start()
            self.smoke.stop()
        elif msg[2] == "low":
            self.smoke.start()
            self.diamond.stop()
        else:
            self.diamond.stop()
            self.smoke.stop()

    def draw(self, surf: pg.Surface):
        for manager in self.all_managers:
            manager.draw(surf)


if __name__ == "__main__":
    import gfx_tester
    gz = GfxZone(0, 200, 300, 350)
    gz.input([None, 'quiet', 'high'])
    gfx_tester.main(gz)
