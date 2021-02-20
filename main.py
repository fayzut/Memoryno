import pygame as pygame

from field import Board

if __name__ == '__main__':
    pygame.init()
    board = Board()
    board.set_view(20, 10, 50, 50)
    size = width, height = board.get_size()
    screen = pygame.display.set_mode(size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
