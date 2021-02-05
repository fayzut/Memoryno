import random

cards = range(10, 100)
cards_data = random.choices(cards, k=14)
cards_number = len(cards_data) * 2
field = []
height = int(cards_number ** 0.5)
width = cards_number // height
last_line_card_number = cards_number % height
for i in range(height):
    field.append([-1] * width)
if last_line_card_number:
    field.append([-1] * (last_line_card_number))
cards_to_add = random.sample(cards_data * 2, k=len(cards_data) * 2)
k = 0
for row in range(len(field)):
    for col in range(len(field[row])):
        field[row][col] = cards_to_add[k]
        k += 1

print(cards_data)
print(field)
print(cards_to_add)
