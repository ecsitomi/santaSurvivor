import pygame
from support import import_folder
from settings import WIDTH,HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animations = {'idle': [], 'walk': [], 'death': [], 'attack': []} # animációk szótára
        self.import_character_assets() # karakter képek betöltése
        self.frame_index = 0 # képek indexeinek száma
        self.animation_speed = 0.15 # indexelés sebessége
        self.image = self.animations['idle'][self.frame_index] # kezdő kép
        self.rect = self.image.get_rect(center=(x, y)) # kezdő pozíció
        self.direction = pygame.math.Vector2(0, 0) # x, y irányú vektoriális elmozdulás (lényeg, csak irányt mutat)
        self.speed = 5 # mozgás sebessége
        self.counter = 0 # számláló
        self.status = 'idle' # kezdő státusz
        self.facing_right = True # jobbranéz
        self.death=False
        self.attack=False
        self.resize_death(5.8)

    def import_character_assets(self): # hogyan jussunk el a képekhez
        character_path = 'img/enemy/' # hol a karakter könyvtár
        for animation in self.animations.keys(): # animation szótárban hozzá akarom rendelni a keys-eket
            full_path = character_path + animation # kép teljes elérési útja
            self.animations[animation] = import_folder(full_path,1.3) # ez a függvény visszaad egy listát a megfelelő animációhoz a szótárban

    def get_status(self): # karakter státusz változása
        if self.death: 
            self.status='death' #meghalt
            self.speed=0 #sebesség 0
            self.direction=pygame.math.Vector2(0,0) #irány 0
        if not self.death:
            if self.direction.x != 0 and not self.attack: # vízszintes irányú mozgás
                self.status = 'walk' # futás
            elif self.attack:
                self.status = 'attack' #támadás
            else:
                self.status = 'idle' # más esetben áll
                self.speed=0 #sebesség 0
                self.direction=pygame.math.Vector2(0,0) #irány 0

    def animate(self): # státusznak megfelelő animálás
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed # indexelés növelése
        if self.frame_index >= len(animation): # hogy ne indexeljünk túl
            self.frame_index = 0

        image = animation[int(self.frame_index)] # státusznak megfelelő kép indexelve
        if self.direction.x >= 0: # ha jobbranéz
            self.image = image
            self.facing_right = True
        elif self.direction.x < 0: # ha balranéz
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.facing_right = False

    def death_animation(self):
        if self.status == 'death' and self.frame_index >= len(self.animations['death']) - 1:
            self.frame_index = 0  # Nullázd vissza a frame_index-et
            self.kill()

    def resize_death(self, size):
        for i in range(len(self.animations['death'])):
            self.animations['death'][i] = pygame.image.load('img/enemy/death/' + str(i) + '.png').convert_alpha()

        for i in range(len(self.animations['death'])):
            self.animations['death'][i] = pygame.transform.scale(self.animations['death'][i], (self.animations['death'][i].get_width() / size, self.animations['death'][i].get_height() / size))


    def update(self): # játékos folyamatos frissítése
        self.get_status()
        self.animate()
        self.death_animation()

        
