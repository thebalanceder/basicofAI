import numpy as np

# Rastrigin function to minimize
def rastrigin_function(x):
    return 10 * len(x) + sum([xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x])

# Parameters for the SFLA algorithm
POPULATION_SIZE = 50  # Total number of frogs
MEMEPLEX_COUNT = 5    # Number of memeplexes
MAX_ITERATIONS = 1000 # Maximum number of iterations
MAX_LOCAL_ITERATIONS = 10  # Maximum local search iterations per memeplex
LEAP_PROBABILITY = 0.5  # Probability of making a local leap
BOUNDS = [-5.12, 5.12]  # Search space bounds
GENOME_LENGTH = 2  # Dimensionality of the problem

# Initialize a frog (random position in the search space)
def create_frog():
    return np.random.uniform(BOUNDS[0], BOUNDS[1], GENOME_LENGTH)

# Evaluate fitness for each frog (using the Rastrigin function)
def evaluate_fitness(population):
    return [rastrigin_function(frog) for frog in population]

# Sort frogs by fitness and divide them into memeplexes
def form_memeplexes(population, fitnesses, memeplex_count):
    sorted_indices = np.argsort(fitnesses)
    sorted_population = [population[i] for i in sorted_indices]
    memeplexes = [sorted_population[i::memeplex_count] for i in range(memeplex_count)]
    return memeplexes

# Local search (Leaping) in each memeplex
def local_search(memeplex):
    best_frog = memeplex[0]
    worst_frog = memeplex[-1]
    
    # Try to move the worst frog towards the best frog
    if np.random.rand() < LEAP_PROBABILITY:
        r = np.random.rand()
        new_worst_frog = worst_frog + r * (best_frog - worst_frog)
        new_worst_frog = np.clip(new_worst_frog, BOUNDS[0], BOUNDS[1])  # Ensure within bounds
        
        # Evaluate fitness of the new position
        if rastrigin_function(new_worst_frog) < rastrigin_function(worst_frog):
            memeplex[-1] = new_worst_frog  # Replace worst frog with improved frog
    return memeplex

# Main SFLA algorithm
def shuffled_leaping_frog_algorithm():
    # Step 1: Initialize population of frogs
    population = [create_frog() for _ in range(POPULATION_SIZE)]
    best_solution = None
    best_fitness = float('inf')
    
    # Step 2: Iteratively optimize
    for iteration in range(MAX_ITERATIONS):
        # Evaluate fitness of frogs
        fitnesses = evaluate_fitness(population)
        
        # Update best solution
        for i, fitness in enumerate(fitnesses):
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = population[i]
        
        # Step 3: Form memeplexes
        memeplexes = form_memeplexes(population, fitnesses, MEMEPLEX_COUNT)
        
        # Step 4: Perform local search in each memeplex
        for memeplex in memeplexes:
            for _ in range(MAX_LOCAL_ITERATIONS):
                memeplex = local_search(memeplex)
        
        # Step 5: Shuffle memeplexes (Recombine the frogs)
        population = [frog for memeplex in memeplexes for frog in memeplex]
        
        # Print progress
        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best fitness = {best_fitness}")
    
    return best_solution, best_fitness

# Run the SFLA algorithm
best_solution, best_fitness = shuffled_leaping_frog_algorithm()
print(f"Best solution: {best_solution}, Fitness: {best_fitness}")

