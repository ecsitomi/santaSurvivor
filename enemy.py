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

    def import_character_assets(self): # hogyan jussunk el a képekhez
        character_path = 'img/enemy/' # hol a karakter könyvtár
        for animation in self.animations.keys(): # animation szótárban hozzá akarom rendelni a keys-eket
            full_path = character_path + animation # kép teljes elérési útja
            self.animations[animation] = import_folder(full_path) # ez a függvény visszaad egy listát a megfelelő animációhoz a szótárban

    def get_status(self): # karakter státusz változása
        if self.direction.x != 0 and not self.attack: # vízszintes irányú mozgás
            self.status = 'walk' # futás
        elif self.attack:
            self.status = 'attack' #támadás
        elif self.death: 
            self.status='death' #meghalt
        else:
            self.status = 'idle' # más esetben áll

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


    def update(self): # játékos folyamatos frissítése
        self.get_status()
        self.animate()

        
