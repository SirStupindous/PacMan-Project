import pygame as pg
from nodes import Node,NodeGroup
from vector import Vector


class Ghost:
    def __init__(self, game, type, pac_pos):
        self.game = game
        self.pacx= pac_pos[0]
        self.pacy = pac_pos[1]
        self.screen = game.screen
        self.image = pg.image.load('images/ghost.png')
        self.rect = self.image.get_rect()
        self.type = type
        self.x = self.rect.x
        self.y = self.rect.y

    def red(self): 
        if self.atNode():
            currentNode = self.NodeGroup.getNodeFromTiles(self.x,self.y)
            up = currentNode.neighbors["UP"]
            down = currentNode.neighbors["DOWN"]
            right = currentNode.neighbors["RIGHT"]
            left = currentNode.neighbors["LEFT"]



            
    def pink(self): 
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

    def blue(self): pass

    def move(self, dir):pass

    def atNode(self):
        pass

    def update(self):pass
    
    
