import pickle
import random

GENOME_SIZE = 50  # Define the size of each genome

population_per_generation = 10
number_of_generations = 10
mutation_rate = 0.1

def fitness_function(model):
    """Dummy fitness function: Returns the length of the model."""
    return len(model)

def crossover(parent1, parent2):
    """Perform crossover between two parents."""
    crossover_point = random.randint(0, GENOME_SIZE - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(model):
    """Mutate the model based on mutation_rate."""
    for i in range(len(model)):
        if random.random() < mutation_rate:
            model[i] = random.choice(["w", "a", "s", "d"])
    return model

def generate_models(population_per_generation, number_of_generations, mutation_rate):
    best_model = None

    models = [[random.choice(["w", "a", "s", "d"]) for _ in range(GENOME_SIZE)] for _ in range(population_per_generation)]

    for generation in range(number_of_generations):
        # Evaluate fitness for each model
        fitness_values = [fitness_function(model) for model in models]

        # Select models based on fitness (for simplicity, select the best half)
        sorted_indices = sorted(range(len(fitness_values)), key=lambda k: fitness_values[k], reverse=True)
        best_model = models[sorted_indices[0]]  # Get the best model

        # Perform crossover and mutation to generate new models
        new_models = []
        while len(new_models) < population_per_generation:
            parent1 = random.choice(models)
            parent2 = random.choice(models)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_models.append(child)

        models = new_models

    # Save the best model from the last generation
    with open("best_model_from_last_generation.pkl", "wb") as f:
        pickle.dump(best_model, f)

# Generate models using the enhanced genetic algorithm approach
generate_models(population_per_generation, number_of_generations, mutation_rate)
