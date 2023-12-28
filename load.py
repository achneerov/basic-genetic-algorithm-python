# load.py

from game import run_game, WIDTH, HEIGHT, Dot, WhiteDot, NUMBER_OF_RED_DOTS, distance, WHITE_DOT_RADIUS, RED_DOT_RADIUS
import pickle
import random
import time
import pygame

# Initialize Pygame
pygame.init()

# Create a Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Optionally set a caption for the window
pygame.display.set_caption("Load Model and Play Game")

def play_game_with_model(some_model):
    white_dot = WhiteDot(WIDTH // 2, HEIGHT // 2)
    red_dots = [Dot(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUMBER_OF_RED_DOTS)]

    print(f"Model Directions: {some_model}")

    index = 0
    while index < len(some_model):
        direction = some_model[index]

        print(f"Current Direction from Model: {direction}")
        print(f"White Dot Position: ({white_dot.x}, {white_dot.y})")

        # Move the white dot based on the model's direction
        if direction == "w":
            white_dot.move_towards(white_dot.x, white_dot.y - 10)
        elif direction == "s":
            white_dot.move_towards(white_dot.x, white_dot.y + 10)
        elif direction == "a":
            white_dot.move_towards(white_dot.x - 10, white_dot.y)
        elif direction == "d":
            white_dot.move_towards(white_dot.x + 10, white_dot.y)

        # Check for collisions and remove red dots
        for red_dot in red_dots[:]:
            if distance(white_dot.x, white_dot.y, red_dot.x, red_dot.y) < WHITE_DOT_RADIUS + RED_DOT_RADIUS:
                red_dots.remove(red_dot)

        # Redraw the screen
        screen.fill((0, 0, 0))  # Clear the screen
        white_dot.draw()  # Redraw the white dot
        for red_dot in red_dots:
            red_dot.draw()  # Redraw the remaining red dots

        pygame.display.flip()  # Update the display

        # Move to the next direction in the model
        index += 1

        # Add a delay for better visualization (optional)
        pygame.time.delay(200)  # Delay in milliseconds

    print(f"Final White Dot Position: ({white_dot.x}, {white_dot.y})")

    return len(red_dots)



def main():
    # Load the models
    with open("best_model_from_last_generation.pkl", "rb") as f:
        model = pickle.load(f)
        remaining_red_dots = play_game_with_model(model)
        print(f"Remaining Red Dots: {remaining_red_dots}")

    # Start the game loop
    run_game()

if __name__ == "__main__":
    main()
