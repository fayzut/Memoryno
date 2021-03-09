import pygame
import my_sprites


def check_faced_cards(new_card):
    if not faced_cards:
        faced_cards.append(new_card)
    else:
        if new_card.is_same_with(faced_cards[0]):
            print('SAME!!!')
            pygame.time.wait(500)
            print('Scored for You!!!')
        else:
            print('DIFFERENT')
            pygame.time.wait(500)
            new_card.on_click()
            faced_cards[0].on_click()
        faced_cards.clear()



pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
sprites_group = pygame.sprite.Group()
field = my_sprites.SpriteField(sprites_group)
faced_cards = []
field.set_pos(30, 20)
running = True
while running:
    fpsClock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_card = field.on_click(event.pos)
            check_faced_cards(clicked_card)
    screen.fill((0, 0, 0))
    field.update()
    sprites_group.draw(screen)
    pygame.display.flip()
