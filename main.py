# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import Player


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0  # Delta time initialization

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # this spawns the player triangle


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))
        pygame.display.flip()

        player.draw(screen)  # Vykreslení hráče



        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Limit to 60 FPS and calculate delta time






    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")











if __name__ == "__main__":
    main()
