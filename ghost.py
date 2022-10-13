import pygame as pg
from vector import Vector


class Ghost:
    def __init__(self, game, type, pac_pos):
        self.game = game
        self.pac_pos = pac_pos
        self.screen = game.screen
        # self.image = pg.image.load('images/redGhost.png')
        # self.rect = self.image.get_rect()
        self.type = type
        self.speed = 100
        self.directions = {
            "UP": Vector(0, -1),
            "DOWN": Vector(0, 1),
            "LEFT": Vector(-1, 0),
            "RIGHT": Vector(0, 1),
            "STOP": Vector(0, 0),
        }
        self.direction = "STOP"

    def red(self):
        pass

    def pink(self):
        pass

    def orange(self):
        pass

    def blue(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass
