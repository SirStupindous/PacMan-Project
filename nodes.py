import pygame as pg
from vector import Vector
import numpy as np


class Node:
    def __init__(self, x, y):
        self.position = Vector(x, y)
        self.neighbors = {"UP": None, "DOWN": None, "LEFT": None, "RIGHT": None}

    def draw(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                start = self.position.x, self.position.y
                end = self.neighbors[n].position.x, self.neighbors[n].position.y
                pg.draw.line(screen, (255, 255, 255), start, end, 4)
                pg.draw.circle(
                    screen,
                    (255, 0, 0),
                    (int(self.position.x), int(self.position.y)),
                    12,
                )


class NodeGroup:
    def __init__(self, file):
        self.file = file
        self.nodesDict = {}
        self.nodeSymbols = ["+"]
        self.pathSymbols = ["."]
        data = self.readMazeFile(file)
        self.createGraph(data)
        self.connectHorizontally(data)
        self.connectVertically(data)

    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype="<U1")

    def createGraph(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col + xoffset, row + yoffset)
                    self.nodesDict[(x, y)] = Node(x, y)

    def constructKey(self, x, y):
        return x * 24, y * 2445

    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.constructKey(col + xoffset, row + yoffset)
                        self.nodesDict[key].neighbors["RIGHT"] = self.nodesDict[
                            otherkey
                        ]
                        self.nodesDict[otherkey].neighbors["LEFT"] = self.nodesDict[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.constructKey(col + xoffset, row + yoffset)
                        self.nodesDict[key].neighbors["DOWN"] = self.nodesDict[otherkey]
                        self.nodesDict[otherkey].neighbors["UP"] = self.nodesDict[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    def getNodeFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodesDict.keys():
            return self.nodesDict[(xpixel, ypixel)]
        return None

    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesDict.keys():
            return self.nodesDict[(x, y)]
        return None

    def draw(self, screen):
        for node in self.nodesDict.values():
            node.draw(screen)
