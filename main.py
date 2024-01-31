if __name__ == "__main__":
    import pygame
    from settings import *
    from level import Level

    #inicializálás
    pygame.init() #játék
    pygame.mixer.init() #hang
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #ablak
    pygame.display.set_caption('Santa Survivor') #cím
    clock = pygame.time.Clock() #időzítő

    level=Level(level_map,screen) #szint példányosítása

    #futtatás
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #játék futtatása
        level.run()

        #képfrissítés
        pygame.display.update()
        clock.tick(FPS)

    #kilépés
    pygame.quit()
