# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
from explosion import Explosion
import os  # For file handling



background = pygame.image.load("assets/background.png")  # Load background image
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to fit screen



def main():
    # Main function to initialize the game and run the game loop

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init() # Initialize pygame
    
    # Create the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock() # Create a clock to control frame rate
    dt = 0  # Delta time initialization for smooth movement calculations


    # Groups for managing game objects
    updatable = pygame.sprite.Group() # Objects that need updating each frame
    drawable = pygame.sprite.Group() # Objects that need to be drawn each frame
    asteroids = pygame.sprite.Group() # Group for all asteroids
    shots = pygame.sprite.Group() # Group for all shots fired
    explosions = pygame.sprite.Group()



    # Assign sprite groups to each class
    Player.containers = (updatable, drawable) # Player is updatable and drawable
    Asteroid.containers = (asteroids, updatable, drawable) # Asteroids are in all three groups
    AsteroidField.containers = (updatable,) # Asteroid field is only updatable
    Shot.containers = (shots, updatable, drawable) # Shots are in all three groups


    # Create the asteroid field (spawns asteroids over time)
    asteroid_field = AsteroidField()


    # Spawn the player at the center of the screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # this spawns the player triangle
    player.lives = 3  # Ensure player starts with 3 lives

    

    #EXTRA FEATURES
    score = 0  # Initialize score counter
    high_score = 0
    lives = 3  # Player starts with 3 lives

    # Load high score from file (if exists)
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            try:
                high_score = int(file.read().strip())  # Read and convert high score
            except ValueError:
                high_score = 0  # Default if file is empty


    # GAME LOOP (runs indefinitely until the player quits or loses)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return # Exit the game loop
        
        player.update(dt)  # Update player actions


        updatable.update(dt)  # Update all objects in the updatable group
        explosions.update(dt)  # Update explosions


        # Check for collisions between shots and asteroids
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    # Assign points based on asteroid size
                    if asteroid.radius > ASTEROID_MIN_RADIUS * 2:  
                        score += ASTEROID_SCORE_LARGE  # Large asteroid (50 pts)
                    elif asteroid.radius > ASTEROID_MIN_RADIUS:  
                        score += ASTEROID_SCORE_MEDIUM  # Medium asteroid (75 pts)
                    else:
                        score += ASTEROID_SCORE_SMALL  # Small asteroid (100 pts)

                    explosions.add(Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius))  # Spawn explosion
                    asteroid.split()  # Split or remove asteroid
                    shot.kill()  # Remove the shot


        # Check for collisions between the player and asteroids
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                player.lives -= 1  # Reduce lives directly in Player class
                if player.lives <= 0:
                    print("Game over!")
                    player.explode(screen, updatable, drawable)

                    # Check and update high score
                    if score > high_score:
                        high_score = score
                        with open("highscore.txt", "w") as file:
                            file.write(str(high_score))  # Save new high score

                    # Display final score and high score
                    print(f"Final Score: {score}")
                    print(f"High Score: {high_score}")

                    pygame.display.flip()
                    pygame.time.delay(3000)
                    return

                
                # Respawn the player at the center of the screen
                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player.velocity = pygame.Vector2(0, 0)  # Reset movement
       

        screen.blit(background, (0, 0))  # Draw background

        # Render score on screen
        font = pygame.font.Font(None, 36)  # Default font, size 36
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
        lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
        
        screen.blit(lives_text, (10, 40))  # Lives below score
        screen.blit(score_text, (10, 10))  # Draw text at the top-left corner



        # Draw all drawable objects on the screen
        for obj in drawable:
            obj.draw(screen)
        
        for explosion in explosions:
            explosion.draw(screen)  # Draw all explosion effects
        





        pygame.display.flip() # Update the screen
        dt = clock.tick(60) / 1000  #  Limit to 60 FPS and calculate delta time




if __name__ == "__main__":
    main()
