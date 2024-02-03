import pygame
from settings import setup_font

class Damage(pygame.sprite.Sprite):  # sebzés osztály
    def __init__(self,number, x, y,color):
        super().__init__()
        self.counter = 0
        self.font=setup_font(16) #betűtípus és méret
        self.image=self.font.render(f'{number}', True, color) #mit
        self.rect=self.image.get_rect(center=(x,y-40)) #hova

    def counting(self):
        self.counter += 1
        if self.counter >= 15:
            self.kill()

    def update(self):
        self.counting()