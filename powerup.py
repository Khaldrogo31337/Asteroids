import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, POWERUP_RADIUS, POWERUP_LIFETIME_SECONDS

POWERUP_COLORS = {
    "shield": "cyan",
    "speed": "yellow",
}


class PowerUp(CircleShape):
    def __init__(self, x: float, y: float, kind: str) -> None:
        super().__init__(x, y, POWERUP_RADIUS)
        self.kind = kind
        self.lifetime = POWERUP_LIFETIME_SECONDS

    def draw(self, screen: pygame.Surface) -> None:
        color = POWERUP_COLORS[self.kind]
        pygame.draw.circle(screen, color, self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return
        self.wrap_position()
