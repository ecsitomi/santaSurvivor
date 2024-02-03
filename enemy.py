import pygame
from support import import_folder


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animations = {'idle': [], 'walk': [], 'death': [], 'attack': []}
        self.import_character_assets() # karakter képek betöltése
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.counter = 0
        self.status = 'walk'
        self.facing_right = True
        self.death=False
        self.attack=False
        self.resize_death(5.8)

    def import_character_assets(self): #a karakter képeinek betöltése
        character_path = 'img/enemy/'
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path,1.3)

    def get_status(self): # karakter státusz változása
        if self.death: 
            self.status='death'
            self.speed=0
            self.direction=pygame.math.Vector2(0,0)
        if not self.death:
            if self.status == 'idle':
                self.speed=0
            elif self.direction.x != 0 and not self.attack:
                self.status = 'walk'
            elif self.attack:
                self.status = 'attack'

    def animate(self): # karakter animációja
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.direction.x >= 0:
            self.image = image
            self.facing_right = True
        elif self.direction.x < 0:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.facing_right = False

    def death_animation(self): # halál animációja, hogy ne ismétlődjön
        if self.status == 'death' and self.frame_index >= len(self.animations['death']) - 1:
            self.frame_index = 0
            self.kill()

    def resize_death(self, size): #halál animáció képeinek átméretezése
        for i in range(len(self.animations['death'])):
            self.animations['death'][i] = pygame.image.load('img/enemy/death/' + str(i) + '.png').convert_alpha()

        for i in range(len(self.animations['death'])):
            self.animations['death'][i] = pygame.transform.scale(self.animations['death'][i], (self.animations['death'][i].get_width() / size, self.animations['death'][i].get_height() / size))

    def update(self): #frissítés
        self.get_status()
        self.animate()
        self.death_animation()

        
