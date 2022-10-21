from game_functions import Entity
import pygame as pg
from animation import PortalTimer
from maze_functions import MazeData
from pacman import Pacman
from settings import *


class Portal(Entity):
    portal1_images = [
        pg.transform.scale(pg.image.load(f"images/orange-{n}.png"), (22, 22))
        for n in range(1, 5)
    ]

    portal2_images = [
        pg.transform.scale(pg.image.load(f"images/blue-{n}.png"), (22, 22))
        for n in range(1, 5)
    ]

    def __init__(self, pacman, game):
        self.portal1 = False
        self.portal2 = False
        self.portal1_timer = PortalTimer(Portal.portal1_images, delay=50)
        self.portal2_timer = PortalTimer(Portal.portal2_images, delay=50)
        self.pacman = pacman
        self.game = game
        self.nodes = game.nodes
        self.portal_set = False

    def createPortal1(self):
        self.portal1_pos = self.pacman.target
        self.x1 = self.portal1_pos.position.x
        self.y1 = self.portal1_pos.position.y
        self.portal1 = True

    def createPortal2(self):
        self.portal2_pos = self.pacman.target
        self.x2 = self.portal2_pos.position.x
        self.y2 = self.portal2_pos.position.y
        self.portal2 = True

    def drawPortal(self, screen):
        if self.portal1:
            image = self.portal1_timer.image()
            rect = image.get_rect()
            rect.left, rect.top = self.x1, self.y1
            screen.blit(image, rect)
        if self.portal2:
            image = self.portal2_timer.image()
            rect = image.get_rect()
            rect.left, rect.top = self.x2, self.y2
            screen.blit(image, rect)

    def teleport(self):
        if self.portal1 and self.portal2:
            self.nodes.setPortalPair(
                (self.portal1_pos.position.x / 16, self.portal1_pos.position.y / 16),
                (self.portal2_pos.position.x / 16, self.portal2_pos.position.y / 16),
            )

    def reset(self):
        self.portal1 = False
        self.portal2 = False
        self.nodes.deletePortalPair(
            (self.portal1_pos.position.x / 16, self.portal1_pos.position.y / 16),
            (self.portal2_pos.position.x / 16, self.portal2_pos.position.y / 16),
        )
