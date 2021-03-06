import pygame
import my_sprites

pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
sprites_group = pygame.sprite.Group()
field = my_sprites.SpriteField(sprites_group)
field.set_pos(30, 20)
running = True
while running:
    fpsClock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            field.on_click(event.pos)
    screen.fill((0, 0, 0))
    field.update()
    sprites_group.draw(screen)
    pygame.display.flip()
