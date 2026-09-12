from this import d

import sys

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_LIVES, BOMB_BLAST_RADIUS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from bomb import Bomb
from powerup import PowerUp
from powerupfield import PowerUpField

def main():
    print("Hello from asteroids!")
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0.0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 32)
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

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    powerup_field = PowerUpField()

    score = 0
    lives = PLAYER_LIVES

    running = True
    while running:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    return
        updatable.update(dt)

        for asteroid in list(asteroids):
            if not player.is_invulnerable() and asteroid.collides_with(player):
                lives -= 1
                log_event("player_hit", lives_left=lives)
                if lives <= 0:
                    print("Game over!")
                    log_event("game_over", score=score)
                    sys.exit()
                player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

            for shot in list(shots):
                if asteroid.collides_with(shot):
                    score += asteroid.value()
                    log_event("asteroid_shot", score=score)
                    shot.kill()
                    asteroid.split()
                    break

        for bomb in list(bombs):
            if bomb.has_detonated():
                log_event("bomb_exploded")
                for asteroid in list(asteroids):
                    if bomb.position.distance_to(asteroid.position) <= BOMB_BLAST_RADIUS:
                        score += asteroid.value()
                        asteroid.split()
                bomb.kill()

        for powerup in list(powerups):
            if powerup.collides_with(player):
                log_event("powerup_collected", kind=powerup.kind)
                if powerup.kind == "shield":
                    player.activate_shield()
                elif powerup.kind == "speed":
                    player.activate_speed_boost()
                powerup.kill()

        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)

        score_surface = font.render(f"Score: {score}", True, "white")
        lives_surface = font.render(f"Lives: {lives}", True, "white")
        screen.blit(score_surface, (10, 10))
        screen.blit(lives_surface, (10, 40))

        pygame.display.flip()
        dt = clock.tick(60) / 1000.0
        #print(f"dt: {dt}")
    



if __name__ == "__main__":
    main()
