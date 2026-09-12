import pygame
from constants import LINE_WIDTH, EXPLOSION_DURATION_SECONDS


class Explosion(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(*self.containers)
        self.position = pygame.Vector2(x, y)
        self.max_radius = radius * 1.6
        self.timer = EXPLOSION_DURATION_SECONDS

    def update(self, dt: float) -> None:
        self.timer -= dt
        if self.timer <= 0:
            self.kill()

    def draw(self, screen: pygame.Surface) -> None:
        progress = 1 - max(self.timer, 0) / EXPLOSION_DURATION_SECONDS
        radius = self.max_radius * progress
        if radius > 0:
            pygame.draw.circle(screen, "orange", self.position, radius, LINE_WIDTH)
