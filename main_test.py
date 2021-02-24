import pygame
import my_sprites

if __name__ == '__main__':
    pygame.init()
    FPS = 30
    fpsClock = pygame.time.Clock()
    size = width, height = 300, 300
    screen = pygame.display.set_mode(size)
    sprites_group = pygame.sprite.Group()
    board = my_sprites.plane()
    running = True
    while running:
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        board.draw(screen)
        pygame.display.flip()
