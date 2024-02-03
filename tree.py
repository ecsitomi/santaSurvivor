import pygame
from settings import tree_img

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

    def jump(self,speed,min,max,hit): #pattogás
        if self.up:
            self.rect.y -= self.jump_speed
            self.jump_speed -= speed
            if self.jump_speed == min:
                self.up = False
                self.down = True
        elif self.down:
            self.rect.y += self.jump_speed
            self.jump_speed += speed
            if self.jump_speed == max:
                self.up = True
                self.down = False
                self.hit += 1
                if self.hit == hit:
                    self.first = False

    def jump_bumb(self,counting): #fa koordinálása
        if self.first:
            self.jump(0.5,1,9,3)
        if not self.first:
            self.counter += 1
            if self.counter % counting == 0:
                self.first = True
                self.up = True
                self.down = False
        

    def update(self): #frissítés
        self.jump_bumb(1111)