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
        self.terrain_tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.other_tiles = pygame.sprite.Group()

        # háttérkép betöltése és méretezése
        self.bg_surf = pygame.image.load(BG_IMG).convert_alpha()
        self.bg_rect = self.bg_surf.get_rect()
        self.bg_surf = self.scale_background()

        self.setup_level(level_data) # pálya betöltése

    def scale_background(self):
        original_width, original_height = self.bg_surf.get_size()  # Az eredeti háttérkép méretének lekérdezése

        # Az új méretek kiszámolása az ablak méretéhez igazítva
        new_height = HEIGHT
        new_width = int(original_width * (HEIGHT / original_height))
        
        return pygame.transform.scale(self.bg_surf, (new_width, new_height)) # Háttérkép méretének beállítása és visszaadása

    def setup_level(self, layout):
        player_sprite = Player()
        self.player.add(player_sprite)
        for row_index, row in enumerate(layout):
            for col_index, tile_type in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if tile_type in others:
                    tile = OtherTile(tile_size, x, y, tile_type)
                    self.other_tiles.add(tile)
                elif tile_type != ' ':
                    tile = TerrainTile(tile_size, x, y, tile_type)
                    self.terrain_tiles.add(tile)

    def movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed #mozgás -> irány*sebesség
        player.rect.y+=player.direction.y*player.speed 

        #mozgás korlátozása
        if player.rect.right > WIDTH: #ha jobb oldalról kilép
            player.rect.right = WIDTH #akkor ne lépjen ki
        if player.rect.left < 0: #ha bal oldalról kilép
            player.rect.left = 0 #akkor ne lépjen ki
        if player.rect.top < 0: #ha felső oldalról kilép
            player.rect.top = 0 #akkor ne lépjen ki
        if player.rect.bottom > HEIGHT: #ha alsó oldalról kilép
            player.rect.bottom = HEIGHT #akkor ne lépjen ki

    # futtatás
    def run(self):
        self.movement_collision()  #mozgás & ütközések
        self.display_surface.blit(self.bg_surf, self.bg_rect)  # háttérkép kirajzolása
        self.terrain_tiles.draw(self.display_surface)  # játékablakban
        self.enemies.update()  # ellenség update
        self.enemies.draw(self.display_surface)  # ellenség kirajzolása
        self.other_tiles.update()  # díszítőelemek frissítése
        self.other_tiles.draw(self.display_surface)  # díszítőelemek kirajzolása
        self.player.update()  # játékos frissítése
        self.player.draw(self.display_surface)  # játékos kirajzolása a (játékablakban)
