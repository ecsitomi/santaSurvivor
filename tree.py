import pygame
from settings import WIDTH, HEIGHT, tree_img

class Tree(pygame.sprite.Sprite): #fa osztály
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(tree_img).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.jump_speed = 9 
        self.counter = 0
        self.first = True
        self.up = True
        self.down = False
        self.hit=0

    def jump(self):
        if self.up:
            self.rect.y -= self.jump_speed
            self.jump_speed -= 0.5
            if self.jump_speed == 1:
                self.up = False
                self.down = True
        elif self.down:
            self.rect.y += self.jump_speed
            self.jump_speed += 0.5
            if self.jump_speed == 9.5:
                self.up = True
                self.down = False
                self.hit += 1
                if self.hit == 3:
                    self.first = False

    def first_jump(self): #fa hozzáadása  
        if self.first:
            self.jump()
        if not self.first:
            self.counter += 1
            if self.counter % 511 == 0:
                self.first = True
                self.up = True
                self.down = False
        

    def update(self): #frissítés
        self.first_jump()
        