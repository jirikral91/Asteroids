import pygame
import random
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN, PLAYER_SPEED, PLAYER_TURN_SPEED
from shot import Shot  # Import Shot
from constants import PLAYER_SHOOT_SPEED  # Import Shot speed

class Player(CircleShape):
    def __init__(self, x, y):
        # Initialize player with position, rotation, and shoot cooldown
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0


    def rotate(self, dt):
        #  Rotate player by adjusting the rotation angle
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def triangle(self):
        # Compute the three points of the player's triangle shape
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]



    def shoot(self):
        if self.shoot_timer > 0:  # If cooldown is active, cannot shoot
            return

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity = forward * PLAYER_SHOOT_SPEED
        Shot(self.position.x, self.position.y, velocity)

        self.shoot_timer = PLAYER_SHOOT_COOLDOWN  # sets cooldown after shooting



    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]: # move right
            self.rotate(-dt)
        if keys[pygame.K_d]: # move left
            self.rotate(dt)
        if keys[pygame.K_w]:  # move forward
            self.move(dt)
        if keys[pygame.K_s]:  # move backward
            self.move(-dt)
        if keys[pygame.K_SPACE]:  # Shoot with spacebar
            self.shoot()

        if self.shoot_timer > 0:  # Decreasing cooldown between shots
            self.shoot_timer -= dt

        self.wrap_around_screen()  # Enable screen wrapping

    
    def move(self, dt):
        # Move player forward based on current rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt


    def draw(self, screen):
    # Draw the player with a Star Destroyer gray fill, yellow outline, and flickering rocket glow """
        points = self.triangle()

        # Draw player shape
        pygame.draw.polygon(screen, (169, 169, 169), points)  # Light gray fill
        pygame.draw.polygon(screen, (255, 255, 0), points, 2)  # Yellow outline

        # Calculate engine glow position and direction
        base_left = points[1]  # Left base corner
        base_right = points[2]  # Right base corner
        engine_tip = (base_left + base_right) / 2  # Middle of the base

        # Calculate glow direction (same as player's forward direction)
        forward = pygame.Vector2(0, -1).rotate(self.rotation)  # Player's forward direction

            # Increase the flame length (double the previous size)
        flicker_variation = random.uniform(0.8, 1.2)  # Adds slight flicker variation
        glow_length = self.radius * flicker_variation  # Engine glow extends further

        glow_tip = engine_tip + forward * glow_length  # Extend the glow from base

        # Draw the flickering engine glow
        glow_color = (255, random.randint(100, 160), 0)  # Orange fire with slight hue variation
        glow_points = [base_left, base_right, glow_tip]
        pygame.draw.polygon(screen, glow_color, glow_points)  # Draw the flickering glow