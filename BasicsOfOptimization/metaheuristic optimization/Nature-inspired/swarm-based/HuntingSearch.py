import numpy as np
import random

# Objective function (example: minimize sum of squares)
def objective_function(x):
    return sum(x_i ** 2 for x_i in x)

# Initialize population (hunters)
def initialize_population(pop_size, dim, lower_bound, upper_bound):
    return [np.random.uniform(lower_bound, upper_bound, dim).tolist() for _ in range(pop_size)]

# Hunting Search Algorithm
def hunting_search(pop_size=50, dim=5, lower_bound=-10, upper_bound=10, max_iter=100):
    # Initialize hunters (positions in the solution space)
    population = initialize_population(pop_size, dim, lower_bound, upper_bound)
    
    # Find the best hunter in the initial population
    best_hunter = min(population, key=objective_function)
    best_fitness = objective_function(best_hunter)

    # Main optimization loop
    for t in range(max_iter):
        for i in range(pop_size):
            # Get current hunter
            hunter = population[i]

            # Generate two random numbers for the balance between exploration and exploitation
            r1 = random.random()
            r2 = random.random()

            # Random exploration vector
            R = np.random.uniform(-1, 1, dim)

            # Update hunter's position (combination of exploitation and exploration)
            new_position = hunter + r1 * (np.array(best_hunter) - np.array(hunter)) + r2 * R

            # Ensure new position is within bounds
            new_position = np.clip(new_position, lower_bound, upper_bound)

            # Replace the old hunter if the new one is better
            if objective_function(new_position) < objective_function(hunter):
                population[i] = new_position.tolist()

        # Update the best hunter in the population
        current_best_hunter = min(population, key=objective_function)
        current_best_fitness = objective_function(current_best_hunter)
        
        if current_best_fitness < best_fitness:
            best_hunter = current_best_hunter
            best_fitness = current_best_fitness

        # Optionally: print progress
        print(f"Iteration {t+1}: Best Fitness = {best_fitness}")

    return best_hunter, best_fitness

# Run the Hunting Search algorithm
best_solution, best_fitness = hunting_search()
print("Best Solution Found:", best_solution)
print("Best Fitness:", best_fitness)

