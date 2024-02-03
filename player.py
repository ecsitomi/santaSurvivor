import pygame
from support import import_folder #segít a képfájlok rendszerezésében
from settings import WIDTH, HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations = {'idle':[],'run':[],'death':[]} #animációk szótára
        self.import_character_assets() #karakter képek betöltése
        self.frame_index = 0 #képek indexeinek száma
        self.animation_speed = 0.3 #indexelés sebessége
        self.image=self.animations['idle'][self.frame_index] #kezdő kép
        self.rect=self.image.get_rect(center=(WIDTH/2,HEIGHT/2)) #kezdő pozíció
        self.direction = pygame.math.Vector2(0,0) #x,y irányú vektoriális elmozdulás (lényeg, csak irányt mutat)
        self.speed = 8 #mozgás sebessége
        self.status = 'idle' #kezdő státusz
        self.facing_right = True #jobbranéz
        #self.stop_vertical = False
        #self.stop_horizontal = False
        self.health = 1000 #élet
        self.points = 0 #pont
        self.kills = 0 #ölt
        self.death = False
        self.resize_death(5.8)

    def import_character_assets(self): #hogyan jussunk el a képekhez
        character_path='img/santa/' #hol a karakter könyvtár
        for animation in self.animations.keys(): #animation szótárban hozzá akarom rendelni a keys-eket
            full_path=character_path+animation #kép teljes elérési útja
            self.animations[animation]=import_folder(full_path,1.3) #ez a függvény visszaad egy listát a megfelelő animációhoz a szótá
    
    def get_input(self): #gombnyomásra mit tegyen
        if self.health > 0:
            keys=pygame.key.get_pressed() #gomb változó
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: #jobb
                self.direction.x=1 #iránymódosítás
                self.facing_right=True #jobbranéz
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]: #bal
                self.direction.x=-1 #iránymódosítás
                self.facing_right=False #balranéz
            else:
                self.direction.x=0 #ha nincs elmozdulás nincs iránymódosítás

            if keys[pygame.K_UP] or keys[pygame.K_w]: #fel
                self.direction.y=-1 #iránymódosítás felfelé
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]: #le
                self.direction.y=1
            else:
                self.direction.y=0 #ha nincs elmozdulás nincs iránymódosítás

    def get_status(self): #karakter státusz változása
        if self.health <= 0: #halál
            self.status = 'death'
            self.health = 0
            self.speed = 0
            self.direction = pygame.math.Vector2(0,0)
        elif self.direction.x!=0 or self.direction.y!=0: #irányú mozgás
            self.status='run' #futás
        else:
            self.status='idle' #más esetben áll


    def animate(self): #státusznak megfelelő animálás
        animation=self.animations[self.status]
        self.frame_index+=self.animation_speed #indexelés növelése
        if self.frame_index>=len(animation): #hogy ne indexeljünk túl
            self.frame_index=0 #visszaállítás
        image=animation[int(self.frame_index)] #státusznak megfelelő kép indexelve
        if self.facing_right: #ha jobbranéz
            self.image=image #nem kell tükrözni
        else:
            flipped_image=pygame.transform.flip(image,True,False) #kép/horizontális/vertikális tükrözés
            self.image=flipped_image #tükrözött kép

    def resize_death(self, size):
        for i in range(len(self.animations['death'])):
            self.animations['death'][i] = pygame.image.load('img/santa/death/' + str(i) + '.png').convert_alpha()

        for i in range(len(self.animations['death'])):
            self.animations['death'][i] = pygame.transform.scale(self.animations['death'][i], (self.animations['death'][i].get_width() / size, self.animations['death'][i].get_height() / size))


    def update(self): #frissítés
        if not self.death: #ha él
            self.get_status()
            self.get_input()
            self.animate()

            #halál animáció végének vizsgálata
            if self.status == 'death' and self.frame_index >= len(self.animations['death']) - 1:
                self.death = True
                self.frame_index = len(self.animations['death']) - 1  # Állítsd a frame_index-et a death animáció utolsó képére.
        
            