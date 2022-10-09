import pygame as pg
from settings import Settings
import game_functions as gf
from button import Button
import sys


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


    #A basic starter main menu page
    def menu(self):
        pg.display.set_caption("Menu")

        while True:
            menu_mouse_pos = pg.mouse.get_pos()

            pac = ("PACMAN!")
            color = (255,255,0)

            text = pg.font.Font(f'images/PAC-FONT.ttf', 75).render(pac,True,color)
            text_rec = text.get_rect(center = (350, 100))
            self.screen.blit(text,text_rec)

            pac2 = ("999912")
            color2 = (255,255,0)

            text2 = pg.font.Font(f'images/PAC-FONT.ttf', 75).render(pac2,True,color2)
            text2_rec = text2.get_rect(center=(350,200))
            self.screen.blit(text2,text2_rec)



            PLAY_BUTTON = Button(image=None, pos=(350,300),text_input = "Play", font=pg.font.Font(f'images/PAC-FONT.TTF', 75), base_color="Red", hovering_color="White")

            for button in [PLAY_BUTTON]:
                    button.changeColor(menu_mouse_pos)
                    button.update(screen=self.screen)

            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type ==pg.MOUSEBUTTONDOWN:
                        if PLAY_BUTTON.checkForInput(menu_mouse_pos):
                            g = Game()
                            g.play()

            pg.display.update()


def main():
    g = Game()
    g.menu()


if __name__ == "__main__":
    main()
