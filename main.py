import json

import pygame
import my_sprites
import game_params


class GamePlayers:
    def __init__(self, parameters, group):
        self.current_player = 0
        self.players_sprites = []
        player_colors = [(100, 255, 100), (255, 100, 100), (100, 100, 255), (100, 255, 255)]
        for i in range(int(parameters['players_number'])):
            self.players_sprites.append(my_sprites.Player(parameters['player_names'][i], 0))
            self.players_sprites[-1].add(group)
            self.players_sprites[-1].set_color(player_colors[i])
            self.players_sprites[-1].move_to(width - (self.players_sprites[-1].rect.width + 5),
                                             (self.players_sprites[-1].rect.height + 5) * i + 10)

    def next(self):
        self.current_player = (self.current_player + 1) % len(self.players_sprites)
        for player in self.players_sprites:
            player.unset_current()
        self.players_sprites[self.current_player].set_current()

    def current(self):
        return self.players_sprites[self.current_player]

    def add_score(self, point):
        self.players_sprites[self.current_player].add_score(point)


def check_faced_cards(new_card):
    global game_is_over
    if not faced_cards:
        faced_cards.append(new_card)
    else:
        if new_card.is_same_with(faced_cards[0]):
            print('SAME!!!')
            pygame.time.wait(500)
            players.add_score(1)
            # print(f'Scored for {players.current().name}!!!')
            if check_end_of_game(field):
                game_over(get_winners(), screen)
                game_is_over = True
        else:
            print('DIFFERENT')
            pygame.time.wait(500)
            new_card.on_click()
            faced_cards[0].on_click()
            players.next()
            current_player_label.set_text(f"Ходит {players.current().name}")
        faced_cards.clear()


def get_winners():
    max_score = max(map(lambda player: player.score, players.players_sprites))
    return list(map(lambda player: player.name,
                    (filter(lambda player: player.score == max_score, players.players_sprites))))


def redraw(surface):
    surface.fill((0, 0, 0))
    field.update()
    sprites_group.draw(surface)
    pygame.display.flip()


def read_params():
    return json.load(open('game.json', 'r'))


def check_end_of_game(game_field: my_sprites.SpriteField):
    return all(map(lambda card: card.faced, game_field.cards))


def game_over(winners, surface: pygame.Surface):
    font = pygame.font.Font(None, 100)
    color = 'red'
    surface.fill('black')
    username_label = my_sprites.SpriteLabel(', '.join(winners), width // 2,
                                            height - 60, sprites_group)
    username_label.set_font(font)
    username_label.set_color(color)
    username_label.move_to((width - username_label.image.get_width()) // 2,
                           height // 2 - username_label.image.get_height())
    over_label = my_sprites.SpriteLabel(f"ВЫИГРАЛ!!!", width // 2,
                                        height - 60, sprites_group)
    over_label.set_font(font)
    over_label.set_color(color)
    over_label.move_to((width - over_label.image.get_width()) // 2,
                       height // 2 + over_label.image.get_height())


game_params.main()
params = read_params()
pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
size = width, height = 600, 500
screen = pygame.display.set_mode(size)
sprites_group = pygame.sprite.Group()
players = GamePlayers(params, sprites_group)
field = my_sprites.SpriteField(sprites_group, folder=params['folder'])
current_player_label = my_sprites.SpriteLabel(f"Ходит {players.current().name}", width // 2,
                                              height - 60, sprites_group)
current_player_label.move_to((width - current_player_label.image.get_width()) // 2,
                             current_player_label.y)
current_player_label.set_color('magenta')
faced_cards = []
field.set_pos(30, 20)
running = True
game_is_over = False

while running:
    fpsClock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_card = field.on_click(event.pos)
            if clicked_card and not game_is_over:
                redraw(screen)
                check_faced_cards(clicked_card)
    redraw(screen)
