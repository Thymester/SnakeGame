import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Snake initial position and size
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_dir = 'RIGHT'
change_to = snake_dir

# Food position
food_pos = [random.randrange(1, (width // 10)) * 10,
            random.randrange(1, (height // 10)) * 10]
food_spawn = True

# Score
score = 0
top_score = 0

# Load top score from a file
try:
    with open("top_score.txt", "r") as file:
        top_score = int(file.read())
except FileNotFoundError:
    pass

# Game Over
game_over = False

# FPS controller
fps = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 40)

# Main logic
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Validation of direction
    if change_to == 'UP' and not snake_dir == 'DOWN':
        snake_dir = 'UP'
    if change_to == 'DOWN' and not snake_dir == 'UP':
        snake_dir = 'DOWN'
    if change_to == 'LEFT' and not snake_dir == 'RIGHT':
        snake_dir = 'LEFT'
    if change_to == 'RIGHT' and not snake_dir == 'LEFT':
        snake_dir = 'RIGHT'

    # Moving the snake
    if snake_dir == 'UP':
        snake_pos[1] -= 10
    if snake_dir == 'DOWN':
        snake_pos[1] += 10
    if snake_dir == 'LEFT':
        snake_pos[0] -= 10
    if snake_dir == 'RIGHT':
        snake_pos[0] += 10

    # Game Over conditions
    if snake_pos[0] < 0 or snake_pos[0] >= width or snake_pos[1] < 0 or snake_pos[1] >= height:
        game_over = True
    
    # Check for self-collision
    for segment in snake_body[1:]:
        if segment == snake_pos:
            game_over = True

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        while True:
            food_pos = [random.randrange(1, (width // 10)) * 10,
                        random.randrange(1, (height // 10)) * 10]
            if food_pos not in snake_body:  # Check if the food is on the snake's body
                break
        food_spawn = True

    # Update top score
    if score > top_score:
        top_score = score

    # Draw snake
    screen.fill(black)
    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw food
    pygame.draw.rect(screen, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Display scores
    score_text = font.render(f'Score: {score}', True, white)
    top_score_text = font.render(f'Top Score: {top_score}', True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(top_score_text, (width - top_score_text.get_width() - 10, 10))

    # Update screen
    pygame.display.update()

    # Refresh rate
    fps.tick(10)  # Adjust the speed here

# Save top score to a file
with open("top_score.txt", "w") as file:
    file.write(str(top_score))

# Quit Pygame
pygame.quit()