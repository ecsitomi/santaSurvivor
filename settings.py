import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 60
WIDTH = 1280 #64x20
HEIGHT = 960 #64x15
BG_COLOR = WHITE
BG_IMG = 'img/bg/bg.jpg'

''' ABLAK MONITORHOZ IGAZÍTÁSA
monitor_info = pygame.display.Info() #lekérdezi mekkora a monitor mérete
WIDTH = monitor_info.current_w #az ablak mérete legyen a monoitor méretéhez igazítva
HEIGHT = monitor_info.current_h
'''

tile_size = 64 #csempék szélessége/magassága pixelben, ha később szükséges lesz

others = { #különböző pályaelemek kódjai
'1': 'Crate',
'2': 'Crystal',
'3': 'IceBox',
'4': 'Igloo',
'5': 'Sign_1',
'6': 'Sign_2',
'7': 'SnowMan',
'8': 'Strone',
'9': 'Tree_1',
'0': 'Tree_2',
}  

level_map = [
    '                    ',
    '                    ',
    '                    ',
    '                    ',
    '                    ',
    '                    ',
    '                    ',
    '                    ',
    '                    ',
    '                    ',
    '                    ',
    '                    ',
    '                    ',
    '                    '
]

