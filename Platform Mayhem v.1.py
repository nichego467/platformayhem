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
PLAYER_COLOR = (255, 255, 255)  # White
PLATFORM_COLOR = (255, 0, 0)  # Red
GOLD_COLOR = (255, 255, 0)  # Yellow
BG_COLOR = (0, 0, 0)
STAR_COLOR = (255, 255, 255)  # White

# Additional Constants
REQUIRED_GOLD_COINS = 5

# Create the window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Welcome to Platform Mayhem!")

# Player setup
player_x = WIDTH // 2
player_y = HEIGHT - 2 * PLAYER_SIZE
player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
player_color = PLAYER_COLOR

# Platform setup
platforms = []

# Gold coin setup
gold_coins = []
gold_spawn_time = 0
gold_coins_collected = 0
font = pygame.font.Font(None, 36)

# Gold coin spawning interval
gold_spawn_interval = 300  # 5 seconds for level 1

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

# "Next Level" screen
next_level_text = pygame.font.Font(None, 36).render("Press SPACE for the Next Level", True, (255, 255, 255))
next_level_rect = next_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))

# Score
score = 0

# Background stars
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

# Level information
level_1 = True
level_2 = False

# Platform speed increment for level 2
platform_speed_increment = 1

# Start menu
start_menu = True
start_menu_text = pygame.font.Font(None, 72).render("Welcome to Platform Mayhem!", True, (255, 255, 255))
start_menu_rect = start_menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
start_instructions_text = pygame.font.Font(None, 36).render("Press SPACE to Start", True, (255, 255, 255))
start_instructions_rect = start_instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
start_instructions2_text = pygame.font.Font(None, 28).render(
    "Avoid the platforms and collect the required gold coins for the next level!", True, (255, 255, 255))
start_instructions2_rect = start_instructions2_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.3))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start_menu:
                start_menu = False  # Start the game when SPACE is pressed
            elif event.key == pygame.K_SPACE and game_over:
                # Restart the game
                game_over = False
                player_rect.x = WIDTH // 2
                player_rect.y = HEIGHT - 2 * PLAYER_SIZE
                platforms = []
                gold_coins = []
                gold_coins_collected = 0
                score = 0
            elif event.key == pygame.K_SPACE and gold_coins_collected >= REQUIRED_GOLD_COINS and level_1:
                # "Well Done" screen when enough gold coins collected
                game_over = True

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

        # Create a gold coin every X seconds
        if score > gold_spawn_time + gold_spawn_interval:
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

        # Increment the score
        score += 1

        # Move the background stars
        for i in range(len(stars)):
            star_x, star_y = stars[i]
            stars[i] = (star_x, star_y + 1)  # Adjust the speed here for slower/faster movement
            if star_y > HEIGHT:
                stars[i] = (random.randint(0, WIDTH), 0)

    # Clear the screen and draw stars
    window.fill(BG_COLOR)
    for star_x, star_y in stars:
        pygame.draw.circle(window, STAR_COLOR, (star_x, star_y), 1)

    if not start_menu:
        if not game_over:
            # Draw the player
            pygame.draw.rect(window, player_color, player_rect)

            # Draw the platforms
            for platform in platforms:
                pygame.draw.rect(window, PLATFORM_COLOR, platform)

                       # Draw the gold coins
            for gold_coin in gold_coins:
                pygame.draw.ellipse(window, GOLD_COLOR, gold_coin)

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

    if gold_coins_collected >= REQUIRED_GOLD_COINS and level_1:
        # Display the "Well Done" screen
        window.fill(BG_COLOR)
        window.blit(well_done_text, well_done_rect)
        window.blit(next_level_text, next_level_rect)
        level_1 = False  # Transition to level 2
        level_2 = True
        gold_coins_collected = 0  # Reset gold coins collected
        gold_spawn_interval = 420  # 7 seconds for level 2
        platforms = []  # Clear level 1 platforms

    # Update the display
    pygame.display.update()

    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
