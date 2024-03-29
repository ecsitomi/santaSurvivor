import pygame

def setup_font(size): #betűtípus beállítása
    font_path='img/font/Sobread.ttf'
    font_size=size
    return pygame.font.Font(font_path,font_size)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (27,85,131)
RED = (255, 0, 0)
GREEN=(0,125,0)
FPS = 60
BG_COLOR = WHITE
BG_IMG = 'img/bg/bg.jpg'
WIDTH = 1280 #64x20
HEIGHT = 960 #64x15
tile_size = 64 #csempék szélessége/magassága pixelben
attack_img='img/elements/attack.png' #lövedék képe
tree_img='img/elements/tree.png' #karácsonyfa képe
hit_img='img/elements/hit.png' #sebzés képe
bomb_img='img/elements/bomb.png' #találat robbanás képe
bg_music='sound/bg_music.mp3' #zene
zombie_sound='sound/zombi.mp3' #zombi hangja
hohoho='sound/hohoho.mp3' #hohoho hangja
jingling='sound/jingle-bells.mp3' #csengő hangja

''' ABLAK MONITORHOZ IGAZÍTÁSA
monitor_info = pygame.display.Info() #lekérdezi mekkora a monitor mérete
WIDTH = monitor_info.current_w #az ablak mérete legyen a monoitor méretéhez igazítva
HEIGHT = monitor_info.current_h
#'''

others = { #különböző pályaelemek kódjai
'1': 'Crate',
'2': 'Crystal',
'3': 'IceBox',
'4': 'Igloo',
'5': 'Sign_1',
'6': 'Sign_2',
'7': 'SnowMan',
'8': 'Stone',
'9': 'Tree_1',
'0': 'Tree_2',
}  

level_map = [ #pályaszerkezet
    '                    ',
    '          8         ',
    '                    ',
    '               5    ',
    '  9                 ',
    '                    ',
    '                    ',
    '      2             ',
    '                    ',
    '                    ',
    '                    ',
    '       6            ',
    '                    ',
    '  7            0    ',
    '                    '
]

