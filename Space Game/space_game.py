import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 500
screen_height = 800

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Game")

# Longboan-Stelios, LabActivity1, I added this line to change the icon of the game
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Load background image
# Make sure you have a background image. Change the background image to your liking. Use creative commons images or DYI.
# Longboan-Stelios, LabActivity1, I added this to change the background
background_img = pygame.image.load("space.jpg")

# Load tank image
# Make sure you have a tank image. Change the tank image to you liking.
# Draw your own tank or get images from the internet but use creative commons/unlicensed images.
# Longboan-Stelios, LabActivity1, I added this to change the player model
player_img = pygame.image.load("player.png")

# Tank properties
# Longboan-Stelios, LabActivity1, modified tank properties
player_width = 64
player_height = 64
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height

# Bullet properties
# Longboan-Stelios, LabActivity1, modified bullet properties
bullet_width = 5
bullet_height = 30
bullet_color = red
bullet_speed = 15
bullets = []

# Enemy properties
# Longboan-Stelios, LabActivity1, modified enemy properties
enemy_width = 64
enemy_height = 64
enemy_color = black
enemy_speed = 3
enemies = []

# Longboan-Stelios, LabActivity1, I added this to randomize the enemies
enemy_types = ['rock.png', 'comet.png']

# Load enemy tank image
enemy_img = pygame.image.load(random.choice(enemy_types))  # Make sure you have an enemy tank image

# Game loop
game_over = False  # Initialize game over state
running = True  # The game will continue to run unless running = False
score = 0  # Initialize the score. Try fixing this.
# Longboan-Stelios, LabActivity1, scoring fixed

# Game Over Font
font = pygame.font.SysFont("Arial", 64)


def game_over_screen():
    global game_over
    game_over_text = font.render("Game Over! Press R to Restart", True, red)
    screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2,
                                 (screen_height - game_over_text.get_height()) // 2))


while running:
    font = pygame.font.Font(None, 36)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x + player_width // 2, player_y])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 5
    if keys[pygame.K_RIGHT]:
        player_x += 5
    # Longboan-Stelios, LabActivity1, I added this to make a boundary so that the model won't go pass window of the game
    if player_x <= 0:
        player_x = 0
    elif player_x >= 436:
        player_x = 436

    if not game_over:  # Only update game if not in game over state
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 5
        if keys[pygame.K_RIGHT]:
            player_x += 5

    # Move bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed

    # Spawn additional enemies if there are less than the maximum
    min_enemies = 3  # Adjust the minimum number of enemies you want
    max_enemies = 5  # Adjust the maximum number of enemies you want

    # Determine how many new enemies to add
    enemies_to_add = min(max_enemies - len(enemies), 1)  # Add 1 enemy at a time

    # Add the specified number of new enemies
    for _ in range(enemies_to_add):
        new_enemy_x = random.randint(0, screen_width - enemy_width)
        new_enemy_y = random.randint(0, 0)

        # Longboan-Stelios, LabActivity1, this is to fix the overlapping of the spawned enemies
        # Check for overlap with existing enemies
        overlap = any(
            enemy_rect.colliderect(pygame.Rect(new_enemy_x, new_enemy_y, enemy_width, enemy_height))
            for enemy_rect in (pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height) for enemy in enemies)
        )

        if not overlap:
            enemies.append([new_enemy_x, new_enemy_y])

    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))

    # Move enemies
    for enemy in enemies:
        enemy[1] += enemy_speed

    # Collision detection
    bullets_to_remove = []
    enemies_to_remove = []

    # Longboan-Stelios, LabActivity1, revised collision detection
    for bullet in bullets:
        enemies_hit = []  # List to keep track of enemies hit by the current bullet

        for enemy in enemies:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)

            if bullet_rect.colliderect(enemy_rect):
                enemies_hit.append(enemy)  # Add the enemy to the list of enemies hit by the current bullet
                score += 1  # Increase the score when an enemy is hit

                # Remove bullets that hit enemies
                bullets_to_remove.append(bullet)

        # Remove enemies hit by the current bullet
        for enemy in enemies_hit:
            enemies_to_remove.append(enemy)

    # Remove bullets that hit enemies
    for bullet in bullets_to_remove:
        bullets.remove(bullet)

    # Remove enemies that were hit by bullets
    for enemy in enemies_to_remove:
        enemies.remove(enemy)

    # Clear the screen
    screen.fill(white)
    screen.blit(background_img, (0, 0))
    # Collision detection between tank and enemies
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)

        if player_rect.colliderect(enemy_rect):
            game_over = True  # Game over if collision detected

        if game_over:  # Game over state
            # Display game over message and restart prompt
            game_over_screen()

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, (bullet[0], bullet[1], bullet_width, bullet_height))

    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))

    # Draw the tank
    screen.blit(player_img, (player_x, player_y))

    # Draw the score
    # Longboan-Stelios, LabActivity1, this is to fix the display of the scoring
    score_text = font.render(f"Score: {score}", True, (0, 128, 0))
    screen.blit(score_text, (10, 10))  # Display the score at (10, 10)

    # Update the display
    pygame.display.flip()

    # Draw the background
    screen.blit(background_img, (0, 0))  # Blit the background at (0, 0)

    # Control the frame rate
    pygame.time.delay(30)

    # Check for restart input
    # Longboan-Stelios, LabActivity1, fixed the restarting of the game when pressing "r" even though it's not yet game
    # over. Also fixed to reset the score too.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and game_over:
        # Reset game variables
        game_over = False
        score = 0
        player_x = (screen_width - player_width) // 2
        player_y = screen_height - player_height
        bullets.clear()
        enemies.clear()

# Quit Pygame
pygame.quit()
sys.exit()
