import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_SPLIT_SPEED_MULTIPLIER, ASTEROID_SPLIT_ANGLE_MIN, ASTEROID_SPLIT_ANGLE_MAX

class Asteroid(CircleShape):
    # Represents an asteroid in the game, which can move and split into smaller
    # asteroids when destroyed
    def __init__(self, x, y, radius):
        # Initialize an asteroid with a position and size
        super().__init__(x, y, radius)

    def draw(self, screen):
        # Draw the asteroid as a white circle
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        # Update asteroid position based on its velocity
        self.position += self.velocity * dt  # Move asteroid in a straight line


    def split(self):
        # Split the asteroid into two smaller asteroids upon destruction
        self.kill()  # Remove the current asteroid from the game

        if self.radius <= ASTEROID_MIN_RADIUS:
            return  # Smallest asteroids disappear without splitting

        new_radius = self.radius - ASTEROID_MIN_RADIUS  # Decrease the size of new asteroids

        # Generate a random angle for splitting direction
        random_angle = random.uniform(ASTEROID_SPLIT_ANGLE_MIN, ASTEROID_SPLIT_ANGLE_MAX)
        
        # Calculate new velocity vectors for the two smaller asteroids
        velocity_1 = self.velocity.rotate(random_angle) * ASTEROID_SPLIT_SPEED_MULTIPLIER
        velocity_2 = self.velocity.rotate(-random_angle) * ASTEROID_SPLIT_SPEED_MULTIPLIER


        # Import Asteroid here to avoid circular import issues
        from asteroid import Asteroid


        # Create two new asteroids at the same position as the original one
        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Assign new velocities to the smaller asteroids
        asteroid_1.velocity = velocity_1
        asteroid_2.velocity = velocity_2
#