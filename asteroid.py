import random

import pygame
from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    ASTEROID_MIN_RADIUS,
    ASTEROID_KINDS,
    SCORE_ASTEROID_BASE,
    ASTEROID_LUMP_POINTS,
    ASTEROID_LUMP_VARIANCE,
)
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.lump_rotation = random.uniform(0, 360)
        self.lump_offsets = [
            random.uniform(1 - ASTEROID_LUMP_VARIANCE, 1 + ASTEROID_LUMP_VARIANCE)
            for _ in range(ASTEROID_LUMP_POINTS)
        ]

    def draw(self, screen: pygame.Surface) -> None:
        points = []
        for i, offset in enumerate(self.lump_offsets):
            angle = self.lump_rotation + i * (360 / len(self.lump_offsets))
            point = self.position + pygame.Vector2(0, 1).rotate(angle) * self.radius * offset
            points.append(point)
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.wrap_position()

    def value(self) -> int:
        kind = round(self.radius / ASTEROID_MIN_RADIUS)
        return (ASTEROID_KINDS - kind + 1) * SCORE_ASTEROID_BASE

    def split(self) -> None:
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        angle = random.uniform(20, 50)
        velocity_a = self.velocity.rotate(angle)
        velocity_b = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid_a = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_a.velocity = velocity_a * 1.2

        asteroid_b = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_b.velocity = velocity_b * 1.2
