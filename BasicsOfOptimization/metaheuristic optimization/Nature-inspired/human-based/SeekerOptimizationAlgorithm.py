
import numpy as np

# Objective function: Sphere function
def sphere_function(x):
    return np.sum(x ** 2)

# Initialize seekers (population)
def initialize_seekers(pop_size, dimensions, bounds):
    population = np.random.uniform(bounds[0], bounds[1], (pop_size, dimensions))
    return population

# Fitness evaluation
def evaluate_seekers(population):
    fitness = np.array([sphere_function(individual) for individual in population])
    return fitness

# Seeker Optimization Algorithm (SOA)
def seeker_optimization_algorithm(pop_size=50, dimensions=5, bounds=(-5, 5), generations=100, w1=0.5, w2=0.3, w3=0.2):
    # Step 1: Initialize population (seekers)
    population = initialize_seekers(pop_size, dimensions, bounds)
    best_solution = None
    best_fitness = float('inf')

    # Step 2: Evolve seekers over generations
    for generation in range(generations):
        # Step 3: Evaluate fitness of seekers
        fitness = evaluate_seekers(population)

        # Step 4: Keep track of the best solution
        min_fitness = np.min(fitness)
        if min_fitness < best_fitness:
            best_fitness = min_fitness
            best_solution = population[np.argmin(fitness)]

        # Step 5: Update positions of seekers
        social_best = population[np.argmin(fitness)]  # Social best is the best in the population
        for i in range(pop_size):
            self_best = population[i]  # Self-best is the seeker's own position
            random_vector = np.random.uniform(-1, 1, dimensions)

            # Update seeker's position based on self, social, and random experiences
            population[i] += w1 * (self_best - population[i]) + \
                             w2 * (social_best - population[i]) + \
                             w3 * random_vector

        # Ensure seekers stay within bounds
        population = np.clip(population, bounds[0], bounds[1])

        print(f"Generation {generation + 1}, Best fitness: {best_fitness}")

    return best_solution, best_fitness

# Run the SOA on the Sphere function
best_solution, best_fitness = seeker_optimization_algorithm()

# Output the final result
print(f"Best solution found: {best_solution}")
print(f"Best fitness: {best_fitness}")

