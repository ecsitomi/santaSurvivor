import pygame
from settings import others

class Tile(pygame.sprite.Sprite): #csempe osztály
    def __init__(self,size,x,y):
        super().__init__()
        self.image=pygame.Surface((size,size))
        self.rect=self.image.get_rect(topleft=(x,y))

class TerrainTile(Tile): #terrain csempe
    def __init__(self, size, x, y, terrain_type): #terrain csempe, származik a nagy csempe osztályból, lesznek típusai (terrain_type)
        super().__init__(size,x,y)
        self.image=pygame.image.load(f'img/tiles/terrain/{terrain_type}.png').convert_alpha()

class OtherTile(Tile): #díszítőelemek
    def __init__(self,size,x,y,type):
        super().__init__(size,x,y)
        self.image=pygame.image.load(f'img/tiles/{others[type]}.png').convert_alpha()
        offset_y=y+size
        self.rect=self.image.get_rect(bottomleft=(x,offset_y))