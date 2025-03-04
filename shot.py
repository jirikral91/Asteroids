import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS

class Shot(CircleShape):
    # Represents a bullet (shot) fired by the player
    def __init__(self, x, y, velocity):
        # Initialize a shot with a position and velocity
        super().__init__(x, y, SHOT_RADIUS) # set position and size of the shot
        self.velocity = velocity # set velocity for movement direction

    def draw(self, screen):
        # Draw the shot as a small white circle
        pygame.draw.circle(screen, "white", self.position, self.radius)

    def update(self, dt):
        # Update the position of the shot based on its velocity
        self.position += self.velocity * dt  # Move the shot in a straight line
        
