import pygame
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_RESPAWN_INVULNERABILITY_SECONDS,
    WEAPON_SINGLE,
    WEAPON_SPREAD,
    WEAPON_RAPID,
    WEAPON_SPREAD_ANGLE,
    WEAPON_RAPID_COOLDOWN_SECONDS,
    SHIELD_DURATION_SECONDS,
    SPEED_BOOST_DURATION_SECONDS,
    SPEED_BOOST_MULTIPLIER,
    BOMB_COOLDOWN_SECONDS,
)
from shot import Shot
from bomb import Bomb
from logger import log_event


class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.bomb_timer = 0
        self.weapon = WEAPON_SINGLE
        self.invulnerable_timer = 0
        self.shield_timer = 0
        self.speed_boost_timer = 0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        if self.shield_timer > 0:
            pygame.draw.circle(screen, "cyan", self.position, self.radius + 6, 1)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        speed = PLAYER_SPEED * (SPEED_BOOST_MULTIPLIER if self.speed_boost_timer > 0 else 1)
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * speed * dt
        self.position += rotated_with_speed_vector

    def is_invulnerable(self) -> bool:
        return self.invulnerable_timer > 0 or self.shield_timer > 0

    def activate_shield(self) -> None:
        self.shield_timer = SHIELD_DURATION_SECONDS

    def activate_speed_boost(self) -> None:
        self.speed_boost_timer = SPEED_BOOST_DURATION_SECONDS

    def respawn(self, x: float, y: float) -> None:
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invulnerable_timer = PLAYER_RESPAWN_INVULNERABILITY_SECONDS

    def switch_weapon(self, weapon: str) -> None:
        self.weapon = weapon

    def shoot(self) -> None:
        if self.shoot_timer > 0:
            return

        if self.weapon == WEAPON_RAPID:
            self.shoot_timer = WEAPON_RAPID_COOLDOWN_SECONDS
        else:
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        if self.weapon == WEAPON_SPREAD:
            angles = (-WEAPON_SPREAD_ANGLE, 0, WEAPON_SPREAD_ANGLE)
        else:
            angles = (0,)

        for angle in angles:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = (
                pygame.Vector2(0, 1).rotate(self.rotation + angle) * PLAYER_SHOOT_SPEED
            )

    def drop_bomb(self) -> None:
        if self.bomb_timer > 0:
            return
        self.bomb_timer = BOMB_COOLDOWN_SECONDS
        Bomb(self.position.x, self.position.y)
        log_event("bomb_dropped")

    def update(self, dt: float) -> None:
        self.shoot_timer -= dt
        self.bomb_timer -= dt
        self.invulnerable_timer -= dt
        self.shield_timer -= dt
        self.speed_boost_timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_b]:
            self.drop_bomb()
        if keys[pygame.K_1]:
            self.switch_weapon(WEAPON_SINGLE)
        if keys[pygame.K_2]:
            self.switch_weapon(WEAPON_SPREAD)
        if keys[pygame.K_3]:
            self.switch_weapon(WEAPON_RAPID)

        self.wrap_position()
