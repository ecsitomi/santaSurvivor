import pygame
from settings import attack_img, WIDTH, HEIGHT

class Bullet(pygame.sprite.Sprite): #lövedék osztály
    def __init__(self, x, y, direction):
        super().__init__()
        self.original_image = pygame.image.load(attack_img).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7
        self.direction = direction
        self.angle = 10

    def rotation(self,angle_num): #forgatás
        self.image = pygame.transform.rotate(self.original_image, angle_num)
        self.rect = self.image.get_rect(center=self.rect.center)

    def death(self): # Törlés, ha a lövedék kimegy a képernyőről
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()  

    def move(self): #lövedék mozgása
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def update(self): #frissítés
        self.death()
        self.move()
        self.rotation(self.angle)
        self.angle += 10 #folyamatos forgatást biztosít
        
