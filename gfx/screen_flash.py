import pygame as pg


class ScreenFlasher:
    def __init__(self, surf: pg.Surface):
        self.overlaid_surf = surf.copy()
        self.alpha = 0

    def init_color(self, color: tuple):
        self.alpha = 255
        self.overlaid_surf.fill(color)

    def draw(self, surf: pg.Surface):
        if self.alpha > 2:
            self.alpha -= 3
            self.overlaid_surf.set_alpha(self.alpha)
            surf.blit(self.overlaid_surf, (0, 0))


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((200, 200))
    sf = ScreenFlasher(screen)
    sf.init_color((255, 255, 255))
    while True:
        clock = pg.time.Clock()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
        screen.fill((0, 0, 0))
        sf.draw(screen)
        pg.display.update()
        clock.tick(30)