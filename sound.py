import pygame as pg
import time

class Sound:
    def __init__(self):
        pg.mixer.init()
        pg.mixer.music.set_volume(0.1)
        waka = pg.mixer.Sound('sounds/wakawaka.wav')

    def play_startup(self):
        pg.mixer.music.load('sounds/startup.wav')
        pg.mixer.music.play(-1,0.0)

    def stop_sound(self):
        pg.mixer.music.stop()

    def play_dead(self):
        pg.mixer.music.load('sounds/pacman_dead.wav')
        pg.mixer.music.play(0, 0.0)

    def play_waka(self):
        pg.mixer.music.load('sounds/wakawaka.wav')
        pg.mixer.music.play(0,0.0)

