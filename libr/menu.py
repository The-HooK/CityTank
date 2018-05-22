"""
Affichage et gestion du menu
"""

import pygame
from pygame.locals import *
import sys

from libr.game import *


class Menu:


    def __init__(self, screen): # constructeur de la classe menu

        self.screen = screen
        self.font = pygame.font.Font(filepath("Abduction II.ttf"), 35)
        self.font2 = pygame.font.Font(filepath("Abduction III.ttf"), 35)
        self.font3 = pygame.font.Font(filepath("Abduction II.ttf"), 50)
        self.option = 1
        self.vehicle = None
        self.veh_pos = (100, 200)
        self.angle = 360
        self.tank= pygame.image.load(filepath("tank2.png")).convert_alpha()


    def loop(self): # Affichage du menu en continu

        while True:
            # Debut gestion evenements dans le menu
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_DOWN:
                        if self.option < 2:
                            self.option += 1
                        else:
                            pass
                    elif event.key == K_UP:
                        if self.option > 1:
                            self.option -= 1
                        else:
                            pass
                    elif event.key == K_RETURN:
                        if self.option == 1:
                            self.vehicle = "tank"
                            game = Game(self.screen, self.vehicle)
                            game.run()

                        if self.option == 2:
                            pygame.quit()
                            sys.exit()

            # ***** Affichage du menu *****

            # Definition des boutons
            title = self.font3.render("City Tank", 1, (255, 0, 0))
            start_button = self.font.render("Start", 1, (255, 0, 0))
            exit_button = self.font.render("Exit", 1, (255, 0, 0))

            # Gestion de la selection
            if self.option == 1:
                start_button = self.font2.render("Start", 1, (0, 230, 0))
                self.image = pygame.transform.rotozoom(self.tank, self.angle, 2.5)
                rect = self.image.get_rect()    # Cela sert ÃƒÂ  centrer la surface de l'image qui a subit une rotation
                self.screen.blit(self.image, (150-(rect.width/2), 250-(rect.height/2)))
            elif self.option == 2:
                exit_button = self.font2.render("Exit", 1, (0, 230, 0))

            # "blitting" -> Cette operation consiste aÂ dessiner les diferents elements
            self.screen.blit(title, (400-title.get_width()/2, 50))
            self.screen.blit(start_button, (400-start_button.get_width()/2, 210))
            self.screen.blit(exit_button, (400-exit_button.get_width()/2, 330))

            pygame.display.flip()
            self.screen.fill((0, 0, 0))
            self.angle += 0.2
