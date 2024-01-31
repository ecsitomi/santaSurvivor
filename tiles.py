import pygame
from settings import others

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__(size,x,y)
        self.image=pygame.Surface((size,size)) #csak réteget hozunk létre, a size az a csempe pixelszáma, most 64*64
        self.rect=self.image.get_rect(topleft=(x,y)) #réteg elhelyezése az objektum koordinátája szerint

class TerrainTile(Tile): #terrain csempe
    def __init__(self, size, x, y, terrain_type): #terrain csempe, származik a nagy csempe osztályból, lesznek típusai (terrain_type)
        super().__init__(size,x,y)
        self.image=pygame.image.load(f'img/tiles/terrain/{terrain_type}.png').convert_alpha()

class OtherTile(Tile): #díszítőelemek
    def __init__(self,size,x,y,type):
        super().__init__(size,x,y)
        self.image=pygame.image.load(f'img/others/{others[type]}.png').convert_alpha()
        offset_y=y+size
        self.rect=self.image.get_rect(bottomleft=(x,offset_y))