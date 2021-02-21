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
        self.front_image = None
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.text = text
        if link:
            self.pic = link
            self.front_image = load_image(self.pic)

        else:
            font = pygame.font.Font(None, 50)
            self.front_image = font.render(self.text, True, (100, 255, 100))
        self.back_image = pygame.font.Font(None, 50).render('X', True, (100, 255, 100))

    def is_same_with(self, other):
        return self.text == other.text

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, *args, **kwargs) -> None:  # (self, surface, border_color):
        self.image = self.back_image
        if self.faced:
            self.image = self.front_image
        self.rect = self.image.get_rect()

        # self.surface = kwargs['surface']
        # self.border_color = kwargs['border_color']
        # pygame.draw.rect(self.surface, self.border_color, self.rect, 1)
        # if self.faced:
        #     self.surface.blit(self.image, self.rect.topleft)
        # else:
        #     self.surface.blit(self.back_image, self.rect.topleft)

    def on_click(self):
        self.faced = not self.faced

    def set_scored(self):
        self.faced = True
        self.border_color = pygame.Color('Green')

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

    def get_field_size(self):
        length = len(self.field)
        board_height = int(length ** 0.5)
        board_width = length // board_height + length % board_height
        return board_width, board_height

    def get_size(self):
        filed_size = self.get_field_size()
        return filed_size[0] * self.cell_width, filed_size[1] * self.cell_height

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
        self.field.all_cards_group.draw(screen)
        # self.field.all_cards_group.update()#surface=screen, border_color=self.field_line_color)

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] <= self.cell_width * len(self.field) + self.left and \
                self.top <= mouse_pos[1] <= self.cell_height * len(self.field) + self.top:
            x = (mouse_pos[0] - self.left) // self.cell_width
            y = (mouse_pos[1] - self.top) // self.cell_height
            k = x + y * self.get_field_size()[1]
            if k < len(self.field):
                return self.field.cards[k]
            else:
                return None
        else:
            return False  # Не попали в карту

    def on_click(self, card):
        card.on_click()
        if self.field.faced_card:
            if card.is_same_with(self.field.faced_card):
                self.field.faced_card.set_scored()
                card.set_scored()
                self.scores += 1
            else:
                # card.blink()
                # self.field.faced_card.blink()
                card.on_click()

                self.field.faced_card.on_click()
            self.field.faced_card = None
        else:
            self.field.faced_card = card

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
