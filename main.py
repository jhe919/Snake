import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 128, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Snake variables
snake = [(5, 5)]
snake_direction = (1, 0)
snake_growth = 0
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Game over flag
game_over = True

# Score
score = 0
high_score = 0

# Initialize font
font = pygame.font.Font(None, 36)

# Function to start the game
def start_game():
    global snake, snake_direction, snake_growth, food, game_over, score, high_score
    snake = [(5, 5)]
    snake_direction = (1, 0)
    snake_growth = 0
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    game_over = False
    score = 0

# Load high score from a file if it exists
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save the high score before quitting
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)
            else:
                if event.key == pygame.K_SPACE:
                    start_game()

    if not game_over:
        # Update snake position
        x, y = snake[0]
        new_head = (x + snake_direction[0], y + snake_direction[1])

        # Check for collision with food
        if new_head == food:
            snake_growth += 1
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            score += 1

        # Check for collision with walls or self
        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
            or new_head in snake
        ):
            game_over = True

        # Move snake
        snake.insert(0, new_head)

        # Remove tail if not growing
        if snake_growth == 0:
            snake.pop()
        else:
            snake_growth -= 1

        # Update high score if necessary
        if score > high_score:
            high_score = score

        # Clear screen
        screen.fill(LIGHT_BLUE)

        # Draw food
        pygame.draw.rect(
            screen,
            RED,
            pygame.Rect(
                food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE
            ),
        )

        # Draw snake
        for segment in snake:
            pygame.draw.rect(
                screen,
                DARK_GREEN,
                pygame.Rect(
                    segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE
                ),
            )

        # Draw score and high score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (10, 40))

    else:
        # Display "Game Over" message and instructions centered on the screen
        game_over_text = font.render("Game Over - SPACE to Play Again", True, WHITE)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

    # Update display
    pygame.display.flip()

    # Control game speed
    clock.tick(FPS)
