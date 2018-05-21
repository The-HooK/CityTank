import pygame
from pygame.locals import *
from menu import *



def main():
    pygame.init()
    pygame.display.set_caption("City Tank")
    screen = pygame.display.set_mode((800,600),0,32)
    menu = Menu(screen)
    menu.loop()

