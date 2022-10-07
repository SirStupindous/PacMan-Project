import sys
import pygame as pg


def check_events():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
