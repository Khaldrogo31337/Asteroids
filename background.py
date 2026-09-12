import random

import pygame


def create_starfield(width: int, height: int, star_count: int) -> pygame.Surface:
    background = pygame.Surface((width, height))
    background.fill("black")
    for _ in range(star_count):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        brightness = random.randint(80, 255)
        size = random.choice((1, 1, 1, 2))
        pygame.draw.circle(background, (brightness, brightness, brightness), (x, y), size)
    return background
