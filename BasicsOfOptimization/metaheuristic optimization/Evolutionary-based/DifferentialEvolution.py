import numpy as np

# Parameters
POPULATION_SIZE = 50
GENOME_LENGTH = 2  # Optimizing for 2 variables (x1, x2)
GENERATIONS = 1000
MUTATION_FACTOR = 0.8  # F: Scaling factor for mutation
CROSSOVER_RATE = 0.7   # Cr: Crossover probability
BOUNDS = [-5.12, 5.12]  # Bounds for variables (Rastrigin domain)

# Rastrigin function to minimize
def rastrigin_function(solution):
    return 10 * len(solution) + sum(x**2 - 10 * np.cos(2 * np.pi * x) for x in solution)

# Create a random individual (solution)
def create_individual():
    return np.random.uniform(BOUNDS[0], BOUNDS[1], GENOME_LENGTH)

# Create an initial population
def create_population(size):
    return [create_individual() for _ in range(size)]

# Differential Evolution Algorithm
def differential_evolution():
    # Initialize population
    population = create_population(POPULATION_SIZE)
    best_solution = None
    best_fitness = float('inf')

    for generation in range(GENERATIONS):
        new_population = []

        for i in range(POPULATION_SIZE):
            # Mutation: Create mutant vector
            indices = list(range(POPULATION_SIZE))
            indices.remove(i)
            r1, r2, r3 = np.random.choice(indices, 3, replace=False)
            x_r1, x_r2, x_r3 = population[r1], population[r2], population[r3]
            mutant = x_r1 + MUTATION_FACTOR * (x_r2 - x_r3)
            mutant = np.clip(mutant, BOUNDS[0], BOUNDS[1])  # Ensure mutant is within bounds

            # Crossover: Create trial vector
            target = population[i]
            trial = np.copy(target)
            for j in range(GENOME_LENGTH):
                if np.random.rand() < CROSSOVER_RATE or j == np.random.randint(GENOME_LENGTH):
                    trial[j] = mutant[j]

            # Selection: Choose between trial and target
            if rastrigin_function(trial) < rastrigin_function(target):
                new_population.append(trial)
            else:
                new_population.append(target)

        # Update population
        population = new_population

        # Track the best solution found so far
        for individual in population:
            fitness = rastrigin_function(individual)
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = individual

        # Output the best fitness in the current generation
        print(f"Generation {generation}: Best fitness = {best_fitness}")

    return best_solution, best_fitness

# Run the Differential Evolution Algorithm
best_solution, best_fitness = differential_evolution()
print(f"Best solution: {best_solution}, Fitness: {best_fitness}")

