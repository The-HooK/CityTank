#! /usr/bin/env python

import pygame
from libr.menu import *

pygame.init()
pygame.display.set_caption("City Tank")
screen = pygame.display.set_mode((800, 600), 0, 32)
menu = Menu(screen)
menu.loop()
