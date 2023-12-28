#load.py

from game import Dot, WhiteDot, WIDTH, HEIGHT, WHITE_DOT_RADIUS, RED_DOT_RADIUS, NUMBER_OF_RED_DOTS, distance
import pickle
import random

def play_game_with_model(model):
    # Initialize white dot
    white_dot = WhiteDot(WIDTH // 2, HEIGHT // 2)
    red_dots = [Dot(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUMBER_OF_RED_DOTS)]

    for direction in model:
        if direction == "UP":
            white_dot.move_towards(white_dot.x, white_dot.y - 10)
        elif direction == "DOWN":
            white_dot.move_towards(white_dot.x, white_dot.y + 10)
        elif direction == "LEFT":
            white_dot.move_towards(white_dot.x - 10, white_dot.y)
        elif direction == "RIGHT":
            white_dot.move_towards(white_dot.x + 10, white_dot.y)

        # Check for collision and eat red dots
        for red_dot in red_dots[:]:
            if distance(white_dot.x, white_dot.y, red_dot.x, red_dot.y) < WHITE_DOT_RADIUS + RED_DOT_RADIUS:
                red_dots.remove(red_dot)

    return len(red_dots)

# Load the models
with open("generation_9_model.pkl", "rb") as f:
    model = pickle.load(f)
    remaining_red_dots = play_game_with_model(model)
    print(f"Remaining Red Dots: {remaining_red_dots}")
