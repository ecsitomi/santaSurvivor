import pygame
from pygame.sprite import _Group
from settings import WIDTH,HEIGHT
from support import import_folder #segít a képfájlok rendszerezésében

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations={'idle':[],'run':[],'death':[]} #animációk szótára
        self.import_character_assets() #karakter képek betöltése
        self.frame_index=0 #képek indexeinek száma
        self.animation_speed=0.15 #indexelés sebessége
        self.image=self.animations['idle'][self.frame_index] #kezdő kép
        self.rect=self.image.get_rect(center=(WIDTH/2,HEIGHT/2)) #kezdő pozíció
        self.direction=pygame.math.Vector2(0,0) #x,y irányú vektoriális elmozdulás (lényeg, csak irányt mutat)
        self.speed=8 #mozgás sebessége
        self.on_ground=True #földön van e
        self.counter=0 #számláló
        self.status='idle' #kezdő státusz
        self.facing_right=True #jobbranéz

    def import_character_assets(self): #hogyan jussunk el a képekhez
        character_path='img/santa/' #hol a karakter könyvtár
        for animation in self.animations.keys(): #animation szótárban hozzá akarom rendelni a keys-eket
            full_path=character_path+animation
            self.animations[animation]=import_folder(full_path) #ez a függvény visszaad egy listát a megfelelő animációhoz a szótárban

    def get_input(self): #gombnyomásra mit tegyen
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: #jobb
            self.direction.x=1 #iránymódosítás
            self.facing_right=True #jobbranéz
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]: #bal
            self.direction.x=-1 #iránymódosítás
            self.facing_right=False #balranéz
        else:
            self.direction.x=0 #ha nincs elmozdulás nincs iránymódosítás

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

    def update(self): #játékos folyamatos frissítése
        self.get_input() #milyen billenytyű parancsot kapott
        self.get_status() #mozgás státusz
        self.animate() #animálás