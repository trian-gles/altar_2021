from pyo import *


class SynthManager:
    def __init__(self):
        self.zones = (ZoneOne(), ZoneTwo(), ZoneThree())

    def input(self, msg):
        # Messages should be a list, with the first element being the zone to be acted on i.e. [0, ..., ...]
        self.zones[msg[0]].input(msg[1:])
        pass


class Zone:
    def input(self, msg):
        pass


class ZoneOne(Zone):
    pass


class ZoneTwo(Zone):
    pass


class ZoneThree(Zone):
    pass


class Node:
    pass
