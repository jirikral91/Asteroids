import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_SPLIT_SPEED_MULTIPLIER, ASTEROID_SPLIT_ANGLE_MIN, ASTEROID_SPLIT_ANGLE_MAX

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt  # Pohyb v přímé linii


    def split(self):
        self.kill()  # Aktuální asteroid zmizí

        if self.radius <= ASTEROID_MIN_RADIUS:
            return  # Malé asteroidy se dále nedělí

        new_radius = self.radius - ASTEROID_MIN_RADIUS  # Nové asteroidy budou menší

        # Vytvoření nových vektorů rychlosti s náhodným úhlem
        random_angle = random.uniform(ASTEROID_SPLIT_ANGLE_MIN, ASTEROID_SPLIT_ANGLE_MAX)
        velocity_1 = self.velocity.rotate(random_angle) * ASTEROID_SPLIT_SPEED_MULTIPLIER
        velocity_2 = self.velocity.rotate(-random_angle) * ASTEROID_SPLIT_SPEED_MULTIPLIER



        # Import Asteroid tady, aby se zabránilo cirkulárnímu importu
        from asteroid import Asteroid


        # Vytvoření dvou nových asteroidů na stejné pozici jako původní
        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Nastavení rychlosti novým asteroidům
        asteroid_1.velocity = velocity_1
        asteroid_2.velocity = velocity_2
