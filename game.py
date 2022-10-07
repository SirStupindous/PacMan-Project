import pygame as pg
from settings import Settings
import game_functions as gf


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Pacman")
        self.map = pg.transform.scale(pg.image.load("images/pacman_map.jpg"), (size))

    def play(self):
        while True:
            gf.check_events()

            self.screen.blit(self.map, (0, 0))

            pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == "__main__":
    main()
