import os
from my_sprites import load_image


def cards_generation(folder):
    for filename in os.listdir(path=folder):
        try:
            image = load_image(filename, folder)
        except Exception as exeption:
            print(f"The {filename} is not an image\n Or {exeption} occured")


cards_generation('data')
