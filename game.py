import pygame
import math
import random
import json
import time

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WHITE_DOT_RADIUS = 10
RED_DOT_RADIUS = 5
SPEED = 20
MOVEMENT_DELAY = 0.00000000000001  # in seconds
TIMEOUT_TICKS = 1

POPULATION_SIZE = 4
GENERATIONS = 8
MUTATION_RATE = 0.1
SEQUENCE_LENGTH = 150


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Dot:
    def __init__(self, x, y, color=RED):
        self.x = x
        self.y = y
        self.color = color
        self.radius = RED_DOT_RADIUS

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class WhiteDot(Dot):
    def __init__(self, x, y):
        super().__init__(x, y, WHITE)
        self.radius = WHITE_DOT_RADIUS
        self.speed = SPEED
        self.last_movement_time = 0

    def move_towards(self, x, y):
        # if self.can_move():
        angle = math.atan2(y - self.y, x - self.x)
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)
        self.last_movement_time = pygame.time.get_ticks()


def run_game(input_queue=None):
    red_dot_positions = [
        (200, 300),
        (600, 400),
        (366, 236),
        (434, 464),
        (266, 364),
        (534, 336),
        (166, 400),
        (634, 300),
        (233, 264),
        (567, 436),
        (300, 236),
        (500, 464),
        (233, 464),
        (567, 236),
        (300, 464),
        (500, 236)
    ]
    balls_eaten = 0
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Eat the Dots!")
    font = pygame.font.Font(None, 36)
    white_dot = WhiteDot(WIDTH // 2, HEIGHT // 2)
    red_dots = [Dot(x, y) for x, y in red_dot_positions]
    start_time = None
    win_displayed = False
    running = True

    if input_queue is None:
        input_queue = []

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    input_queue.append(pygame.key.name(event.key).lower())

        if input_queue:
            time.sleep(MOVEMENT_DELAY)
            direction = input_queue.pop(0)
            if direction == 'w':
                white_dot.move_towards(white_dot.x, white_dot.y - 10)
            elif direction == 's':
                white_dot.move_towards(white_dot.x, white_dot.y + 10)
            elif direction == 'a':
                white_dot.move_towards(white_dot.x - 10, white_dot.y)
            elif direction == 'd':
                white_dot.move_towards(white_dot.x + 10, white_dot.y)

        if pygame.time.get_ticks() - white_dot.last_movement_time > TIMEOUT_TICKS:
            running = False

        for red_dot in red_dots[:]:
            if distance(white_dot.x, white_dot.y, red_dot.x, red_dot.y) < WHITE_DOT_RADIUS + RED_DOT_RADIUS:
                red_dots.remove(red_dot)
                balls_eaten += 1

        if start_time is None:
            start_time = pygame.time.get_ticks()

        if not red_dots and not win_displayed:
            end_time = pygame.time.get_ticks()
            win_displayed = True
            elapsed_time = (end_time - start_time) / 1000.0  # Convert to seconds

        white_dot.draw(screen)
        for red_dot in red_dots:
            red_dot.draw(screen)

        if win_displayed:
            win_text = font.render(f"You Win! Time: {elapsed_time:.2f} seconds", True, WHITE)
            screen.blit(win_text, ((WIDTH - win_text.get_width()) // 2, (HEIGHT - win_text.get_height()) // 2))
            balls_text = font.render(f"Balls Eaten: {balls_eaten}", True, WHITE)
            screen.blit(balls_text, (10, 10))  # Displaying at (10, 10) position

        pygame.display.flip()
        pygame.time.delay(10)

    pygame.quit()
    return balls_eaten


def generate_random_sequence(length):
    return [random.choice(['w', 'a', 's', 'd']) for _ in range(length)]


def calculate_fitness(sequence):
    input_queue = sequence.copy()
    return run_game(input_queue)


def mutate(sequence):
    for i in range(len(sequence)):
        if random.random() < MUTATION_RATE:
            sequence[i] = random.choice(['w', 'a', 's', 'd'])
    return sequence


def generate():
    population = [generate_random_sequence(SEQUENCE_LENGTH) for _ in range(POPULATION_SIZE)]
    for generation in range(GENERATIONS):
        fitness_scores = [calculate_fitness(individual) for individual in population]
        population_fitness_pairs = list(zip(population, fitness_scores))
        population_fitness_pairs.sort(key=lambda x: x[0], reverse=True)
        new_population = []
        for i in range(POPULATION_SIZE // 2):
            best_individual = population_fitness_pairs[i][0]
            mutated_clone = mutate(best_individual.copy())
            new_population.append(best_individual)
            new_population.append(mutated_clone)
        population = new_population

    filename_format = f"pop{POPULATION_SIZE}-gen{GENERATIONS}-mut{MUTATION_RATE}-seqlen{SEQUENCE_LENGTH}-fitsc{population_fitness_pairs[0][1]}"

    with open(f'{filename_format}.json', 'w') as f:
        json.dump(population_fitness_pairs[0][0], f)


def unwrap(filename):
    with open(filename, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    #generate()
    run_game(unwrap("pop4-gen8-mut0.1-seqlen150-fitsc2.json"))
    # run_game(["a", "a", "w", "w", "a", "a", "w", "w", "a", "a", "w", "w", "a", "a", "w", "w", "a", "a", "w", "w", "a", "a","w", "w"])
    # run_game()
