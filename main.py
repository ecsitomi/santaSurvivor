if __name__ == "__main__":
    import pygame
    from settings import *
    from level import Level

    #inicializálás
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Santa Survivor') 
    clock = pygame.time.Clock()

    level=Level(level_map,screen)

    #futtatás
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        level.run()

        #képfrissítés
        pygame.display.update()
        clock.tick(FPS)

    #kilépés
    pygame.quit()
