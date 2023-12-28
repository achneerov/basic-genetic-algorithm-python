from game import Dot, WhiteDot, WIDTH, HEIGHT, WHITE_DOT_RADIUS, RED_DOT_RADIUS, NUMBER_OF_RED_DOTS, distance
import pickle
import random


def play_game_with_model(model):
    # Initialize white dot
    white_dot = WhiteDot(WIDTH // 2, HEIGHT // 2)
    red_dots = [Dot(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUMBER_OF_RED_DOTS)]

    # Debugging: Print the model to see its content
    print(f"Model Directions: {model}")

    index = 0  # Start from the first direction in the model
    while index < len(model):
        direction = model[index]

        if direction == "w":
            white_dot.move_towards(white_dot.x, white_dot.y - 10)
        elif direction == "s":
            white_dot.move_towards(white_dot.x, white_dot.y + 10)
        elif direction == "a":
            white_dot.move_towards(white_dot.x - 10, white_dot.y)
        elif direction == "d":
            white_dot.move_towards(white_dot.x + 10, white_dot.y)

        # Check for collision and eat red dots
        for red_dot in red_dots[:]:
            if distance(white_dot.x, white_dot.y, red_dot.x, red_dot.y) < WHITE_DOT_RADIUS + RED_DOT_RADIUS:
                red_dots.remove(red_dot)

        index += 1  # Move to the next direction in the model

    return len(red_dots)


# Load the models
with open("best_model_from_last_generation.pkl", "rb") as f:  # Corrected filename here
    model = pickle.load(f)
    remaining_red_dots = play_game_with_model(model)
    print(f"Remaining Red Dots: {remaining_red_dots}")
