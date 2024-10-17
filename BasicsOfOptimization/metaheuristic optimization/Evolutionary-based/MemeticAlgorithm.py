import numpy as np

# Rastrigin function to minimize
def rastrigin_function(x):
    return 10 * len(x) + sum([xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x])

# Local search: Gradient Descent (or similar)
def local_search(x, learning_rate=0.01, max_iters=100):
    for _ in range(max_iters):
        gradient = 2 * x + 20 * np.pi * np.sin(2 * np.pi * x)  # Derivative of the Rastrigin function
        x = x - learning_rate * gradient
        x = np.clip(x, BOUNDS[0], BOUNDS[1])  # Keep the solution within bounds
    return x

# Genetic Algorithm Parameters
POPULATION_SIZE = 50
GENOME_LENGTH = 2  # Number of variables (dimensionality)
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2
MAX_GENERATIONS = 1000
LOCAL_SEARCH_RATE = 0.3  # Apply local search to 30% of the population
BOUNDS = [-5.12, 5.12]  # Bounds for variables in Rastrigin function

# Create a random individual
def create_individual():
    return np.random.uniform(BOUNDS[0], BOUNDS[1], GENOME_LENGTH)

# Create initial population
def create_population(size):
    return [create_individual() for _ in range(size)]

# Evaluate fitness of each individual
def evaluate_population(population):
    return [rastrigin_function(individual) for individual in population]

# Selection: Roulette Wheel Selection based on fitness
def select_parents(population, fitnesses):
    # Convert fitnesses to probabilities for selection
    fitness_total = sum(fitnesses)
    selection_probs = [f / fitness_total for f in fitnesses]
    
    # Ensure population is a 1D list of individuals
    population = np.array(population)  # Convert to a numpy array if not already

    # Randomly select two parents based on the probabilities
    parents_indices = np.random.choice(len(population), size=2, p=selection_probs, replace=False)
    
    parent1 = population[parents_indices[0]]
    parent2 = population[parents_indices[1]]
    
    return parent1, parent2

# Crossover between two parents
def crossover(parent1, parent2):
    if np.random.rand() < CROSSOVER_RATE:
        alpha = np.random.rand()
        child1 = alpha * parent1 + (1 - alpha) * parent2
        child2 = (1 - alpha) * parent1 + alpha * parent2
        return child1, child2
    return parent1, parent2

# Mutation: Random perturbation of an individual
def mutate(individual):
    if np.random.rand() < MUTATION_RATE:
        mutation_vector = np.random.uniform(-1, 1, GENOME_LENGTH)
        individual = individual + mutation_vector
        individual = np.clip(individual, BOUNDS[0], BOUNDS[1])  # Ensure within bounds
    return individual

# Memetic Algorithm (Genetic Algorithm with Local Search)
def memetic_algorithm():
    population = create_population(POPULATION_SIZE)
    best_solution = None
    best_fitness = float('inf')

    for generation in range(MAX_GENERATIONS):
        # Evaluate fitness
        fitnesses = evaluate_population(population)

        # Update the best solution found so far
        for i, fitness in enumerate(fitnesses):
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = population[i]

        # Generate next population
        next_population = []
        while len(next_population) < POPULATION_SIZE:
            # Select parents
            parent1, parent2 = select_parents(population, fitnesses)
            
            # Apply crossover
            child1, child2 = crossover(parent1, parent2)

            # Apply mutation
            child1 = mutate(child1)
            child2 = mutate(child2)

            next_population.append(child1)
            next_population.append(child2)

        # Apply local search to a subset of the population
        for i in range(int(LOCAL_SEARCH_RATE * POPULATION_SIZE)):
            individual_index = np.random.randint(POPULATION_SIZE)
            next_population[individual_index] = local_search(next_population[individual_index])

        population = next_population

        # Print progress
        if generation % 100 == 0:
            print(f"Generation {generation}: Best fitness = {best_fitness}")

    return best_solution, best_fitness

# Run the Memetic Algorithm
best_solution, best_fitness = memetic_algorithm()
print(f"Best solution: {best_solution}, Fitness: {best_fitness}")

