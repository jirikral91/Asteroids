import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS
import pygame.gfxdraw  # For smoother laser glow effect
from constants import SCREEN_WIDTH, SCREEN_HEIGHT



class Shot(CircleShape):
    # Represents a bullet (shot) fired by the player
    def __init__(self, x, y, velocity):
        # Initialize a shot with a position and velocity
        super().__init__(x, y, SHOT_RADIUS) # set position and size of the shot
        self.velocity = velocity # set velocity for movement direction

    
    def draw(self, screen):
    # Draw a glowing red laser shot with a soft glow effect
        core_color = (255, 50, 50)  # Bright red core
        glow_color = (255, 0, 0, 100)  # Transparent outer glow

        # Ensure shot is within screen bounds before drawing
        if not (0 <= self.position.x <= SCREEN_WIDTH and 0 <= self.position.y <= SCREEN_HEIGHT):
            return  # Skip drawing if out of bounds

        # Reduce shot size slightly
        small_radius = max(int(self.radius * 0.6), 2)  # Ensure minimum size of 2 pixels

        # Draw soft glow layers for a laser effect
        for i in range(2, 0, -1):  # Outer glow effect
            glow_radius = max(2, min(small_radius + i, 10))  # Ensure safe radius size
            pygame.gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), glow_radius, glow_color)
            pygame.gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), glow_radius, glow_color[:3])  # Anti-aliasing

        # Draw the bright core of the laser shot
        pygame.gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), small_radius, core_color)
        pygame.gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), small_radius, core_color)  # Anti-aliasing




    def update(self, dt):
        # Update the position of the shot based on its velocity
        self.position += self.velocity * dt  # Move the shot in a straight line
        
