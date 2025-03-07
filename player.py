import pygame
import random
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN, PLAYER_SPEED, PLAYER_TURN_SPEED
from shot import Shot  # Import Shot
from constants import PLAYER_SHOOT_SPEED  # Import Shot speed
import pygame.gfxdraw  # Required for anti-aliased rendering (soft glow effect)
import math  # Required for trigonometric functions
from constants import SCREEN_WIDTH, SCREEN_HEIGHT




class Player(CircleShape):
    def __init__(self, x, y):
        # Initialize player with position, rotation, and shoot cooldown
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.destroyed = False  # Track if player has exploded


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

        if self.destroyed:
            return  # Stop updating if player has exploded

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


    import random

    def draw(self, screen):
    # Draw the player with a Star Destroyer gray fill, yellow outline, and a blurred rocket glow effect
        points = self.triangle()

        # More realistic metallic shading for the ship
        ship_color = (192, 192, 192)  # Lighter metallic silver-gray
        shading_color = (128, 128, 128)  # Darker metallic shading

        # Create a gradient effect by splitting the triangle into two tones
        midpoint = ((points[0][0] + points[1][0]) / 2, (points[0][1] + points[1][1]) / 2)

        pygame.draw.polygon(screen, shading_color, [points[1], midpoint, points[2]])  # Shaded lower part
        pygame.draw.polygon(screen, ship_color, [points[0], midpoint, points[1]])  # Lighter upper part

        # Yellow outline remains for visibility
        pygame.draw.polygon(screen, (255, 255, 0), points, 2)

        # Calculate engine glow position and direction
        base_left = points[1]  # Left base corner
        base_right = points[2]  # Right base corner
        engine_tip = (base_left + base_right) / 2  # Middle of the base

        # Calculate glow direction (same as player's forward direction)
        forward = pygame.Vector2(0, -1).rotate(self.rotation)  # Player's forward direction

        # Determine if accelerating
        keys = pygame.key.get_pressed()
        is_accelerating = keys[pygame.K_w]  # True if moving forward

        # Adjust flame flicker based on acceleration
        base_flicker = 0.8 if not is_accelerating else 0.6  # Less variation when idle, more when accelerating
        max_flicker = 1.2 if not is_accelerating else 1.5  # Increased flickering range when accelerating
        flicker_variation = random.uniform(base_flicker, max_flicker)

        # Increase the flame length (double the previous size)
        glow_length = self.radius * flicker_variation  # Engine glow extends further
        glow_tip = engine_tip + forward * glow_length  # Extend the glow from base

        # Adjust glow color intensity when accelerating
        glow_intensity = random.randint(100, 160) if not is_accelerating else random.randint(180, 255)

        # Draw multiple layers for a blurred effect
        for i in range(3, 0, -1):  # Draw layers of glow for a soft blur effect
            alpha = int(80 * (i / 3))  # Reduce intensity for outer layers
            glow_color = (255, glow_intensity, 0, alpha)  # Orange glow with fading transparency

            # Expand the glow slightly for each layer
            glow_size = glow_length * (1 + i * 0.1)
            glow_tip_layered = engine_tip + forward * glow_size

            # Use anti-aliased polygon rendering for a smoother effect
            pygame.gfxdraw.filled_polygon(screen, [base_left, base_right, glow_tip_layered], glow_color)
            pygame.gfxdraw.aapolygon(screen, [base_left, base_right, glow_tip_layered], glow_color[:3])  # Anti-aliasing

    def explode(self, screen, updatable, drawable):
    # Play an explosion animation while the game continues running
        self.destroyed = True  # Mark player as destroyed
        self.velocity = pygame.Vector2(0, 0)  # Stop movement after explosion
        explosion_pieces = []  
        num_fragments = random.randint(36, 54)  


        for _ in range(num_fragments):
            angle = random.uniform(0, 360)  
            speed = random.uniform(0.5, 1.5)  # Prevent fragments from moving too fast
            velocity = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * speed
            radius = max(2, min(self.radius // 6, 8))  # Ensure valid size (between 2 and 8 pixels)
            explosion_pieces.append({"pos": self.position.copy(), "vel": velocity, "radius": radius, "life": 180})  

        explosion_timer = 0  # Track explosion time

        while explosion_timer < 180:  # ~3 seconds animation
            # Continue updating the game world while explosion plays
            updatable.update(1 / 60)  
            screen.fill((0, 0, 0))  # Keep background clear for smooth animation

            for obj in drawable:
                obj.draw(screen)

            # Animate explosion
            for fragment in explosion_pieces:
                fragment["pos"] += fragment["vel"]  # Move fragment outward
                fragment["pos"].x = max(-50, min(SCREEN_WIDTH + 50, fragment["pos"].x))  # Keep within safe bounds
                fragment["pos"].y = max(-50, min(SCREEN_HEIGHT + 50, fragment["pos"].y))  # Keep within safe bounds

                fragment["life"] -= 1  # Reduce lifespan
                fade_alpha = max(int(255 * (fragment["life"] / 180)), 0)  # Gradual fade effect

                explosion_color = (255, random.randint(100, 160), 0, fade_alpha)  # Flickering orange

                # Ensure valid drawing values
                if 2 <= fragment["radius"] <= 10:  
                    pygame.gfxdraw.filled_circle(screen, int(fragment["pos"].x), int(fragment["pos"].y), fragment["radius"], explosion_color)
                    pygame.gfxdraw.aacircle(screen, int(fragment["pos"].x), int(fragment["pos"].y), fragment["radius"], explosion_color[:3])

            pygame.display.flip()
            pygame.time.delay(15)  # Smooth animation delay
            explosion_timer += 1  # Track animation time

        pygame.time.delay(3000)  # 3-second wait before closing


