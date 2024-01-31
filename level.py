import pygame
from player import Player
from enemy import Enemy
from tiles import Tile, TerrainTile, OtherTile
from settings import tile_size, others

#inicializálás
class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.player = pygame.sprite.GroupSingle()
        self.terrain_tiles = pygame.sprite.Group()
        self.crates = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.constraints = pygame.sprite.Group()
        self.other_tiles = pygame.sprite.Group()
        self.world_shift = 0
        self.setup_level(level_data)

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, tile_type in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if tile_type == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                elif tile_type == 'T':
                    tile = Crate(tile_size, x, y)
                    self.crates.add(tile)
                elif tile_type == 'E':
                    self.enemies.add(Enemy(tile_size, x, y))
                elif tile_type == 'C':
                    constraint = Tile(tile_size, x, y)
                    self.constraints.add(constraint)
                elif tile_type in others:
                    tile = OtherTile(tile_size, x, y, tile_type)
                    self.other_tiles.add(tile)
                elif tile_type != ' ':
                    tile = TerrainTile(tile_size, x, y, tile_type)
                    self.terrain_tiles.add(tile)

    def horizontal_movement_collision(self):
          player = self.player.sprite
          player.rect.x += player.direction.x * player.speed
  
          for sprite in self.terrain_tiles.sprites():
              if sprite.rect.colliderect(player.rect):
                  if player.direction.x < 0:
                      player.rect.left = sprite.rect.right
                  if player.direction.x > 0:
                      player.rect.right = sprite.rect.left

    #futtatás
    def run(self):
        pass

