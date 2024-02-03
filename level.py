import pygame, random, math
from settings import *
from player import Player
from enemy import Enemy
from tiles import OtherTile
from bullet import Bullet
from tree import Tree
from hit import Hit
from bomb import Bomb
from damage import Damage

# inicializálás
class Level:
    def __init__(self, level_data, surface):
        self.starting=True
        self.display_surface = surface # játékablak hivatkozva a mainből
        self.counter=0
        self.attack_counter=0
        self.tree_counter=0
        self.weapon_level=1
        self.level=1
        self.hit_counter=0
        self.high_score=0
        self.start_time = pygame.time.get_ticks() 

        #sprite csoportok
        self.player = pygame.sprite.GroupSingle() 
        self.enemies = pygame.sprite.Group()
        self.other_tiles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.hit = pygame.sprite.Group()
        self.bomb = pygame.sprite.Group()
        self.damage = pygame.sprite.Group()

        self.setup_BG(BG_IMG) # háttérkép betöltése
        self.setup_level(level_data) # pálya betöltése

    def setup_BG(self,img): #háttérkép betöltése
        self.bg_surf = pygame.image.load(img).convert_alpha()
        self.bg_rect = self.bg_surf.get_rect()
        self.bg_surf = self.scale_background()
    
    def scale_background(self): #háttérkép méretezése
        original_width, original_height = self.bg_surf.get_size()  # Az eredeti háttérkép méretének lekérdezése

        # Az új méretek kiszámolása az ablak méretéhez igazítva
        new_height = HEIGHT
        new_width = int(original_width * (HEIGHT / original_height))
        
        return pygame.transform.scale(self.bg_surf, (new_width, new_height)) # Háttérkép méretének beállítása és visszaadása

    def setup_level(self, layout): #pálya betöltése
        player_sprite = Player()
        self.player.add(player_sprite)
        for row_index, row in enumerate(layout):
            for col_index, tile_type in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if tile_type in others:
                    tile = OtherTile(tile_size, x, y, tile_type)
                    self.other_tiles.add(tile)

    def movement(self): #mozgás
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed #mozgás -> irány*sebesség
        player.rect.y+=player.direction.y*player.speed 

        #mozgás korlátozása
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH
        if player.rect.left < 0: 
            player.rect.left = 0 
        if player.rect.top < 0: 
            player.rect.top = 0 
        if player.rect.bottom > HEIGHT: 
            player.rect.bottom = HEIGHT 

    def create_zombi_horizontal(self): #zombi létrehozása oldalt
        x=random.randint(-50,WIDTH+50)
        y=random.choice([-50,HEIGHT+50])
        zombi=Enemy(x,y)
        self.enemies.add(zombi)

    def create_zombi_vertical(self): #zombi létrehozása fent/lent
        x=random.choice([-50,WIDTH+50])
        y=random.randint(-50,HEIGHT+50)
        zombi=Enemy(x,y)
        self.enemies.add(zombi)
    
    def add_zombi(self): #zombi hozzáadása
        self.counter+=1
        if self.counter%100-3*self.level==0:
            self.create_zombi_horizontal()
        if self.counter%250-5*self.level==0:
            self.create_zombi_horizontal()
        if self.counter%150-5*self.level==0:
            self.create_zombi_vertical()
        if self.counter%200-3*self.level==0:
            self.create_zombi_vertical()

        if self.level > 6:
            if self.counter%100==0:
                self.create_zombi_horizontal()
        if self.level > 8:
            if self.counter%100==0:
                self.create_zombi_vertical()
            
    def zombi_move(self): #zombi mozgása
        player_pos = self.player.sprite.rect.center
        for zombi in self.enemies:
            angle = math.atan2(player_pos[1] - zombi.rect.centery, player_pos[0] - zombi.rect.centerx)
            zombi.direction = pygame.math.Vector2(math.cos(angle), math.sin(angle))
            zombi.rect.x += zombi.direction.x * zombi.speed
            zombi.rect.y += zombi.direction.y * zombi.speed

    def zombi_attack(self): #zombi támadása
        player = self.player.sprite
        for zombi in self.enemies:
            if not zombi.death:
                if abs(player.rect.x - zombi.rect.x) < 200 and abs(player.rect.y - zombi.rect.y) < 200:
                    zombi.attack=True
                else:
                    zombi.attack=False

                if not player.death:
                    if zombi.rect.colliderect(player.rect):
                        player.health-=1
                        zombi.rect.x += zombi.direction.x * zombi.speed *-0.5
                        zombi.rect.y += zombi.direction.y * zombi.speed *-1
                        self.hit_counter+=1
                        if self.hit_counter % 25 == 0:
                            hit_sign = Hit(player.rect.centerx, player.rect.centery)
                            self.hit.add(hit_sign)

    def santa_attack(self,weapon_level): #játékos támadása
        self.attack_counter += 1
        player = self.player.sprite
        if not player.death:
            if len(self.enemies)==0 and len(self.bullets)!=0:
                for bullet in self.bullets:
                    bullet.kill()
            if len(self.enemies)!=0:
                if self.attack_counter % 70-3*weapon_level == 0:
                    for _ in range(weapon_level):
                        target = random.choice(self.enemies.sprites()) #véletlen célpont, folyton frissül
                        angle = math.atan2(target.rect.centery - player.rect.centery, target.rect.centerx - player.rect.centerx) #szög folyamatos frissítése
                        direction = pygame.math.Vector2(math.cos(angle), math.sin(angle)) #irány folyamatos frissítése
                        bullet = Bullet(player.rect.centerx, player.rect.centery, direction) #itt az irány már fix érték lesz
                        self.bullets.add(bullet)

        # Ütközések kezelése
        for enemy in self.enemies:
            if pygame.sprite.spritecollide(enemy, self.bullets, True):
                bomb_sign = Bomb(enemy.rect.centerx, enemy.rect.centery)
                self.bomb.add(bomb_sign)
                enemy.death = True
                random_number = random.randint(10, 30)
                dmg = Damage(random_number, enemy.rect.centerx, enemy.rect.centery, RED)
                self.damage.add(dmg)
                player.points += random_number
                player.kills += 1
                
    def create_tree(self): #karácsonyfa létrehozása
        x=random.randint(50,WIDTH-50)
        y=random.randint(100,HEIGHT-50)
        tree=Tree(x,y)
        self.trees.add(tree)

    def add_tree(self): #karácsonyfa hozzáadása
        self.tree_counter+=1
        random_number=random.randint(500,800)
        if self.counter%random_number==0:
            self.create_tree()

        self.trees.draw(self.display_surface) #kirajzolás

        #ütközés
        for tree in self.trees:
            tree.update()
            if tree.rect.colliderect(self.player.sprite.rect):
                random_number = random.randint(30,60)
                self.player.sprite.points+=random_number
                self.player.sprite.health+=50
                dmg = Damage('+HP/LvL', tree.rect.centerx, tree.rect.centery, GREEN)
                self.damage.add(dmg)
                tree.kill()
                self.level_correction()
                
    def santa_death(self): #játékos halála
        player = self.player.sprite
        if player.status == 'death':
            for zombi in self.enemies:
                zombi.status='idle'
                zombi.speed=0
            self.trees.empty()
            self.hit.empty()
            if player.points>self.high_score:
                self.high_score=player.points
        if self.counter%200==0:
            self.restart()
                
    def starter(self,time):#kezdőképernyő
        if self.starting: 
            font=setup_font(111) 
            text=font.render('Santa Survivor', True, RED) 
            text_rect=text.get_rect(center=(WIDTH/2,HEIGHT/2)) 
            self.display_surface.blit(text,text_rect) 
            pygame.display.update() 
            pygame.time.delay(time) 
            self.starting=False    

    def restart(self): #újraindítás
        player = self.player.sprite
        if player.death:
            self.counter=0
            self.attack_counter=0
            self.tree_counter=0
            self.weapon_level=1
            self.level=1
            self.hit_counter=0
            self.player.empty()
            self.enemies.empty()
            self.other_tiles.empty()
            self.bullets.empty()
            self.trees.empty()
            self.hit.empty()
            self.bomb.empty()
            self.starting=True
            self.starter(850)
            self.setup_level(level_map)
            self.start_time = pygame.time.get_ticks()
    
    def statsOnScreen(self): #életerő és pontok kiiratása
        player = self.player.sprite
        font=setup_font(32) #felül megjelenő adatok
        text=font.render(f'Health: {player.health//10}  Kills: {player.kills}  Points: {player.points}', True, BLUE) #mit
        text_rect=text.get_rect(center=(WIDTH/2,50)) #hova
        self.display_surface.blit(text,text_rect)

        font2=setup_font(18) #alul megjelenő adatok
        text2=font2.render(f'Saved Christmas Trees: {self.level-1}  Highest: {self.high_score}', True, RED) #mit
        text_rect2=text2.get_rect(center=(WIDTH/2,HEIGHT-30))
        self.display_surface.blit(text2,text_rect2)

    def get_elapsed_time(self): #eltelt idő kiszámolása
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) // 1000  # Másodpercekben
        return elapsed_time

    def display_elapsed_time(self): #eltelt idő kiiratása
        sec =  self.get_elapsed_time()
        minute = sec // 60
        hour = 0
        if sec == 60:
            minute += 1
            sec = 0
        if minute == 60:
            hour += 1
            minute = 0
        font = setup_font(32)
        text = font.render(f'{minute}:{sec}', True, BLUE)
        text_rect = text.get_rect(center=(WIDTH/2, 100))
        self.display_surface.blit(text, text_rect)
    
    def level_correction(self): #szintlépés
        self.level +=1 
        player = self.player.sprite
        if self.level%3==0:
            self.weapon_level+=1
            if self.weapon_level>4:
                self.weapon_level=4
        if self.level%2==0:
            player.speed+=1
            if player.speed>13:
                player.speed=13
        if player.health>1000:
            player.health=1000      
    
    #futtatás
    def run(self):
        self.display_surface.blit(self.bg_surf, self.bg_rect)  # háttérkép kirajzolása
        self.starter(1000) #kezdőképernyő
        self.statsOnScreen() #életerő és pontok kiiratása
        self.display_elapsed_time() #eltelt idő kiiratása
        self.enemies.update()  # ellenség update
        self.enemies.draw(self.display_surface)  # ellenség kirajzolása
        self.player.update()  # játékos frissítése
        self.player.draw(self.display_surface)  # játékos kirajzolása a (játékablakban)
        self.bullets.update() #golyók frissítése
        self.bullets.draw(self.display_surface) #golyók kirajzolása
        self.hit.update() #találat frissítése
        self.hit.draw(self.display_surface) #találat kirajzolása
        self.bomb.update() #robbanás frissítése
        self.bomb.draw(self.display_surface) #robbanás kirajzolása
        self.damage.update() #sebzés frissítése
        self.damage.draw(self.display_surface) #sebzés kirajzolása
        self.movement()  #mozgás & ütközések
        self.add_zombi() #zombi hozzáadása
        self.zombi_move() #zombi mozgása
        self.zombi_attack() #zombi támadása
        self.santa_attack(self.level) #játékos támadása
        self.add_tree() #jutalom fák hozzáadása
        self.santa_death() #játékos halála