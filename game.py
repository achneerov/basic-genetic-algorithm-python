#game.py

import pygame
import random
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WHITE_DOT_RADIUS = 10
RED_DOT_RADIUS = 5
SPEED = 20
MOVEMENT_DELAY = 100  # in milliseconds
NUMBER_OF_RED_DOTS = 5
BALLS_EATEN = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eat the Dots!")
font = pygame.font.Font(None, 36)


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Dot:
    def __init__(self, x, y, color=RED):
        self.x = x
        self.y = y
        self.color = color
        self.radius = RED_DOT_RADIUS

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class WhiteDot(Dot):
    def __init__(self, x, y):
        super().__init__(x, y, WHITE)
        self.radius = WHITE_DOT_RADIUS
        self.speed = SPEED
        self.last_movement_time = 0

    def can_move(self):
        return pygame.time.get_ticks() - self.last_movement_time > MOVEMENT_DELAY

    def move_towards(self, x, y):
        if self.can_move():
            angle = math.atan2(y - self.y, x - self.x)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
            self.last_movement_time = pygame.time.get_ticks()


white_dot = WhiteDot(WIDTH // 2, HEIGHT // 2)
red_dots = []

start_time = None
end_time = None
win_displayed = False

running = True

while len(red_dots) < NUMBER_OF_RED_DOTS:
    red_dots.append(Dot(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            white_dot.move_towards(mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # Move up with 'W'
                white_dot.move_towards(white_dot.x, white_dot.y - 10)
            elif event.key == pygame.K_s:  # Move down with 'S'
                white_dot.move_towards(white_dot.x, white_dot.y + 10)
            elif event.key == pygame.K_a:  # Move left with 'A'
                white_dot.move_towards(white_dot.x - 10, white_dot.y)
            elif event.key == pygame.K_d:  # Move right with 'D'
                white_dot.move_towards(white_dot.x + 10, white_dot.y)

    # Check for collision and eat red dots
    for red_dot in red_dots[:]:
        if distance(white_dot.x, white_dot.y, red_dot.x, red_dot.y) < WHITE_DOT_RADIUS + RED_DOT_RADIUS:
            red_dots.remove(red_dot)
            BALLS_EATEN += 1  # Increment the counter when a red dot is eaten

    if start_time is None:
        start_time = pygame.time.get_ticks()

    # Check for collision and eat red dots
    for red_dot in red_dots[:]:
        if distance(white_dot.x, white_dot.y, red_dot.x, red_dot.y) < WHITE_DOT_RADIUS + RED_DOT_RADIUS:
            red_dots.remove(red_dot)

    # Check win condition
    if not red_dots and not win_displayed:
        end_time = pygame.time.get_ticks()
        win_displayed = True
        elapsed_time = (end_time - start_time) / 1000.0  # Convert to seconds

    # Draw and move white dot
    white_dot.draw()
    for red_dot in red_dots:
        red_dot.draw()

    if win_displayed:
        win_text = font.render(f"You Win! Time: {elapsed_time:.2f} seconds", True, WHITE)
        screen.blit(win_text, ((WIDTH - win_text.get_width()) // 2, (HEIGHT - win_text.get_height()) // 2))
        balls_text = font.render(f"Balls Eaten: {BALLS_EATEN}", True, WHITE)
        screen.blit(balls_text, (10, 10))  # Displaying at (10, 10) position

    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()

