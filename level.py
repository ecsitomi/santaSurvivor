import pygame
from player import Player
from enemy import Enemy
from tiles import Tile, TerrainTile, OtherTile
from settings import tile_size, others, WIDTH, HEIGHT, BG_IMG

# inicializálás
class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface # játékablak a main-ben meghatározottak szerint

        self.player = pygame.sprite.GroupSingle() #csoportok amibe jönnek a sprite-ok
        self.enemies = pygame.sprite.Group()
        self.other_tiles = pygame.sprite.Group()

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
            
    #HIBÁS!!!!!!!!!!!!!!!!!!
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

    #futtatás
    def run(self):
        self.movement()  #mozgás & ütközések
        self.display_surface.blit(self.bg_surf, self.bg_rect)  # háttérkép kirajzolása
        self.enemies.update()  # ellenség update
        self.enemies.draw(self.display_surface)  # ellenség kirajzolása
        self.player.update()  # játékos frissítése
        self.player.draw(self.display_surface)  # játékos kirajzolása a (játékablakban)
        
        #AZ ÜTKÖZÉS HIBÁS,EZÉRT A CSEMPÉKET SEM RAJZOLJUK KI
        #self.tile_collision() #ütközések a csempékkel
        #self.other_tiles.update()  # díszítőelemek frissítése
        #self.other_tiles.draw(self.display_surface)  # díszítőelemek kirajzolása
