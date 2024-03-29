import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 40
PLAYER_SPEED = 5
PLATFORM_SIZE = 100
PLATFORM_SPEED = 3
BG_COLOUR = (0, 0, 0)
STAR_COLOUR = (255, 255, 255)  # White

# Additional Constants
REQUIRED_GOLD_COINS = 5

# Create the window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Welcome to Platform Mayhem!")

# Load your player image
player_image = pygame.image.load("jetpack2.png")  # The Jetpack Character
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

# Player setup
player_x = WIDTH // 2
player_y = HEIGHT - 2 * PLAYER_SIZE
player_rect = player_image.get_rect()
player_rect.topleft = (player_x, player_y)

# Platform setup
platforms = []

# Gold coin setup
gold_coins = []
gold_spawn_time = 0
gold_coins_collected = 0
font = pygame.font.Font(None, 36)

# Clock to control frame rate
clock = pygame.time.Clock()

# Game over flag
game_over = False
game_over_text = pygame.font.Font(None, 72).render("Game Over", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
restart_text = pygame.font.Font(None, 36).render("Press SPACE to Restart", True, (255, 255, 255))
restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))

# "Well Done" screen
well_done_text = pygame.font.Font(None, 72).render("Well Done!", True, (0, 255, 0))
well_done_rect = well_done_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Score
score = 0

# Background stars
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]
elapsed_time = 0  # Define elapsed_time

# Start menu
start_menu = True
start_menu_text = pygame.font.Font(None, 72).render("Welcome to Platform Mayhem!", True, (255, 255, 255))
start_menu_rect = start_menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
start_instructions_text = pygame.font.Font(None, 36).render("Press SPACE to Start", True, (255, 255, 255))
start_instructions_rect = start_instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
start_instructions2_text = pygame.font.Font(None, 28).render("Avoid the platforms and collect the required gold coins for the next level!", True, (255, 255, 255))
start_instructions2_rect = start_instructions2_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.3))

# Music setup
pygame.mixer.init()
pygame.mixer.music.load("backgroundmusic.mp3")  # Background music for the game
pygame.mixer.music.set_volume(0.5)  # Initial volume

music_playing = False  # Flag to check if music is playing
music_volume = 0.5  # Initial volume
music_volume_change = 0.1  # Volume change step

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start_menu:
                start_menu = False  # Start the game when SPACE is pressed
                if not music_playing:
                    pygame.mixer.music.play(-1)  # Start the music
                    music_playing = True
            elif event.key == pygame.K_SPACE and game_over:
                # Restart the game
                game_over = False
                player_rect.x = WIDTH // 2
                player_rect.y = HEIGHT - 2 * PLAYER_SIZE
                platforms = []
                gold_coins = []
                gold_coins_collected = 0
                score = 0
            elif event.key == pygame.K_SPACE and gold_coins_collected >= REQUIRED_GOLD_COINS:
                # "Well Done" screen when enough gold coins collected
                game_over = True
            elif event.key == pygame.K_UP:
                music_volume = min(1.0, music_volume + music_volume_change)  # Increase volume
                pygame.mixer.music.set_volume(music_volume)
            elif event.key == pygame.K_DOWN:
                music_volume = max(0.0, music_volume - music_volume_change)  # Decrease volume
                pygame.mixer.music.set_volume(music_volume)

    if not start_menu and not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            player_rect.x += PLAYER_SPEED
        if keys[pygame.K_w]:
            player_rect.y -= PLAYER_SPEED
        if keys[pygame.K_s]:
            player_rect.y += PLAYER_SPEED

        # Create new platforms at random intervals
        if random.randint(0, 100) < 3:
            platform_x = random.randint(0, WIDTH - PLATFORM_SIZE)
            platform_rect = pygame.Rect(platform_x, 0, PLATFORM_SIZE, 20)
            platforms.append(platform_rect)

        # Create a gold coin every 5 seconds
        if score > gold_spawn_time + 300:  # 60 frames per second * 5 seconds
            gold_x = random.randint(0, WIDTH - 20)
            gold_y = random.randint(20, HEIGHT - 20)
            gold_coin = pygame.Rect(gold_x, gold_y, 20, 20)
            gold_coins.append(gold_coin)
            gold_spawn_time = score

        # Move platforms downward
        for platform in platforms:
            platform.y += PLATFORM_SPEED

        # Move gold coins downward
        for gold_coin in gold_coins:
            gold_coin.y += PLATFORM_SPEED

        # Remove platforms that go off the screen
        platforms = [p for p in platforms if p.y < HEIGHT]

        # Check for collisions with platforms
        for platform in platforms:
            if player_rect.colliderect(platform):
                game_over = True  # Game over if there's a collision

        # Check for collecting gold coins
        for gold_coin in gold_coins:
            if player_rect.colliderect(gold_coin):
                gold_coins.remove(gold_coin)
                gold_coins_collected += 1
                pygame.mixer.Sound("pickupCoin.wav").play()  # Play a sound when collecting a coin

        # Increment the score
        score += 1

        # Add new stars to the top when they go off the screen
        elapsed_time += clock.get_rawtime()
        if elapsed_time > 500:  # Add a new star every 500 milliseconds
            stars.append((random.randint(0, WIDTH), 0))
            elapsed_time = 0

        # Remove stars that go off the screen
        stars = [star for star in stars if star[1] < HEIGHT]

    # Clear the screen and draw stars
    window.fill(BG_COLOUR)
    for star_x, star_y in stars:
        pygame.draw.circle(window, STAR_COLOUR, (star_x, star_y), 1)

    if not start_menu:
        if not game_over:
            # Draw the player
            window.blit(player_image, player_rect)

            # Draw the platforms
            for platform in platforms:
                pygame.draw.rect(window, (255, 0, 0), platform)

            # Draw the gold coins
            for gold_coin in gold_coins:
                pygame.draw.ellipse(window, (255, 255, 0), gold_coin)

            # Display the score
            score_text = font.render(f"Score: {score // 60}", True, (255, 255, 255))
            window.blit(score_text, (10, 10))

            # Display the gold coins collected
            coins_collected_text = font.render(f"Gold Coins: {gold_coins_collected}", True, (255, 255, 255))
            window.blit(coins_collected_text, (10, 40))
        else:
            # Display the game over screen
            window.blit(game_over_text, game_over_rect)
            window.blit(restart_text, restart_rect)
    else:
        # Display the start menu
        window.blit(start_menu_text, start_menu_rect)
        window.blit(start_instructions_text, start_instructions_rect)
        window.blit(start_instructions2_text, start_instructions2_rect)

    if gold_coins_collected >= REQUIRED_GOLD_COINS:
        # Display the "Well Done" screen
        window.fill(BG_COLOUR)
        window.blit(well_done_text, well_done_rect)

    # Update the display
    pygame.display.update()

    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
