import numpy as np
import random

# Parameters
POPULATION_SIZE = 100
GENOME_LENGTH = 2  # Optimizing for 2 variables (x, y)
GENERATIONS = 200
MUTATION_RATE = 0.1
MUTATION_SCALE = 0.1

# Rastrigin function to minimize
def rastrigin_function(solution):
    x, y = solution
    return 10 * 2 + (x**2 - 10 * np.cos(2 * np.pi * x)) + (y**2 - 10 * np.cos(2 * np.pi * y))

# Create a random individual (solution)
def create_individual():
    return np.random.uniform(-5.12, 5.12, GENOME_LENGTH)

# Create an initial population
def create_population(size):
    return [create_individual() for _ in range(size)]

# Mutation: apply small changes to the solution
def mutate(individual):
    if np.random.rand() < MUTATION_RATE:
        mutation = np.random.normal(0, MUTATION_SCALE, size=GENOME_LENGTH)
        individual += mutation
    return np.clip(individual, -5.12, 5.12)

# Selection: choose the best individuals for the next generation
def select(population, fitnesses, retain_fraction=0.2):
    retain_length = int(len(population) * retain_fraction)
    sorted_indices = np.argsort(fitnesses)  # Sort by fitness (ascending)
    selected = [population[i] for i in sorted_indices[:retain_length]]
    return selected

# Crossover: combine two parents to create a child (simple average)
def crossover(parent1, parent2):
    return (parent1 + parent2) / 2

# Evolutionary Algorithm
def evolutionary_algorithm():
    population = create_population(POPULATION_SIZE)

    for generation in range(GENERATIONS):
        fitnesses = np.array([rastrigin_function(individual) for individual in population])

        # Get best fitness in current generation
        best_fitness = np.min(fitnesses)
        print(f"Generation {generation}: Best fitness = {best_fitness}")

        # Selection: Retain the best individuals
        selected = select(population, fitnesses)

        # Create new population via crossover and mutation
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            # Use random.choices to select parents from the selected individuals
            parent1, parent2 = random.choices(selected, k=2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population

    # Return the best solution found
    best_fitness = np.min([rastrigin_function(ind) for ind in population])
    best_solution = population[np.argmin([rastrigin_function(ind) for ind in population])]
    return best_solution, best_fitness

# Run the EA
best_solution, best_fitness = evolutionary_algorithm()
print(f"Best solution: {best_solution}, Fitness: {best_fitness}")

