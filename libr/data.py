import os
import pygame
from pygame.locals import *

data_dir = 'data'

def filepath(filename):
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    return open(os.path.join(data_dir, filename), mode)

def load_image(filename, ck=False):
    img = pygame.image.load(filepath(filename))
    return img.convert()

