import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, BOMB_RADIUS, BOMB_FUSE_SECONDS


class Bomb(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, BOMB_RADIUS)
        self.fuse_timer = BOMB_FUSE_SECONDS

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "orange", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.fuse_timer -= dt
        self.wrap_position()

    def has_detonated(self) -> bool:
        return self.fuse_timer <= 0
