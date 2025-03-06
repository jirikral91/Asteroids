import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # Subclasses must override this method to define how the object is drawn
        pass

    def update(self, dt):
        # Subclasses must override this method to update object behavior each frame
        pass

    def collides_with(self, other):
        # Check if this object collides with another CircleShape object
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius
    
    def wrap_around_screen(self):
    # Make objects reappear on the opposite side when going off-screen """
        if self.position.x < -self.radius:  # Left edge
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:  # Right edge
            self.position.x = -self.radius

        if self.position.y < -self.radius:  # Top edge
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:  # Bottom edge
            self.position.y = -self.radius

