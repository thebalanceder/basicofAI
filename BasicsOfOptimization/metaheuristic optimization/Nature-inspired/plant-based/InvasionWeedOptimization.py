import numpy as np

# Rastrigin function to minimize
def rastrigin_function(x):
    return 10 * len(x) + sum([xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x])

# Parameters for the IWO algorithm
POPULATION_SIZE = 50     # Initial population size
MAX_POPULATION = 100     # Maximum population size
MAX_ITERATIONS = 1000    # Maximum number of iterations
MIN_SEEDS = 1            # Minimum number of seeds produced by a weed
MAX_SEEDS = 5            # Maximum number of seeds produced by a weed
INITIAL_SPREAD = 1.0     # Initial standard deviation for seed dispersion
FINAL_SPREAD = 0.01      # Final standard deviation for seed dispersion
BOUNDS = [-5.12, 5.12]   # Search space bounds
GENOME_LENGTH = 2        # Dimensionality of the problem

# Initialize a weed (random position in the search space)
def create_weed():
    return np.random.uniform(BOUNDS[0], BOUNDS[1], GENOME_LENGTH)

# Evaluate fitness for each weed (using the Rastrigin function)
def evaluate_fitness(population):
    return [rastrigin_function(weed) for weed in population]

# Generate seeds (offspring) around a weed
def generate_seeds(weed, num_seeds, spread):
    seeds = []
    for _ in range(num_seeds):
        seed = weed + np.random.randn(GENOME_LENGTH) * spread
        seed = np.clip(seed, BOUNDS[0], BOUNDS[1])  # Ensure within bounds
        seeds.append(seed)
    return seeds

# Main IWO algorithm
def invasive_weed_optimization():
    # Step 1: Initialize population of weeds
    population = [create_weed() for _ in range(POPULATION_SIZE)]
    best_solution = None
    best_fitness = float('inf')

    # Step 2: Iterative optimization process
    for iteration in range(MAX_ITERATIONS):
        # Evaluate fitness of weeds
        fitnesses = evaluate_fitness(population)
        
        # Update best solution
        for i, fitness in enumerate(fitnesses):
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = population[i]
        
        # Step 3: Reproduce seeds based on fitness
        f_min, f_max = min(fitnesses), max(fitnesses)
        seeds = []
        for i, weed in enumerate(population):
            # Number of seeds is inversely proportional to fitness
            num_seeds = int(MAX_SEEDS - (MAX_SEEDS - MIN_SEEDS) * (fitnesses[i] - f_min) / (f_max - f_min + 1e-6))
            # Disperse seeds around the weed
            spread = INITIAL_SPREAD - (INITIAL_SPREAD - FINAL_SPREAD) * (iteration / MAX_ITERATIONS)
            seeds += generate_seeds(weed, num_seeds, spread)

        # Step 4: Combine parents and offspring
        population += seeds
        
        # Step 5: Competitive exclusion (keep the fittest weeds)
        if len(population) > MAX_POPULATION:
            fitnesses = evaluate_fitness(population)
            sorted_indices = np.argsort(fitnesses)
            population = [population[i] for i in sorted_indices[:MAX_POPULATION]]

        # Print progress
        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best fitness = {best_fitness}")

    return best_solution, best_fitness

# Run the IWO algorithm
best_solution, best_fitness = invasive_weed_optimization()
print(f"Best solution: {best_solution}, Fitness: {best_fitness}")

