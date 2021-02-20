import random, os

import pygame

STANDART_COLOR = (0, 255, 0)


def load_image(name, folder='data', colorkey=None):
    fullname = os.path.join(folder, name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Card(pygame.sprite.Sprite):
    def __init__(self, group, link, text):
        super(Card, self).__init__(group)
        self.faced = False
        self.pic = None
        self.image = None

        self.rect = pygame.Rect(0, 0, 50, 50)
        self.text = text
        if link:
            self.pic = link
            self.image = load_image(self.pic)
            self.rect = self.image.get_rect()
        else:
            font = pygame.font.Font(None, 50)
            self.image = font.render(self.text, True, (100, 255, 100))
        self.back_image = pygame.font.Font(None, 50).render('X', True, (100, 255, 100))

    # def set_pos(self, x, y):
    #     self.left = x
    #     self.top = y
    #
    def update(self, *args, **kwargs) -> None:  # (self, surface, border_color):
        self.surface = kwargs['surface']
        self.border_color = kwargs['border_color']
        pygame.draw.rect(self.surface, self.border_color, self.rect, 1)
        if self.faced:
            self.surface.blit(self.image, self.rect.topleft)
        else:
            self.surface.blit(self.back_image, self.rect.topleft)
    #
    # def on_click(self):
    #     self.faced = not self.faced
    #
    # def set_scored(self):
    #     self.faced = True
    #     self.text = '+'
    #
    # def blink(self):
    #     old_color = self.text_color
    #     self.text_color = (255, 10, 10)
    #     start = pygame.time.Clock()
    #     if start.tick(500):
    #         self.text_color = old_color
    #


class Label:
    def __init__(self, text, screen, coords, color=STANDART_COLOR, bordered=True,
                 border_color=STANDART_COLOR):
        self.text = text
        self.screen = screen
        self.coords = coords
        self.text_color = color
        self.bordered = bordered
        self.border_color = border_color

    def draw(self):
        font = pygame.font.Font(None, 50)
        text = font.render(self.text, True, self.text_color)
        text_x = self.coords[0]
        text_y = self.coords[1]
        text_w = text.get_width()
        text_h = text.get_height()
        self.screen.blit(text, (text_x, text_y))
        if self.bordered:
            pygame.draw.rect(self.screen, self.border_color, (text_x - 10, text_y - 10,
                                                              text_w + 20, text_h + 20), 1)


class Field:
    def __init__(self, cards, left=20, top=60, card_width=50,
                 card_height=50):
        self.left = left
        self.top = top
        self.card_width = card_width
        self.card_height = card_height
        self.cards = []
        self.all_cards_group = pygame.sprite.Group()
        for card in cards:
            if type(card) is str:
                self.cards.append(Card(self.all_cards_group, None, card))
            elif type(card) is dict:
                self.cards.append(Card(self.all_cards_group, card['link'], card['text']))
            else:
                raise TypeError
        self.faced_card = None

    def __len__(self):
        return len(self.cards)


class Board:
    # создание поля
    def __init__(self):
        # self.need_to_render = True
        # значения по умолчанию
        self.top = 0
        self.left = 0
        self.cell_width = 50
        self.cell_height = 50
        self.cell_border_width = 1
        # self.set_view(self.left, self.top, self.cell_width, self.cell_height)

        self.field_line_color = STANDART_COLOR
        # Стандартные карточки - числа в массиве
        # генерация поля карточек
        # список карточек для игры - TODO: объекты карточек Card
        cards_to_use = 14
        cards_data = list(map(str, random.choices(range(10, 100), k=cards_to_use)))
        cards_data = list(random.sample(cards_data * 2, cards_to_use * 2))
        self.field = Field(cards_data)
        self.scores = 0

    def get_size(self):
        length = len(self.field)
        board_height = int(length ** 0.5)
        board_width = length // board_height + length % board_height
        return board_width, board_height

    # настройка внешнего вида
    def set_view(self, left, top, cell_width, cell_height):
        self.left = left
        self.top = top
        self.cell_width = cell_width
        self.cell_height = cell_height

    def render(self, surface):
        self.surface = surface
        self.surface.fill((0, 0, 0))
        # Надпись на экране игры
        font = pygame.font.Font(None, 50)
        text = font.render("Welcome to Memoryno!", True, (100, 255, 100))
        text_x = self.surface.get_width() // 2 - text.get_width() // 2
        text_y = 10  # screen.get_height() // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        self.surface.blit(text, (text_x, text_y))
        pygame.draw.rect(self.surface, (0, 255, 0), (text_x - 10, text_y - 10,
                                                     text_w + 20, text_h + 20), 1)
        # КОНЕЦ Надпись на экране игры
        # Надписи счета
        scores = Label(f'Счет: {self.scores}', self.surface, (self.surface.get_width() - 200, 100))
        scores.draw()
        # Конец Надписи счета
        self.draw_field()

    def draw_field(self):
        cards_number = len(self.field)
        screen = self.surface
        h = int(cards_number ** 0.5)
        w = cards_number // h
        # last_line_card_number = cards_number % h
        for i in range(len(self.field)):
            col = i % w
            row = i // h
            self.field.cards[i].rect.x = self.left + self.cell_width * col
            self.field.cards[i].rect.y = self.top + self.cell_height * row
        self.field.all_cards_group.update(surface=screen, border_color=self.field_line_color)

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] <= self.cell_width * len(self.field[0]) + self.left and \
                self.top <= mouse_pos[1] <= self.cell_height * len(self.field) + self.top:
            x = (mouse_pos[0] - self.left) // self.cell_width
            y = (mouse_pos[1] - self.top) // self.cell_height
            try:
                return self.field[y][x]
            except:
                return None
        else:
            return False  # Не попали в карту

    def on_click(self, card):
        card.on_click()

        if self.faced_card:
            if self.faced_card.text == card.text:  # TODO: Написать функцию сравнения Карт вместо
                # сравнения текстов
                self.faced_card.set_scored()
                card.set_scored()
                self.scores += 1
            else:
                pygame.time.delay(500)
                card.blink()
                self.faced_card.blink()
                card.on_click()
                self.faced_card.on_click()
            self.faced_card = None
        else:
            self.faced_card = card

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
