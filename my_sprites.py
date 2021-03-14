import os

import pygame
from pygame.sprite import AbstractGroup

CARD_WIDTH = 70
CARD_HEIGHT = 80
DEFAULT_COLOR = (100, 255, 100)


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


class SpriteLabel(pygame.sprite.Sprite):
    # Надпись - текст в определенном месте экрана
    def __init__(self, text, x, y, *groups):
        self.border_inner = 10
        super().__init__(*groups)
        self.font = pygame.font.Font(None, 50)
        self.text_to_screen = text
        self.x = x
        self.y = y
        self.color = DEFAULT_COLOR
        self.border_width = 1
        self.refresh()

    def set_font(self, new_font: pygame.font.Font):
        self.font = new_font
        self.refresh()

    def set_color(self, color):
        self.color = color
        self.refresh()

    def refresh(self):
        text_image = self.font.render(self.text_to_screen, True, self.color)
        text_w = text_image.get_width()
        text_h = text_image.get_height()
        d = self.border_inner
        self.image = pygame.Surface([text_w + d * 2, text_h + d * 2])
        self.image.blit(text_image, (d, d, text_w, text_h))
        pygame.draw.rect(self.image, self.color, (0, 0, text_w + d * 2, text_h + d * 2),
                         self.border_width)
        self.rect = self.image.get_rect()
        self.move_to(self.x, self.y)

    def move_to(self, x, y):
        self.rect.x = self.x = x
        self.rect.y = self.y = y

    def set_text(self, new_text: str):
        self.text_to_screen = new_text
        self.refresh()


class Player(SpriteLabel):
    # Игрок - наследуется от надписи, добавляются имя, баллы, выделение во время хода
    # а так же обработка этих событий
    def __init__(self, name, score, x=200, y=50, *groups):
        self.name = name
        self.score = score
        super().__init__(f'{self.name}: {self.score}', x, y, *groups)
        self.add_score(0)

    def add_score(self, point):
        self.score += point
        self.text_to_screen = f'{self.name}: {self.score}'
        self.refresh()

    def set_current(self):
        self.border_width = 5
        self.refresh()

    def unset_current(self):
        self.border_width = 1
        self.refresh()


class Card(pygame.sprite.Sprite):
    # Карта с картинкой или текстом, "переворачивание" карты
    def __init__(self, text, link, *groups):
        super().__init__(*groups)
        self.faced = False
        self.pic = None
        self.image = None
        self.pos = 0, 0
        self.front_image = None
        self.size = CARD_WIDTH, CARD_HEIGHT
        self.rect = pygame.Rect(*self.pos, *self.size)
        self.text = text
        font = pygame.font.Font(None, CARD_WIDTH * 2)
        if link:
            self.pic = link
            self.front_image = pygame.transform.scale(load_image(self.pic), self.size)
        else:
            self.front_image = font.render(self.text, True, (100, 255, 100))
        self.back_image = font.render('X', True, (100, 255, 100))

        self.update()

    def is_same_with(self, other):
        return self.text == other.text

    def set_pos(self, x, y):
        self.pos = x, y
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def get_pos(self):
        return self.pos

    def update(self, *args, **kwargs) -> None:
        self.image = self.back_image
        if self.faced:
            self.image = self.front_image
        self.rect = self.image.get_rect()
        self.set_pos(*self.pos)

    def on_click(self):
        self.faced = not self.faced
        self.update()

    def set_scored(self):
        self.faced = True
        self.border_color = pygame.Color('Green')


class SpriteField(pygame.sprite.Sprite):
    # Основной класс поля игры, обработка нажатия на поле - передача нажатия в Карту
    def __init__(self, *groups: AbstractGroup, folder='data'):
        super().__init__(*groups)
        self.cards_group = pygame.sprite.Group()
        self.cards = self.cards_generation(folder)
        self.card_width = CARD_WIDTH
        self.card_height = CARD_HEIGHT
        width, height = self.get_size()
        extra_borders_x = 5 * 2 + 2 * (self.get_field_table_size()[0] - 1)
        extra_borders_y = 5 * 2 + 2 * (self.get_field_table_size()[1] - 1)
        self.image = pygame.Surface([width + extra_borders_x, height + extra_borders_y])
        self.rect = self.image.get_rect()
        self.set_pos(5, 5)
        self.cards_positioning()

    def cards_positioning(self):
        w, h = self.get_field_table_size()
        for i in range(len(self.cards)):
            col = i % w
            row = i // w
            x = 5 + self.card_width * col + 2 * col
            y = 5 + self.card_height * row + 2 * row
            self.cards[i].set_pos(x, y)
        self.update()

    def cards_generation(self, folder):
        cards_list = []
        for filename in filter(lambda s: s.split('.')[-1].lower() == 'png',
                               os.listdir(path=folder)):
            new_card1 = Card(str(len(cards_list)), folder + '/' + filename, self.cards_group)
            new_card2 = Card(str(len(cards_list)), folder + '/' + filename, self.cards_group)
            cards_list.append(new_card1)
            cards_list.append(new_card2)
        import random
        return list(random.sample(cards_list, len(cards_list)))

    def get_field_table_size(self):
        """Размеры таблицы для карточек"""
        length = len(self.cards)
        table_height = int(length ** 0.5)
        table_width = length // table_height + length % table_height
        return table_width, table_height

    def get_size(self):
        """Размеры поля с карточками"""
        field_table_size = self.get_field_table_size()
        return field_table_size[0] * self.card_width, field_table_size[1] * self.card_height

    def update(self, *args, **kwargs) -> None:
        self.image.fill('Yellow')
        self.cards_group.draw(self.image)

    def set_pos(self, x, y):
        """Установить позицию поля"""
        self.rect.x = x
        self.rect.y = y

    def on_click(self, mouse_pos):
        # обработка нажатия на поле - передача нажатия в Карту
        # print(*mouse_pos)
        if self.rect.x < mouse_pos[0] < self.rect.x + self.rect.width and \
                self.rect.y < mouse_pos[1] < self.rect.y + self.rect.height:
            pos = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
            # print(f"Pos in table {pos[0]}, {pos[1]}")
            x = (pos[0]) // self.card_width
            y = (pos[1]) // self.card_height
            # print(f"coords in table - {x} {y}")
            k = x + y * self.get_field_table_size()[0]
            if 0 <= k < len(self.cards):
                # print(f"Card number - {k}")
                self.cards[k].on_click()
                return self.cards[k]
        return None
