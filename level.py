import pygame, random, math
from player import Player
from enemy import Enemy
from tiles import OtherTile
from settings import tile_size, others, WIDTH, HEIGHT, BG_IMG
from bullet import Bullet
from tree import Tree

# inicializálás
class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface # játékablak a main-ben meghatározottak szerint
        self.counter=0
        self.attack_counter=0
        self.tree_counter=0
        self.weapon_level=1

        self.player = pygame.sprite.GroupSingle() #csoportok amibe jönnek a sprite-ok
        self.enemies = pygame.sprite.Group()
        self.other_tiles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()

        # háttérkép betöltése és méretezése
        self.bg_surf = pygame.image.load(BG_IMG).convert_alpha()
        self.bg_rect = self.bg_surf.get_rect()
        self.bg_surf = self.scale_background()

        self.setup_level(level_data) # pálya betöltése

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

    def create_zombi_horizontal(self):
        x=random.randint(-50,WIDTH+50)
        y=random.choice([-50,HEIGHT+50])
        zombi=Enemy(x,y)
        self.enemies.add(zombi)

    def create_zombi_vertical(self):
        x=random.choice([-50,WIDTH+50])
        y=random.randint(-50,HEIGHT+50)
        zombi=Enemy(x,y)
        self.enemies.add(zombi)
    
    def add_zombi(self): #zombi hozzáadása
        self.counter+=1
        if self.counter%100==0:
            self.create_zombi_horizontal()
        if self.counter%150==0:
            self.create_zombi_vertical()
            
    def zombi_move(self):
        player_pos = self.player.sprite.rect.center
        for zombi in self.enemies:
            angle = math.atan2(player_pos[1] - zombi.rect.centery, player_pos[0] - zombi.rect.centerx)
            zombi.direction = pygame.math.Vector2(math.cos(angle), math.sin(angle))
            zombi.rect.x += zombi.direction.x * zombi.speed
            zombi.rect.y += zombi.direction.y * zombi.speed

    def zombi_attack(self):
        player = self.player.sprite
        for zombi in self.enemies:
            if abs(player.rect.x - zombi.rect.x) < 200 and abs(player.rect.y - zombi.rect.y) < 200:
                zombi.attack=True
            else:
                zombi.attack=False

            if zombi.rect.colliderect(player.rect):
                player.health-=1

    def santa_attack(self,weapon_level): #játékos támadása
        self.attack_counter += 1
        player = self.player.sprite
        if len(self.enemies)==0 and len(self.bullets)!=0:
            for bullet in self.bullets:
                bullet.kill()
        if len(self.enemies)!=0:
            target = random.choice(self.enemies.sprites()) #véletlen célpont, folyton frissül
            angle = math.atan2(target.rect.centery - player.rect.centery, target.rect.centerx - player.rect.centerx) #szög folyamatos frissítése
            direction = pygame.math.Vector2(math.cos(angle), math.sin(angle)) #irány folyamatos frissítése
            if self.attack_counter % 75 == 0:
                for i in range(weapon_level):
                    bullet = Bullet(player.rect.centerx, player.rect.centery, direction) #itt az irány már fix érték lesz
                    self.bullets.add(bullet)


        # Ütközések kezelése
        for enemy in self.enemies:
            if pygame.sprite.spritecollide(enemy, self.bullets, True):
                enemy.kill()
                player.kills += 1

    def create_tree(self): #karácsonyfa létrehozása
        x=random.randint(50,WIDTH-50)
        y=random.randint(100,HEIGHT-50)
        tree=Tree(x,y)
        self.trees.add(tree)

    def add_tree(self): #karácsonyfa hozzáadása
        self.tree_counter+=1
        if self.counter%700==0:
            self.create_tree()

        self.trees.draw(self.display_surface)

        for tree in self.trees:
            tree.update()
            if tree.rect.colliderect(self.player.sprite.rect):
                self.player.sprite.points+=1
                tree.kill()
                
    ''' #HIBÁS!!!!!!!!!!!!!!!!!!
    def tile_collision(self): #ütközések a csempékkel
        player=self.player.sprite #játékos sprite
        
        for sprite in self.other_tiles.sprites():
            if sprite.rect.colliderect(player.rect): #ha ütközik az egyik csempével

                if player.direction.x > 0 and player.rect.right > sprite.rect.left and not player.stop_horizontal and player.facing_right: #JOBBRA
                    player.rect.right -= player.speed
                    player.stop_vertical = True

                elif player.direction.x < 0 and player.rect.left < sprite.rect.right and not player.stop_horizontal and not player.facing_right: #BALRA
                    player.rect.left += player.speed
                    player.stop_vertical = True

                if player.direction.y > 0 and player.rect.bottom > sprite.rect.top and not player.stop_vertical: #LE
                    player.rect.bottom -= player.speed
                    player.stop_horizontal = True

                elif player.direction.y < 0 and player.rect.top < sprite.rect.bottom and not player.stop_vertical: #FEÉ
                    player.rect.top += player.speed
                    player.stop_horizontal = True
                else:
                    player.stop_vertical = False
                    player.stop_horizontal = False
        '''

    #futtatás
    def run(self):
        self.movement()  #mozgás & ütközések
        self.display_surface.blit(self.bg_surf, self.bg_rect)  # háttérkép kirajzolása
        self.enemies.update()  # ellenség update
        self.enemies.draw(self.display_surface)  # ellenség kirajzolása
        self.player.update()  # játékos frissítése
        self.player.draw(self.display_surface)  # játékos kirajzolása a (játékablakban)
        self.add_zombi() #zombi hozzáadása
        self.enemies.draw(self.display_surface) #zombi kirajzolása
        self.zombi_move() #zombi mozgása
        self.zombi_attack() #zombi támadása
        self.santa_attack(self.weapon_level) #játékos támadása
        self.add_tree() #jutalom fák hozzáadása
        self.bullets.draw(self.display_surface)
        self.bullets.update()
        
        
        #AZ ÜTKÖZÉS HIBÁS,EZÉRT A CSEMPÉKET SEM RAJZOLJUK KI
        #self.tile_collision() #ütközések a csempékkel
        #self.other_tiles.update()  # díszítőelemek frissítése
        #self.other_tiles.draw(self.display_surface)  # díszítőelemek kirajzolása
