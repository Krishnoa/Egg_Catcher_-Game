import pygame
import random
import time

# Initializing Pygame
pygame.init()

# Screen settings
screen_width = 500
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chicken Egg Catch")

# Colors
WHITE = (135, 0, 0)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

# Load Background Image
try:
    bg_img = pygame.image.load("bg.png")
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
except pygame.error as e:
    print("Error loading background image:", e)
    exit()

# Load Images
try:
    chicken_img = pygame.image.load("chicken.png")
    chicken_img = pygame.transform.scale(chicken_img, (100, 100))
    
    egg_img = pygame.image.load("egg.png")
    egg_img = pygame.transform.scale(egg_img, (30, 40))
    
    basket_img = pygame.image.load("basket.png")
    basket_img = pygame.transform.scale(basket_img, (120, 80))

    secret_img = pygame.image.load("secret.png")  # Image to show at score 12
    secret_img = pygame.transform.scale(secret_img, (200, 200))  # Resize if needed
except pygame.error as e:
    print("Error loading images:", e)
    exit()

# Load & Play Background Music
try:
    pygame.mixer.music.load("music.mp3")  # Change if using .wav
    pygame.mixer.music.set_volume(0.10)  # Adjust volume
    pygame.mixer.music.play(-1)  # Loop forever
except pygame.error as e:
    print("Error loading music:", e)

# Font
font = pygame.font.Font(None, 36)

# Function to show Game Over screen
def game_over_screen(score):
    screen.blit(bg_img, (0, 0))  # Keep background image
    game_over_text = font.render("GAME OVER", True, RED)
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)
    restart_text = font.render("Restart", True, WHITE)
    
    restart_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 - 120, 120, 50)
    
    screen.blit(game_over_text, (screen_width // 2 - 80, screen_height // 2 - 60))
    screen.blit(final_score_text, (screen_width // 2 - 80, screen_height // 2 - 20))
    screen.blit(restart_text, (screen_width // 2 - 50, screen_height // 2 - 120))
    
    pygame.display.flip()
    
    # Wait for restart click
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return  # Restart game

# Function to run the game
def run_game():
    # Initial Positions & Variables
    chicken_x = (screen_width - 100) // 2
    chicken_y = 100
    chicken_speed_x = 4
    chicken_speed_y = 2

    basket_x = (screen_width - 120) // 2
    basket_y = screen_height - 100
    basket_speed = 7

    eggs = []
    egg_speed = 3
    egg_speed_increase_time = time.time()

    score = 0
    missed_eggs = 0  # Track consecutive misses
    paused_at_143 = False  # Ensure we only pause once at score 12

    running = True
    while running:
        screen.blit(bg_img, (0, 0))  # Draw the background image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERMOTION:  # Touch controls
                basket_x = int(event.x * screen_width) - 60  # Convert touch x-coordinate to screen x

        # Check Game Over Condition
        if missed_eggs >= 3:
            game_over_screen(score)
            return  # Restart the game

        # Increase egg drop speed over time
        if time.time() - egg_speed_increase_time > 20:
            egg_speed += 2
            egg_speed_increase_time = time.time()

        # Basket movement (Keyboard)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x + 120 < screen_width:
            basket_x += basket_speed

        # Move Chicken in Zigzag
        chicken_x += chicken_speed_x
        chicken_y += chicken_speed_y
        if chicken_x + 100 >= screen_width or chicken_x <= 0:
            chicken_speed_x *= -1
        if chicken_y >= 150 or chicken_y <= 50:
            chicken_speed_y *= -1

        # Randomly drop eggs
        if random.randint(1, 100) > 98:
            eggs.append([chicken_x + 50 - 15, chicken_y + 100])

        # Move Eggs Down & Check for Catch/Miss
        new_eggs = []
        for egg in eggs:
            egg[1] += egg_speed
            if basket_y < egg[1] + 40 < basket_y + 80 and basket_x < egg[0] + 15 < basket_x + 120:
                score += 1  # Egg caught
                missed_eggs = 0  # Reset missed count
            elif egg[1] >= screen_height:
                missed_eggs += 1  # Egg missed
            else:
                new_eggs.append(egg)  # Keep egg if still falling
        eggs = new_eggs

        # Draw Chicken, Eggs, and Basket
        screen.blit(chicken_img, (chicken_x, chicken_y))
        for egg in eggs:
            screen.blit(egg_img, (egg[0], egg[1]))
        screen.blit(basket_img, (basket_x, basket_y))

        # Display Score & Missed Eggs
        score_text = font.render(f"Score: {score}", True, BLACK)
        missed_text = font.render(f"Missed: {missed_eggs}/3", True, RED)
        screen.blit(score_text, (20, 20))
        screen.blit(missed_text, (screen_width - 150, 20))

        # Secret Image - Pause at Score 12 (Only Once)
        if score == 143 and not paused_at_143:
            screen.blit(secret_img, (screen_width // 2 - 100, screen_height // 2 - 100))  # Show image
            pygame.display.flip()

            # Pause the game until the player clicks anywhere
            paused = True
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:  # Click/tap to continue
                        paused = False

            paused_at_143 = True  # Prevent repeating pause

        pygame.display.flip()
        pygame.time.delay(20)

# Run the game loop
while True:
 run_game()