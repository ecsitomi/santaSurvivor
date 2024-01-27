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

    #háttérkép
    bg_surf = pygame.image.load(BG_IMG).convert_alpha()
    bg_rect = bg_surf.get_rect(bottomleft=(0,HEIGHT))

    level=Level(screen)

    #futtatás
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                               
                running = False

        #háttérszín/kép megjelenítés
        screen.fill(BG_COLOR)
        screen.blit(bg_surf,bg_rect)

        #játék futtatása
        level.run()

        #képfrissítés
        pygame.display.update()
        clock.tick(FPS)

    #kilépés
    pygame.quit()
