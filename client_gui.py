import pygame as pg

WIDTH = 1920
HEIGHT = 1080

BLACK = (55, 55, 55)
WHITE = (255, 255, 255)
LIGHT_GREY = (191, 191, 191)
RED = (255, 0, 0)

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
FONT = pg.font.Font('../resources/JetBrainsMono-Medium.ttf', 12)
pg.display.set_caption("DX7 testing GUI")