import pygame as pygame

from field import Board

if __name__ == '__main__':
    pygame.init()
    FPS = 30
    fpsClock = pygame.time.Clock()
    # screen = pygame.display.set_mode((800, 600))
    board = Board()
    board.set_view(20, 70, 50, 50)
    width, height = board.get_size()
    width += 100
    height += 150
    size = width, height
    screen = pygame.display.set_mode(size)

    running = True
    while running:
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
