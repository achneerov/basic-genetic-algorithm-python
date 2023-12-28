# generate.py

import pickle
import random

population_per_generation = 10
number_of_generations = 10
mutation_rate = 0.1


def generate_models(population_per_generation, number_of_generations, mutation_rate):
    for generation in range(number_of_generations):
        models = []
        for _ in range(population_per_generation):
            model = [random.choice(["UP", "DOWN", "LEFT", "RIGHT"]) for _ in range(GENOME_SIZE)]
            models.append(model)

        # Save all models for the current generation
        with open(f"generation_{generation}_models.pkl", "wb") as f:
            pickle.dump(models, f)

        # For a real Genetic Algorithm, you'd evaluate fitness, select parents, perform crossover, mutate, etc.
        # Here, for simplicity, we're just saving all models for each generation.
