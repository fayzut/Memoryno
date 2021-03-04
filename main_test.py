import os

import pygame

from my_sprites import Card





pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)
ready_cards, ready_group = cards_generation('data')
print('DONE')
