import random

import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 20
        self.cell_size = 50
        # Стандартные карточки - числа в массиве
        cards_data = random.choices(range(10, 100), k=10)
        cards_number = len(cards_data) * 2
        # генерация поля карточек
        cards = range(10, 100) # список карточек для игры - TODO: объекты карточек
        cards_data = random.choices(cards, k=14)
        cards_number = len(cards_data) * 2
        field = []
        height = int(cards_number ** 0.5)
        width = cards_number // height
        last_line_card_number = cards_number % height
        for i in range(height):
            field.append([-1] * width)
        if last_line_card_number:
            field.append([-1] * last_line_card_number)
        cards_to_add = random.sample(cards_data * 2, k=len(cards_data) * 2)
        k = 0
        for row in range(len(field)):
            for col in range(len(field[row])):
                field[row][col] = cards_to_add[k]
                k += 1

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen=pygame.display.set_mode((1, 1))):
        screen.fill((0, 0, 0))
        # Надпись на экране игры
        font = pygame.font.Font(None, 50)
        text = font.render("Welcome to Memoryno!", True, (100, 255, 100))
        text_x = screen.get_width() // 2 - text.get_width() // 2
        text_y = 15  # screen.get_height() // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)
        # КОНЕЦ Надпись на экране игры


    def get_cell(self, mouse_pos):
        pass

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)
