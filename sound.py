import pygame as pg
import time

class Sound:
    def __init__(self):
        pg.mixer.init()
        start_up_music = pg.mixer.Sound('sounds/startup.wav')
        waka = pg.mixer.Sound('sounds/wakawaka.wav')

        def play_startup(self):
            pg.mixer.music.load(start_up_music)
            pg.mixer.music.play(-1,0.0)

        def stop_sound(self):
            pg.mixer.music.stop()

