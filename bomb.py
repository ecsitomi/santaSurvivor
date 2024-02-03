import pygame
import random
from settings import bomb_img

class Bomb(pygame.sprite.Sprite):  # sebzés osztály
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load(bomb_img).convert_alpha()
        self.image = self.original_image
        self.random_number = random.randint(-90, 90)
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = 0

    def rotation(self, angle_num): # forgatás
        self.image = pygame.transform.rotate(self.original_image, angle_num)
        self.rect = self.image.get_rect(center=self.rect.center)

    def counting(self): #visszaszámlálás & törlés
        self.counter += 1
        if self.counter >= 10:
            self.kill()

    def update(self): # frissítés
        self.rotation(self.random_number)
        self.counting()

