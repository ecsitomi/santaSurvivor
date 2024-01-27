import pygame
from pygame.sprite import _Group
from support import import_folder #segít a képfájlok rendszerezésében

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations={'idle':[],'run':[],'death':[]}

