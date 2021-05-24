import pygame as pg

class Text:
    def __init__(self, msg, loc, font, color=(255, 255, 255)):
        self.color = color
        self.msg = msg
        self.new_msg = msg
        self.loc = loc
        self.font = font
        self.image = self.font.render(msg, True, color)

    def change_msg(self, new_msg):
        self.msg = new_msg
        self.image = self.font.render(self.msg, 0, self.color)

    def draw(self, surf):
        surf.blit(self.image, self.loc)



class MessageBox(Text):
    def __init__(self, msg, loc, font,
 bkg_color=(0, 0, 0), text_color=(255, 255, 255)):
        super().__init__(msg, loc, font, text_color)
        self.bkg_color = bkg_color
        self._build_rect()

    def _build_rect(self):
        self.rect = self.image.get_rect().move(*self.loc)
        self.rect.inflate_ip(30, 30)

    def change_msg(self, msg):
        super().change_msg(msg)
        self._build_rect()

    def draw(self, surf):
        #draw the background rectangle
        pg.draw.rect(surf, self.bkg_color, self.rect)
        #draw the overlaid text
        super().draw(surf)


class MessageButton(MessageBox):
    def __init__(self, msg: str, loc: tuple, callback: callable, font: pg.font.Font,
     bkg_color=(0, 0, 0), text_color=(255, 255, 255)):
        super().__init__(msg, loc, font, bkg_color, text_color)
        self.callback = callback
        self.hover = False

    def check_mouse(self, mouse_coor):
        if self.rect.collidepoint(mouse_coor):
            self.hover = True
        else:
            self.hover = False

    def try_click(self):
        if self.hover:
            self.callback()