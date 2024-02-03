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

    #zenelejátszó
    pygame.mixer.set_num_channels(3)
    sound1 = pygame.mixer.Sound(bg_music)
    sound2 = pygame.mixer.Sound(zombie_sound)
    sound1.set_volume(0.4)
    sound2.set_volume(0.2)
    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)
    channel1.play(sound1, loops=-1)
    channel2.play(sound2, loops=-1)

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
