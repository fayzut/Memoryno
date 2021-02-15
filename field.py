import random

import pygame

STANDART_COLOR = (0, 255, 0)


class Card:
    def __init__(self, data, left=0, top=0, width=50, height=50):
        self.faced = True
        self.pic = ''
        self.text = data
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.border = 1
        self.border_color = STANDART_COLOR
        self.text_color = STANDART_COLOR
        self.text_font = pygame.font.Font(None, 50)

    def draw(self, surfase=pygame.display.set_mode((1, 1)), x=0, y=0):
        pygame.draw.rect(surfase, self.border_color, (x, y, self.width, self.height), 1)
        if self.faced:
            text = self.text_font.render(self.text, True, (100, 255, 100))
        else:
            text = self.text_font.render('X', True, (100, 255, 100))
        text_x = x + (self.width - text.get_width()) // 2
        text_y = y + (self.height - text.get_height()) // 2
        surfase.blit(text, (text_x, text_y))

    def on_click(self):
        self.faced = not self.faced

    def set_scored(self):
        self.faced = True
        self.text = '+'


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


class Board:
    # создание поля
    def __init__(self, cards=range(10, 100), cards_to_use=14, left=20, top=60, cell_width=50,
                 cell_height=50):
        self.need_to_render = True
        # значения по умолчанию
        self.top = top
        self.left = left
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cell_border_width = 1
        self.set_view(self.left, self.top, self.cell_width, self.cell_height)

        self.field_line_color = STANDART_COLOR
        # Стандартные карточки - числа в массиве
        # генерация поля карточек
        # cards = range(10, 100)  # список карточек для игры - TODO: объекты карточек Card
        cards_data = random.choices(cards, k=cards_to_use)
        cards_number = len(cards_data) * 2
        self.field = []
        height = int(cards_number ** 0.5)
        width = cards_number // height
        last_line_card_number = cards_number % height
        for i in range(height):
            self.field.append([-1] * width)
        if last_line_card_number:
            self.field.append([-1] * last_line_card_number)
        cards_to_add = random.sample(cards_data * 2, k=len(cards_data) * 2)
        k = 0
        for row in range(len(self.field)):
            for col in range(len(self.field[row])):
                self.field[row][col] = Card(str(cards_to_add[k]))
                k += 1

        self.faced_card = None
        self.scores = 0

    # настройка внешнего вида
    def set_view(self, left, top, cell_width, cell_height):
        self.left = left
        self.top = top
        self.cell_width = cell_width
        self.cell_height = cell_height

    def render(self, screen=pygame.display.set_mode((1, 1))):
        screen.fill((0, 0, 0))
        # Надпись на экране игры
        font = pygame.font.Font(None, 50)
        text = font.render("Welcome to Memoryno!", True, (100, 255, 100))
        text_x = screen.get_width() // 2 - text.get_width() // 2
        text_y = 10  # screen.get_height() // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)
        # КОНЕЦ Надпись на экране игры
        # Надписи счета
        scores = Label(f'Счет: {self.scores}', screen, (screen.get_width() - 200, 100))
        scores.draw()
        # Конец Надписи счета

        for row in range(len(self.field)):
            for col in range(len(self.field[row])):
                pygame.draw.rect(screen, self.field_line_color,
                                 (self.left + self.cell_width * col,
                                  self.top + self.cell_height * row,
                                  self.cell_width + self.cell_border_width,
                                  self.cell_height + self.cell_border_width
                                  ), self.cell_border_width)
                self.field[row][col].draw(screen, self.left + self.cell_width * col,
                                          self.top + self.cell_height * row)

        # self.need_to_render = False

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
                card.on_click()
                self.faced_card.on_click()
            self.faced_card = None
        else:
            self.faced_card = card

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
