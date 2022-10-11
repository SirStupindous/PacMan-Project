import pygame as pg
from vector import Vector


class Ghost:
    def __init__(self, node):
        self.name = None
        self.directions = {
            "UP": Vector(0, -1),
            "DOWN": Vector(0, 1),
            "LEFT": Vector(-1, 0),
            "RIGHT": Vector(1, 0),
            "STOP": Vector(),
        }
        self.direction = "STOP"
        self.node = node

    def isValidDirection(self, direction):
        if direction is not "STOP":
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def getNewDirection(self, direction):
        if self.isValidDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    
