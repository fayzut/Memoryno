import os

import pygame
from pygame.sprite import AbstractGroup


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
    def __init__(self, text, x, y, *groups):
        self.border_inner = 10
        super().__init__(*groups)
        font = pygame.font.Font(None, 50)
        text_image = font.render(text, True, (100, 255, 100))
        text_w = text_image.get_width()
        text_h = text_image.get_height()
        d = self.border_inner
        self.image = pygame.Surface([text_w + d * 2, text_h + d * 2])
        self.image.blit(text_image, (d, d, text_w, text_h))
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, text_w + d * 2, text_h + d * 2), 1)
        self.rect = self.image.get_rect()
        self.move_to(x, y)
        # КОНЕЦ Надпись на экране игры

    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Card(pygame.sprite.Sprite):
    def __init__(self, text, link, *groups):
        super().__init__(*groups)
        self.faced = False
        self.pic = None
        self.image = None
        self.front_image = None
        self.size = 50, 50
        self.rect = pygame.Rect(0, 0, *self.size)
        self.text = text
        font = pygame.font.Font(None, 50)
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
        self.rect.x = x
        self.rect.y = y

    def update(self, *args, **kwargs) -> None:  # (self, surface, border_color):
        self.image = self.back_image
        if self.faced:
            self.image = self.front_image
        self.rect = self.image.get_rect()

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


class SpriteField(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.cards = []
        self.card_width = 50
        self.card_height = 60

    def cards_generation(self, folder):
        cards_list = []
        for filename in os.listdir(path=folder):
            new_card = Card('1', filename, *self.groups())
            cards_list.append(new_card)
        return cards_list

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
        pass

    def set_pos(self, x, y):
        """Установить позицию поля"""
        self.rect.x = x
        self.rect.y = y



