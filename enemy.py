import pygame, math
from tiles import Tile
from support import import_folder
from settings import WIDTH,HEIGHT
from level import player_pos
from random import randint


class Enemy(Tile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y)
        self.animations={'idle':[],'walk':[],'death':[], 'attack':[]} #animációk szótára
        self.import_character_assets() #karakter képek betöltése
        self.frame_index=0 #képek indexeinek száma
        self.animation_speed=0.15 #indexelés sebessége
        self.image=self.animations['idle'][self.frame_index] #kezdő kép
        self.rect=self.image.get_rect(left=(WIDTH-20,HEIGHT/2)) #kezdő pozíció
        self.direction=pygame.math.Vector2(0,0) #x,y irányú vektoriális elmozdulás (lényeg, csak irányt mutat)
        self.speed=8 #mozgás sebessége
        self.counter=0 #számláló
        self.status='idle' #kezdő státusz
        self.facing_right=True #jobbranéz

    def import_character_assets(self): #hogyan jussunk el a képekhez
        character_path='img/enemy/' #hol a karakter könyvtár
        for animation in self.animations.keys(): #animation szótárban hozzá akarom rendelni a keys-eket
            full_path=character_path+animation #kép teljes elérési útja
            self.animations[animation]=import_folder(full_path) #ez a függvény visszaad egy listát a megfelelő animációhoz a szótárban

    def get_status(self): #karakter státusz változása
        if self.direction.x!=0: #vízszintes irányú mozgás
                self.status='run' #futás
        else:
            self.status='idle' #más esetben áll

    def animate(self): #státusznak megfelelő animálás
        animation=self.animations[self.status]
        self.frame_index+=self.animation_speed #indexelés növelése
        if self.frame_index>=len(animation): #hogy ne indexeljünk túl
            self.frame_index=0

        image=animation[int(self.frame_index)] #státusznak megfelelő kép indexelve
        if self.facing_right: #ha jobbranéz
            self.image=image #nem kell tükrözni
        else:
            flipped_image=pygame.transform.flip(image,True,False) #kép/horizontális/vertikális tükrözés
            self.image=flipped_image

    def move(self, player_pos):
        angle = math.atan2(player_pos[1] - self.rect.centery, player_pos[0] - self.rect.centerx)
        self.direction = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def update(self, player_pos): #játékos folyamatos frissítése
        self.get_status()
        self.animate()
        self.move(player_pos)
        
