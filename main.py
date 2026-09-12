from this import d

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state

def main():
    print("Hello from asteroids!")
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0.0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}, \nScreen height: {SCREEN_HEIGHT}")

    running = True
    while running:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    return
        screen.fill("black")
        pygame.display.flip()
        dt = clock.tick(60) / 1000.0
        #print(f"dt: {dt}")
    



if __name__ == "__main__":
    main()
