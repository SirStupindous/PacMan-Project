import pygame as pg

class Ghost():
    def __init__(self, game,type, pac_pos):
        self.game = game
        self.pac_pos = pac_pos
        self.screen = game.screen
        #self.image = pg.image.load('images/redGhost.png')
        #self.rect = self.image.get_rect()
        self.type = type

    def red(self): pass

    def pink(self): pass

    def orange(self):pass

    def blue(self): pass
    