import pygame
from settings import WIDTH, HEIGHT, attack_img

class Bullet(pygame.sprite.Sprite): #lövedék osztály
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(attack_img).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7  # Lövedék sebessége
        self.direction = pygame.math.Vector2(0,0)

    def update(self):
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()  # Törlés, ha a lövedék kimegy a képernyőről