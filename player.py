import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN, PLAYER_SPEED, PLAYER_TURN_SPEED
from shot import Shot  # Import střely
from constants import PLAYER_SHOOT_SPEED  # Import rychlosti střely

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0


    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]



    def shoot(self):
        if self.shoot_timer > 0:  # Pokud je cooldown aktivní, nemůže střílet
            return

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity = forward * PLAYER_SHOOT_SPEED
        Shot(self.position.x, self.position.y, velocity)

        self.shoot_timer = PLAYER_SHOOT_COOLDOWN  # Nastavení cooldownu po výstřelu



    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:  # Pohyb vpřed
            self.move(dt)
        if keys[pygame.K_s]:  # Pohyb vzad (negativní dt)
            self.move(-dt)
        if keys[pygame.K_SPACE]:  # Střelba mezerníkem
            self.shoot()

        if self.shoot_timer > 0:  # Snižování cooldownu mezi výstřely
            self.shoot_timer -= dt

    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt


    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

