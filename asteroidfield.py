import pygame
import random
from asteroid import Asteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    # Manages spawning and movement of asteroids in the game
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        # Initialize the asteroid field and spawn timer
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        # Create a new asteroid at the given position with a set velocity
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        # Update asteroid field, spawning new asteroids over time
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE: # Check if it's time to spawn
            self.spawn_timer = 0

            # Choose a random edge for spawning a new asteroid
            edge = random.choice(self.edges)

            # Determine speed and velocity for the new asteroid
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))

            # Determine random spawn position along the chosen edge
            position = edge[1](random.uniform(0, 1))

            # Determine asteroid size (Large, Medium, Small)
            kind = random.randint(1, ASTEROID_KINDS)

            # Spawn the new asteroid
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
