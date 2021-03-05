import os

import pygame

from my_sprites import Card, SpriteField

pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
size = width, height = 500, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
Field = SpriteField(all_sprites)
Field.set_pos(30, 20)
running = True
while running:
    fpsClock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
