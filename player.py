import pygame
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

    
    def move(self, dt):
        # Move player forward based on current rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt


    def draw(self, screen):
        # Draw the player's triangular shape on the screen
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

