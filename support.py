#létrehozunk egy funkciót, ami segít meghatározni, hogy milyen képek tartoznak az animációban és azokat hozzárendeli
#os.walk segít a képek feltérképezésében, sulipy mutatta be ezt a lehetőséget

import pygame
from settings import tile_size
from os import walk #beépített modulból csak a walk kell

def import_folder(path):
    surface_list=[] #képek listája
    for _, _, img_files in walk(path): # _ _ azok a változók amiket a for kiszámol, de nem fog kelleni
                                        #walk kiszámolja a mappa linkjét, almappáit és a fájlait, most nekünk az első kettő nem kell
        for image in img_files: #a szöveges lista megadja a fájlok neveit
            full_path=path+'/'+image #a képfájlok teljes elérési útvonala
            image_surf=pygame.image.load(full_path).convert_alpha() #létrehozza képként az adott fájlt a játékban

            #kép méretezése
            new_width = tile_size * 1.3
            new_height = int(image_surf.get_height() * (new_width/image_surf.get_width()))
            small_image = pygame.transform.scale(image_surf, (new_width, new_height))

            surface_list.append(small_image) #kép listához adása
            
    return surface_list
