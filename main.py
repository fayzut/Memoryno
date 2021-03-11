import json

import pygame
import my_sprites
import game_params


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


def redraw(surface):
    surface.fill((0, 0, 0))
    field.update()
    sprites_group.draw(surface)
    pygame.display.flip()


def read_params():
    return json.load(open('game.json', 'r'))


game_params.main()
params = read_params()
pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
size = width, height = 600, 500
screen = pygame.display.set_mode(size)
sprites_group = pygame.sprite.Group()
players = []
player_colors = [(100, 255, 100), (255, 100, 100), (100, 100, 255), (100, 255, 255)]
for i in range(int(params['players_number'])):
    players.append(my_sprites.Player(params['player_names'][i], 0))
    players[-1].add(sprites_group)
    players[-1].set_color(player_colors[i])
    players[-1].move_to(width - (players[-1].rect.width + 5),
                        (players[-1].rect.height + 5) * i + 10)
field = my_sprites.SpriteField(sprites_group, folder=params['folder'])
faced_cards = []
field.set_pos(30, 20)
running = True
cur_player = 0
while running:
    fpsClock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_card = field.on_click(event.pos)
            if clicked_card:
                redraw(screen)
                check_faced_cards(clicked_card)
    redraw(screen)
