import pygame
import math
import random
import json

# Initialize pygame


# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WHITE_DOT_RADIUS = 10
RED_DOT_RADIUS = 5
SPEED = 20
MOVEMENT_DELAY = 100  # in milliseconds
NUMBER_OF_RED_DOTS = 2
BALLS_EATEN = 0


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

    def can_move(self):
        return pygame.time.get_ticks() - self.last_movement_time > MOVEMENT_DELAY

    def move_towards(self, x, y):
        if self.can_move():
            angle = math.atan2(y - self.y, x - self.x)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
            self.last_movement_time = pygame.time.get_ticks()


def run_game(input_queue=None):
    global BALLS_EATEN

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Eat the Dots!")
    font = pygame.font.Font(None, 36)

    white_dot = WhiteDot(WIDTH // 2, HEIGHT // 2)

    # Fixed positions for red dots
    red_dot_positions = [(200, 300), (600, 400)]
    red_dots = [Dot(x, y) for x, y in red_dot_positions]

    start_time = None
    end_time = None
    win_displayed = False
    running = True

    if input_queue is None:
        input_queue = []  # Initialize an empty list if input_queue is not provided

    tick_counter = 0  # Initialize tick counter

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    input_queue.append(pygame.key.name(event.key).lower())

        if input_queue:
            direction = input_queue.pop(0)
            if direction == 'w':
                white_dot.move_towards(white_dot.x, white_dot.y - 10)
            elif direction == 's':
                white_dot.move_towards(white_dot.x, white_dot.y + 10)
            elif direction == 'a':
                white_dot.move_towards(white_dot.x - 10, white_dot.y)
            elif direction == 'd':
                white_dot.move_towards(white_dot.x + 10, white_dot.y)

        if pygame.time.get_ticks() - white_dot.last_movement_time > 1000:
            running = False

        # Collision check and other game logic can be placed here
        for red_dot in red_dots[:]:
            if distance(white_dot.x, white_dot.y, red_dot.x, red_dot.y) < WHITE_DOT_RADIUS + RED_DOT_RADIUS:
                red_dots.remove(red_dot)
                BALLS_EATEN += 1  # Increment the counter when a red dot is eaten

        if start_time is None:
            start_time = pygame.time.get_ticks()

        # Check win condition
        if not red_dots and not win_displayed:
            end_time = pygame.time.get_ticks()
            win_displayed = True
            elapsed_time = (end_time - start_time) / 1000.0  # Convert to seconds

        # Draw and move white dot
        white_dot.draw(screen)
        for red_dot in red_dots:
            red_dot.draw(screen)

        if win_displayed:
            win_text = font.render(f"You Win! Time: {elapsed_time:.2f} seconds", True, WHITE)
            screen.blit(win_text, ((WIDTH - win_text.get_width()) // 2, (HEIGHT - win_text.get_height()) // 2))
            balls_text = font.render(f"Balls Eaten: {BALLS_EATEN}", True, WHITE)
            screen.blit(balls_text, (10, 10))  # Displaying at (10, 10) position

        pygame.display.flip()
        pygame.time.delay(10)

    pygame.quit()  # Move the pygame.quit() call to the end of the function


# Genetic Algorithm Constants
POPULATION_SIZE = 100
GENERATIONS = 50
MUTATION_RATE = 0.1
SEQUENCE_LENGTH = 300


# Function to generate a random sequence of moves
def generate_random_sequence(length):
    return [random.choice(['w', 'a', 's', 'd']) for _ in range(length)]


# Function to calculate fitness (number of red dots eaten)
def calculate_fitness(sequence):
    input_queue = sequence.copy()
    run_game(input_queue)
    return BALLS_EATEN


# Function for tournament selection
def tournament_selection(population, fitnesses):
    tournament_size = 5
    tournament = random.sample(list(zip(population, fitnesses)), tournament_size)
    tournament.sort(key=lambda x: x[1], reverse=True)
    return tournament[0][0]


# Function for single-point crossover
def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child


# Function for mutation
def mutate(sequence):
    for i in range(len(sequence)):
        if random.random() < MUTATION_RATE:
            sequence[i] = random.choice(['w', 'a', 's', 'd'])
    return sequence


def generate():
    # Generate initial population
    population = [generate_random_sequence(SEQUENCE_LENGTH) for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        # Calculate fitness for each individual
        fitnesses = [calculate_fitness(individual) for individual in population]

        # Select parents and perform crossover and mutation
        new_population = []
        for _ in range(POPULATION_SIZE // 2):
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            new_population.extend([mutate(child1), mutate(child2)])

        # Replace old population with new population
        population = new_population

    # Find the best sequence and save to JSON
    best_sequence = max(population, key=calculate_fitness)
    with open('best_sequence.json', 'w') as f:
        json.dump(best_sequence, f)


def unwrap(filename):
    with open(filename, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    generate()
    # jsonAsArray = unwrap("best_sequence.json")
    # run_game(jsonAsArray)
    # run_game(["a", "a", "w", "w", "a", "a", "w", "w", "a", "a", "w", "w", "a", "a", "w", "w", "a", "a", "w", "w", "a", "a","w", "w"])
    # run_game()
