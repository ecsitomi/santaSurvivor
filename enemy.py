import pygame
from tiles import Tile

class Enemy(Tile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y)
