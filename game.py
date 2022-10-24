from ast import While
import sys
import string
import pygame as pg
from pygame.locals import *
from portal import Portal
from settings import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from timer import Pause
from timer import Timer
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites
from button import Button
from maze_functions import MazeData
from sound import Sound


class Game(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREENSIZE, 0, 32)
        pg.display.set_caption("Pacman")
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pg.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 1
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []
        self.fruitNode = None
        self.mazedata = MazeData()
        self.sound = Sound()
        self.running = False
        # self.menu()

        self.menu_images = [pg.transform.rotozoom(pg.image.load(f'images/menu_animation/menu_animation{n}.png'),0,2)for n in range(93)]
        self.menu_timer = Timer(image_list=self.menu_images)




    # A basic starter main menu page
    def menu(self):
        pg.display.set_caption("Menu")

        menu_running = True
        while menu_running:
            # get mouse position
            menu_mouse_pos = pg.mouse.get_pos()

            # Text to display on screen
            pac = "PACMAN!"
            color = (255, 255, 0)
            text = pg.font.Font(f"fonts/PAC-FONT.ttf", 50).render(pac, True, color)
            text_rec = text.get_rect(center=(225, 50))
            self.screen.blit(text, text_rec)

            # stand in for animated ghosts and pacman
            pac2 = "999912"
            color2 = (255, 255, 0)
            text2 = pg.font.Font(f"fonts/PAC-FONT.ttf", 50).render(pac2, True, color2)
            text2_rec = text2.get_rect(center=(225, 150))
            self.screen.blit(text2, text2_rec)

            #animation
            self.draw_animation()



            # play button creation
            PLAY_BUTTON = Button(
                image=None,
                pos=(225, 450),
                text_input="Play",
                font=pg.font.Font(f"fonts/PressStart2P-Regular.ttf", 50),
                base_color="Blue",
                hovering_color="White",
            )

            HS_BUTTON = Button(
                image=None,
                pos=(225,525),
                text_input = "High Scores",
                font = pg.font.Font(f"fonts/PressStart2P-Regular.ttf", 40),
                base_color="Blue",
                hovering_color="White",
                )

            # when mouse is hovering over the play button update it
            for button in [PLAY_BUTTON]:
                button.changeColor(menu_mouse_pos)
                button.update(screen=self.screen)

            for button in [HS_BUTTON]:
                button.changeColor(menu_mouse_pos)
                button.update(screen=self.screen)    



            # check events
            for event in pg.event.get():
                # if game is quit exit
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                # if mouse button is pressed check if the click was on the play button and if it was play game
                if event.type == pg.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(menu_mouse_pos):
                        menu_running=False
                        g = Game()
                        g.start()
                        

                    if HS_BUTTON.checkForInput(menu_mouse_pos):
                        menu_running=False
                        g=Game()
                        g.highscores()


            pg.display.update()

    def draw_animation(self):
        image = self.menu_timer.image()
        rect = image.get_rect()
        rect.left = 0
        rect.top = 275
        self.screen.blit(image,rect)

    def highscores(self):
        pg.display.set_caption("Highscores")
        self.screen.fill("black")
        hs_running = True

        while hs_running:
            menu_mouse_pos = pg.mouse.get_pos()

            hs = 'High Scores'
            color = (255,255,255)
            text = pg.font.Font(f"fonts/PressStart2P-Regular.ttf", 30).render(hs, True, color)
            text_rec = text.get_rect(center = (225,75))
            self.screen.blit(text,text_rec)

            color1="White"
            count = 0
            file = open('highscores.txt')
            line = file.readline

            for line in file:
                text1 = pg.font.Font(f"fonts/PressStart2P-Regular.ttf", 30).render(line,True,color1)
                text1_rec = text1.get_rect(center = (225,150+50*count))
                self.screen.blit(text1,text1_rec)
                count+=1
            file.close()
            
                

            BACK_BUTTON = Button(
                image=None,
                pos=(50, 25),
                text_input="Back",
                font=pg.font.Font(f"fonts/PAC-FONT.ttf", 25),
                base_color="Red",
                hovering_color="White",
            )

            for button in [BACK_BUTTON]:
                button.changeColor(menu_mouse_pos)
                button.update(screen=self.screen)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()


                if event.type == pg.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(menu_mouse_pos):
                            hs_running=False
                            g=Game()
                            g.menu()

            pg.display.update()




    def setBackground(self):
        self.background_norm = pg.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pg.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(
            self.background_norm, self.level % 5
        )
        self.background_flash = self.mazesprites.constructBackground(
            self.background_flash, 5
        )
        self.flashBG = False
        self.background = self.background_norm

    def start(self):
        self.screen.fill('White')
        self.running = True

        self.mazedata.loadMaze(self.level)
        self.mazesprites = MazeSprites(
            "mazes/" + self.mazedata.obj.name + ".txt",
            "mazes/" + self.mazedata.obj.name + "_rotation.txt",
        )
        self.setBackground()
        self.nodes = NodeGroup("mazes/" + self.mazedata.obj.name + ".txt")
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)
        self.pacman = Pacman(
            self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart)
        )
        self.pellets = PelletGroup("mazes/" + self.mazedata.obj.name + ".txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)

        self.ghosts.pinky.setStartNode(
            self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3))
        )
        self.ghosts.inky.setStartNode(
            self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3))
        )
        self.ghosts.clyde.setStartNode(
            self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3))
        )
        self.ghosts.setSpawnNode(
            self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3))
        )
        self.ghosts.blinky.setStartNode(
            self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0))
        )
        self.portal = Portal(self.pacman, self)

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)
        self.sound.play_startup()
        while self.running:
            self.update()
            
        
        

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()
            self.portal.teleport()

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pg.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            # self.hideEntities()
                elif event.key == K_LSHIFT or event.key == K_RSHIFT:
                    if not self.pause.paused:
                        self.portal.createPortal1()
                elif event.key == K_LCTRL or event.key == K_RCTRL:
                    if not self.pause.paused:
                        self.portal.createPortal2()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.startFreight()
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)
                    self.textgroup.addText(
                        str(ghost.points),
                        WHITE,
                        ghost.position.x,
                        ghost.position.y,
                        8,
                        time=1,
                    )
                    self.ghosts.updatePoints()

                        

                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -= 1
                        self.lifesprites.removeImage()
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.showText(GAMEOVERTXT)
                            self.update_highscore()
                            self.pause.setPause(pauseTime=3, func=self.restart)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)
        if self.level == 1:
            ghost.disablePortal = False

    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)
                print(self.fruit)
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.updateScore(self.fruit.points)
                self.textgroup.addText(
                    str(self.fruit.points),
                    WHITE,
                    self.fruit.position.x,
                    self.fruit.position.y,
                    8,
                    time=1,
                )
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.start()
        self.textgroup.updateLevel(self.level)

    def restart(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.start()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)
        self.fruitCaptured = []
        self.portal.reset()

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.portal.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)
        self.sound.play_startup()

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)


    def update_highscore(self):
         #function for updating high scores kinda works but it crashes the game a lot
        file = open('highscores.txt','r') 
        filedata = file.read()

        for filedata in file:
            if int(filedata) > self.score:
                filedata = filedata.replace(int(filedata),self.score)

                with open('highscores.txt','w') as file1:
                    file1.write(filedata)
                break
        file.close()

        


    def render(self):
        self.screen.blit(self.background, (0, 0))
        # self.nodes.render(self.screen)
        self.portal.drawPortal(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i + 1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))

        pg.display.update()

def main():
    g = Game()
    g.menu()

if __name__ == "__main__":
    main()
    
    
