import pygame
import sys
import numpy as np  # Import numpy

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)  # Optimized for sound

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Paddle
paddle_width = 100
paddle_height = 20
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - 40
paddle_speed = 10

# Ball
ball_width = 20
ball_height = 20
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_x_speed = 5
ball_y_speed = -5  # Start moving upwards

# Bricks
brick_width = 75
brick_height = 20
bricks = []
num_rows = 5
num_cols = 10
for row in range(num_rows):
    for col in range(num_cols):
        brick_x = col * (brick_width + 5) + 25
        brick_y = row * (brick_height + 5) + 50
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game Over Flag
game_over = False

# --- Sound Generation ---

def create_square_wave(frequency, duration, volume=0.5):
    """Creates a square wave sound."""
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples, False)
    wave = np.sign(np.sin(2 * np.pi * frequency * t))
    wave = (wave * 32767 * volume).astype(np.int16)  # Scale to 16-bit and apply volume
    return pygame.mixer.Sound(wave)

# Create sound effects
paddle_sound = create_square_wave(440, 0.05, 0.3)  # A4 note, short duration
brick_sound = create_square_wave(660, 0.04, 0.5)  # E5 note, shorter, higher volume
wall_sound = create_square_wave(220, 0.03, 0.2)    # A3, lower, for wall bounce
game_over_sound = create_square_wave(110, 0.5, 0.7)  # A2, long and low for game over


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if game_over:
        screen.fill(black)
        draw_text("Game Over! Press R to Restart", font, white, screen, screen_width//4, screen_height//2)
        draw_text(f"Final Score: {score}", font, white, screen, screen_width // 4, screen_height // 2 + 40)


        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset the game
            game_over = False
            score = 0
            ball_x = screen_width // 2
            ball_y = screen_height // 2
            ball_x_speed = 5
            ball_y_speed = -5
            paddle_x = (screen_width - paddle_width) // 2
            bricks = []  # Recreate the bricks
            for row in range(num_rows):
                for col in range(num_cols):
                    brick_x = col * (brick_width + 5) + 25
                    brick_y = row * (brick_height + 5) + 50
                    bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))
        pygame.display.update()
        continue #Skip rest of the loop


    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed

    # Ball movement
    ball_x += ball_x_speed
    ball_y += ball_y_speed

    # Ball collision with walls
    if ball_x <= 0 or ball_x >= screen_width - ball_width:
        ball_x_speed *= -1
        wall_sound.play() # Play wall sound
    if ball_y <= 0:
        ball_y_speed *= -1
        wall_sound.play()
    if ball_y >= screen_height - ball_height:
        game_over = True
        game_over_sound.play()


    # Ball collision with paddle
    if pygame.Rect(ball_x, ball_y, ball_width, ball_height).colliderect(pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)):
        ball_y_speed *= -1
        paddle_sound.play() # Play paddle sound
        paddle_center = paddle_x + paddle_width / 2
        ball_center = ball_x + ball_width / 2
        difference = ball_center - paddle_center
        ball_x_speed = difference * 0.2
        ball_x_speed = max(-8, min(ball_x_speed, 8))



    # Ball collision with bricks
    for brick in bricks[:]:
        if pygame.Rect(ball_x, ball_y, ball_width, ball_height).colliderect(brick):
            bricks.remove(brick)
            ball_y_speed *= -1
            brick_sound.play() # Play brick sound
            score += 10
            break

    # Clear the screen
    screen.fill(black)

    # Draw the paddle
    pygame.draw.rect(screen, blue, (paddle_x, paddle_y, paddle_width, paddle_height))

    # Draw the ball
    pygame.draw.rect(screen, white, (ball_x, ball_y, ball_width, ball_height))

    # Draw the bricks
    for brick in bricks:
        pygame.draw.rect(screen, red, brick)

    # Draw the score
    draw_text(f"Score: {score}", font, white, screen, 10, 10)

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
