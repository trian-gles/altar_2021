import pygame as pg
from gfx import DustManager, DiamondManager, SmokeManager, BoltSpots, EyeManager


class GfxManager:
    def __init__(self, zone_coors: tuple):
        self.zones = []
        for zone_coor in zone_coors:
            new_zone = GfxZone(*self.get_bounds(zone_coor))
            self.zones.append(new_zone)

    def input(self, msg):
        for i, zone_msg in enumerate(msg):
            self.zones[i].input(zone_msg)

    def get_bounds(self, coor):
        x_min = coor[0]
        x_max = coor[0] + 420
        y_min = coor[1]
        y_max = coor[1] + 200
        return x_min, x_max, y_min, y_max

    def draw(self, surf: pg.Surface):
        for zone in self.zones:
            zone.draw(surf)


class GfxZone:
    def __init__(self, x_min, x_max, y_min, y_max):
        bounds = (x_min, x_max, y_min, y_max)
        self.diamond = DiamondManager(*bounds)
        self.smoke = SmokeManager(*bounds)
        self.dust = DustManager(*bounds)
        self.bolt = BoltSpots(*bounds)
        self.eye = EyeManager(*bounds)

        self.all_managers = (self.diamond, self.smoke, self.dust, self.bolt, self.eye)

        self.run = False

    def start_all(self):
        for manager in self.all_managers:
            manager.start()

    def start(self):
        self.run = True

    def stop(self):
        self.run = False
        for manager in self.all_managers:
            manager.stop()

    def input(self, msg: list):
        if not msg:
            self.stop()
            return

        self.start()

        if msg[0] == 'tonal':
            self.eye.stop()
        elif msg[0] == "atonal":
            self.eye.start()
        else:
            self.eye.stop()

        if msg[1] == "quiet":
            self.dust.start()
            self.bolt.stop()
        elif msg[1] == "static":
            self.bolt.start()
            self.dust.stop()
        else:
            self.dust.stop()
            self.bolt.stop()

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
    gz.start()
    gfx_tester.main(gz)
