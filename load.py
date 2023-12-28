# load.py

from game import run_game, WIDTH, HEIGHT, Dot, WhiteDot, NUMBER_OF_RED_DOTS, distance, WHITE_DOT_RADIUS, RED_DOT_RADIUS
import pickle
import random

def play_game_with_model(some_model):
    white_dot = WhiteDot(WIDTH // 2, HEIGHT // 2)
    red_dots = [Dot(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUMBER_OF_RED_DOTS)]

    print(f"Model Directions: {some_model}")

    index = 0
    while index < len(some_model):
        direction = some_model[index]

        if direction == "w":
            white_dot.move_towards(white_dot.x, white_dot.y - 10)
        elif direction == "s":
            white_dot.move_towards(white_dot.x, white_dot.y + 10)
        elif direction == "a":
            white_dot.move_towards(white_dot.x - 10, white_dot.y)
        elif direction == "d":
            white_dot.move_towards(white_dot.x + 10, white_dot.y)

        for red_dot in red_dots[:]:
            if distance(white_dot.x, white_dot.y, red_dot.x, red_dot.y) < WHITE_DOT_RADIUS + RED_DOT_RADIUS:
                red_dots.remove(red_dot)

        index += 1

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
