import pygame


class SpriteLabel(pygame.sprite.Sprite):
    def __init__(self, text, x, y, *groups):
        self.border_inner = 10
        # Надпись на экране игры
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
        self.rect.x = x
        self.rect.y = y
        # КОНЕЦ Надпись на экране игры

    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y


if __name__ == '__main__':
    pygame.init()
    spriteGroup = pygame.sprite.Group()
    surface = pygame.display.set_mode((500, 500))
    sprite = SpriteLabel('Sample Text', 150, 150, spriteGroup)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sprite.move_to(sprite.rect.x, sprite.rect.y - 10)
        surface.fill((0, 0, 0))
        spriteGroup.draw(surface)
        spriteGroup.update()
        pygame.display.flip()
