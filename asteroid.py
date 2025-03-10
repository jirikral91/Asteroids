import pygame
import random
import math  # Required for trigonometric functions
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_SPLIT_SPEED_MULTIPLIER, ASTEROID_SPLIT_ANGLE_MIN, ASTEROID_SPLIT_ANGLE_MAX

class Asteroid(CircleShape):
    # Represents an asteroid in the game, which can move and split into smaller
    # asteroids when destroyed
    def __init__(self, x, y, radius):
        # Initialize an asteroid with a position and size
        super().__init__(x, y, radius)

        # Assign a fixed random rock-like color upon creation
        self.color = random.choice([(100, 100, 100), (120, 110, 100), (90, 85, 80)])  # Shades of gray and brown

        self.points = self.generate_lumpy_shape()  # Store the shape once during initialization

        # Assign a random slow rotation speed
        self.rotation_angle = 0  # Initial rotation
        self.rotation_speed = random.uniform(-1, 1)  # Slow rotation in degrees per frame
    
    def generate_lumpy_shape(self):
    # Generate a lumpy asteroid shape with random variation in the radius (relative points) """
        num_points = random.randint(8, 14)  # Number of points in the asteroid shape
        angle_step = 360 / num_points  # Evenly distribute points around a circle
        points = []

        for i in range(num_points):
            angle = math.radians(i * angle_step)  # Convert angle to radians
            radius_variation = random.uniform(0.7, 1.2)  # Randomize lumpiness
            point_x = math.cos(angle) * self.radius * radius_variation
            point_y = math.sin(angle) * self.radius * radius_variation
            points.append((point_x, point_y))  # Store relative points

        return points  # Store shape relative to the asteroid's center


    def draw(self, screen):
    # Draw the asteroid with a realistic solid rock color and a white outline """
        transformed_points = [
        (
            self.position.x + math.cos(math.radians(self.rotation_angle)) * p[0] - math.sin(math.radians(self.rotation_angle)) * p[1],
            self.position.y + math.sin(math.radians(self.rotation_angle)) * p[0] + math.cos(math.radians(self.rotation_angle)) * p[1]
        )
        for p in self.points
        ]

        pygame.draw.polygon(screen, self.color, transformed_points)  # Solid asteroid color
        pygame.draw.polygon(screen, "white", transformed_points, 2)  # White outline




    def update(self, dt):
        # Update asteroid position based on its velocity
        self.position += self.velocity * dt  # Move asteroid in a straight line
        self.rotation_angle += self.rotation_speed  # Rotate asteroid slowly
        self.wrap_around_screen()  # Enable screen wrapping



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