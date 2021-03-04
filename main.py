import pygame
import my_sprites

if __name__ == '__main__':
    pygame.init()
    FPS = 30
    fpsClock = pygame.time.Clock()
    size = width, height = 300, 300
    screen = pygame.display.set_mode(size)
    sprites_group = pygame.sprite.Group()
    label = my_sprites.SpriteLabel('Text', 50, 50, sprites_group)
    card = my_sprites.Card('CardText', 'card.png', sprites_group)
    card.faced = True
    running = True
    while running:
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        sprites_group.draw(screen)
        pygame.display.flip()
