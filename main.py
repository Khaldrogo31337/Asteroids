from this import d

import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_LIVES,
    BOMB_BLAST_RADIUS,
    BACKGROUND_STAR_COUNT,
    LINE_WIDTH,
)
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from bomb import Bomb
from powerup import PowerUp
from powerupfield import PowerUpField
from explosion import Explosion
from background import create_starfield


def draw_game_over_overlay(
    screen: pygame.Surface,
    font: pygame.font.Font,
    big_font: pygame.font.Font,
    score: int,
    button_rect: pygame.Rect,
) -> None:
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    title_surface = big_font.render("GAME OVER", True, "white")
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    screen.blit(title_surface, title_rect)

    score_surface = font.render(f"Final Score: {score}", True, "white")
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
    screen.blit(score_surface, score_rect)

    pygame.draw.rect(screen, "gray20", button_rect)
    pygame.draw.rect(screen, "white", button_rect, LINE_WIDTH)
    ok_surface = font.render("OK", True, "white")
    ok_rect = ok_surface.get_rect(center=button_rect.center)
    screen.blit(ok_surface, ok_rect)


def main():
    print("Hello from asteroids!")
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0.0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Khaldrogo's Asteroids Game")
    font = pygame.font.SysFont(None, 32)
    big_font = pygame.font.SysFont(None, 64)
    background = create_starfield(SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_STAR_COUNT)
    ok_button_rect = pygame.Rect(0, 0, 120, 44)
    ok_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}, \nScreen height: {SCREEN_HEIGHT}")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Bomb.containers = (bombs, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    PowerUpField.containers = (updatable,)
    Explosion.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    powerup_field = PowerUpField()

    score = 0
    lives = PLAYER_LIVES
    game_over = False

    running = True
    while running:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button_rect.collidepoint(event.pos):
                    return

        if not game_over:
            updatable.update(dt)

            for asteroid in list(asteroids):
                if not player.is_invulnerable() and player.collides_with(asteroid):
                    lives -= 1
                    log_event("player_hit", lives_left=lives)
                    if lives <= 0:
                        print("Game over!")
                        log_event("game_over", score=score)
                        game_over = True
                    else:
                        player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

                for shot in list(shots):
                    if asteroid.collides_with(shot):
                        score += asteroid.value()
                        log_event("asteroid_shot", score=score)
                        Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                        shot.kill()
                        asteroid.split()
                        break

            for bomb in list(bombs):
                if bomb.has_detonated():
                    log_event("bomb_exploded")
                    for asteroid in list(asteroids):
                        if bomb.position.distance_to(asteroid.position) <= BOMB_BLAST_RADIUS:
                            score += asteroid.value()
                            Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                            asteroid.split()
                    bomb.kill()

            for powerup in list(powerups):
                if player.collides_with(powerup):
                    log_event("powerup_collected", kind=powerup.kind)
                    if powerup.kind == "shield":
                        player.activate_shield()
                    elif powerup.kind == "speed":
                        player.activate_speed_boost()
                    powerup.kill()

        screen.blit(background, (0, 0))
        for obj in drawable:
            obj.draw(screen)

        score_surface = font.render(f"Score: {score}", True, "white")
        lives_surface = font.render(f"Lives: {lives}", True, "white")
        screen.blit(score_surface, (10, 10))
        screen.blit(lives_surface, (10, 40))

        if game_over:
            draw_game_over_overlay(screen, font, big_font, score, ok_button_rect)

        pygame.display.flip()
        dt = clock.tick(60) / 1000.0
        #print(f"dt: {dt}")
    



if __name__ == "__main__":
    main()
