import pygame
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_ACCELERATION,
    PLAYER_MAX_SPEED,
    PLAYER_DRAG,
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
        max_speed = PLAYER_MAX_SPEED * (SPEED_BOOST_MULTIPLIER if self.speed_boost_timer > 0 else 1)
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        sign = 1 if dt >= 0 else -1
        self.velocity += direction * PLAYER_ACCELERATION * abs(dt) * sign
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)

    def _apply_drag(self, dt: float) -> None:
        drag = PLAYER_DRAG * dt
        speed = self.velocity.length()
        if speed <= drag:
            self.velocity = pygame.Vector2(0, 0)
        else:
            self.velocity -= self.velocity.normalize() * drag

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

        self._apply_drag(dt)
        self.position += self.velocity * dt
        self.wrap_position()

    def collides_with(self, other: "CircleShape") -> bool:
        triangle = self.triangle()
        if _point_in_triangle(other.position, triangle):
            return True
        for i in range(len(triangle)):
            a = triangle[i]
            b = triangle[(i + 1) % len(triangle)]
            if _point_segment_distance(other.position, a, b) <= other.radius:
                return True
        return False


def _point_in_triangle(p: pygame.Vector2, triangle: list[pygame.Vector2]) -> bool:
    a, b, c = triangle

    def sign(p1: pygame.Vector2, p2: pygame.Vector2, p3: pygame.Vector2) -> float:
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    d1 = sign(p, a, b)
    d2 = sign(p, b, c)
    d3 = sign(p, c, a)
    has_neg = d1 < 0 or d2 < 0 or d3 < 0
    has_pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (has_neg and has_pos)


def _point_segment_distance(p: pygame.Vector2, a: pygame.Vector2, b: pygame.Vector2) -> float:
    ab = b - a
    if ab.length_squared() == 0:
        return p.distance_to(a)
    t = max(0, min(1, (p - a).dot(ab) / ab.length_squared()))
    closest = a + ab * t
    return p.distance_to(closest)
