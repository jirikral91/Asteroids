import pygame
import random

class Explosion(pygame.sprite.Sprite):
    """ Represents an explosion effect when an asteroid is destroyed """

    def __init__(self, x, y, size):
        """ Initialize explosion at the given position and size """
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.size = size  # Explosion size based on asteroid size
        self.lifetime = 0.5  # Explosion lasts for 0.5 seconds
        self.time_elapsed = 0  # Timer for fading effect

    def update(self, dt):
        """ Update explosion effect and fade it out over time """
        self.time_elapsed += dt
        if self.time_elapsed > self.lifetime:
            self.kill()  # Remove explosion after lifetime expires

    def draw(self, screen):
        """ Draw explosion effect as expanding particles """
        alpha = max(255 - (self.time_elapsed / self.lifetime) * 255, 0)  # Fade effect
        for _ in range(5):  # Generate random explosion particles
            offset = pygame.Vector2(random.uniform(-self.size, self.size),
                                    random.uniform(-self.size, self.size))
            pygame.draw.circle(screen, (255, random.randint(100, 200), 0, alpha),
                               (int(self.position.x + offset.x), int(self.position.y + offset.y)), 
                               random.randint(2, 5))  # Small particles
