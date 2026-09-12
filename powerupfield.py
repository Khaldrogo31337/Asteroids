import random

import pygame
from powerup import PowerUp
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, POWERUP_SPAWN_RATE_SECONDS, POWERUP_RADIUS

KINDS = ("shield", "speed")


class PowerUpField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        if self.spawn_timer > POWERUP_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            x = random.uniform(POWERUP_RADIUS, SCREEN_WIDTH - POWERUP_RADIUS)
            y = random.uniform(POWERUP_RADIUS, SCREEN_HEIGHT - POWERUP_RADIUS)
            kind = random.choice(KINDS)
            PowerUp(x, y, kind)
